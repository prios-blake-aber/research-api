

import boto3
import logging
import psycopg2
import datetime
import pandas as pd
from psycopg2.extras import LoggingConnection, DictCursor

from src import config

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


class BaseSql(object):

    def __init__(self, db_credentials):
        self.db_conn = psycopg2.connect(
            connection_factory=LoggingConnection,
            **db_credentials
        )
        self.db_conn.initialize(logger)
        self.db_conn.autocommit = True

    def remap_columns_to_sql(self, data_dict):
        inverted_column_mapping = {v['title']: k for k, v in config.COLUMN_MAPPING.items()}
        return {inverted_column_mapping.get(k, k): v for k, v in data_dict.items()}

    def escape_quotes(self, text, slug='Q'):
        """Escapes quotes in text fields"""
        if isinstance(text, str):
            return "${s}${t}${s}$".format(t=text, s=slug)
        elif isinstance(text, datetime.datetime):
            return "${s}${t}${s}$".format(t=text, s=slug)
        elif text is None:
            return 'NULL'
        else:
            return str(text)

    def apply_change_tracking(self, data_dict, user, user_lookup, default_user_id=-1):
        data_dict['last_modified'] = datetime.datetime.now()
        data_dict['modified_by'] = user_lookup['user_id'].get(user, default_user_id)
        return data_dict

    def db_query(self, query, dict_cursor=False, get_results=False):
        """Queries the database"""
        def get_cursor_type(dict_cursor):
            if dict_cursor:
                return self.db_conn.cursor(cursor_factory=DictCursor)
            else:
                return self.db_conn.cursor()

        with get_cursor_type(dict_cursor) as cursor:
            cursor.execute(query)
            if get_results:
                return cursor.fetchall()

    def get_dataframe_from_select(self, query):
        """Queries the database into a DataFrame"""
        return pd.read_sql(query, self.db_conn)

    def get_table_primary_key(self, table):
        """Returns the primary key of a table for reference"""
        base_sql_query = """
            SELECT kc.column_name 
            FROM  
                information_schema.table_constraints tc,  
                information_schema.key_column_usage kc  
            WHERE 
                tc.table_name = '{t}'
                and tc.constraint_type = 'PRIMARY KEY' 
                and kc.table_schema = tc.table_schema
                and kc.constraint_name = tc.constraint_name
        """.format(t=table)
        primary_key_result = self.db_query(base_sql_query, dict_cursor=True, get_results=True)
        primary_key_result = primary_key_result.pop()
        return primary_key_result['column_name']

    def get_column_names(self, table):
        base_sql_query = """
            SELECT column_name
            FROM information_schema.columns
            WHERE table_name = '{t}'
            ORDER BY ordinal_position
        """.format(t=table)
        column_names_result = self.db_query(base_sql_query, dict_cursor=True, get_results=True)
        return [i['column_name'] for i in column_names_result]

    def filter_bad_columns(self, table, data_dict):
        input_columns = data_dict.keys()
        target_columns = self.get_column_names(table)
        common_columns = set(input_columns).intersection(set(target_columns))
        return {key: data_dict[key] for key in common_columns}

    def check_if_row_exists(self, table, predicate_dict):
        predicate_sql_query = self.generate_predicates(predicate_dict)
        row_exists = self.db_query("""
            SELECT EXISTS (
                SELECT 1 FROM {t} {p}
            )
        """.format(t=table, p=predicate_sql_query), get_results=True)
        row_exists = row_exists.pop()

        return row_exists[0]  # TODO: BRITTLE

    def generate_predicates(self, predicate_dict):
        predicate_string = [
            '{k} = {v}'.format(k=k, v=self.escape_quotes(v))
            for k, v in predicate_dict.items()
            if v is not None
        ]
        predicate_string.extend([
            '{k} IS {v}'.format(k=k, v=self.escape_quotes(v))
            for k, v in predicate_dict.items()
            if v is None
        ])
        predicate_string = ' AND '.join(predicate_string)
        return 'WHERE {p}'.format(p=predicate_string)

    def filter_unchanged_fields(self, table, data_dict, predicate_dict):
        predicate_sql_query = self.generate_predicates(predicate_dict)

        existing_dict = self.db_query("""
            SELECT * FROM {t} {p}
        """.format(t=table, p=predicate_sql_query), dict_cursor=True, get_results=True)
        existing_dict = existing_dict.pop()

        return {
            k: data_dict[k] for k, _ in existing_dict.items()
            if k in data_dict
            and existing_dict[k] != data_dict[k]
        }

    def db_delete(self, table, predicate_dict, user):
        """Deletes rows from a table that meet a simple equality predicates"""
        # TODO: only works on ONE row at a time now, could be MULTIPLE
        base_sql_query = 'DELETE FROM {t}'.format(t=table)
        predicate_sql_query = self.generate_predicates(predicate_dict)

        self.db_query(
            '{b} {p}'.format(
                b=base_sql_query,
                p=predicate_sql_query
            ),
            get_results=False
        )

    def preprocess_ddl_queries(self, table, data_dict, user, user_lookup):
        data_dict = self.apply_change_tracking(data_dict, user, user_lookup)
        data_dict = self.remap_columns_to_sql(data_dict)
        data_dict = self.filter_bad_columns(table, data_dict)
        return data_dict

    def db_insert(self, table, data_dict, user, user_lookup, return_id=False):
        """Inserts rows (and returns primary key) for a (sub)set of table columns"""
        # TODO: only works on ONE row at a time now, could be MULTIPLE
        data_dict = self.preprocess_ddl_queries(table, data_dict, user, user_lookup)

        columns = ','.join(data_dict.keys())
        values = ','.join([self.escape_quotes(field) for field in data_dict.values()])
        base_sql_query = 'INSERT INTO {t} ({c}) VALUES ({v})'.format(t=table, c=columns, v=values)

        if return_id:
            primary_key = self.get_table_primary_key(table)
            return_id_query = 'RETURNING {pk}'.format(pk=primary_key)

            insert_result = self.db_query('{b} {r}'.format(
                b=base_sql_query, r=return_id_query),
                get_results=True
            )
            return insert_result
        else:
            self.db_query(
                base_sql_query,
                get_results=False
            )

    def db_update(self, table, data_dict, predicate_dict, user, user_lookup):
        """NOTE: This function only accepts dictionaries of simple equality predicates"""
        updates_to_process = self.filter_unchanged_fields(table, data_dict, predicate_dict)
        if not updates_to_process:
            pass
        else:
            data_dict = self.preprocess_ddl_queries(table, updates_to_process, user, user_lookup)

            base_sql_query = 'UPDATE {t}'.format(t=table)

            update_string = ', '.join([
                '{c} = {v}'.format(c=c, v=self.escape_quotes(v)) for c, v in data_dict.items()
            ])
            update_sql_query = 'SET {u}'.format(u=update_string)

            predicate_sql_query = self.generate_predicates(predicate_dict)

            self.db_query(
                '{b} {u} {p}'.format(
                    b=base_sql_query,
                    u=update_sql_query,
                    p=predicate_sql_query
                ),
                get_results=False
        )

    def db_update_insert(self, table, data_dict, predicate_dict, user, user_lookup):
        """NOTE: This function only accepts dictionaries of simple equality predicates"""

        if self.check_if_row_exists(table, predicate_dict):
            self.db_update(table, data_dict, predicate_dict, user, user_lookup)
        else:
            data_dict.update(predicate_dict)
            self.db_insert(table, data_dict, user, user_lookup)


SQL_API = BaseSql(config.DB_CREDENTIALS)
