
import os
import snowflake.connector


class Snowflake(object):
    """Snowflake Connector
    Credentials available in 1Password
    """
    def __init__(
            self, 
            user=os.environ['SNOWFLAKE_USER'], 
            password=os.environ['SNOWFLAKE_PASSWORD'], 
            account=os.environ['SNOWFLAKE_ACCOUNT']
    ):
        assert (user and password and account), 'Must specify snowflake warehouse credentials!'
        self.ctx = snowflake.connector.connect(
            user=user,
            password=password,
            account=account
            )

    def query(self, input_queries=):
        with self.ctx.cursor() as cs:
            for input_query in input_queries:
                cs.execute(input_query)
            return cs.fetchall()

    def __del__(self):
        self.ctx.close()


# snow = Snowflake()
# for item in snow.query():
#     print(item)
