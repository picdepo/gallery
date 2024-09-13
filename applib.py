import mydblib, secretconf


def prp(msg):
    #return
    print(str(msg))
    print(type(msg))
    print(len(str(msg)))


def db_get_items(items_per_page = 25, page = 0):

    #calculate limit ond offset 
    limit = items_per_page
    offset = (int(page)-1) * int(items_per_page)

    prp(limit)
    prp(offset)

    sql = "select * from %s.%s where image_c_date > '1970-01-01' order by image_c_date, id asc limit %s, %s" % (secretconf.dbname, secretconf.table_sort, int(offset), int(limit))
    prp(sql)
    arr_data = mydblib.select(sql)
    return arr_data


def db_get_items_count():
    sql = "select count(*) cnt from %s.%s where image_c_date > '1970-01-01'" % (secretconf.dbname, secretconf.table_sort)
    arr_data = mydblib.select(sql)
    return arr_data[0]["cnt"]


if __name__ == "__main__":
    db_get_items()