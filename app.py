from flask import Flask, render_template, request, session, redirect, url_for
import session_items as session

_STATUS = ['Not Started', 'In Progress', 'Completed']
app = Flask(__name__)
app.config.from_object('flask_config.Config')


@app.route('/', methods=['GET', 'POST'])
def get_items():
    items = session.get_items()
    return render_template("index.html", data=items)


@app.route('/add', methods=['GET', 'POST'])
def add_item():
    items = session.get_items()
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        status = request.form['status']
        todo_item = session.add_item(title, description, status)
        return redirect(url_for('get_items'))
    else:
        return render_template("add_new_item.html", statuses=_STATUS)


@app.route('/update', methods=['GET', 'POST'])
def update_item():
    if request.method == 'POST':
        id_value = request.form['id']
        title = request.form['title']
        description = request.form['description']
        status = request.form['status']
        item = {'id': int(id_value), 'title': title, 'description': description, 'status': status}
        app.logger.info('%s going to save item', item)
        session.save_item(item)

        return redirect(url_for('get_items'))
    else:
        id_value = request.args.get('id')
        item = session.get_item(id_value)
        return render_template("update_item.html", item=item, statuses=_STATUS)


@app.route('/delete')
def delete():
    items = session.get_items()
    id_value = request.args.get('id')
    item = session.get_item(id_value)
    session.delete_item(item)
    return redirect(url_for('get_items'))


if __name__ == '__main__':
    app.run()
