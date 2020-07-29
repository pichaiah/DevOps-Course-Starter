from flask import Flask, render_template, request, session, redirect, url_for
import trello_items as trello

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def get_boards():
    boards = trello.get_boards()
    return render_template("index.html", data=boards)

@app.route('/view_board', methods=['GET', 'POST'])
def view_board():
    id = request.args.get('id')    
    board = trello.get_board(id)
    lists = trello.get_lists(id)
    cards = trello.get_cards_and_lists(id)    
    return render_template("trello_board.html", board=board, lists=lists, cards=cards)

@app.route('/add_board', methods=['GET', 'POST'])
def add_board():    
    if request.method == 'POST':
        board_name = request.form['board_name']                
        trello.create_board(board_name)
        return redirect(url_for('get_boards'))
    else:        
        return render_template("add_new_board.html")

@app.route('/delete_board')
def delete_board():
    board_id = request.args.get('id')  
    trello.delete_board(board_id)
    return redirect(url_for('get_boards'))


@app.route('/add_list', methods=['GET', 'POST'])
def add_list():    
    if request.method == 'POST':
        board_id = request.form['board_id']
        list_name = request.form['list_name']
        trello.create_list(board_id, list_name)
        return redirect(url_for('view_board', id=board_id))
    else:
        board_id = request.args.get('board_id')
        board = trello.get_board(board_id)    
        return render_template("add_new_list.html", board=board)


@app.route('/add_card', methods=['GET', 'POST'])
def add_card():    
    if request.method == 'POST':
        card_name = request.form['card_name']
        list_id = request.form['list_id']
        board_id = request.form['board_id']         
        trello.create_card(list_id, card_name)
        return redirect(url_for('view_board', id=board_id))
    else:
        board_id = request.args.get('board_id')
        lists = trello.get_lists(board_id)
        return render_template("add_new_card.html", board_id=board_id, lists=lists)

@app.route('/move_card', methods=['GET', 'POST'])
def move_card():
    if request.method == 'POST':
        id = request.form['id']        
        board_id = request.form['board_id'] 
        list_id = request.form['list_id']                       
        trello.move_card(list_id, id)
        return redirect(url_for('view_board', id=board_id))
    else:
        board_id = request.args.get('board_id')
        card_id = request.args.get('card_id')
        lists = trello.get_lists(board_id)
        card = trello.get_card(card_id)        
        return render_template("move_card.html", card=card, lists=lists)

@app.route('/delete_card')
def delete_card():
    card_id = request.args.get('card_id')    
    board_id = request.args.get('board_id')
    trello.delet_card(card_id)
    return redirect(url_for('view_board', id=board_id))

if __name__ == '__main__':
    app.run()
