import loompy
import pandas as pd
from matplotlib import pyplot as plt
import matplotlib.colors as clr
import plotly.graph_objects as go
import plotly.express as px
import plotly.io as pio
import numpy as np
import json
import time
from copy import copy
from io import BytesIO
from PIL import Image
import requests
import matplotlib
import matplotlib.cm as cm
import math
from django.conf import settings
import os

N_MAX_CELLS = 20000

def get_available_reductions(loom_path):
    '''
    Return labels of available reduction as list
    
    Params
    ------
    loom_path : str
        Path to a loom file
        
    Return
    ------
    list
    '''
    df = loompy.connect(loom_path,'r')
    red_json = json.loads(df.attrs['reductions'])
    df.close()
    return list(red_json.keys())

def get_reduction_x_y(loom_path,reduction):
    '''
    Return reduction X,Y labels
    
    Params
    ------
    loom_path : str
        Path to a .loom file
    reduction: str
        Name of reduction being used
        
    Return
    ------
    Tuple of X,Y labels
    '''
    df = loompy.connect(loom_path,'r')
    red_json = json.loads(df.attrs['reductions'])
    df.close()
    return red_json[reduction]

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
    df = loompy.connect(loom_path,'r') # open loom connection
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
    
    df = loompy.connect(loom_path,'r') # open loom connection
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
    df = loompy.connect(loom_path,'r')
    valid = df.ca.keys()
    df.close()
    for attr in attrs:
        if attr not in valid:
            return False
    return True

def multiple_intersect(arr):
    tmp = arr[0]
    for a in arr[1:]:
        tmp = np.intersect1d(tmp,a)
    return tmp

def get_filter_indices(loom_path,filt):
    '''
    Extract column indices, row indices matching filter
    
    Params
    ------
    loom_path : str
        Path to a .loom file
    filt: dict
        Dictionary containing column and row filters
        
    Return
    ------
    column indices, row indices matching filter
    '''
    
    df = loompy.connect(loom_path,'r') # open loom file

    try:
        cidx_filter = [] # empty list to store indices of columns
        for k in filt['ca'].keys(): # for each column attribute key 
            cidx_filter.append(np.where(np.isin(df.ca[k], filt['ca'][k])==True)[0])
        cidx_filter = multiple_intersect(cidx_filter)
    except:
        cidx_filter = None
    
    try:
        ridx_filter = [] # epmty list to store indices of rows
        for k in filt['ra'].keys(): # for each row attribute key
            ridx_filter.append(np.where(np.isin(df.ra[k],filt['ra'][k])==True)[0])
        ridx_filter = multiple_intersect(ridx_filter)
    except:
        ridx_filter = None
        
    df.close() # close loom file
    return cidx_filter,ridx_filter

def get_dataframe(loom_path,attrs,cidx_filter=None):
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
    df = loompy.connect(loom_path,'r')
    for attr in attrs:
        if isinstance(cidx_filter, np.ndarray):
            d[attr] = df.ca[attr][cidx_filter]
        else:
            d[attr] = df.ca[attr]
    df.close()
    return pd.DataFrame(d)

def n_colors_old(n):
    l = ['#8BC34A','#FFC107','#3F51B5','#9C27B0','#E91E63','#008C93','#CDDC39','#FFE708','#22ADF2','#FF7224','#BC199D','#DB0B29','#5C8C1E','#EA9713','#3A4884','#712B7F','#B2265B','#0C685D','#AFB53A','#E2C729','#2996C1','#E53C20','#7F2877','#A50A1D','#C0F96E','#F9F15F','#7095F2','#CA2FEA','#FC63A1','#22C6AE','#D1EF7F','#F4EAB3','#86DCF7','#F7AD8D','#F757E1','#EF5472','#99AF69','#FCC57C','#7586BC','#9D59AD','#E25D93','#33A090','#D8D861','#F9DF70','#58C7E0','#FC6C65','#A553A1','#CC2E45','#D6A427','#63554B']
    
    return l[:n]

def n_colors(NbColors,rgbonly=False):
    ListOfColors = []
    phis = np.linspace(0, 2*np.pi, NbColors+1)
    for phi in phis[:-1]:
        R = round(.5*(1.+np.cos(phi))*255)
        G = round(.5*(1.+np.cos(phi+2*np.pi/3))*255)
        B = round(.5*(1.+np.cos(phi-2*np.pi/3))*255)
        A = .6
        if rgbonly:
            ListOfColors.append('rgb('+str(R)+','+str(G)+','+str(B)+')')            
        else:
            ListOfColors.append('rgba('+str(R)+','+str(G)+','+str(B)+','+str(A)+')')
    return ListOfColors

def n_colors_float(NbColors):
    ListOfColors = []
    phis = np.linspace(0, 2*np.pi, NbColors+1)
    A = 0.6
    for phi in phis[:-1]:
        R = round(.5*(1.+np.cos(phi))*255)
        R = round(A*R + (1-A)*255)/255
        G = round(.5*(1.+np.cos(phi+2*np.pi/3))*255)
        G = round(A*G + (1-A)*255)/255
        B = round(.5*(1.+np.cos(phi-2*np.pi/3))*255)
        B = round(A*B + (1-A)*255)/255
        ListOfColors.append((R,G,B,1))
    #print(ListOfColors)
    return ListOfColors

# def n_colors(NbColors,rgbonly=False):
#     pi = 3.14159265359
#     pid2 = pi/2
#     angle = 0
#     step = pi/(NbColors)
#     ListOfColors = []
#     for i in range(0,NbColors):
#         R = round((math.cos(angle)+1)/2 * 200)
#         G = round((math.cos(angle-pid2)+1)/2 * 200)
#         B = round((math.cos(angle-pi)+1)/2 * 200)
#         A = .4
#         angle = angle + step
#         if rgbonly:
#             ListOfColors.append('rgb('+str(R)+','+str(G)+','+str(B)+')')            
#         else:
#             ListOfColors.append('rgba('+str(R)+','+str(G)+','+str(B)+','+str(A)+')')
#     #print(ListOfColors)
#     return ListOfColors

# def n_colors_float(NbColors):
#     pi = 3.14159265359
#     pid2 = pi/2
#     angle = 0
#     step = pi/(NbColors)
#     ListOfColors = []
#     for i in range(0,NbColors):
#         R = round((math.cos(angle)+1)/2 * 200)
#         R = round(0.4*R + (1-0.4)*255)/255
#         G = round((math.cos(angle-pid2)+1)/2 * 200)
#         G = round(0.4*G + (1-0.4)*255)/255
#         B = round((math.cos(angle-pi)+1)/2 * 200)
#         B = round(0.4*B + (1-0.4)*255)/255
#         A = 1
#         angle = angle + step
#         ListOfColors.append((R,G,B,A))
#     #print(ListOfColors)
#     return ListOfColors

#def n_colors(NbColors,forcefloat=False):
#    pi = 3.14159265359
#    pid2 = pi/2
#    angle = 0
#    step = pi/(NbColors)
#    ListOfColors = []
#    alpha = .4
#    alpha_inv = .6
#    for i in range(0,NbColors):
#        R = round((math.cos(angle)+1)/2 * 200)
#        R = round(alpha*R + alpha_inv*255)
#        G = round((math.cos(angle-pid2)+1)/2 * 200)
#        G = round(alpha*G + alpha_inv*255)
#        B = round((math.cos(angle-pi)+1)/2 * 200)
#        B = round(alpha*B + alpha_inv*255)
#        A = 1
#        angle = angle + step
#        if forcefloat:
#            R /= 255
#            G /= 255
#            B /= 255
#            ListOfColors.append((R,G,B,A))
#        else:
#            ListOfColors.append('rgba('+str(R)+','+str(G)+','+str(B)+','+str(A)+')')
#    print(ListOfColors)
#    return ListOfColors

def json_component_chartjs(loom_path,style='pie',attrs=[],cidx_filter=None):
    '''
    Compute JSON for ChartJs figure
    
    Params
    ------
    loom_path: str
        path to Loom file
    style: str
        plot style. Must be pie or bar
    attrs: list
        List of up to two attributes to plot
        
    Return
    ------
    JSON
    '''
    if style not in ['pie','bar']:
        raise Exception('style must be one of [pie,bar]')
    if attrs==[]:
        raise Exception('empty attributes list given')
    if len(attrs)>2:
        raise Exception('attributes list contains more than two elements')
    if not is_valid_attrs_list(loom_path,attrs):
        raise Exception('attributes list must only contain valid attributes')
        
    df = get_dataframe(loom_path,attrs,cidx_filter=cidx_filter)
    col = attrs[0]
    lbls,vals = np.unique(df[col].values,return_counts=True)
    idx = np.argsort(vals)[::-1]
    lbls = lbls[idx]
    vals = vals[idx]
    
    res = dict()
    chart = dict()
    datasets=dict()
    plugins=dict()
    res['options']=dict()
    datasets['data'] = vals.tolist()
    datasets['backgroundColor'] = n_colors(len(vals))
    chart['datasets'] = [datasets]
    chart['labels'] = lbls.tolist()
    if style=='bar':
        res['options']['legend']={'display':False}
        res['options']['scales']={'xAxes':[{'ticks':{'min':0}}]}
    if style=='pie':
        res['options']['legend']={'position':'left','maxWidth':120,'labels':{'boxWidth':10,'padding':4,'font':{'size':8,'lineHeight':1}}}
    
    res['chart'] = chart
    res['style'] = style
    res['options']['plugins'] = plugins

    return json.dumps(res)

def get_symbol_values(loom_path,symbol,cidx_filter=None):
    '''
    Attempt to retrieve gene expression values
    
    Params
    ------
    loom_path: str
        path to Loom file
    symbol: str
        Potential symbol
    '''
    df = loompy.connect(loom_path,'r')
    symbols = df.ra['Symbol']
    set_symbols = set(symbols)
    if symbol in set_symbols:
        idx = np.where(symbols==symbol)[0][0]
        if isinstance(cidx_filter, np.ndarray):
            symbol_values = df[idx,:][cidx_filter]
        else:
            symbol_values = df[idx,:]
        df.close()
        return symbol_values
    df.close()
    raise Exception('Input not a valid symbol name')
        
def continuous_scatter_gl(x,y,color,tracename=''):
    if tracename=='All cells':
        hoverinfo='skip'
    else:
        hoverinfo=None
    trace=go.Scattergl(
        x = x, 
        y = y, 
        mode='markers',
        marker=dict(
            color=color,
            #colorscale='matter',
            colorscale='plasma',
            size=4,
            colorbar=dict(thickness=20)
        ),
        name=tracename,
        hoverinfo=hoverinfo
    )
    return trace

def discrete_scatter_gl(x,y,color):
    unique_classes = np.unique(color)
    traces=[]
    color_seq = n_colors(len(unique_classes))
    for i,unique_class_ in enumerate(unique_classes):
        idx = np.where(color==unique_class_)[0]
        subX = x[idx]
        subY = y[idx]
        traces.append(go.Scattergl(
                x=subX,
                y=subY,
                mode='markers',
                name=unique_class_,
                marker=dict(
                    color=color_seq[i],
                    size=4
                ),
                showlegend=True
            )
        )
    return traces

def continuous_scatter_gl_3d(x,y,z,color,tracename=''):
    if tracename=='All cells':
        hoverinfo='skip'
    else:
        hoverinfo=None
    trace=go.Scatter3d(
        x = x, 
        y = y,
        z = z,
        mode='markers',
        marker=dict(
            color=color,
            #colorscale='matter',
            colorscale='plasma',
            size=3,
            opacity=0.4
        ),
        name=tracename,
        hoverinfo=hoverinfo
    )
    return trace

def discrete_scatter_gl_3d(x,y,z,color):
    unique_classes = np.unique(color)
    traces=[]
    color_seq = n_colors(len(unique_classes), rgbonly=True)

    for i,unique_class_ in enumerate(unique_classes):
        idx = np.where(color==unique_class_)[0]
        subX = x[idx]
        subY = y[idx]
        subZ = z[idx]
        traces.append(go.Scatter3d(
                x=subX,
                y=subY,
                z=subZ,
                mode='markers',
                name=unique_class_,
                marker=dict(
                    color=color_seq[i],
                    size=3,
                    opacity=0.4,
                ),
                showlegend=True
            )
        )
    return traces

def check_color(loom_path,color,cidx_filter=None):
    if color==None:
        return '#dddddd'
    elif is_valid_attrs_list(loom_path,[color]): # if color is a valid column attribute
        return get_ca(loom_path,key=color,unique=False,cidx_filter=cidx_filter)
    else: # supposed to be a gene symbol
        try:
            return get_symbol_values(loom_path,color,cidx_filter=cidx_filter)
        except:
            raise Exception(f'color must be None, a valid gene symbol or a valid data attribute')

def json_scatOrSpat(style,loom_path,color=None,reduction=None,returnjson=True,cidx_filter=None):
    if reduction==None :
        reduction = get_available_reductions(loom_path)[0]
    l = get_reduction_x_y(loom_path,reduction)

    if len(l)==3:
        result=json_scatter3d(loom_path,reduction,color,returnjson,cidx_filter)
    elif len(l)==2 and 'spatial' in reduction:
        result=json_spatial(loom_path,color,reduction,returnjson,cidx_filter)
    elif len(l)==2 and style=='scatter':
        result=json_scatter(loom_path,color,reduction,returnjson,cidx_filter)
    elif len(l)==2 and style=='hexbin':
        result=json_hexbin(loom_path,reduction=reduction,color=color,returnjson=returnjson,cidx_filter=cidx_filter)
    elif len(l)==2 and style=='density':
        result=json_density(loom_path,reduction=reduction,symbol=color,cidx_filter=cidx_filter)
    return result

# def json_scatter(loom_path,color=None,reduction=None,returnjson=True,cidx_filter=None):
#     '''
#     Compute JSON from Plotly figure
    
#     Params
#     ------
#     loom_path: str
#         path to Loom file
#     color: str or None
#         column attribute or gene symbol
#     attrs: list
#         List of up to two attributes to plot
#     returnjson: bool
#         return figure or its JSON form
#     cidx_filter: array
#         column indices filter
        
#     Return
#     ------
#     Plotly figure or its JSON form
#     '''
#     start = time.time()
#     if reduction==None:
#         reduction = get_available_reductions(loom_path)[0] # first reduction available

#     X,Y = get_reduction_x_y(loom_path,reduction)
    
#     fig = go.Figure()
#     if isinstance(cidx_filter, np.ndarray): # if filter exists, draw all points first as background
#         df = get_dataframe(loom_path,[X,Y],cidx_filter=None) # all points
#         if df.shape[0]>N_MAX_CELLS:
#             sub_idx = np.random.choice(df.shape[0], N_MAX_CELLS, replace=False) # select 200 cells randomly
#             x = df[X].values[sub_idx]
#             y = df[Y].values[sub_idx]
#         else:
#             x = df[X].values
#             y = df[Y].values
#         tmpcolor = check_color(loom_path,None,cidx_filter=None) # None means default background color
#         fig.add_trace(continuous_scatter_gl(x,y,tmpcolor,tracename='All cells'))

#     df = get_dataframe(loom_path,[X,Y],cidx_filter=cidx_filter) # pandas dataframe
#     tmpcolor = check_color(loom_path,color,cidx_filter=cidx_filter) # numpy array
    
#     if df.shape[0]>N_MAX_CELLS:
#         sub_idx = np.random.choice(df.shape[0], N_MAX_CELLS, replace=False) # select 200 cells randomly
#         x = df[X].values[sub_idx]
#         y = df[Y].values[sub_idx]
#         if isinstance(tmpcolor, np.ndarray): # if color is an array (numerical or strings)
#             tmpcolor = tmpcolor[sub_idx]
#     else:
#         x = df[X].values
#         y = df[Y].values

#     if color!=None:
#         if np.issubdtype(tmpcolor.dtype, np.number): # if color is None or type of color array is numerical
#             idx = np.argsort(tmpcolor)
#             tmpcolor = tmpcolor[idx]
#             x = x[idx]
#             y = y[idx]
#             fig.add_trace(continuous_scatter_gl(x,y,tmpcolor,tracename=color))
#         else: # discrete
#             fig.add_traces(discrete_scatter_gl(x,y,tmpcolor))
#     elif color==None and not isinstance(cidx_filter, np.ndarray): # fallback case
#         fig.add_trace(continuous_scatter_gl(x,y,tmpcolor))

#     fig.update_layout(
#         # background color white
#         paper_bgcolor='rgba(0,0,0,0)',
#         plot_bgcolor='rgba(0,0,0,0)',
#         xaxis_title=X,
#         yaxis_title=Y,
#         margin=dict(
#             l=0,
#             r=0,
#             b=0,
#             t=0
#         ),
#         legend = dict(
#             yanchor ="bottom",
#             y = 0,
#             xanchor = "right",
#             x = 1,
#             bgcolor = "rgba(255,255,255,0.8)",
#         )
#     )

#     if "PCA" not in reduction.upper():
#         fig.update_yaxes(showticklabels=False)
#         fig.update_xaxes(showticklabels=False)

#     end = time.time()
#     if returnjson:
#         #print('#######################')
#         #print(end - start)
#         #print('#######################')
#         try : 
#             jsonD = json.loads(pio.to_json(fig, validate = True, pretty=False, remove_uids=True))
#             #print(jsonD)
#             return jsonD
#         except json.decoder.JSONDecodeError:
#             print("String could not be converted to JSON")
#             return json.loads('{}')
#     else:
#         #print('#######################')
#         #print(end - start)
#         #print('#######################')
#         return fig

def json_scatter(loom_path,color=None,reduction=None,returnjson=True,cidx_filter=None):
    '''
    Compute JSON from Plotly figure
    
    Params
    ------
    loom_path: str
        path to Loom file
    color: str or None
        column attribute or gene symbol
    attrs: list
        List of up to two attributes to plot
    returnjson: bool
        return figure or its JSON form
    cidx_filter: array
        column indices filter
        
    Return
    ------
    Plotly figure or its JSON form
    '''
    if reduction==None:
        reduction = get_available_reductions(loom_path)[0] # first reduction available

    X,Y = get_reduction_x_y(loom_path,reduction)
    
    fig = go.Figure()
    if isinstance(cidx_filter, np.ndarray): # if filter exists, draw all points first as background
        df = get_dataframe(loom_path,[X,Y],cidx_filter=None) # all points
        if df.shape[0]>N_MAX_CELLS:
            sub_idx = np.random.choice(df.shape[0], N_MAX_CELLS, replace=False) # select 200 cells randomly
            x = df[X].values[sub_idx]
            y = df[Y].values[sub_idx]
        else:
            x = df[X].values
            y = df[Y].values
        tmpcolor = check_color(loom_path,None,cidx_filter=None) # None means default background color
        fig.add_trace(continuous_scatter_gl(x,y,tmpcolor,tracename='All cells'))

    df = get_dataframe(loom_path,[X,Y],cidx_filter=cidx_filter) # pandas dataframe
    tmpcolor = check_color(loom_path,color,cidx_filter=cidx_filter) # numpy array
    
    if df.shape[0]>N_MAX_CELLS:
        sub_idx = np.random.choice(df.shape[0], N_MAX_CELLS, replace=False) # select 200 cells randomly
        x = df[X].values[sub_idx]
        y = df[Y].values[sub_idx]
        if isinstance(tmpcolor, np.ndarray): # if color is an array (numerical or strings)
            tmpcolor = tmpcolor[sub_idx]
    else:
        x = df[X].values
        y = df[Y].values
        
    fig.update_layout(
        # background color white
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        xaxis_title=X,
        yaxis_title=Y,
        margin=dict(
            l=0,
            r=0,
            b=0,
            t=0
        ),
        legend = dict(
            yanchor ="bottom",
            y = 0,
            xanchor = "right",
            x = 1,
            bgcolor = "rgba(255,255,255,0.8)",
            )
    )

    if color!=None:
        if np.issubdtype(tmpcolor.dtype, np.number): # if color is None or type of color array is numerical
            idx = np.argsort(tmpcolor)
            tmpcolor = tmpcolor[idx]
            x = x[idx]
            y = y[idx]
            fig.add_trace(continuous_scatter_gl(x,y,tmpcolor,tracename=color))
            fig.update_xaxes(showgrid=False, zeroline=False)
            fig.update_yaxes(showgrid=False, zeroline=False)
            fig.update_layout(plot_bgcolor='rgba(0,0,0,1)')
        else: # discrete
            fig.add_traces(discrete_scatter_gl(x,y,tmpcolor))
    elif color==None and not isinstance(cidx_filter, np.ndarray): # fallback case
        fig.add_trace(continuous_scatter_gl(x,y,tmpcolor))
        fig.update_xaxes(showgrid=False, zeroline=False)
        fig.update_yaxes(showgrid=False, zeroline=False)
        fig.update_layout(plot_bgcolor='rgba(0,0,0,1)')

    if "PCA" not in reduction.upper():
        fig.update_yaxes(showticklabels=False)
        fig.update_xaxes(showticklabels=False)

    if returnjson:
        try : 
            jsonD = json.loads(pio.to_json(fig, validate = True, pretty=False, remove_uids=True))
            return jsonD
        except json.decoder.JSONDecodeError:
            print("String could not be converted to JSON")
            return json.loads('{}')
    else:
        return fig

def json_scatter3d(loom_path,reduction,color=None,returnjson=True,cidx_filter=None):
    '''
    Compute JSON from Plotly figure
    
    Params
    ------
    loom_path: str
        path to Loom file
    color: str or None
        column attribute or gene symbol
    attrs: list
        List of up to two attributes to plot
    returnjson: bool
        return figure or its JSON form
    cidx_filter: array
        column indices filter
        
    Return
    ------
    Plotly figure or its JSON form
    '''
    start = time.time()

    X,Y,Z = get_reduction_x_y(loom_path,reduction)
    
    fig = go.Figure()
    if isinstance(cidx_filter, np.ndarray): # if filter exists, draw all points first as background
        df = get_dataframe(loom_path,[X,Y,Z],cidx_filter=None) # all points
        if df.shape[0]>N_MAX_CELLS:
            sub_idx = np.random.choice(df.shape[0], N_MAX_CELLS, replace=False) # select 200 cells randomly
            x = df[X].values[sub_idx]
            y = df[Y].values[sub_idx]
            z = df[Z].values[sub_idx]
        else:
            x = df[X].values
            y = df[Y].values
            z = df[Z].values
        tmpcolor = check_color(loom_path,None,cidx_filter=None) # None means default background color
        fig.add_trace(continuous_scatter_gl_3d(x,y,z,tmpcolor,tracename='All cells'))
        
    df = get_dataframe(loom_path,[X,Y,Z],cidx_filter=cidx_filter) # pandas dataframe
    tmpcolor = check_color(loom_path,color,cidx_filter=cidx_filter) # numpy array
    
    if df.shape[0]>N_MAX_CELLS:
        sub_idx = np.random.choice(df.shape[0], N_MAX_CELLS, replace=False) # select 200 cells randomly
        x = df[X].values[sub_idx]
        y = df[Y].values[sub_idx]
        z = df[Z].values[sub_idx]
        if isinstance(tmpcolor, np.ndarray): # if color is an array (numerical or strings)
            tmpcolor = tmpcolor[sub_idx]
    else:
        x = df[X].values
        y = df[Y].values
        z = df[Z].values
        
    if color!=None:
        if np.issubdtype(tmpcolor.dtype, np.number): # if color is None or type of color array is numerical
            idx = np.argsort(tmpcolor)
            tmpcolor = tmpcolor[idx]
            x = x[idx]
            y = y[idx]
            z = z[idx]
            fig.add_trace(continuous_scatter_gl_3d(x,y,z,tmpcolor,tracename=color))
            fig.update_layout(plot_bgcolor='rgba(0,0,0,1)')
        else: # discrete
            fig.add_traces(discrete_scatter_gl_3d(x,y,z,tmpcolor))
    elif color==None and not isinstance(cidx_filter, np.ndarray): # fallback case
        fig.add_trace(continuous_scatter_gl_3d(x,y,z,tmpcolor))
        fig.update_layout(plot_bgcolor='rgba(0,0,0,1)')

    fig.update_layout(
        # background color white
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        margin=dict(
            l=0,
            r=0,
            b=0,
            t=0
        ),
        legend = dict(
            yanchor ="bottom",
            y = 0,
            xanchor = "right",
            x = 1,
            bgcolor = "rgba(255,255,255,0.8)",
        ),
        scene=dict(
            xaxis=dict(showticklabels=False),
            yaxis=dict(showticklabels=False),
            zaxis=dict(showticklabels=False),
            xaxis_title=X,
            yaxis_title=Y,
            zaxis_title=Z
        )
    )

    #fig.update_yaxes(showticklabels=False)
    #fig.update_xaxes(showticklabels=False)
    end = time.time()
    if returnjson:
        #print('#######################')
        #print(end - start)
        #print('#######################')
        try : 
            jsonD = json.loads(pio.to_json(fig, validate = True, pretty=False, remove_uids=True))
            #print(jsonD)
            return jsonD
        except json.decoder.JSONDecodeError:
            print("String could not be converted to JSON")
            return json.loads('{}')
    else:
        #print('#######################')
        #print(end - start)
        #print('#######################')
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

def json_hexbin(loom_path,reduction=None,color=None,gridsize=40,cmap=plt.cm.plasma,background='black',returnjson=True,cidx_filter=None):
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
    if reduction==None:
        reduction = get_available_reductions(loom_path)[0] # first reduction available
    X,Y = get_reduction_x_y(loom_path,reduction)

    df = get_dataframe(loom_path,[X,Y],cidx_filter=cidx_filter)

    if df.shape[0]>N_MAX_CELLS:
        sub_idx = np.random.choice(df.shape[0], N_MAX_CELLS, replace=False) # select 20k cells randomly
        x = df[X].values[sub_idx]
        y = df[Y].values[sub_idx]
    else:
        x = df[X].values
        y = df[Y].values

    if 'spatial' in reduction:
        y = -y
    
    if color is None:
        HB = plt.hexbin(x,y,gridsize=gridsize,cmap=cmap)
    else:
        C = check_color(loom_path,color,cidx_filter=cidx_filter)
        if len(C)>N_MAX_CELLS:
            C=C[sub_idx]
        HB = plt.hexbin(x,y,gridsize=gridsize,cmap=cmap,C=C)
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
        width=636, height=660,
        xaxis=axis,
        yaxis=axis,
        xaxis_title=X,
        yaxis_title=Y,
        hovermode='closest',
        shapes=shapes,
        plot_bgcolor=background)
    
    if "PCA" not in reduction.upper():
        fig.update_yaxes(showticklabels=False)
        fig.update_xaxes(showticklabels=False)
    
    if returnjson:
        return json.loads(pio.to_json(fig, validate=True, pretty=False, remove_uids=True))
    else:
        return fig
    
def get_classes(loom_path):
    '''
    Extract classes stored in loom
    
    Params
    ------
    loom_path : str
        Path to a .loom file

    Return
    ------
    list
    '''
    df = loompy.connect(loom_path,'r') # open loom connection
    classes = df.attrs.Classes.split(',')
    df.close()
    return classes

def get_most_variable_genes(loom_path):
    '''
    Extract most variable genes stored in loom
    
    Params
    ------
    loom_path : str
        Path to a .loom file

    Return
    ------
    list
    '''
    df = loompy.connect(loom_path,'r') # open loom connection
    genes = df.attrs.most_variable_genes.split(',')
    df.close()
    return genes

def check_ra(loom_path,key):
    '''
    Check if the row metadata exists

    Params
    ------
    loom_path : str
        Path to a .loom file

    key : str
        Name of the metadata 

    Return
    ------
    True or False
    '''
    df = loompy.connect(loom_path,'r')
    if key in df.ra :
        return True
    return False

def get_ra(loom_path,key='Symbol',unique=False,ridx_filter=None):
    '''
    Extract row attribute data from loom file
    
    Params
    ------
    loom_path : str
        Path to a .loom file
    key: str
        Column key. Default is Symbol
        
    Return
    ------
    arr
    '''
    df = loompy.connect(loom_path,'r') # open loom connection
    if isinstance(ridx_filter, np.ndarray):
        labels = df.ra[key][ridx_filter]
    else:
        labels = df.ra[key]
    df.close()
    if unique:
        return np.unique(labels)
    else:
        return labels

def get_ca_metalist(loom_path,metadata):

    df = loompy.connect(loom_path,'r')
    classes= [item.strip() for item in df.attrs["Classes"].split(",")]

    for key in classes : 
        for key2,value in df.ca.items() :
            if key == key2 : 
                metadata['filters'][key] = {'name':key,'values':np.unique(value),'attributes':'ca'}
                metadata['filters_keys']['ca'].append(key)
    df.close()
    return metadata



def get_ca(loom_path,key='Sample',unique=False,cidx_filter=None):
    '''
    Extract column attribute data from loom file
    
    Params
    ------
    loom_path : str
        Path to a .loom file
    key: str
        Column key. Default is Sample

    Return
    ------
    arr
    '''
    df = loompy.connect(loom_path,'r') # open loom connection
    if isinstance(cidx_filter, np.ndarray):
        labels = df.ca[key][cidx_filter]
    else:
        labels = df.ca[key]
    df.close()
    if unique:
        return np.unique(labels)
    else:
        return labels

def get_shape(loom_path):
    '''
    Extract numbers of cells and genes in loom file
    
    Params
    ------
    loom_path : str
        Path to a .loom file
        
    Return
    ------
    tuple
    '''
    df = loompy.connect(loom_path,'r') # open loom connection
    shape = df.shape
    df.close()
    return shape

def most_variable_symbols(loom_path,n=10,ridx_filter=None,cidx_filter=None):
    '''
    Return the most variable genes
    
    Params
    ------
    loom_path : str
        Path to a .loom file
    n : int
        Number of genes to return
    ridx_filter : array or None
        Row indices to filter genes to use
        
    Return
    ------
    Array of symbols
    '''
    
    #df = loompy.connect(loom_path,'r')
    #try: # if a filter != None, comparing an array to None throws an error
    #    if cidx_filter==None and ridx_filter==None and df.attrs.most_variable_genes:
    #        return df.attrs.most_variable_genes.split(',')
    #except:
    #    pass # do nothing
    #        
    #labels = get_ra(loom_path,key='Symbol',unique=False,ridx_filter=ridx_filter) # get symbols (filter applied)
    #if isinstance(ridx_filter, np.ndarray) and isinstance(cidx_filter, np.ndarray):
    #    tmp = df[ridx_filter,:] # can't slice both axes at once
    #    tmp = tmp[:,cidx_filter]
    #    v = np.var(tmp,axis=1) # computer variance
    #elif isinstance(ridx_filter, np.ndarray):
    #    v = np.var(df[ridx_filter, :],axis=1) # compute variances
    #elif isinstance(cidx_filter, np.ndarray):
    #    v = np.var(df[:, cidx_filter],axis=1) # compute variances
    #else:
    #    v = np.var(df[:, :],axis=1)
    #df.close()
    #idx = np.argsort(v)[::-1][:n] # sort and select in descending order
    #labels = labels[idx] # trim synbol array
    #return np.delete(labels, np.where(labels == 'nan')) # remove potential nan values and return

    df = loompy.connect(loom_path,'r')
    arr = df.attrs.most_variable_genes.split(',')
    df.close()
    return arr


def first_n_symbols(loom_path,n=10,ridx_filter=None):
    '''
    Retrieve first n genes
    
    Params
    ------
    loom_path : str
        Path to a .loom file
    n : int
        Number of genes to return
    ridx_filter : array or None
        Row indices to filter genes to use
        
    Return
    ------
    Array of symbols
    '''
    labels = get_ra(loom_path,key='Symbol',unique=False,ridx_filter=ridx_filter)
    return labels[:n]

def get_relevant_genes(loom_path):
    '''
    Retrieve relevant genes
    
    Params
    ------
    loom_path : str
        Path to a .loom file
        
    Return
    ------
    List of genes
    '''
    df = loompy.connect(loom_path, 'r')
    labels = df.attrs.relevant_genes.split(',')
    df.close()
    return labels

def auto_get_symbols(loom_path,n=10,ridx_filter=None,cidx_filter=None,method='relevant'):
    '''
    Get genes automatically, first n genes or n most variable genes
    
    Params
    ------
    loom_path : str
        Path to a .loom file
    n : int
        Number of genes to return
    ridx_filter : array or None
        Row indices to filter genes to use
    cidx_filter : array or None
        Column indices to filter cells to use
    method: str
        Either first or variance
        
    Return
    ------
    Array of symbols
    '''
    if method=='relevant':
        try:
            return get_relevant_genes(loom_path)
        except:
            return most_variable_symbols(loom_path,n=n,ridx_filter=ridx_filter,cidx_filter=cidx_filter)    
    elif method=='variance':
        return most_variable_symbols(loom_path,n=n,ridx_filter=ridx_filter,cidx_filter=cidx_filter)
    else:
        raise Exception('method not recognized')

def dotplot_json(loom_path,attribute='',symbols=[],cidx_filter=None,ridx_filter=None,returnjson=True,log=False,scale=False):
    '''
    Create dotplot figure
    
    Params
    ------
    loom_path : str
        Path to a .loom file
    attribute : str
        Name of column attribute to use for Y axis
    symbols : list
        Symbols to display on X axis
    cidx_filter: array
        Column indices to filter cells
    returnjson: bool
        return Plotly figure or its JSON
    log: bool
        Wether to log the expression values or not
    scale: bool
        Wether to scale the expression to 1 for each symbol
        
    Return
    ------
    JSON
    '''
    
    if symbols == []: # if empty symbol list
        symbols = most_variable_symbols(loom_path,n=10,ridx_filter=ridx_filter) # retrive
    allsymbols = get_ra(loom_path,key='Symbol') # symbol list
    vals = dict()
    vals[attribute] = get_ca(loom_path,key=attribute,unique=False,cidx_filter=cidx_filter) # get column attribute values
    df = loompy.connect(loom_path,'r')
    
    for s in symbols:
        i = np.where(allsymbols==s)[0][0]
        if isinstance(cidx_filter, np.ndarray):
            vals[s] = df[i,cidx_filter]
        else:
            vals[s] = df[i,:]

    if log==True:
        for s in symbols:
            vals[s] = np.log(vals[s]+1)
    df.close()
    
    df = pd.DataFrame(vals)
    colors = df.groupby([attribute]).mean() # average value for each gene grouped by attribute
    sizes = df.groupby([attribute]).agg(lambda x: x.ne(0).sum()/len(x)) # percentage of non-zeros for each gene grouped by attribute
    
    if scale==True:
        colors -= colors.min() # minimum becomes 0
        colors /= colors.max() # maximum becomes 1
    r,c = colors.shape
    i_coords, j_coords = np.meshgrid(range(c), range(r), indexing='ij')
    
    x = i_coords.flatten()
    y = j_coords.flatten()
    cs = [[0.0, "#EBC89B"], [0.5,"#FB6404"],[1, "#67000C"]]
    #cs = [[0.0,"#ebe7e1"],[0.5, "#c27a67"],[1, "#c27a67"]]
    fig = px.scatter(x=x, y=y,size=sizes.values.T.flatten(),color=colors.values.T.flatten(),color_continuous_scale=cs)
    
    fig.update_layout(
        # background color white
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        margin=dict(
            l=0,
            r=0,
            b=0,
            t=0
        )
    )
    
    fig.update_layout(
        xaxis = dict(
            tickmode = 'array',
            tickvals = i_coords[:,0],
            ticktext = symbols
        ),
        yaxis = dict(
            tickmode = 'array',
            tickvals = j_coords[0,:],
            ticktext = colors.index.values,
        )
    )
    #print('15')
    # hide subplot y-axis titles and x-axis titles
    for axis in fig.layout:
        if type(fig.layout[axis]) == go.layout.YAxis:
            fig.layout[axis].title.text = attribute
        if type(fig.layout[axis]) == go.layout.XAxis:
            fig.layout[axis].title.text = ''

    if returnjson:
        return json.loads(pio.to_json(fig, validate=True, pretty=False, remove_uids=True))
    else:
        return fig
    
def violin_json(loom_path,attribute='',symbols=[],cidx_filter=None,returnjson=True,log=False):
    '''
    Create violin plot figure
    
    Params
    ------
    loom_path : str
        Path to a .loom file
    attribute : str
        Name of column attribute to use for Y axis
    symbols : str
        Symbol to use
    cidx_filter: array
        Column indices to filter cells
    returnjson: bool
        return Plotly figure or its JSON
    log: bool
        Wether to log the expression values or not
        
    Return
    ------
    JSON
    '''
    allsymbols = get_ra(loom_path,key='Symbol') # symbol list
    attr_values = get_ca(loom_path,key=attribute,unique=False,cidx_filter=cidx_filter) # get column attribute values
    symbol = symbols[0]
    
    df = loompy.connect(loom_path,'r')
    i = np.where(allsymbols==symbol)[0][0]
    if isinstance(cidx_filter, np.ndarray):
        symbol_values = df[i,cidx_filter]
    else:
        symbol_values = df[i,:]
    df.close()
    if log==True:
        symbol_values = np.log(symbol_values+1)

    fig = go.Figure()
    unique_values = np.unique(attr_values)
    colors = n_colors(len(unique_values))
    for i,value in enumerate(unique_values):
        idx = np.where(attr_values==value)[0]
        # name are visible so no need to show legend
        fig.add_trace(go.Violin(x=symbol_values[idx],
                                name=value,
                                showlegend=False,
                                box_visible=True,
                                meanline_visible=True,
                                line=dict(color=colors[i])))


    fig.update_layout(
        # background color white
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        margin=dict(
            l=0,
            r=0,
            b=0,
            t=0
        )
    )
    fig.update_traces(orientation='h', width=0.8, points=False)
    fig.update_layout(xaxis_showgrid=False, xaxis_zeroline=True)
    fig.update_xaxes(showticklabels=False)
    
    if returnjson:
        return json.loads(pio.to_json(fig, validate=True, pretty=False, remove_uids=True))
    else:
        return fig
    
def density_ca(loom_path,X,Y,cidx_filter=None,ca=None):
    df = get_dataframe(loom_path,[X,Y],cidx_filter=None) # pandas dataframe
    fig = px.density_contour(df, x=X, y=Y)
    fig['data'][0]['line']['color'] = '#D3D3D3'
    
    if isinstance(cidx_filter, np.ndarray):
        df = get_dataframe(loom_path,[X,Y],cidx_filter=cidx_filter) # pandas dataframe    
    
    if ca!=None:
        df[ca] = get_ca(loom_path,key=ca,cidx_filter=cidx_filter)
        color_seq = n_colors(len(df[ca].unique()))
        traces = px.density_contour(df, x=X, y=Y, color=ca, color_discrete_sequence=color_seq).data
        fig.add_traces(traces)
        lgd = {trace['name']:trace['line']['color'] for trace in traces}
    else:
        traces = px.density_contour(df, x=X, y=Y).data
        fig.add_traces(traces)
        lgd = {}
    
    for i,trace in enumerate(fig['data']):
        fig['data'][i]['ncontours'] = 20
    return fig,lgd

# def density_symbols(loom_path,X,Y,symbols,cidx_filter=None):
#     df = get_dataframe(loom_path,[X,Y],cidx_filter=None) # pandas dataframe

#     fig = px.density_contour(df, x=X, y=Y)
#     fig['data'][0]['line']['color'] = '#D3D3D3'
#     for i,trace in enumerate(fig['data']):
#         fig['data'][i]['ncontours'] = 20
    
#     lgd = dict()
#     gene_colors = ['rgba(214,121,5,1)','rgba(239, 122, 4,1)','rgba(239, 239, 4,1)','rgba(122, 239, 4,1)','rgba(4, 239, 239,1)','rgba(4, 122, 239,1)','rgba(122, 4, 239,1)','rgba(239, 4, 239,1)','rgba(239, 4, 122,1)','rgba(4, 239, 4,1)']

#     traces=[]
#     if isinstance(cidx_filter, np.ndarray): # if filter exists
#         df = get_dataframe(loom_path,[X,Y],cidx_filter=cidx_filter) # pandas dataframe
#     for i,symbol in enumerate(symbols):
#         gene_color = gene_colors[i]
#         lgd[symbol] = gene_color
#         exp = get_symbol_values(loom_path,symbol,cidx_filter=cidx_filter)
#         trace = go.Histogram2dContour(
#             x = df[X].values,
#             y = df[Y].values,
#             z=exp,
#             colorscale=[[0,'rgba(255,255,255,0)'],[1,gene_color]],
#             histfunc='sum',
#             ncontours = 20,
#             contours = dict(
#                 showlines=False
#             ),
#             hoverinfo='none'
#         )

#         traces.append(trace)
#     fig.add_traces(traces)
        
#     return fig,lgd

def density_symbols(loom_path,X,Y,symbol,cidx_filter=None):
    df = get_dataframe(loom_path,[X,Y],cidx_filter=None) # pandas dataframe

    fig = px.density_contour(df, x=X, y=Y)
    fig['data'][0]['line']['color'] = '#D3D3D3'
    for i,trace in enumerate(fig['data']):
        fig['data'][i]['ncontours'] = 20
    
    gene_colors = ['rgba(214,121,5,1)','rgba(239, 122, 4,1)','rgba(239, 239, 4,1)','rgba(122, 239, 4,1)','rgba(4, 239, 239,1)','rgba(4, 122, 239,1)','rgba(122, 4, 239,1)','rgba(239, 4, 239,1)','rgba(239, 4, 122,1)','rgba(4, 239, 4,1)']
    if isinstance(cidx_filter, np.ndarray): # if filter exists
        df = get_dataframe(loom_path,[X,Y],cidx_filter=cidx_filter) # pandas dataframe
    gene_color = gene_colors[0]
    exp = get_symbol_values(loom_path,symbol,cidx_filter=cidx_filter)
    trace = go.Histogram2dContour(
        x = df[X].values,
        y = df[Y].values,
        z=exp,
        colorscale='inferno',#[[0,'rgba(255,255,255,0)'],[1,gene_color]],
        histfunc='avg',
        ncontours = 20,
        contours = dict(
            showlines=False
        ),
        hoverinfo='none'
    )
    fig.add_traces([trace])   
    return fig

# def json_density(loom_path,reduction=None,ca=None,symbols=[],returnjson=True,cidx_filter=None):
#     if reduction==None:
#         reduction = get_available_reductions(loom_path)[0] # first reduction available
#     X,Y = get_reduction_x_y(loom_path,reduction)
    
#     if symbols==[]: # if no gene list provided
#         fig,lgd = density_ca(loom_path,X,Y,cidx_filter=cidx_filter,ca=ca) # plot simple density contour or with categorical column attribute
#     else:
#         fig,lgd = density_symbols(loom_path,X,Y,symbols,cidx_filter=cidx_filter)

#     fig.update_layout(
#         paper_bgcolor='rgba(0,0,0,0)',
#         plot_bgcolor='rgba(0,0,0,0)',
#         margin=dict(
#             l=0,
#             r=0,
#             b=0,
#             t=0
#         ),
#         xaxis_title='',
#         yaxis_title='',
#     )
#     fig.update_yaxes(showticklabels=False)
#     fig.update_xaxes(showticklabels=False)

#     if 'spatial' in reduction:
#         fig.update_yaxes(autorange="reversed")
    
#     if returnjson:
#         return json.loads(pio.to_json(fig, validate=True, pretty=False, remove_uids=True)),lgd
#     else:
#         return fig
    
def json_density(loom_path,reduction=None,symbol=None,returnjson=True,cidx_filter=None):
    if reduction==None:
        reduction = get_available_reductions(loom_path)[0] # first reduction available
    X,Y = get_reduction_x_y(loom_path,reduction)
    
    fig = density_symbols(loom_path,X,Y,symbol,cidx_filter=cidx_filter)

    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        margin=dict(
            l=0,
            r=0,
            b=0,
            t=0
        ),
        xaxis_title=X,
        yaxis_title=Y,
    )
    
    if "PCA" not in reduction.upper():
        fig.update_yaxes(showticklabels=False)
        fig.update_xaxes(showticklabels=False)

    if 'spatial' in reduction:
        fig.update_yaxes(autorange="reversed")
    
    if returnjson:
        return json.loads(pio.to_json(fig, validate=True, pretty=False, remove_uids=True))
    else:
        return fig

# SPATIAL TRANSCRIPTOMICS

#from PIL import Image
#import requests
#from io import BytesIO
#import matplotlib
#import matplotlib.cm as cm

def spatial_points_solid(x,y,colorvector,r=8):
    if isinstance(colorvector, str):
        kwargs = {'type': 'circle', 'xref': 'x', 'yref': 'y', 'fillcolor': colorvector,'line': {'width':1}}
        points = [go.layout.Shape(x0=x-r, y0=y-r, x1=x+r, y1=y+r, **kwargs) for x, y in zip(x,y)]
    else:
        unique_values = np.unique(colorvector)
        colors = n_colors_float(len(unique_values))
        colordict = dict(zip(unique_values,colors))
        c=[colordict[x] for x in colorvector]
        kwargs = {'type': 'circle', 'xref': 'x', 'yref': 'y', 'line': {'width':0}}
        points = [go.layout.Shape(x0=x_-r, y0=y_-r, x1=x_+r, y1=y_+r, fillcolor=matplotlib.colors.to_hex(c[i]), opacity=1, **kwargs) for i, (x_, y_) in enumerate(zip(x,y))]
    return points
    
def spatial_points_continuous(x, y, exp, mapper,r=8):
    kwargs = {'type': 'circle', 'xref': 'x', 'yref': 'y', 'line': {'width':0}}
    c=[mapper.to_rgba(exp_) for exp_ in exp]
    points = [go.layout.Shape(x0=x_-r, y0=y_-r, x1=x_+r, y1=y_+r, fillcolor=matplotlib.colors.to_hex(c[i]), **kwargs) for i, (x_, y_) in enumerate(zip(x,y))]
    return points

def rgb2hex(s):
    s = s.strip('rgb(').strip(')')
    s = s.split(',')
    r,g,b = [int(x) for x in s]
    return "#{:02x}{:02x}{:02x}".format(r,g,b)

def json_spatial(loom_path, color=None, reduction=None,returnjson=True, cidx_filter=None):
    '''
    Compute JSON from Plotly figure, for Spatial Transcriptomics data
    
    Params
    ------
    loom_path : str
        Path to a .loom file
    color : str
        Symbol name. Default is None (solid orange color)
    returnjson: bool
        return figure or its JSON form
    cidx_filter : array or None
        Column indices to filter cells to use
        
    Return
    ------
    Array of symbols
    '''
    X,Y = get_reduction_x_y(loom_path,'spatial') # get column attribute names for X and Y
    df = get_dataframe(loom_path,[X,Y],cidx_filter=cidx_filter) # pandas dataframe
    x = df[X].values
    y = -df[Y].values

    df = loompy.connect(loom_path,"r") # open loom file
    #url = df.attrs.spatial_img_url # get image file path
    url = os.path.join(settings.MEDIA_ROOT,df.attrs.spatial_img_url)
    keys = df.ca.keys()
    df.close() # close loom file

    # adjust dot size depending on image resolution
    if 'hires' in url:
        r = 8
    else:
        r = 2.5

    if color==None:
        colorvector = 'orange'
        points = spatial_points_solid(x,y,colorvector,r=r)
    else:
        colorvector = check_color(loom_path,color,cidx_filter=cidx_filter)
        if np.issubdtype(colorvector.dtype, np.number):
            minima = min(colorvector)
            maxima = max(colorvector)
            norm = matplotlib.colors.Normalize(vmin=minima, vmax=maxima, clip=True)
            #mapper = cm.ScalarMappable(norm=norm, cmap=cm.magma)
            #mapper = cm.ScalarMappable(norm=norm, cmap=clr.ListedColormap([rgb2hex(x) for x in px.colors.sequential.matter], name='matter'))
            mapper = cm.ScalarMappable(norm=norm, cmap=clr.ListedColormap([rgb2hex(x) for x in px.colors.sequential.Plasma], name='plasma'))
            points = spatial_points_continuous(x, y, colorvector, mapper,r=r)
        else:
            points = spatial_points_solid(x,y,colorvector,r=r)
#        
    fig = go.Figure() # create figure
    fig.update_layout(shapes=points) # add points to figure
    fig.update_layout(template="plotly_white", width=600, height=600, xaxis_showgrid=False, yaxis_showgrid=False,margin=dict(l=5, r=5, t=5, b=5)) # set layout attributes
#    
    try:
        response = requests.get(url) # get img
        img = Image.open(BytesIO(response.content)) # open image
    except:
        img = Image.open(url) # open image

    w,h = img.size # get image width and height
    fig.add_layout_image( # add image to figure
        source=img,
        xref="x",
        yref="y",
        x=0,
        y=0,
        xanchor="left",
        yanchor="top",
        layer="below",
        sizing="stretch",
        sizex=w,
        sizey=h
    )

    fig.update_xaxes(range=[0, w]) # set x axis range
    fig.update_yaxes(range=[-h, 0]) # set y axis range
    fig.update_xaxes(showticklabels=False) # remove x axis ticks
    fig.update_yaxes(showticklabels=False) # remove y axis ticks

    if returnjson:
        return json.loads(pio.to_json(fig, validate=True, pretty=False, remove_uids=True))
    else:
        #print("return fig")
        return fig
