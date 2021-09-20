import json
import re


def valid_cocktails(ingredients):

    ingredients = [drinks.capitalize() for drinks in ingredients]

    f = open('cocktail_data.json',)

    data = json.load(f)

    valid_drinks = []
    index_json = []
    index_count = 0

    for i in data:
        temp_list = []
        for j in i["ingredients"]:
            temp_list.append(j["name"])
        valid = len(temp_list)
        for j in range(len(ingredients)):
            r = [l for l, item in enumerate(temp_list) if re.search(r"\b%s\b" % str(ingredients[j]), item)]
            if len(r) > 0:
                valid -= 1
                del temp_list[r[0]]
        if valid == 0:
            valid_drinks.append(i["name"])
            index_json.append(index_count)
        index_count +=1
    return index_json
