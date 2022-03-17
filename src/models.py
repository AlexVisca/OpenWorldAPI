from src.database import Connect, SQL

# Models
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

# Country profile creator
class CountryProfile(Country):
    def __init__(self, config):
        super().__init__(*config)
        self.capital: str
        self.cities: list
    
    @classmethod
    def creator(cls, query: str):
        with Connect() as cursor:
            raw_data = SQL.search(cursor, query)
            if raw_data is None:
                raise Exception(f"Content '{query}' does not exist")
            
            canada = CountryProfile(raw_data)
            canada.capital = SQL.lookup(cursor, canada.capital_id)
            canada.cities = SQL.select_cities(cursor, canada.code)
            json_format = canada.__dict__
        # --
        return json_format

class SQL:
    @staticmethod
    def select_index(cursor):
        query = "SELECT Name, Continent FROM country;"
        cursor.execute(query)
        raw_data = cursor.fetchall()
        result = [{"Name": country[0], "Continent": country[1]} for country in raw_data]
        return result
    
    @staticmethod
    def search(cursor: object, country: str) -> tuple:
        query = "SELECT * FROM country WHERE NAME = %s;"
        cursor.execute(query, (country,))
        result = cursor.fetchone()
        return result
    
    @staticmethod
    def lookup(cursor: object, city_id: int) -> tuple:
        query = "SELECT Name FROM city WHERE ID = %s;"
        cursor.execute(query, (city_id,))
        result = cursor.fetchone()
        return result[0]

    @staticmethod
    def select_cities(cursor, country_code):
        query = "SELECT Name, District FROM city WHERE CountryCode = %s;"
        cursor.execute(query, (country_code,))
        raw_data = cursor.fetchall()
        result = [{"Name": city[0], "District": city[1]} for city in raw_data]
        return result


def test_main():
    try:
        profile = CountryProfile.creator('Canad')
        print(profile)
    except Exception as exc:
        print({"status_code": 404, "message": str(exc)})


if __name__ == '__main__':
    test_main()





# SNIPPETS
# class City:
#     def __init__(self, idx, name, code, dist, pop):
#         self.idx: int   = idx
#         self.name: str  = name
#         self.code: str  = code
#         self.dist: str  = dist
#         self.pop: int   = pop
    
#     @classmethod
#     def construct(cls, config):
#         city = City(
#             idx=config[0], 
#             name=config[1], 
#             code=config[2], 
#             dist=config[3],
#             pop=config[4]
#         )
#         return city

    # @classmethod
    # def construct(cls, config):
    #     country = Country(
    #         code=config[0], 
    #         name=config[1], 
    #         continent=config[2], 
    #         region=config[3], 
    #         surface_area=config[4], 
    #         indep_year=config[5], 
    #         population=config[6], 
    #         life_expect=config[7], 
    #         gnp=config[8], 
    #         gnp_old=config[9], 
    #         local_name=config[10], 
    #         gov_form=config[11], 
    #         head_of_state=config[12], 
    #         capital_id=config[13], 
    #         code_2=config[14]
    #     )
    #     return country

# == Test Runtime ==
# class TestCountry:
#     def __init__(self, uid, name, code, pop):
#         self.uid: int = uid
#         self.name: str = name
#         self.code: str = code
#         self.pop: int = pop

#     @classmethod
#     def construct(cls, config):
#         test_country = TestCountry(
#             uid=config[0], 
#             name=config[1], 
#             code=config[2], 
#             pop=config[3]
#             )
#         return test_country


# class TestProfile(TestCountry):
#     def __init__(self, country: object):
#         super().__init__(**country.__dict__)
#         self.attr: str = "attribute"

#     @classmethod
#     def construct(cls):
#         mock_country = (42, 'Canada', 'CAN', 26000000)
#         fake_country = super().construct(mock_country)
#         print(fake_country.__dict__)
#         test_profile = TestProfile(fake_country)
#         return test_profile


# def test():
#     fake_country = TestProfile.construct()
#     print(fake_country.__dict__)
