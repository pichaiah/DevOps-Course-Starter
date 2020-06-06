from flask import session

_DEFAULT_ITEMS = [
    {'id': 1, 'title': 'List saved todo items', 'description': '', 'status': 'Not Started'},
    {'id': 2, 'title': 'Allow new items to be added', 'description': '', 'status': 'Not Started'}
]


def get_items():
    """
    Fetches all saved items from the session.

    Returns:
        list: The list of saved items.
    """
    return session.get('items', _DEFAULT_ITEMS)


def get_item(id):
    """
    Fetches the saved item with the specified ID.

    Args:
        id: The ID of the item.

    Returns:
        item: The saved item, or None if no items match the specified ID.
    """
    items = get_items()
    return next((item for item in items if item['id'] == int(id)), None)


def add_item(title, description, status):
    """
    Adds a new item with the specified title to the session.

    Args:
        title: The title of the item.
        description: Details of the task
        status:  Status ['Not Started', 'In Progress', 'Completed']

    Returns:
        item: The saved item.
    """
    items = get_items()

    # Determine the ID for the item based on that of the previously added item
    id = items[-1]['id'] + 1 if items else 0

    item = {'id': id, 'title': title, 'description': description, 'status': status}

    # Add the item to the list
    items.append(item)
    session['items'] = items

    return item


def save_item(item):
    """
    Updates an existing item in the session. If no existing item matches the ID of the specified item, nothing is saved.

    Args:
        item: The item to save.
    """

    existing_items = get_items()
    updated_items = [item if item['id'] == existing_item['id'] else existing_item for existing_item in existing_items]
    session['items'] = updated_items

    return item


def delete_item(item):
    """
    Deleting an existing item in the session.
    If no existing item matches the ID of the specified item, nothing is deleted.

    Args:
        item: The item to delete.
    """
    items = get_items()
    if items.__contains__(item):
        items.remove(item)

    print("Deleted Items: {}".format(items))

    session['items'] = items

    return item
