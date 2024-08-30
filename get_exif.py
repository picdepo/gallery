import mydblib, secretconf, json
from datetime import datetime


def prp(msg):
    #return
    print(str(msg))
    print(type(msg))
    print(len(str(msg)))


def start():
    id = 4

    sql = "select * from " + secretconf.dbname + ".exif where id = %s"
    arr_data = mydblib.select(sql, (int(id),))
    prp(arr_data[0])
    str_json = (arr_data[0]["data"])
    obj_data = json.loads(str_json)
    prp(obj_data)
    prp(obj_data["EXIF DateTimeOriginal"])

    date_str = obj_data["EXIF DateTimeOriginal"]
    date_format = '%Y:%m:%d %H:%M:%S'

    date_obj = datetime.strptime(date_str, date_format)
    print(date_obj)








if __name__ == "__main__":
    start()