from config import CONFIG

import mysql.connector
from mysql.connector import errorcode


class Connect:
    def __init__(self):
        self.connection: object
        self.config: dict = CONFIG

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
            return self.connection
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
    def version(cursor):
        query = "SHOW VARIABLES like 'version';"
        cursor.execute(query)
        result = cursor.fetchone()
        return {"version": result[1]}

    @staticmethod
    def search(cursor, country):
        query = "SELECT * FROM country WHERE NAME=%s;"
        cursor.execute(query, (country,))
        result = cursor.fetchone()
        return result
    
    @staticmethod
    def lookup(cursor, city_id):
        query = "SELECT * FROM city WHERE ID=%s;"
        cursor.execute(query, (city_id,))
        result = cursor.fetchone()
        return result


class Country:
    """
    Country object blueprint
    """
    def __init__(self, code, name, continent, 
    region, surface_area, indep_year, population, 
    life_expect, gnp, gnp_old, local_name, gov_form, 
    head_of_state, capital_id, code_2
    ):
        self.code: str                  = code
        self.name: str                  = name
        self.continent: str             = continent
        self.region: str                = region
        self.surface_area: float        = surface_area
        self.indep_year: int            = indep_year
        self.population: int            = population
        self.life_expectancy: float     = life_expect
        self.GNP: float                 = gnp
        self.GNP_old: float             = gnp_old
        self.local_name: str            = local_name
        self.government: str            = gov_form
        self.head_of_state: str         = head_of_state
        self.capital_id: int            = capital_id
        self.code_2: str                = code_2
    
    @classmethod
    def construct(cls, config):
        country = Country(
            code=config[0], 
            name=config[1], 
            continent=config[2], 
            region=config[3], 
            surface_area=config[4], 
            indep_year=config[5], 
            population=config[6], 
            life_expect=config[7], 
            gnp=config[8], 
            gnp_old=config[9], 
            local_name=config[10], 
            gov_form=config[11], 
            head_of_state=config[12], 
            capital_id=config[13], 
            code_2=config[14]
        )
        return country


# class Country:
#     def __init__(self, uid, name, code, pop):
#         self.uid: int = uid
#         self.name: str = name
#         self.code: str = code
#         self.pop: int = pop

#     @classmethod
#     def construct(cls, config):
#         test_country = Country(
#             uid=config[0], 
#             name=config[1], 
#             code=config[2], 
#             pop=config[3]
#             )
#         return test_country



def main():
    mock_country = (42, 'Canada', 'CAN', 26000000)
    fake_country = Country.construct(mock_country)
    print(fake_country.__dict__)




if __name__ == '__main__':
    main()
