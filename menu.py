#!/usr/bin/env python3

import pickle
from os import system
from scrap import get_link_from_page


cls = lambda: system('clear')
with open('dict_cars.pickle', 'rb') as pickle_in:
    cars_dict = pickle.load(pickle_in)
    cars_keys = list(cars_dict.keys())
    cars_values = list(cars_dict.values())
    cars_dict = dict()
    for i in range(len(cars_keys)):
        cars_dict[cars_keys[i]] = cars_values[i]
    for k, v in cars_dict.items():
        tmp_dict = {k: v}
        get_link_from_page(tmp_dict)
        cls()
