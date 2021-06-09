import pyodbc
import sys
import traceback




class Db:
    DRIVER   =  r'DRIVER={SQL Server};'
    SERVER   =  r'SERVER=172.25.2.40\SQLEXPRESS;'
    DATABASE =  r'DATABASE=bcore;'
    USERNAME =  r'UID=bcommerp;'
    PASSWORD =  r'PWD=bcomm$01'

    def __init__(self):
        try:
            self.cnxn = pyodbc.connect(self.DRIVER + self.SERVER + \
                        self.DATABASE + self.USERNAME + self.PASSWORD)
        except Exception:
            self.__exit__(sys.exc_info())

        self.cursor = self.cnxn.cursor()

    def __enter__(self):
        return self

    #def __exit__(self, exc_type, exc_value, traceback):
    def __exit__(self, exc_msg):
        print("__exit__")
        print(exc_msg)
        self.cursor.close()
        self.cnxn.close()

with Db() as d:
    print(d)