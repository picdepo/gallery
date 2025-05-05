import mydblib, secretconf


def prp(msg):
    #return
    print(str(msg))
    print(type(msg))
    print(len(str(msg)))


def db_get_items(date_from, date_to, items_per_page = 25, page = 0):

    #calculate limit ond offset 
    limit = items_per_page
    offset = (int(page)-1) * int(items_per_page)

    prp(limit)
    prp(offset)

    sql = "select * from %s.%s where deleted = 0 and image_c_date >= '%s' and image_c_date < '%s' order by sort_date, id asc limit %s, %s" % (secretconf.dbname, secretconf.table_sort, date_from, date_to, int(offset), int(limit))
    prp(sql)
    arr_data = mydblib.select(sql)
    return arr_data


def db_get_items_count(date_from, date_to):
    sql = "select count(*) cnt from %s.%s where deleted = 0 and image_c_date >= '%s' and image_c_date < '%s'" % (secretconf.dbname, secretconf.table_sort, date_from, date_to)
    arr_data = mydblib.select(sql)
    return arr_data[0]["cnt"]


if __name__ == "__main__":
    db_get_items()