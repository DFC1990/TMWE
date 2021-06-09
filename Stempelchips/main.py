import pyodbc


conn = pyodbc.connect('Driver={SQL Server};'
                                  'Server=192.168.12.1;'
                                  'Database=ogkadenkasse_new;'
                                  'UID=dfc;'
                                  'PWD=daNiel,1611;'
                                  'Trusted_Connection=no;')