#!/usr/bin/env python3

from datetime import datetime
import mysql.connector as engine
from mysql.connector import Error

def flatten(iterable):
    '''Compress a list of nested lists into a single list.
    '''
    for item in iterable:
        if isinstance(item, (list, tuple)):
            yield from flatten(item)
        else:
            yield item


class MySqlDb:
    """A class wrapper for simplified SQL syntax and database interface.

    METHODS:

        create_table(table_name, columns)

            Creates a table in the database.


        write(table, column, data)

            Writes user data to the specified table in the apporpiate column.


        save_data()

            A thin wrapper for sqlite3.commit(). Calling this function
            commits the data and saves the current state of the database.
            Must be called before closing the database.

        rollback():

            Reverts changes because of exception


        closeall():

            Closes connection to the server.


        select(self, table, *columns **options)

            Retrieves and returns data from the specified table, column and row.


        update_row(self, table, field, primaryID, data)

            Insert into or Update data in a specified field in a specified row and table.


        get_max_id(self, table)

            Returns the highest row ID of the specified table.


        get_info(table):

            Returns a list of tuples containing information about each column.


        reset_id(self, table):

            Resets the row id values from 1.
            Use after rows have been dropped from the table.


        delete_null(self, table, field):

            Removes empty fields from the specified table


        get_tables(self):

            Returns a list of the tables contained within the database


        get_columns(table):

            Returns a list of column names


        select_table(columns):

            Find the first table containing all of the specified columns


        rename_table(table):

            Rename an existing table in the database
    """
    def __init__(self, **connect):
        '''**connect are mandatory kwargs:

             ARGUMENTS:
                 user=username
                 password=pass
                 host=hostname
                 database=dbname

             USAGE:
                 db = MySqlDb(user=username, password=pass, host=hostname, database=dbname)
        '''
        self.credentials = {**connect, 'auth_plugin': 'mysql_native_password'}
        self.user = self.credentials['user']
        self.db = self.credentials['database']

        try:
            self.konnect = engine.connect(**self.credentials)
            self.kursor = self.konnect.cursor(buffered=True)
            self.vers = self.konnect.get_server_info()

            if self.konnect.is_connected():
                print(f'\t\033[1;40mMySQL {self.vers}\n\tConnected to Database: {self.db}\033[00m')

        except Error as error:
            print(f'\t\033[1;31mConnection Error: {error}\033[00m')


    def __status__(self):
        connected = f'Version {self.vers} - Database: {self.db}'
        disconnected = f'Version {self.vers} Status \033[1;31mDisconnected.'
        return connected if self.konnect.is_connected() else disconnected


    def __repr__(self):
        return f'MySqlDB[ {self.__status__()} ]'


    def create_table(self, table):
        '''Create a new table in the database.

           ARGUMENTS:
               table: dict:
                      Pass in a specially formatted dictionary containing two keys:

                      'name': str: is the name of the table that is being created.

                      'fields': list: is a list of string formatted values representing fields'.

               Example:
                      MY_TABLE = {
                        'name': 'WebPages',
                        'fields': [
                            'urls VARCHAR(255) NOT NULL UNIQUE',
                            'content VARCHAR(255) NOT NULL',
                            'title VARCHAR(255) NOT NULL UNIQUE'
                            'submission_date DATE'
                        ]
                      }

           USAGE:
               Pass in the user created dictionary MY_TABLE:

               create_table(MY_TABLE)

           This method automatically adds an INTEGER PRIMARY KEY ID
           to each table row.
        '''
        try:
            fields = ', '.join(table['fields'])
            rowid = 'id INT NOT NULL AUTO_INCREMENT'
            self.kursor.execute(f"CREATE TABLE IF NOT EXISTS {table['name']}( {rowid}, {fields}, PRIMARY KEY ( id ))")

            print(f"\n\t\033[1;32;40mCreated Table: {table['name']}\033[00m\n")

        except Error as error:
            print(f'\t\033[1;31m{error}\033[00m')


    def get_info(self, table):
        '''Returns a list of tuples containing information
           about each column.
        '''
        try:
            self.kursor.execute(f"DESC {table};")
            return self.kursor.fetchall()

        except Error as error:
            print(f'\t\033[1;31m{error}')


    def write(self, table, fields, *data):

         '''Write data to the table into the specified field(s).

            USAGE:
                write('My_Table', 'Field_1, Field_2', data1, data2)

            ARGUMENTS:
                 table: str: the table name in string format
                 fields: str: a string of comma separated field names
                 *data: args: the data objects being passed to each corresponding field.
         '''
         try:
             values = ('%s, ' * len(data)).strip(', ')
             self.kursor.execute(f'INSERT IGNORE INTO {table} ({fields}) VALUES ({values})', tuple(data))
             print(f"\t\033[1;32;40mData Written to {table}\033[00m")

         except Error as error:
             print(f'\t\033[1;31m{error}\033[00m')


    def update_row(self, table, field, rowid, data):
        '''Insert into or update data in the specified field
           within the specified row and table.
        '''
        try:
            self.kursor.execute(f"UPDATE {table} SET {field}=%s WHERE Id={rowid}", (data,))
            print(f'\t\033[1;40mData Insert Into Field: {field} Row: {rowid}\033[00m')

        except Error as error:
            print(f'\t\033[1;31m{error}\033[00m')


    def get_max_id(self, table):
        '''Returns the maximum ID of the table
        '''
        self.kursor.execute(f'SELECT id FROM {table} ORDER BY id DESC LIMIT 1')
        return self.kursor.fetchone()[0]


    def reset_id(self, table):
        '''Resets the row id values from 1.
           Used after rows have been dropped from the table.
        '''
        try:
            if 'id' in self.get_columns(table):
                self.kursor.execute(f'ALTER TABLE {table} DROP COLUMN id')
            self.kursor.execute(f'ALTER TABLE {table} ADD COLUMN id INT NOT NULL AUTO_INCREMENT PRIMARY KEY FIRST')
            print(f'\t\033[1;40mAuto Increment Reset for Table {table}\033[00m')

        except Error as error:
            print(f'\t\033[1;31m{error}\033[00m')


    def delete_null(self, table, field):
        '''Removes empty fields from the table
        '''
        self.kursor.execute(f'DELETE FROM {table} WHERE {field} IS NULL')


    def get_tables(self):
        '''Returns a list of all tables in the database
        '''
        self.kursor.execute("SHOW TABLES")
        result = self.kursor.fetchall()
        return list(flatten(result))


    def get_columns(self, table):
        '''Returns a list of column names
        '''
        self.kursor.execute(f'SELECT * FROM {table}')
        columns = [description[0] for description in self.kursor.description]
        return columns


    def select_table(self, *columns):
        '''Find the first table containing all of the specified columns
        '''
        for table in self.get_tables():
            if all(item in self.get_columns(table) for item in columns):
                result = table
                break

        return result


    def rename_table(self, table, new_name):
        '''Rename an existing table in the database
        '''
        try:
            self.kursor.execute(f'ALTER TABLE {table} RENAME TO {new_name}\033[00m')

        except Error as error:
            print(f'\t\033[1;31m{error}\033[00m')


    def rename_column(self, table, column, new_name):
        '''Renames specified column/field within the specified table.
        '''
        try:
            self.kursor.execute(f'ALTER TABLE {table} RENAME COLUMN {column} TO {new_name}')
            print('\t\033[1;32;40mColumn {column} has been renamed {new_name}\033[00m')

        except Error as error:
            print(f'\t\033[1;31m{error}\033[00m')


    def drop_column(self, table, column):
        '''Deletes specified column from the specified table.
        '''
        try:
            self.kursor.execute(f'ALTER TABLE {table} DROP COLUMN {column}')
            print(f'\t\033[1;32;40mColumn {column} has been dropped from {table}\033[00m')

        except Error as error:
            print(f'\t\033[1;31m{error}\033[00m')


    def add_column(self, table, column, definition, where=None):
        '''Adds specified column to the specified table.

           USAGE:
               db.add_column('WebPages', 'Users', 'INT NOT NULL', 'AFTER urls')
               db.add_column('WebPages', 'Address', 'VARCHAR(10)', 'FIRST')
        '''
        location = 'FIRST' if where is None else where

        try:
            self.kursor.execute(f'ALTER TABLE {table} ADD COLUMN {column} {definition} {location}')
            print(f'\t\033[1;32;40mAdded Column {column} To {table}\033[00m')

        except Error as error:
            print(f'\t\033[1;31m{error}\033[00m')


    def select(self, table, *columns, **opts):
        '''Query a table or tables and retrieve specified data.

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
            columns: str:

           Optional keyword arguments for join formatting:

               target: str: the name of the table to be joined.

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

               join: str: the type of join
               key: str: the foreign or common key between tables used for joins
               where: str: condition determining row selection
        '''
        alldata = ('*', 'all')
        columns = self.get_columns(table) if columns[0] in alldata else columns

        try:
            prefix = f"SELECT {', '.join(columns)} FROM {table}"
            to_be_joined = [col for col in columns if col not in self.get_columns(table)]

            join_table = opts.get('target', self.select_table(*to_be_joined))
            join_class = opts.get('join', 'null')
            foreign_key = opts.get('key')
            condition = opts.get('where')

            ops = {
                'null': prefix,
                'left': f"{prefix} LEFT JOIN {join_table} USING({foreign_key})",
                'inner': f"{prefix} INNER JOIN {join_table} USING({foreign_key})",
                'cross': f"{prefix} CROSS JOIN {join_table}",
                'right': f"{prefix} RIGHT JOIN {join_table}",
            }

            if condition:
                selection = ops[join_class] + f' WHERE {condition}'

            else:
                selection = ops[join_class]

            self.kursor.execute(selection)
            return  self.kursor.fetchall()

        except Error as error:
            print(f'\t\033[1;31m{error}\033[00m')


    def save_data(self):
        '''Save the data to the datatable.
        '''
        try:
            self.konnect.commit()
            print('\t\033[1;32;40mData Has Been Saved to The Table\033[00m')

        except Error as error:
            print(f'\t\033[1;31m{error}\033[00m')


    def rollback(self):
        '''Reverts changes because of exception
        '''
        try:
            self.konnect.rollback()
            print('\t\033[1;32;40mData Reversion Sucessful\033[00m')

        except Error as error:
            print(f'\t\033[1;31m{error}\033[00m')


    def closeall(self):
        if self.konnect.is_connected():
            self.kursor.close()
            self.konnect.close()
            print("\t\033[1;32;40mMySQL Server Connection Closed\033[00m")



