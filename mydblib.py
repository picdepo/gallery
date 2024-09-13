#pip3 install mysql-connector-python
import os
import mysql.connector
from mysql.connector.cursor import MySQLCursorPrepared
import secretconf

def prp(msg):
    print(str(msg))
    print(type(msg))
    print(len(str(msg)))



def get_db():
    db_connection = mysql.connector.connect(
        host=secretconf.host,
        port = secretconf.port,
        user=secretconf.user,
        passwd=secretconf.passwd
    )
    prp(db_connection)
    return db_connection


def insert(table_name, obj_data, ignore = False):
    if ignore:
        sql = "insert ignore into " + table_name + " SET "
    else:
        sql = "insert into " + table_name + " SET "
    list_values = []
    for k, v in obj_data.items():
        if v == "now()":
            sql = sql + " " + k + " = now() ,"
            continue
        sql = sql + " " + k + " = %s ,"
        list_values.append(v)
    
    sql = sql.rstrip(",")
    prp(sql)

    con = get_db()
    cursor = con.cursor(cursor_class=MySQLCursorPrepared)
    prp(cursor)
    cursor.execute(sql, tuple(list_values))

    con.commit()


def select(sql, params = ()):
    con = get_db()
    cursor = con.cursor(dictionary=True)
    cursor.execute(sql, params)
    myresult = cursor.fetchall()
    
    con.commit()
    
    return myresult


def test_insert():
    pass
    table_name = "db1.users"
    obj_data = {}
    obj_data["project_code"] = "itschool"
    obj_data["email"] = "fake3@gmail.com"
    obj_data["f_name"] = "Alexey \"Алексей\""
    obj_data["c_date"] = "now()"
    insert(table_name, obj_data)


def test_select1():
    sql = "select * from poc1.items"
    res = select(sql)
    prp(res)


def test_select2():
    sql = "select * from poc1.items where id = %s"
    select(sql, (3,))



if __name__ == "__main__":
    #get_db()
    #test_insert()
    test_select1()
    #test_select2()