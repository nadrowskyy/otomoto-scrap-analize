#!/usr/bin/env python

import pickle
from os import system
from scrap import get_link_from_page


cls = lambda: system('cls')
with open('dict_cars_tn.pickle', 'rb') as pickle_in:
    cars_dict = pickle.load(pickle_in)
    for k, v in cars_dict.items():
        print('here')
        tmp_dict = {k: v}
        get_link_from_page(tmp_dict)
        cls()
