import json
import re
from read_json import valid_cocktails
import math


def metric(valid_indexes):

    f = open('cocktail_data.json',)

    data = json.load(f)

    #every 1 is 3 cl because the dispenser has max campacity of 3 cl
    thisdict = {
        "cl": 1/3,
        "dl": 10/3,
        "oz": 10,
        "L": 100/3,
        "ml": 1/30,
        "gal": 12.62,
        "tsp": 0.164,
        "shot": 1.5,
        "Fill with": 2,
        "cup": 8,
        "qt": 10,
        "tblsp": 0.5,
        "splashes": 0.25,
        "splash": 0.25,
        "dash": 0.25,
        "part": -1,
        "Top with": 1,
        "Fill to top": 2,
        "drops": 0.01
    }


    all_cocktails_updated = []
    for j in range(len(valid_indexes)):
        updated_dict = data[valid_indexes[j]]["ingredients"]
        for i in range(len(updated_dict)):
            mtrc = updated_dict[i]["measure"].split(" ")
            try:
                #new_measure = round(round(float(mtrc[0])*float(thisdict[str(mtrc[1])]), 1)*4)/4
                new_measure = round(float(mtrc[0])*float(thisdict[str(mtrc[1])]))
                if new_measure == 0:
                    new_measure = 1
            except:
                new_measure = "ignore"
            updated_dict[i]["measure"] = new_measure
        all_cocktails_updated.append(updated_dict)


    return all_cocktails_updated
#print(metric([407]))



def metric2(valid_indexes):

    f = open('cocktail_data.json',)

    data = json.load(f)

    #every 1 is 3 cl because the dispenser has max campacity of 3 cl
    thisdict = {
        "cl": 1/3,
        "dl": 10/3,
        "oz": 10,
        "L": 100/3,
        "ml": 1/30,
        "gal": 12.62,
        "tsp": 0.164,
        "shot": 1.5,
        "Fill with": 2,
        "cup": 8,
        "qt": 10,
        "tblsp": 0.5,
        "splashes": 0.25,
        "splash": 0.25,
        "dash": 0.25,
        "part": -1,
        "Top with": 1,
        "Fill to top": 2,
        "drops": 0.01
    }

    all_cocktails_updated = []
    for i in range(len(valid_indexes)):
        #print(valid_indexes[i]["measure"])
        mtrc = valid_indexes[i].split(" ")
        try:
            new_measure = round(float(mtrc[0])*float(thisdict[str(mtrc[1])]))
            if new_measure == 0:
                new_measure = 1
        except:
            new_measure = "ignore"
        valid_indexes[i] = new_measure
        all_cocktails_updated.append(new_measure)

    return all_cocktails_updated
