'''
Author: Mamunur Rahman
'''

import mysql.connector

mydb = mysql.connector.connect(
        host = 'localhost',
        user = 'root',
        password = 'root',
        database = 'testdb'
        )

mycursor = mydb.cursor()

# create a function that will show all the records of a table
def show_table(table_name):
    mycursor.execute(f"SELECT * FROM {table_name}")
    myresult = mycursor.fetchall()
    # myresult = mycursor.fetchone()
    for x in myresult:
      print(x)

## create a database naming testdb
#mycursor.execute('CREATE DATABASE testdb')

# show the available databases
mycursor.execute('SHOW DATABASES')
for db in mycursor:
    print(db)

# create a table naming students
sql =   'CREATE TABLE students \
        (studentID int PRIMARY KEY AUTO_INCREMENT, \
         name VARCHAR(100), \
         age smallint UNSIGNED)'
mycursor.execute(sql)

# show all the table names in the database
mycursor.execute("SHOW TABLES")
for x in mycursor:
     print(x)
     
# show the columns of the table 'students'
sql =  "SHOW COLUMNS \
        FROM students"
mycursor.execute(sql)
myresult = mycursor.fetchall()
for x in myresult:
  print(x)

### alter a table
# add a column
sql =  'ALTER TABLE students \
        ADD Email varchar(255)'
mycursor.execute(sql)
# delete a column
sql =  'ALTER TABLE students \
        DROP COLUMN Email'
mycursor.execute(sql)

# insert a single row into a table
sql = 'INSERT INTO students(name, age) \
       VALUES(%s, %s)'
val = ('Bob', 66)
mycursor.execute(sql, val)
mydb.commit()
show_table('students')

# insert multiple rows at a time
sql =  'INSERT INTO students(name, age) \
        VALUES(%s, %s)'
val = [('David', 45),
       ('Emma', 35),
       ('Mary', 33),
       ('Alex', 55)]
mycursor.executemany(sql, val)
mydb.commit()
show_table('students')

##Filter    
# Select record(s) where the name is 'David'
sql =  "SELECT * \
        FROM students \
        WHERE name = %s"
val = ('David', )
mycursor.execute(sql, val)
myresult = mycursor.fetchall()
for x in myresult:
  print(x)

##Filter 
#Wild characters   
# Select record(s) where the name contains 'ob'
sql =  "SELECT * \
        FROM students \
        WHERE name LIKE '%bo%'"
mycursor.execute(sql)
myresult = mycursor.fetchall()
for x in myresult:
  print(x) 
    
# sort the result
sql =  "SELECT * \
        FROM students \
        ORDER BY age"
## descending order
#sql = "SELECT * FROM students ORDER BY age DESC"
mycursor.execute(sql)
myresult = mycursor.fetchall()
for x in myresult:
  print(x)

# Delete Record
sql =  "DELETE \
        FROM students \
        WHERE name = %s"
val = ('Bob', )
mycursor.execute(sql, val)
mydb.commit()
print(mycursor.rowcount, "record(s) deleted")

# Delete a Table
sql = "DROP TABLE IF EXISTS customers"
mycursor.execute(sql)

# update existing records in a table by using the "UPDATE" statement
sql =  "UPDATE students \
        SET name = %s \
        WHERE name = %s"
val = ('Boby', 'Emma')
mycursor.execute(sql, val)
mydb.commit()
print(mycursor.rowcount, "record(s) affected")

# limit the number of records returned from the query, by using the "LIMIT" statement
sql =  "SELECT * \
        FROM students \
        LIMIT 3 OFFSET 0"
mycursor.execute(sql)
myresult = mycursor.fetchall()
for x in myresult:
  print(x)

# create a new table naming grades
mycursor.execute('CREATE TABLE grades (name VARCHAR(100), grade VARCHAR(1))')
# insert multiple rows at a time
sql =  'INSERT INTO grades(name, grade) \
        VALUES(%s, %s)'
val = [('David', 'B'),
       ('Emma', 'A'),
       ('Mary', 'C'),
       ('Alex', 'D')]
mycursor.executemany(sql, val)
mydb.commit()
show_table('grades')

# join two tables
sql = "SELECT students.studentID, students.name, grades.grade \
    FROM students \
    LEFT JOIN grades ON students.name = grades.name"
# INNER JOIN, LEFT JOIN, RIGHT JOIN
mycursor.execute(sql)
myresult = mycursor.fetchall()
for x in myresult:
  print(x)

#export the join output to a pandas dataframe
import pandas as pd
df = pd.DataFrame(myresult, columns =['studentID', 'name', 'grade'])
df.head()
#print(df)

### convert pandas dataframe to a sql table
# step-1: create a table
sql =   'CREATE TABLE joined_table \
        (studentID int PRIMARY KEY, \
         name VARCHAR(100), \
         grade VARCHAR(1))'
mycursor.execute(sql)
# step-2: insert multiple rows at a time
sql =  'INSERT INTO joined_table(studentID, name, grade) \
        VALUES(%s, %s, %s)'
# convert pandas dataframe into a list of tuples
val = [tuple(x) for x in df.values]
mycursor.executemany(sql, val)
mydb.commit()
show_table('joined_table')

