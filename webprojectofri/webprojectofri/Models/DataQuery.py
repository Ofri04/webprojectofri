import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure

import base64
import datetime
import io
from os import path

# -------------------------------------------------------------------------------
# Function to convert a plot to an image that can be integrated into an HTML page
# -------------------------------------------------------------------------------
def plot_to_img(fig):
    pngImage = io.BytesIO()
    FigureCanvas(fig).print_png(pngImage)
    pngImageB64String = "data:image/png;base64,"
    pngImageB64String += base64.b64encode(pngImage.getvalue()).decode('utf8')
    return pngImageB64String

# -------------------------------------------------------
# Function that get a dataset that include in the columns 
# -------------------------------------------------------
def Get_NormelizedWeatherDataset():
    dfw = pd.read_csv(path.join(path.dirname(__file__), "..\\static\\data\\weather_description.csv"))
    # Keep only the columns I will need
    dff = pd.DataFrame(columns=list(['datetime', 'Weather', 'State']))
    # Re-arrange the dataset in a way that I will have a olumn with the state name, and for each day, the weather description
    for col in dfw.columns: 
        if (col != 'datetime'):
            dft = dfw[['datetime', col]].copy()
            dft['State'] = col
            dft = dft.rename(columns={col: 'Weather'})
            dff = dff.append(dft)
    # Change string type to date type
    dff['datetime'] = pd.to_datetime(pd.Series(dff['datetime']))
    # remove minutes and second part
    dff['datetime'] = dff['datetime'].dt.date
    # remove rows with Non fields
    dff = dff.dropna()
    # remove duplicate rows
    dff.drop_duplicates(inplace=True)
    return (dff)

# # # the function convert the state to full name  # # #
def Convert_StateCode_ToFullName(df):
    df_short_state = pd.read_csv(path.join(path.dirname(__file__), "..\\static\\data\\USStatesCodes.csv"))
    s = df_short_state.set_index('Code')['State']
    return (df.replace(s))

# # #       # # #
def get_states_choices():
    df_short_state = pd.read_csv(path.join(path.dirname(__file__), "..\\static\\data\\USStatesCodes.csv"))
    s = df_short_state.set_index('Code')['State']
    df1 = df_short_state.groupby('Code').sum()
    #df_short_state = df_short_state.set_index('Code')
    #df_short_state = df_short_state.sort_index()
    l = df1.index
    m = list(zip(l , l))
    return m

