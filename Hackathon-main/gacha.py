import random
from types import NoneType
from weapon import Weapon

def gacha(items:dict)->Weapon:
    roll = round(random.random(),5)
    total = sum(items.values())
    curr_prob = 0
    for item in items:
        probability = items[item]/total
        curr_prob += probability
        if roll<=curr_prob:
            return item


def return_probability(item_name:str, items:dict)->float|NoneType:
    if item_name not in items:
        return None
    total = sum(items.values())
    return items[item_name]/total