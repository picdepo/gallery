from flask import Flask, request, redirect, url_for, send_file, render_template, jsonify
import socket, applib, os


app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello, World!'


@app.route('/get_all_items')
def get_all_items():
    return 'Hello, World!'


# ?items_per_page=25&width=300&page=0
@app.route('/gallery')
def gallery():
    items_per_page = request.args.get('items_per_page', '25')
    page = request.args.get('page', '1')
    item_width = request.args.get('item_width', '250')

    #http://5.39.75.231:30001/width/400/t1722881510t6650c342-6a50-4fe7-b53c-67b0087d8db6.jpg
    list_items = applib.db_get_items(items_per_page, page)
    total_items = applib.db_get_items_count()

    total_pages = int(total_items / int(items_per_page)) + 1

    html_pager = ""
    for i in range(total_pages):
        a = "<a href=\"/gallery?page=%s\">%s</a>&nbsp;\n" % (i, i)
        html_pager = html_pager + a

    obj_tpl = {
        "base_url_resizer"  : os.environ['url_resizer'],
        "list_items"        : list_items,
        "item_width"        : item_width,
        "items_per_page"    : items_per_page,
        "page"              : page,
        "total_items"       : total_items,
        "total_pages"       : total_pages,
        "html_pager"        : html_pager
    }



    return render_template("gallery.html", obj_tpl = obj_tpl)





if __name__ == "__main__":
    if socket.gethostname() == "610757e602ef":
        app.run('0.0.0.0', 5003, debug = True)
    else:
        app.run('0.0.0.0', 5003)