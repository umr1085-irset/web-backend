import loompy
import pandas as pd
from matplotlib import pyplot as plt
import plotly.graph_objects as go
import plotly.express as px
import plotly.io as pio
import numpy as np
import json

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
    
    df = loompy.connect(loom_path) # open loom file

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
    df = loompy.connect(loom_path)
    for attr in attrs:
        if isinstance(cidx_filter, np.ndarray):
            d[attr] = df.ca[attr][cidx_filter]
        else:
            d[attr] = df.ca[attr]
    df.close()
    return pd.DataFrame(d)

def n_colors(n):
    l = ['#8bc34a','#ffc107','#3f51b5','#e91e63','#03a9f4','#ff5722','#9c27b0','#795548','#607d8b','#009688','#2196f3','#cddc39',
    '#c5e1a5','#ffe082','#9fa8da','#f48fb1','#81d4fa','#ffcc80','#ce93d8','#bcaaa4','#b0bec5','#80cbc4','#90caf9','#e6ee9c',
    '#558b2f','#ff8f00','#283593','#ad1457','#0277bd','#ef6c00','#6a1b9a','#4e342e','#37474f','#00695c','#1565c0','#9e9d24']

    return l[:n]

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
    datasets['data'] = vals.tolist()
    datasets['backgroundColor'] = n_colors(len(vals))
    chart['datasets'] = [datasets]
    chart['labels'] = lbls.tolist()

    if style == "pie":
        chart['options'] = {'legend':{ 'position': "left", 'align': "center"}}
    if style == 'bar':
        chart['options'] = {'legend':{ 'display': False}}

    res['chart'] = chart
    res['style'] = style

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
    df = loompy.connect(loom_path)
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
    trace=go.Scattergl(
        x = x, 
        y = y, 
        mode='markers',
        marker=dict(
            color=color,
            colorscale='magma'
        ),
        name=tracename
    )
    return trace

def discrete_scatter_gl(x,y,color):
    unique_classes = np.unique(color)
    traces=[]
    for unique_class_ in unique_classes:
        idx = np.where(color==unique_class_)[0]
        subX = x[idx]
        subY = y[idx]
        traces.append(go.Scattergl(
                x=subX,
                y=subY,
                mode='markers',
                name=unique_class_
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
            
def json_scatter(loom_path,color=None,returnjson=True,cidx_filter=None):
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
    fig = go.Figure()

    if isinstance(cidx_filter, np.ndarray): # if filter exists, draw all points first as background
        df = get_dataframe(loom_path,['X','Y'],cidx_filter=None) # all points
        x = df.X.values
        y = df.Y.values
        tmpcolor = check_color(loom_path,None,cidx_filter=None) # None means default background color
        fig.add_trace(continuous_scatter_gl(x,y,tmpcolor,tracename='All cells'))

    df = get_dataframe(loom_path,['X','Y'],cidx_filter=cidx_filter) # pandas dataframe
    x = df.X.values
    y = df.Y.values
    tmpcolor = check_color(loom_path,color,cidx_filter=cidx_filter) # numpy array

    if color!=None:
        if np.issubdtype(tmpcolor.dtype, np.number): # if color is None or type of color array is numerical
            fig.add_trace(continuous_scatter_gl(x,y,tmpcolor,tracename=color))
        else: # discrete
            fig.add_traces(discrete_scatter_gl(x,y,tmpcolor))
    elif color==None and not isinstance(cidx_filter, np.ndarray): # fallback case
        fig.add_trace(continuous_scatter_gl(x,y,tmpcolor))

    fig.update_layout(
        # background color white
        paper_bgcolor='rgba(0,0,0,0)',
        autosize=True,
        plot_bgcolor='rgba(0,0,0,0)',
        margin=dict(
            l=0,
            r=0,
            b=0,
            t=0
        )
    )
    fig.update_yaxes(showticklabels=False)
    fig.update_xaxes(showticklabels=False)

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

def json_hexbin(loom_path,cmap=plt.cm.Greys,background='white',returnjson=True,cidx_filter=None):
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
    df = get_dataframe(loom_path,['X','Y'],cidx_filter=cidx_filter)
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
    df = loompy.connect(loom_path) # open loom connection
    classes = df.attrs.Classes.split(',')
    df.close()
    return classes

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
    df = loompy.connect(loom_path) # open loom connection
    if isinstance(ridx_filter, np.ndarray):
        labels = df.ra[key][ridx_filter]
    else:
        labels = df.ra[key]
    df.close()
    if unique:
        return np.unique(labels)
    else:
        return labels

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
    df = loompy.connect(loom_path) # open loom connection
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
    df = loompy.connect(loom_path) # open loom connection
    shape = df.shape
    df.close()
    return shape

def most_variable_symbols(loom_path,n=10,ridx_filter=None,cidx_filter=None):
    '''
    Find the most variable genes
    
    Params
    ------
    loom_path : str
        Path to a .loom file
    n : int
        Number of genes to return
    ridx_filter : array or None
        Row indices to filter genes to use
    '''
    labels = get_ra(loom_path,key='Symbol',unique=False,ridx_filter=ridx_filter) # get symbols (filter applied)
    df = loompy.connect(loom_path)
    if isinstance(ridx_filter, np.ndarray) and isinstance(cidx_filter, np.ndarray):
        v = np.var(df[ridx_filter, cidx_filter],axis=1) # compute variances
    elif isinstance(ridx_filter, np.ndarray):
        v = np.var(df[ridx_filter, :],axis=1) # compute variances
    elif isinstance(cidx_filter, np.ndarray):
        v = np.var(df[:, cidx_filter],axis=1) # compute variances
    else:
        v = np.var(df[:, :],axis=1)
    df.close()
    idx = np.argsort(v)[::-1][:n] # sort and select in descending order
    labels = labels[idx] # trim synbol array
    return np.delete(labels, np.where(labels == 'nan')) # remove potential nan values and return

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
def auto_get_symbols(loom_path,n=10,ridx_filter=None,cidx_filter=None,method='first'):
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
    if method=='first':
        return first_n_symbols(loom_path,n=n,ridx_filter=ridx_filter)
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
    
    df = loompy.connect(loom_path)
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
    
    fig = px.scatter(x=x, y=y,size=sizes.values.T.flatten(),color=colors.values.T.flatten(),color_continuous_scale="reds")
    
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
    
    
    df = loompy.connect(loom_path)
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
    for value in unique_values:
        idx = np.where(attr_values==value)[0]
        fig.add_trace(go.Violin(x=symbol_values[idx],
                                name=value,
                                box_visible=True,
                                meanline_visible=True))
    
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