import matplotlib.pyplot as plt
import json
from matplotlib.patches import Shadow
from difflib import SequenceMatcher

with open(r"foods.json") as jsonFile:
    jsonObject = json.load(jsonFile)
    jsonFile.close()


def high(type_):
    """
    Sort all foods by nutritive composition.
    :param type_: Can accept acronyms of carbohydrates, fat and proteins. such as f, p, c, cf, cp and fp
    :type type_: string
    :return: list of foods sorted by the input parameters.
    """
    kind = 'proteins'
    if type_ == 'f':
        kind = 'fat'
    elif type_ == 'c':
        kind = 'carbohydrates'
    elif type_ == 'cf':
        kind = 'carbohydrates and fat'
    elif type_ == 'cp':
        kind = 'carbohydrates and proteins'
    elif type_ == 'fp':
        kind = 'fat and proteins'
    lines = sorted(jsonObject, key=lambda k: k['percentage'][type_], reverse=True)
    result = "list of all foods by " + kind + " :\n"
    for i, index in enumerate(lines, start=1):
        result += index['name'] + " : " + str(int(index['percentage'][type_] * 10_000) / 100) + '%\n'
        if i % 10 == 0:
            result += '---------------------------\n'
    return result


def similar(a, b):
    """
    Compare two words.
    :param a: the user word
    :type a: string
    :param b: word from the database to compere with
    :type b: string
    :return: percentage of similarity between the two words.
    """
    return SequenceMatcher(None, a, b).ratio()


def get_item(message):
    """
    Creates an image of the nutritive composition of a certain food.
    :param message: the food item
    :type message: string
    :return: image of the graph.
    """
    message = message.lower()
    similarity = 0.6
    for index in jsonObject:
        s = similar(message, index["name"].lower())
        if s > similarity:
            similarity = s
            item = index

    if 'item' in locals():
        p = str(item['proteins'] / 10_000)
        f = str(item['fat'] / 10_000)
        c = str(item['carbohydrates'] / 10_000)
        bot_response = f'{item["name"]}\nfat : {f}g\nproteins : {p}g\ncarbohydrates : {c}g\n '
        sizes = [p, f, c]
        labels = ['proteins', 'fat', 'carbohydrates']
        fig = plt.figure(figsize=(9, 9))
        ax = fig.add_axes([0.1, 0.1, 0.8, 0.8])
        explode = (0, 0.05, 0)
        colors = ["orange", "yellow", "brown"]

        pies = ax.pie(sizes, explode=explode, labels=labels, autopct='%1.1f%%', colors=colors)
        for w in pies[0]:
            w.set_gid(w.get_label())
            w.set_edgecolor("none")

        for w in pies[0]:
            s = Shadow(w, -0.01, -0.01)
            s.set_gid(w.get_gid() + "_shadow")
            s.set_zorder(w.get_zorder() - 0.1)
            ax.add_patch(s)
        plt.savefig('img.png')

    else:
        bot_response = 'I didn\'t understand what you wrote.'

    print(f'Bot response:\n{bot_response}')
    return bot_response
