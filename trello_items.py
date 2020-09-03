import requests
import json
import os
import Item as it

headers = {
   "Accept": "application/json"
}

def get_all_items():
    params = (
        ('key', os.environ['KEY']),
        ('token', os.environ['TOKEN']),        
    )

    r = requests.get('https://api.trello.com/1/boards/' + os.environ['BOARD_ID'] + '/cards', params=params)
    data = r.json()
    item_list = []
    for card in data:
        if card['idList'] == os.environ['TODO_LIST_ID']:
            card['idList'] = 'To Do'
        elif card['idList'] == os.environ['DOING_LIST_ID']:
            card['idList'] = 'Doing'
        elif card['idList'] == os.environ['DONE_LIST_ID']:
            card['idList'] = 'Done'

        item_list.append(it.Item(id=card['id'], status=card['idList'], title=card['name'], last_modified=card['dateLastActivity']))
        
    return item_list

def create_todo_item(title):
    params = (
        ('key', os.environ['KEY']),
        ('token', os.environ['TOKEN']),
        ('name', title),
        ('idList', os.environ['TODO_LIST_ID'])
    )
    requests.post('https://api.trello.com/1/cards', params=params)

def move_to_doing(id):
    params = (
        ('key', os.environ['KEY']),
        ('token', os.environ['TOKEN']),
        ('idList', os.environ['DOING_LIST_ID'])
    )
    requests.put("https://api.trello.com/1/cards/" + id, params=params)

def move_to_done(id):    
    params = (
        ('key', os.environ['KEY']),
        ('token', os.environ['TOKEN']),
        ('idList', os.environ['DONE_LIST_ID'])
    )
    requests.put("https://api.trello.com/1/cards/" + id, params=params)

def delete_item(id):
    params = (
        ('key', os.environ['Key']),
        ('token', os.environ['TOKEN'])
    )
    requests.delete("https://api.trello.com/1/cards/" + id, params=params)

def create_board():
    params = (
        ('key', os.environ['Key']),
        ('token', os.environ['TOKEN']),
        ('name', 'TestBoard1234')
    )
    response = requests.post("https://api.trello.com/1/boards/", params=params)
    return response.json()['id']

def delete_board(id):
    params = (
        ('key', os.environ['Key']),
        ('token', os.environ['TOKEN'])
    )
    requests.delete("https://api.trello.com/1/boards/" + id, params=params)