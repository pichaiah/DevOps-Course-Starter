import requests
import json
import os
from item import Item

headers = {
   "Accept": "application/json"
}

def get_all_items():
    params = (
        ('key', os.environ['TRELLO_KEY']),
        ('token', os.environ['TRELLO_TOKEN']),        
    )

    r = requests.get('https://api.trello.com/1/boards/' + os.environ['TRELLO_BOARD_ID'] + '/cards', params=params)
    data = r.json()
    item_list = []
    for card in data:
        if card['idList'] == os.environ['TRELLO_TODO_LIST_ID']:
            card['idList'] = 'To Do'
        elif card['idList'] == os.environ['TRELLO_DOING_LIST_ID']:
            card['idList'] = 'Doing'
        elif card['idList'] == os.environ['TRELLO_DONE_LIST_ID']:
            card['idList'] = 'Done'

        item_list.append(Item(id=card['id'], status=card['idList'], title=card['name'], last_modified=card['dateLastActivity']))
        
    return item_list

def create_todo_item(title):
    params = (
        ('key', os.environ['TRELLO_KEY']),
        ('token', os.environ['TRELLO_TOKEN']),
        ('name', title),
        ('idList', os.environ['TRELLO_TODO_LIST_ID'])
    )
    requests.post('https://api.trello.com/1/cards', params=params)

def move_to_doing(id):
    params = (
        ('key', os.environ['TRELLO_KEY']),
        ('token', os.environ['TRELLO_TOKEN']),
        ('idList', os.environ['TRELLO_DOING_LIST_ID'])
    )
    requests.put("https://api.trello.com/1/cards/" + id, params=params)

def move_to_done(id):    
    params = (
        ('key', os.environ['TRELLO_KEY']),
        ('token', os.environ['TRELLO_TOKEN']),
        ('idList', os.environ['TRELLO_DONE_LIST_ID'])
    )
    requests.put("https://api.trello.com/1/cards/" + id, params=params)

def delete_item(id):
    params = (
        ('key', os.environ['TRELLO_KEY']),
        ('token', os.environ['TRELLO_TOKEN'])
    )
    requests.delete("https://api.trello.com/1/cards/" + id, params=params)

def create_board():
    params = (
        ('key', os.environ['TRELLO_KEY']),
        ('token', os.environ['TRELLO_TOKEN']),
        ('name', 'TestBoard1234')
    )
    response = requests.post("https://api.trello.com/1/boards/", params=params)
    return response.json()['id']

def delete_board(id):
    params = (
        ('key', os.environ['TRELLO_KEY']),
        ('token', os.environ['TRELLO_TOKEN'])
    )
    requests.delete("https://api.trello.com/1/boards/" + id, params=params)