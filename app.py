from flask import Flask, request, redirect, url_for, send_file, render_template, jsonify
import socket, applib, os, mydblib, secretconf


app = Flask(__name__)


def prp(msg):
    #return
    print(str(msg))
    print(type(msg))
    print(len(str(msg)))


@app.route('/log/headers')
def log_headers():
    prp(request.headers)
    return "log"


@app.route('/')
def hello_world():
    return redirect("/gallery", code=302)


@app.route('/get_all_items')
def get_all_items():
    return 'Hello, World!'


# ?items_per_page=25&width=300&page=0
@app.route('/gallery', methods=['GET', 'POST'])
def gallery():
    items_per_page = request.args.get('items_per_page', '25')
    page = request.args.get('page', '1')
    item_width = request.args.get('item_width', '250')

    date_from   = request.args.get('date_from', '1970-01-01')
    date_to     = request.args.get('date_to', '3000-01-01')


    #http://5.39.75.231:30001/width/400/t1722881510t6650c342-6a50-4fe7-b53c-67b0087d8db6.jpg
    list_items = applib.db_get_items(date_from, date_to, items_per_page, page)
    prp(list_items)
    total_items = applib.db_get_items_count(date_from, date_to)
    prp("total items:" + str(total_items))

    total_pages = int(total_items / int(items_per_page)) + 1

    html_pager = ""
    for i in range(1, total_pages):
        a = "<a href=\"/gallery?date_from=%s&date_to=%s&item_width=%s&page=%s&items_per_page=%s\">%s</a>&nbsp;\n" % (date_from, date_to, item_width, i, items_per_page, i)
        html_pager = html_pager + a

    prev_page = int(page) - 1
    if prev_page < 1:
        prev_page = 1

    next_page = int(page) + 1
    if next_page > total_pages:
        nwxt_page = total_pages

    obj_tpl = {
        "base_url_resizer"  : os.environ['url_resizer'],
        "list_items"        : list_items,
        "item_width"        : item_width,
        "items_per_page"    : items_per_page,
        "page"              : page,
        "next_page"         : next_page,
        "prev_page"         : prev_page,
        "total_items"       : total_items,
        "total_pages"       : total_pages,
        "html_pager"        : html_pager,
        "date_from"         : date_from,
        "date_to"           : date_to
    }

    return render_template("gallery.html", obj_tpl = obj_tpl)


@app.route('/item/<item_id>', methods=['GET', 'POST'])
def item(item_id):
    try:
        sql = "select * from " + secretconf.dbname + "." + secretconf.table_sort + " where id = %s and deleted = 0"
        arr_data = mydblib.select(sql, (int(item_id),))

        prp(arr_data)

        obj_tpl = {
            "base_url_resizer"  : os.environ['url_resizer'],
            "item_data" : arr_data[0]
        }
        return render_template("item.html", obj_tpl = obj_tpl)
    except Exception as e:
        return "Not Found"


@app.route('/item/delete/<item_id>', methods=['GET', 'POST'])
def item_delete(item_id):
    sql = "select * from " + secretconf.dbname + "." + secretconf.table_sort + " where id = %s"
    arr_data = mydblib.select(sql, (int(item_id),))

    prp(arr_data)
    md5 = arr_data[0]["file_md5"]
    prp(md5)

    #TODO: add try catch
    obj_insert = {
        "md5" : md5,
        "c_date" : 'now()'
    }
    mydblib.insert(secretconf.dbname + ".deleted", obj_insert, True)

    #sql = "delete from " + secretconf.dbname + "." + secretconf.table_sort + " where file_md5 = %s"
    #arr_data = mydblib.select(sql, (md5,))
    #prp(arr_data)
    sql = "update " + secretconf.dbname + "." + secretconf.table_sort + " set deleted=1 where file_md5 = %s"
    arr_data = mydblib.select(sql, (md5,))
    prp(arr_data)

    return str(item_id)

if __name__ == "__main__":
    if socket.gethostname() == "610757e602ef":
        app.run('0.0.0.0', 5005, debug = True)
    else:
        app.run('0.0.0.0', 5003)