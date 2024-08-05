import mydblib


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

    sql = "select * from picdepo.uploads order by id asc limit %s, %s" % (int(offset), int(limit))
    prp(sql)
    arr_data = mydblib.select(sql)
    return arr_data


def db_get_items_count():
    sql = "select count(*) cnt from picdepo.uploads"
    arr_data = mydblib.select(sql)
    return arr_data[0]["cnt"]


if __name__ == "__main__":
    db_get_items()