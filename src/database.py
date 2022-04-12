import time
import mysql.connector
from mysql.connector import errorcode
from .config import settings


class Connect:
    def __init__(self):
        self.connection: object
        self.config: dict = settings.__dict__

    def __enter__(self):
        """ MySQL connection object

        Returns:
            object: cursor
        """
        try:
            self.connection = mysql.connector.connect(
                user=self.config['MYSQL_USER'],
                passwd=self.config['MYSQL_PASSWORD'],
                database=self.config['MYSQL_DB'],
                host=self.config['MYSQL_HOST'],
                port=self.config['MYSQL_PORT'],
                auth_plugin=self.config['MYSQL_AUTH']
            )
            return self.connection.cursor()
            # --
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                raise Exception("User and/or password is incorrect")
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                raise Exception("Database does not exist")
            else:
                raise Exception(err)

    def __exit__(self, type, value, traceback):
        self.connection.close()


class SQL:
    @staticmethod
    def version(cursor: object) -> tuple:
        """ Version variable query for testing purposes

        Args:
            cursor (object): connection cursor

        Returns:
            tuple: version, number
        """
        query = "SHOW VARIABLES like 'version';"
        cursor.execute(query)
        result = cursor.fetchone()
        return result

    @staticmethod
    def inject(cursor: object, query: str, *args) -> tuple:
        """ NOT SAFE FOR PRODUCTION

        Args:
            cursor (object): connection cursor
            query (str): SQL query string with %s for str formatting
            args(str): variable args

        Returns:
            tuple: query results
        """
        cursor.execute(query, args)
        result = cursor.fetchall()
        return result

# === TEST SUITE ===
# Module methods 
def query_version(ttl=5):
    timeout = 0
    while timeout < ttl:
        try:
            with Connect() as cursor:
                version = SQL.version(cursor)
            timeout=0
            break
        except Exception as error:
            print("ERROR:\t ", error)
            timeout += 1
            time.sleep(2)

    return version

# Initialised at runtime
def session():
    version = query_version() # If cannot connect to database, will await connection
    sys_out = F"INFO:\t  Database running on MySQL v{str(version[1])}"
    print(sys_out)
    # print(type(settings), settings.__dict__)


# == Main ==
if __name__ == '__main__':
    pass



