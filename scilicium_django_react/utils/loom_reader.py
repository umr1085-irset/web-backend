import loompy
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

def getAttributes(loom_file):
    try :
        ds = loompy.connect(loom_file)
        attributes = ds.attrs.keys()
        ds.close()
        return attributes
    except:
        ds.close()
        return("Error reading loom file")

def getClasses(loom_file,sep):
    ds = loompy.connect(loom_file)
    attributes = ds.attrs.keys()
    try :
        classes = ds.attrs.Classes.split(sep)
        ds.close()
        return classes
    except:
        ds.close()
        return("No classes available in file")

def getColumnAttributes(loom_file):
    ds = loompy.connect(loom_file)
    try :
        col_attributes = ds.ca.keys()
        ds.close()
        return col_attributes
    except:
        ds.close()
        return("Error getting columns attributes")

def getRowAttributes(loom_file):
    ds = loompy.connect(loom_file)
    try :
        row_attributes = ds.ra.keys()
        ds.close()
        return row_attributes
    except:
        ds.close()
        return("Error getting rows attributes")

def getCellCount(loom_file):
    """
        Return cell/sample count from loom file
        Samples/cells need to be list in column attribute 'Sample'
    """
    ds = loompy.connect(loom_file)
    try :
        col_attributes = ds.ca.keys()
        if "Sample" not in col_attributes :
            ds.close()
            return("Error loom format: no 'Sample' col attribute")

        cell_count = len(ds.ca.Sample)
        ds.close()
        return cell_count
    except:
        ds.close()
        return("Error getting cell count")

def getRepartitionCluster(loom_file,sep):
    """
        Return count of cluster for each classification from loom file
        Classifications need to be list the lomm file attributes
    """
    ds = loompy.connect(loom_file)
    try :
        repartition = []
        classes = ds.attrs.Classes.split(sep)
        for classification in classes:
            val = len(set(ds.ca[classification]))
            repartition.append({"label":classification,"value":val,"name":"Classification cluster repartition"})
        ds.close()
        return repartition
    except:
        ds.close()
        return("Error getting cluster repartition count")


def getCellCountByCluster(loom_file,cluster):
    """
        Return count of cluster for each classification from loom file
        Classifications need to be list the lomm file attributes
    """
    ds = loompy.connect(loom_file)
    try :
        repartition = []
        (unique, counts) = np.unique(ds.ca[cluster], return_counts=True)
        frequencies = np.asarray((unique, counts)).T
        for classification in frequencies:
            val = classification[1]
            repartition.append({"label":classification[0],"value":val,"name":cluster})
        ds.close()
        return repartition
    except:
        ds.close()
        return("Error getting cluster repartition count")

def getRowAttributes(loom_file):
    ds = loompy.connect(loom_file)
    try :
        row_attributes = ds.ra.keys()
        ds.close()
        return row_attributes
    except:
        ds.close()
        return("Error getting rows attributes")

def scatterFromLoom(loom_file,selected_class):
    ds = loompy.connect(loom_file)
    try:
        result_data = dict()
        result_data["data"] = list()
        uniq_classes = list(set(ds.ca[selected_class]))
        result_data["colors"] = random_color(len(uniq_classes))

        pos_color = 0
        for condition in uniq_classes :

            cond_color = result_data["colors"][pos_color]
            pos_color = pos_color + 1

            data = dict()
            data["x"]= list(ds.ca.X[np.where(ds.ca.clusters == condition)])
            data["y"]= list(ds.ca.Y[np.where(ds.ca.clusters == condition)])
            data["text"] = list(ds.ca.Sample[np.where(ds.ca.clusters == condition)])
            data['name'] = condition
            data['hoverinfo'] = "all"
            data['type'] = 'scattergl'
            data['mode']= 'markers'
            data['marker'] = { 'color': cond_color }

            result_data["data"].append(data)
        
        title = "Scatter plot colored by " + selected_class
        layout = dict()
        layout["paper_bgcolor"] ='rgba(0,0,0,0)'
        layout["plot_bgcolor"] ='rgba(0,0,0,0)'
        layout["title"] = title

        ds.close()
        return {"chart":result_data, "title":title,"layout":layout}

    except:
        ds.close()
        return("Error when convert loom to scatter")
    