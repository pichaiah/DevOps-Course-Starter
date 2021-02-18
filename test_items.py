import pytest
import view_model as view_model
import datetime
from item import Item
    
@pytest.fixture
def test_items():
    today = datetime.datetime.utcnow()
    yesterday = today - datetime.timedelta(days=1)    
    item_list = [
        Item(1, 'To Do', 'Task1', today),
        Item(2, 'To Do', 'Task2', today),
        Item(3, 'Doing', 'Task3', today),
        Item(4, 'Doing', 'Task4', today),
        Item(5, 'Doing', 'Task5', today),
        Item(6, 'Done', 'Task6', today),
        Item(7, 'Done', 'Task7', today),
        Item(8, 'Done', 'Task8', today),
        Item(9, 'Done', 'Task8', today),
        Item(10, 'Done', 'Task10', yesterday),
        Item(11, 'Done', 'Task11', yesterday),
        Item(12, 'Done', 'Task12', yesterday)
    ]

    test_list = view_model.ViewModel(item_list)

    return test_list

@pytest.fixture
def test_items2():
    today = datetime.datetime.utcnow()    
    yesterday = today - datetime.timedelta(days= 1)   
    item_list = [ 
        Item(1, 'To Do', 'Task1', today),
        Item(2, 'To Do', 'Task2', today),
        Item(3, 'Doing', 'Task3', today),
        Item(4, 'Doing', 'Task4', today),
        Item(5, 'Done', 'Task5', today),
        Item(6, 'Done', 'Task6', yesterday),
        Item(7, 'Done', 'Task7', yesterday),
        Item(8, 'Done', 'Task8', yesterday)
    ]
    
    test_list = view_model.ViewModel(item_list)
    return test_list

@pytest.fixture
def test_items3():
    today = datetime.datetime.utcnow()    
    yesterday = today - datetime.timedelta(days= 1)
    item_list = [   
        Item(1, 'Doing', 'Task1', today),
        Item(2, 'Doing', 'Task2', today),
        Item(3, 'Done', 'Task3', today),
        Item(4, 'Done', 'Task4', today),
        Item(5, 'Done', 'Task5', today),
        Item(6, 'Done', 'Task6', yesterday),
        Item(7, 'Done', 'Task7', yesterday)
    ]

    test_list = view_model.ViewModel(item_list)

    return test_list

def test_to_do_items_count(test_items):
    todo = test_items.todo_items
    assert len(todo) == 2

def test_doing_items_count(test_items):
    doing = test_items.doing_items
    assert len(doing) == 3

def test_done_items_count(test_items):
    done = test_items.done_items
    assert len(done) == 7

def test_recent_done_items_count(test_items):
    today_items = test_items.recent_done_items
    assert len(today_items) == 4

def test_older_done_items_count(test_items):
    today_items = test_items.older_done_items
    assert len(today_items) == 3

def test_show_all_items_more_than_5(test_items):
    show_all = test_items.show_all_done
    assert len(show_all) == 4

def test_show_all_items_less_than_5(test_items2):
    show_all = test_items2.show_all_done
    assert len(show_all) == 4

def test_show_all_items_equal_to_5(test_items3):
    show_all = test_items3.show_all_done
    assert len(show_all) == 5