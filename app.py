from flask import Flask, render_template, request, session, redirect, url_for
import view_model as view_model
import db_items 

def create_app():
    app = Flask(__name__)    

    @app.route('/', methods=['Get'])
    def index():
        items = db_items.get_all_items()        
        item_view_model = view_model.ViewModel(items)
        return render_template('index.html', view_model=item_view_model) 

    @app.route('/add_todo', methods=['Post'])
    def add_todo_item():
        db_items.create_todo_item(request.form.get('title'))
        return redirect('/')

    @app.route('/move_to_doing/<todo_item_id>', methods=['Post'])
    def move_to_doing(todo_item_id):
        db_items.move_to_doing(todo_item_id)
        return redirect('/')

    @app.route('/move_to_done/<item_id>', methods=['Post'])
    def move_to_done(item_id):
        db_items.move_to_done(item_id)
        return redirect('/')

    @app.route('/delete_item/<item_id>', methods=['Post'])
    def remove_item(item_id):
        db_items.delete_item(item_id)
        return redirect('/')

    if __name__ == '__main__':
        app.run()

    return app