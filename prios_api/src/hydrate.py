
import snowflake.connector


class Snowflake(object):
    """Snowflake Connector
    Credentials available in 1Password
    """
    def __init__(
            self, user=, password='2LfmoHkmmjDDJWzkbvDGafwN', account='jo77181.us-east-1'
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
