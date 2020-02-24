# MySqlDb

MySqlDb is a lightweight, robust class wrapper designed to simplify SQL syntax and the MySql
database interface. 

## Getting Started:

1. Download or clone this repository


## Using the Class Wrapper:
     
      from mysqldb import MySqlDb
      
      
## Connect to an existing database:

      db = MySqlDb(user='username', password='password', host='localhost', database='your_database')
      

## Create a new table in the database:
      
      db.create_table(table)
      
      ARGUMENTS:
               table: dict:
                      Pass in a specially formatted dictionary containing two keys:

                      'name': str: 
                          is the name of the table that is being created.

                      'fields': list: 
                          is a list of string formatted values representing fields'.

               Example:
                      MY_TABLE = {
                        'name': 'WebPages',
                        'fields': [
                            'URLS VARCHAR(512) NOT NULL',
                            'HTML TEXT NOT NULL',
                            'SUBMISSION_DATE DATE'
                        ]
                      }

           USAGE:
               Pass in the user created dictionary MY_TABLE:

               create_table(MY_TABLE)

           This method automatically adds an INTEGER PRIMARY KEY ID
           to each table row.
           
           
## Write data into database:

        db.write(table, columns, *data)
        
        USAGE:
            write('My_Table', 'Field_1, Field_2', data1, data2)

           ARGUMENTS:
           
               table: str: 
                   the table name in string format
                   
               fields: str: 
                   a string of comma separated field names 
                   
               *data: args: 
                   the data objects being passed to each corresponding field.
                   
                   
## Query the database:

        db.select(table, *columns, **opts):
        
        USAGE:
        
            Standard Query:
                select('artists', 'all')
                select('artists', 'all', where='id=1')
                select('artists', '*', where='ArtistId between 1 and 10')

            Inner Join:
                select('artists', 'Name', 'Title', target='albums', join='inner', key='id', where='id between 1 and 5')

            Left Join:
                select('artists', 'Title', 'Name' target='albums', join='left', key='ArtistId')

            Right Join:
                select('artists', '*', target='albums', join='right')

            Cross Join:
                select('artists', '*', target='albums', join='cross')
                
        ARGUMENTS:

            table: str:
                The name of the table upon which the query is being made.
                
            columns: str:
                The name of each column in string format.

           Optional keyword arguments for join formatting:

              target: str: 
                  the name of the table to be joined.

                  Explicit is better than implicit, but if the target table
                  is not specified, the method searches for and retrieves
                  the first table containing the columns declared for joining.

                  That is to say, any column name passed that is not contained
                  within the first table.

                  This may or may not be the appropiate table,
                  so caution is advised, but this fallback is there to
                  shorten the syntax of calling the method by ommiting the
                  target table argument if possible, desired or its declaration
                  forgotten.

               join: str: 
                   the type of join
                   
               key: str: 
                   the foreign or common key between tables used for joins
                   
               where: str: 
                   condition determining row selection
                   
               
 ## Rename a Column:

        db.rename_column(table, column, new_name)
        
        ARGUMENTS:
               table: str: the name of the table to be altered.
               column: str: the column to be renamed:
               new_name: str: the column name replacement 

        USAGE:
               rename_column('Customers', 'Products', 'Purchased')
               
         
 ## Add a Column:   

        db.add_column(table, column, definition, where=None)
        
        ARGUMENTS:
               table: str: the name of the table to be altered.
               column: str: the name of column to be added:
               definition: str: datatype ie INT, VARCHAR etc...
               where: str: column insertion location. Defaults to FIRST if not specified.

        USAGE:
               add_column('Customers', 'NewProducts', 'VARCHAR(75) NOT NULL', where=AFTER OldProducts')
               
                
  
  ## Delete column from a table:
  
          db.drop_column(table, column)
          
          ARGUMENTS:
              table: str: the name of the table to be altered.
              column: str: the name of column to be deleted.
              
          USAGE:
              drop_column('Customers', 'OldProducts')
              
              
      

For more information: help(MySqlDb)

## Author
* @le-prometheen - https://thepromethean.net/
