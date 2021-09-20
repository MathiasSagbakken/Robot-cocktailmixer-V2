import json
import re
from measurement_conversion import metric2


def drink_order(ingredients_list, recepie, jsondata):
    dict_pos = {}
    volume = []
    teller = 0
    for i in range(len(ingredients_list)):
        dict_pos[str(ingredients_list[i])] = teller
        teller += 1

    index_list = []
    for i in range(len(recepie)):
        for j in range(len(recepie)):
            if str(recepie[i]) in str(jsondata["ingredients"][j]["name"]):
                volume.append(jsondata["ingredients"][j]["measure"])

    volume = metric2(volume)

    for i in range(len(recepie)):
        index_list.append(dict_pos[str(recepie[i])])



    return index_list, volume
