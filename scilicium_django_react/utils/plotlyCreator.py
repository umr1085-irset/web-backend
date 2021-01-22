import math
import numpy as np

def random_color(NbColors):
    pi = 3.14159265359
    pid2 = pi/2
    angle = 0
    step = pi/(NbColors)
    ListOfColors = []
    for i in range(0,NbColors):
        R = round((math.cos(angle)+1)/2 * 200)
        G = round((math.cos(angle-pid2)+1)/2 * 200)
        B = round((math.cos(angle-pi)+1)/2 * 200)
        A = 0.4
        angle = angle + step
        ListOfColors.append('rgba('+str(R)+','+str(G)+','+str(B)+','+str(A)+')')
    return ListOfColors

def createPiePlotly(data):
    """
        Format data to create pie chart with plotlyjs
        data: obj {label:label_value...}
        Return chartjs obj for pie chart
    """
    pie_data = dict()
    pie_data["values"] = []
    pie_data["labels"] = []
    pie_data["type"] = 'pie'
    for obj in data :
        pie_data["labels"].append(obj["label"])
        pie_data["labels"].append(obj["value"])

    layout = {"height": 400,"width": 500}
    return {"data":[pie_data],"layout":layout}