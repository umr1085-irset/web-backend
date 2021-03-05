import loompy
import math
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import plotly.io as pio
import json
from matplotlib import pyplot as plt

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
    
def dict_to_json(d):
    '''
    Convert dictionary to JSON
    
    Params
    ------
    d: dict
        a dictionary
    
    Return
    ------
    JSON output
    '''
    return json.dumps(d)

def extract_attr_keys(loom_path):
    '''
    Extract column and row attribute keys from a Loom file in a dictionary
    
    Params
    ------
    loom_path : str
        Path to a .loom file
        
    Return
    ------
    dictionary
    '''
    df = loompy.connect(loom_path) # open loom connection
    attr_keys = {'col_attr_keys':df.ca.keys(),'row_attr_keys':df.ra.keys()}
    df.close() # close loom connection
    return attr_keys

def extract_attrs(loom_path):
    '''
    Extract column and row attributes from a Loom file in a dictionary
    
    Params
    ------
    loom_path : str
        Path to a .loom file
        
    Return
    ------
    dictionary
    '''
    col_attrs = dict() # empty dictionary to populate future column attributes dataframe
    row_attrs = dict() # empty dictionary to populate future gene attributes dataframe
    
    df = loompy.connect(loom_path) # open loom connection
    for key in df.ca.keys(): # for each column attribute
        col_attrs[key] = df.ca[key] # store attribute array
        
    for key in ['Entrez_ID','Ensembl_ID','Symbol']: # for each potential gene attribute
        try:
            row_attrs[key] = df.ra[key] # store attribute array
        except:
            row_attrs[key] = None # or define it as None
    df.close() # close loom connection
    
    return {'col_attrs': col_attrs, 'row_attrs': row_attrs}

def is_valid_attrs_list(loom_path,attrs):
    '''
    Check if attributes list only contains valid elements
    
    Params
    ------
    loom_path : str
        Path to a .loom file
    attrs: list
        Attributes list to be tested
        
    Return
    ------
    bool
    '''
    df = loompy.connect(loom_path)
    valid = df.ca.keys()
    df.close
    for attr in attrs:
        if attr not in valid:
            return False
    return True

def get_dataframe(loom_path,attrs):
    '''
    Extract column attributes from a Loom file and return them as a Pandas DataFrame
    
    Params
    ------
    loom_path : str
        Path to a .loom file
    attrs: list
        Attributes list
        
    Return
    ------
    Pandas DataFrame
    '''
    d = dict()
    df = loompy.connect(loom_path)
    for attr in attrs:
        d[attr] = df.ca[attr]
    df.close()
    return pd.DataFrame(d)

def label_count_attr(arr):
    '''
    Extract unique labels and their respective counts from an array
    
    Params
    ------
    arr : array
        A numpy array of values
        
    Return
    ------
    Array of labels and array of counts, sorted by counts in descending order
    '''
    labels, counts = np.unique(arr,return_counts=True) # get unique labels and respective counts
    idx = np.argsort(counts)[::-1] # get index of descending count order
    return labels[idx],counts[idx] # return sorted labels and counts

def pie_figure(df,attrs):
    '''
    Generate pie-like figure. Supports up to two attributes
    
    Params
    ------
    df : Pandas DataFrame
        DataFrame containing column attributes
    attrs : args
        Attributes list
        
    Return
    ------
    Plotly figure
    '''
    if len(attrs)==2:
        tmp = df.groupby([attrs[0],attrs[1]]).size().reset_index().rename(columns={0:'count'})
        fig = px.sunburst(tmp, path=[attrs[0], attrs[1]], values='count',color=attrs[1])
        fig.update_traces(textinfo="label+percent parent")
    else:
        labels,counts = label_count_attr(df[attrs[0]].values)
        fig = go.Figure(data=[go.Pie(labels=labels, values=counts, hole=.7)])
        fig.update_traces(textposition='inside', textinfo='percent')
    return fig

def bar_figure(df,attrs):
    '''
    Generate bar figure. Supports up to two attributes (stacked bar chart)
    
    Params
    ------
    df : Pandas DataFrame
        DataFrame containing columns
    attrs : args
        Attributes list
        
    Return
    ------
    Plotly figure
    '''
    if len(attrs)==2:
        tmp = df.groupby([attrs[0],attrs[1]]).size().reset_index().rename(columns={0:'count'})
        fig = px.bar(tmp, x=attrs[0], y="count", color=attrs[1])
    else:
        labels,counts = label_count_attr(df[attrs[0]])
        fig = go.Figure(data=[go.Bar(x=labels, y=counts)])
    return fig

def json_component(loom_path,style='pie',attrs=[],returnjson=True):
    '''
    Compute JSON from Plotly figure
    
    Params
    ------
    loom_path: str
        path to Loom file
    style: str
        plot style. Must be pie or bar
    attrs: list
        List of up to two attributes to plot
    '''
    if style not in ['pie','bar']:
        raise Exception('style must be one of [pie,bar]')
    if attrs==[]:
        raise Exception('empty attributes list given')
    if len(attrs)>2:
        raise Exception('attributes list contains more than two elements')
    if not is_valid_attrs_list(loom_path,attrs):
        raise Exception('attributes list must only contain valid attributes')
        
    df = get_dataframe(loom_path,attrs)

    if style=='pie':
        fig = pie_figure(df,attrs)
    elif style=='bar':
        fig = bar_figure(df,attrs)
    
    if returnjson:
        return json.loads(pio.to_json(fig, validate=True, pretty=False, remove_uids=True))
    else:
        return fig
    
def get_symbol_values(loom_path,symbol):
    '''
    Attempt to retrieve gene expression values
    
    Params
    ------
    loom_path: str
        path to Loom file
    symbol: str
        Potential symbol
    '''
    df = loompy.connect(loom_path)
    symbols = df.ra['Symbol']
    if symbol in symbols:
        idx = np.where(symbols==symbol)[0][0]
        symbol_values = df[idx,:]
        df.close()
        return symbol_values
    df.close()
    raise Exception('Input not a valid symbol name')

def check_color(loom_path,color):
    '''
    Check if color is a valid symbol or class name. Return the array of values for a
    valid symbol, or the class name if valid
    
    Params
    ------
    loom_path: str
        path to Loom file
    color: str
        Potential symbol or column attribute name
    '''
    try:
        return get_symbol_values(loom_path,color)
    except:
        df = loompy.connect(loom_path)
        if color not in df.ca.keys():
            raise Exception(f'color must be None, a valid gene symbol or one of {df.ca.keys()}')
        else:
            color = df.ca[color]
            df.close()
            return color

def discrete_scatter_gl(x,y,color):
    unique_classes = np.unique(color)
    fig = go.Figure()
    for unique_class_ in unique_classes:
        idx = np.where(color==unique_class_)[0]
        subX = x[idx]
        subY = y[idx]
        fig.add_trace(go.Scattergl(
                x=subX,
                y=subY,
                mode='markers',
                name=unique_class_
            )
        )
    return fig

def continuous_scatter_gl(x,y,color):
    fig = go.Figure(data=go.Scattergl(
        x = x, 
        y = y, 
        mode='markers',
        marker=dict(
            color=color,
            colorscale='magma',
            line_width=1)
    ))
    return fig
    
def scatter_figure_gl(df,color):
    '''
    Compute Plotly figure
    
    Params
    ------
    df: Pandas DataFrame
        dataframe with coordinnates and optional attribute
    color: arr or None
        Color attribute array
    '''
    x = df.X.values
    y = df.Y.values

    try:
        if color==None:
            fig = continuous_scatter_gl(x,y,color)
    except:
        if np.issubdtype(color.dtype, np.number): # if color is None or type of color array is numerical
            fig = continuous_scatter_gl(x,y,color)
        else: # discrete
            fig = discrete_scatter_gl(x,y,color)
    return fig
        
def json_scatter(loom_path,color=None,returnjson=True):
    df = get_dataframe(loom_path,['X','Y'])
    if color!=None:
        color = check_color(loom_path,color)
    fig = scatter_figure_gl(df,color)
    
    if returnjson:
        return json.loads(pio.to_json(fig, validate=True, pretty=False, remove_uids=True))
    else:
        return fig

def get_hexbin_attributes(hexbin):
    '''
    Extract hexagons attributes from Matplotlib hexbin object
    
    Params
    ------
    hexbin: Matplotlib hexbin
    
    Return
    ------
    hexagon, offsets, facecolors, values
    '''
    paths = hexbin.get_paths()
    points_codes = list(paths[0].iter_segments())#path[0].iter_segments() is a generator 
    prototypical_hexagon = [item[0] for item in points_codes]
    return prototypical_hexagon, hexbin.get_offsets(), hexbin.get_facecolors(), hexbin.get_array()

def make_hexagon(prototypical_hex, offset, fillcolor, linecolor=None):
    new_hex_vertices = [vertex + offset for vertex in prototypical_hex]
    vertices = np.asarray(new_hex_vertices[:-1])
    # hexagon center
    center=np.mean(vertices, axis=0)
    if linecolor is None:
        linecolor = fillcolor
    #define the SVG-type path:    
    path = 'M '
    for vert in new_hex_vertices:
        path +=  f'{vert[0]}, {vert[1]} L' 
    return  dict(type='path',
                 line=dict(color=linecolor, 
                           width=0.5),
                 path=  path[:-2],
                 fillcolor=fillcolor, 
                ), center 

def pl_cell_color(mpl_facecolors):
    '''
    From matplotlib facecolors to plotly cell colors
    '''
    return [ f'rgb({int(R*255)}, {int(G*255)}, {int(B*255)})' for (R, G, B, A) in mpl_facecolors]

def mpl_to_plotly(cmap, N):
    h = 1.0/(N-1)
    pl_colorscale = []
    for k in range(N):
        C = list(map(np.uint8, np.array(cmap(k*h)[:3])*255))
        pl_colorscale.append([round(k*h,2), f'rgb({C[0]}, {C[1]}, {C[2]})'])
    return pl_colorscale



def json_hexbin(loom_path,cmap=plt.cm.Greys,background='white',returnjson=True):
    '''
    Generate hexbin plot from X,Y scatter coordinates
    
    Params
    ------
    loom_path: str
        Path to a loom file
    cmap: Matplotlib Pyplot colormap
        Colormap from pyplot.cm collection
    background: str
        background of hexbin plot
    returnjson: bool
        Return Plotly figure or its JSON form
    
    Return
    ------
    Plotly figure or its JSON form
    '''
    df = get_dataframe(loom_path,['X','Y'])
    x = df['X'].values
    y = df['Y'].values
    HB = plt.hexbin(x,y,gridsize=20,cmap=cmap)
    xx = plt.draw()

    hexagon_vertices, offsets, mpl_facecolors, counts = get_hexbin_attributes(HB)
    cell_color = pl_cell_color(mpl_facecolors)

    shapes = []
    centers = []
    for k in range(len(offsets)):
        shape, center = make_hexagon(hexagon_vertices, offsets[k], cell_color[k])
        shapes.append(shape)
        centers.append(center)

    xlocs, ylocs = zip(*centers)
    cmapp = mpl_to_plotly(cmap, 11)
    text = [f'x: {round(xlocs[k],2)}<br>y: {round(ylocs[k],2)}<br>counts: {int(counts[k])}' for k in range(len(xlocs))]
    
    fig = go.Figure()
    fig.add_trace(
        go.Scatter(
             x=xlocs, 
             y=ylocs, 
             mode='markers',
             marker=dict(size=0.5, 
                         color=counts, 
                         colorscale=cmapp, 
                         showscale=True,
                         colorbar=dict(
                                     thickness=20,  
                                     ticklen=4
                                     )),
           text=text,
           hoverinfo='text'
          )
    )

    axis = dict(
        showgrid=False,
        showline=False,
        zeroline=False,
        ticklen=4 
    )

    fig.update_layout(
        width=530, height=550,
        xaxis=axis,
        yaxis=axis,
        xaxis_title='UMAP1',
        yaxis_title='UMAP2',
        hovermode='closest',
        shapes=shapes,
        plot_bgcolor=background)
    
    if returnjson:
        return json.loads(pio.to_json(fig, validate=True, pretty=False, remove_uids=True))
    else:
        return fig