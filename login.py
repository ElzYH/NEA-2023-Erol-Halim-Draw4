import sqlite3
import logging

logger = logging.getLogger(f"{__name__}")



def create():
    logger.info(f"Creating database")
    conn = sqlite3.connect("uno_database.db")
    c = conn.cursor()
    for table_name in ["NoWilds","Numbers","Normal"]:
        c.execute(f"""CREATE TABLE {table_name} (
            UserName VARCHAR(10),
            Games INT,
            Wins INT,
            Loss INT,
            Draws INT,
            PRIMARY KEY('UserName'))""")
        conn.commit()
    conn.close()


class User:
    def __init__(self,u=""):
        self.__username = u
        self.error = ""
    
    
    def set_username(self,u):
        logger.info(f"Setting a username")
        conn = sqlite3.connect("uno_database.db")
        c = conn.cursor()
        self.__username = u.replace(" ", "_") 

        try:
            copy_check = c.execute(f'SELECT UserName FROM Normal WHERE UserName IS "{self.__username}"')
            copy_check = str("".join(c.fetchone()))
        except TypeError: logger.warning(f"Type Error Raised copy check = {copy_check}")

        if copy_check == self.__username: 
            self.error = "Please Create A UserName That Not In The Database"
            logger.warning(f"Error code: {self.error} ")
        elif self.__username == "": 
            self.error = "Please Do Not Leave The Username Blank"
            logger.warning(f"Error code: {self.error} ")
        else:
            for table_name in ["NoWilds","Numbers","Normal"]:
                c.execute(f"INSERT INTO {table_name}(UserName,Games,Wins,Loss,Draws) VALUES ('{self.__username.lower()}',0,0,0,0)")
            logger.info(f"{self.__username} added to database")
        
        self.__username = ""
        conn.commit()
        conn.close()
 

    def sign_in(self,u):
        logger.info(f"Signing in")
        conn = sqlite3.connect("uno_database.db")
        c = conn.cursor()

        self.__username = str("".join([i for i in u])).lower()
        check = c.execute(f'SELECT UserName FROM Normal WHERE UserName IS "{self.__username}"')
        logger.info(f"username: {self.__username}, check: {check}") #shows where how private access work

        try:
            check = str("".join(c.fetchone())).lower()
        except TypeError:
            self.__username = ""
            self.error = "Please Enter A Valid Username"
            logger.warning(f"{self.error} Enter a non valid username/ not in table")
            conn.close()
        
        if check == self.__username:
            logger.info(f"Check is True") 
            return self.__username

    def get_user(self):
        return self.__username

    def error_code(self):
        display = self.error 
        self.error = ""
        return display


def login_or_sign(login_options,name):
    account_name = User()
    logger.info(f"account_name = {str(account_name.get_user())}")
    if login_options == "sign up":
            account_name.set_username(name)
            logger.info(f"account_name = {str(account_name.get_user())}")

    elif login_options == "sign in":
        account_name.sign_in(name)
        logger.info(f"account_name = {str(account_name.get_user())}")

    list2 = [account_name.get_user(), account_name.error_code()]
    logger.info(f"User with error code {list2}")
    return list2

    
    
