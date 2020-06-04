from flask import Flask, render_template, request, session, redirect, url_for

_STATUS = ['Not Started', 'In Progress', 'Completed']
app = Flask(__name__)
app.config.from_object('flask_config.Config')


@app.route('/', methods=['GET', 'POST'])
def get_items():
    items = {}
    if 'items' in session:
        items = session['items']
    return render_template("index.html", data=items)


@app.route('/add', methods=['GET', 'POST'])
def add_item():
    #statuses = ['Not Started', 'In Progress', 'Completed']
    items = dict({})
    if session.get('items'):
        items = session.get('items')

    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        status = request.form['status']
        todo_item = crate_item(title, description, status)
        items[todo_item["id"]] = todo_item
        session['items'] = items
        message = " To-DO Item with title '{}' added successfully!".format(title)
        return render_template("index.html", message=message, data=items)
    else:
        return render_template("add_new_item.html", statuses=_STATUS)

@app.route('/update', methods=['GET', 'POST'])
def update_item():
    #statuses = ['Not Started', 'In Progress', 'Completed']
    items = dict({})
    if session.get('items'):
        items = session.get('items')
    if request.method == 'POST':
        id_value = request.form['id']
        title = request.form['title']
        description = request.form['description']
        status = request.form['status']
        item = items[id_value]
        item["title"] = title
        item["description"] = description
        item["status"] = status
        items[id_value] = item
        session['items'] = items
        message = " To-DO Item with title '{}' updated successfully!".format(title)
        return render_template("index.html", message=message, data=items)
    else:
        id_value = request.args.get('id')
        item = items[id_value];
        return render_template("update_item.html", item=item, statuses=_STATUS)

@app.route('/delete')
def delete():
    items = {}
    if 'items' in session:
        items = session['items'];
    id = request.args.get('id')
    item = items[id];
    del items[id];
    message = " To-DO Item with title '" + item["title"] + "' deleted successfully!"
    session['items'] = items;
    return render_template("index.html", message=message, data=items)


def get_json_data(items):
    json_data = {}
    for k, v in items.items():
        json_data[k] = v.tojson()
    return json_data

def crate_item(title, description, status):
    id_value = findid()
    todo_item = dict()
    todo_item["id"] = str(id_value)
    todo_item["title"] = title
    todo_item["description"] = description
    todo_item["status"] = status
    return todo_item


def findid():
    items = {}
    if session.get('items'):
        items = session.get('items')
    max_id = 0
    for k in items.keys():
        if int(k) > max_id:
            max_id = int(k)
    return max_id+1;


if __name__ == '__main__':
    app.run()
