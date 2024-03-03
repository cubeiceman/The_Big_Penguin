import random
from types import NoneType
from weapon import Weapon

# items dictionary with Weapon a_weapon : integer probability
items = {
    Weapon("Weapon 1", 10, "images/random.png"):1,
    Weapon("Weapon 2", 20, "images/random.png"):3,
}

def gacha()->str:
    roll = round(random.random(),5)
    total = sum(items.values())
    curr_prob = 0
    for item in items:
        probability = items[item]/total
        curr_prob += probability
        if roll<=curr_prob:
            return item



def return_probability(item_name:str)->float|NoneType:
    if item_name not in items:
        return None
    total = sum(items.values())
    return items[item_name]/total