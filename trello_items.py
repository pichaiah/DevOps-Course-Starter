import requests
import json

key = "<your trello key>"
token = "<your trello token>"
headers = {
   "Accept": "application/json"
}
 

def create_board(board_name):
    url = "https://api.trello.com/1/boards/"
    querystring = {"name": board_name, "key": key, "token": token}
    response = requests.request("POST", url, params=querystring)
    board_id = response.json()["shortUrl"].split("/")[-1].strip()
    return board_id

def delete_board(id):
    url = f"https://api.trello.com/1/boards/{id}"
    querystring = {"key": key, "token": token}
    response = requests.request("DELETE", url, params=querystring)    
    return response.text

def get_board(id):
    url = f"https://api.trello.com/1/boards/{id}"
    querystring = {"key": key, "token": token}
    response = requests.request("GET", url, params=querystring)
    json_data = response.json()
    board = {"id": id, "name": json_data['name'] }    
    return board

def get_boards():
    url = "https://api.trello.com/1/members/me/boards"
    querystring = {"key": key, "token": token}
    response = requests.request("GET", url, params=querystring)
    data = [] 
    json_data = response.json()
    for entry in json_data:
        data.append({'id': entry['id'], 'name': entry['name']}) 
    return data

 
def create_list(board_id, list_name):
    url = f"https://api.trello.com/1/boards/{board_id}/lists"
    querystring = {"name": list_name, "key": key, "token": token}
    response = requests.request("POST", url, headers=headers, params=querystring)
    list_id = response.json()["id"]
    return list_id


def archive_list(id):
    url = f"https://api.trello.com/1/lists/{id}/closed"
    print("URL:{}",url)
    querystring = {"key": key, "token": token}
    response = requests.request("PUT", url, params=querystring)    
    return response.text

def get_lists(board_id):
    url = f"https://api.trello.com/1/boards/{board_id}/lists"
    querystring = {"key": key, "token": token}
    response = requests.request("GET", url, params=querystring)  
    data = [] 
    json_data = response.json()
    for entry in json_data:
        data.append({'id': entry['id'], 'name': entry['name']}) 
    return data

 
def create_card(list_id, card_name):
    url = f"https://api.trello.com/1/cards"
    querystring = {"name": card_name, "idList": list_id, "key": key, "token": token}
    response = requests.request("POST", url, params=querystring)
    card_id = response.json()["id"]
    return card_id

def move_card(list_id, card_id):
    url = f"https://api.trello.com/1/cards/{card_id}"
    querystring = {"id": card_id, "idList": list_id, "key": key, "token": token}
    response = requests.request("PUT", url, params=querystring)
    card_id = response.json()["id"]
    return card_id

def get_cards(list_id):
    url = f"https://api.trello.com/1/lists/{list_id}/cards"
    querystring = {"key": key, "token": token}
    response = requests.request("GET", url, params=querystring)
    data = [] 
    json_data = response.json()
    for entry in json_data:
        data.append({'id': entry['id'], 'name': entry['name']}) 
    return data

def get_card(id):
    url = f"https://api.trello.com/1/cards/{id}"
    querystring = {"key": key, "token": token}
    response = requests.request("GET", url, params=querystring)    
    json_data = response.json()    
    card = {'id': json_data['id'], 'name': json_data['name'], 'list_id': json_data['idList'], 'board_id':json_data['idBoard'] }
    return card

def get_cards_and_lists(board_d):
    lists = get_lists(board_d)
    cards = []
    for list in lists:
        list_id = list['id']
        list_name = list['name']
        list_cards = get_cards(list_id)
        for card in list_cards:
            cards.append({'id': card['id'], 'name': card['name'], 'list_id': list_id, 'list_name': list_name})    
    return cards
