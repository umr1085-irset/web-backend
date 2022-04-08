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

def createPieChart(data):
    """
        Format data to create pie chart with chartjs
        data: obj {label:label_value...}
        Return chartjs obj for pie chart
    """
    pie_data = dict()
    pie_data["labels"] = []
    pie_data["datasets"] = list()
    dataset = dict()
    dataset["backgroundColor"] = random_color(len(data))
    dataset["label"] = data[0]["name"]
    dataset["data"] = []
    for obj in data :
        pie_data["labels"].append(obj["label"])
        dataset["data"].append(obj["value"])
    pie_data["datasets"].append(dataset)
    
    return pie_data

def createDoughnutChart(data):
    """
        Format data to create doughnut chart with chartjs
        data: obj {label:label_value...}
        Return chartjs obj for pie chart
    """
    doughnut_data = dict()
    doughnut_data["labels"] = []
    doughnut_data["datasets"] = list()
    dataset = dict()
    dataset["backgroundColor"] = random_color(len(data))
    dataset["label"] = data[0]["name"]
    dataset["data"] = []
    for obj in data :
        doughnut_data["labels"].append(obj["label"])
        dataset["data"].append(obj["value"])
    doughnut_data["datasets"].append(dataset)
    
    return doughnut_data

def createBarChart(data):
    """
        Format data to create bar chart with chartjs
        data: obj {label:label_value...}
        Return chartjs obj for pie chart
    """
    bar_data = dict()
    bar_data["labels"] = []
    bar_data["datasets"] = list()
    dataset = dict()
    dataset["backgroundColor"] = random_color(len(data))
    dataset["label"] = data[0]["name"]
    dataset["data"] = []
    for obj in data :
        bar_data["labels"].append(obj["label"])
        dataset["data"].append(obj["value"])
    bar_data["datasets"].append(dataset)
    
    return bar_data