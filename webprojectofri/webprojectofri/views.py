"""
Routes and views for the flask application.
"""

from datetime import datetime
from flask import render_template
from webprojectofri import app
from webprojectofri.Models.LocalDatabaseRoutines import create_LocalDatabaseServiceRoutines

import matplotlib.pyplot as plt
from   matplotlib.figure import Figure


from datetime import datetime
from   flask import render_template, redirect, request

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

import json 
import requests

import io
import base64

from os import path

from flask   import Flask, render_template, flash, request
from wtforms import Form, BooleanField, StringField, PasswordField, validators
from wtforms import TextField, TextAreaField, SubmitField, SelectField, DateField
from wtforms import ValidationError


from webprojectofri.Models.FormStructure import DataQueryFormStructure 
from webprojectofri.Models.FormStructure import LoginFormStructure 
from webprojectofri.Models.FormStructure import UserRegistrationFormStructure 


from webprojectofri.Models.DataQuery     import plot_to_img
from webprojectofri.Models.DataQuery     import Get_NormelizedUFOTestmonials
from webprojectofri.Models.DataQuery     import get_states_choices
from webprojectofri.Models.DataQuery     import Get_NormelizedWeatherDataset
from webprojectofri.Models.DataQuery     import MergeUFO_and_Weather_datasets
from webprojectofri.Models.DataQuery     import MakeDF_ReadyFor_Analysis

###from DemoFormProject.Models.LocalDatabaseRoutines import IsUserExist, IsLoginGood, AddNewUser 

db_Functions = create_LocalDatabaseServiceRoutines() 

##home page
@app.route('/')
@app.route('/home')
def home():
    """Renders the home page."""
    return render_template(
        'index.html',
        title='Home Page',
        year=datetime.now().year,
    )
##contact page
@app.route('/contact')
def contact():
    """Renders the contact page."""
    return render_template(
        'contact.html',
        title='Contact ',
        year=datetime.now().year,
        message='Ofri Manor contact page'
    )
##the aboout page
@app.route('/about')
def about():
    """Renders the about page."""
    return render_template(
        'about.html',
        title='About The Project',
        year=datetime.now().year,
        message='Ofri Manors html project.'
        
    )
# -------------------------------------------------------
# Register new user page
# -------------------------------------------------------
@app.route('/register', methods=['GET', 'POST'])
def Register():
    form = UserRegistrationFormStructure(request.form)

    if (request.method == 'POST' and form.validate()):
        if (not db_Functions.IsUserExist(form.username.data)):
            db_Functions.AddNewUser(form)
            db_table = ""

            flash('Thanks for registering new user - '+ form.FirstName.data + " " + form.LastName.data )
            # Here you should put what to do (or were to go) if registration was good
        else:
            flash('Error: User with this Username already exist ! - '+ form.username.data)
            form = UserRegistrationFormStructure(request.form)

    return render_template(
        'register.html', 
        form=form, 
        title='Register New User',
        year=datetime.now().year,
        repository_name='Pandas',
        )
##data frame page
@app.route('/data')
def data():
    """Renders the data page."""
    return render_template(
        'data.html',
        title='data',
        year=datetime.now().year,
        message='Your application description page.'
    )
##data set page
@app.route('/datadet1')
def dataset1():
    pd.options.display.max_rows = 100
    df = pd.read_csv(path.join(path.dirname(__file__), 'static\\Data\\dataframe.csv'))
    
    raw_data_table = df.to_html(classes = 'table table-hover')
    
    """Renders the dataset page."""
    return render_template(
        'dataset1.html',
        title='This is Data Set 1 page',
        raw_data_table = raw_data_table,
        year=datetime.now().year,
        message='In this page we will display the datasets we are going to use in order to explain the dataset'
        
        )


# -------------------------------------------------------
# Login page
# This page is the filter before the data analysis
# -------------------------------------------------------
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginFormStructure(request.form)

    if (request.method == 'POST' and form.validate()):
        if (db_Functions.IsLoginGood(form.username.data, form.password.data)):
            flash('Login approved!')
            return redirect('<were to go if login is good!')
        else:
            flash('Error in - Username and/or password')
   
    return render_template(
        'login.html', 
        form=form, 
        title='Login to data analysis',
        year=datetime.now().year,
        )

@app.route('/')
@app.route('/DataQuery')
def DataQuery():
    """Renders the DataQuery page."""
    form = DataQueryFormStructure(request.form)
     
    #set default values of datetime, to indicate ALL the rows
    #form.start_date.data = "12/05/2020"
    #df_ufo.Event_Time.min()
    #form.end_date.data = df_ufo.Event_Time.max()


    #Set the list of states from the data set of all US states
    form.states.choices = get_states_choices() 

    if ((request.method == 'POST' and formvalidate()) or True):
        states = form.states.data
        start_date = form.start_date.data
        end_date = form.end_date.data
        kind = form.kind.data

        df = pd.read_csv(path.join(path.dirname(__file__),"static\\Data\\dataframe.csv" ))
        drug_list = ['Morphine_NotHeroin','Tramad','Amphet','Methadone','Benzodiazepine','Hydrocodone','Ethanol','Oxymorphone','FentanylAnalogue','Oxycodone','Fentanyl','Cocaine','Heroin','Hydromorphone']
        l=['Date','Race','ResidenceState']
        coulumn_list= l + drug_list
        df=df[coulumn_list]
        b=df.columns.tolist()
        s=df['Race']
        year='2018'
        df=df[df['Date'].notna()]
        df=df[df['Date'].str.contains(year)]
        ResidenceState='CT'
        df=df[df['ResidenceState'].notna()]
        df=df[df['ResidenceState'].str.contains(ResidenceState)]
        df=df.drop(['Date','ResidenceState','Race'],1)
        df=df.fillna(value=0)
        df.shape[0]
        for drug in drug_list:
           df[drug]=df[drug].replace('Y',1)
           df[drug]=df[drug].replace('YES',1)
           df[drug]=df[drug].astype(int)
        t=[ ]
        for drug in drug_list: 
           t.append(df[drug].sum())
           #print(drug)
           #print(df[drug].sum())

        df1=pd.DataFrame(index=drug_list)
        df1['Death']=t

        print(df1)
        df1.plot(kind='pie',y='Death')
        
        fig = plt.figure()
        ax = fig.add_subplot()
        df1.plot(ax = ax , kind='pie',y='Death', figsize=(10,10))
        chart = plot_to_img(fig)
        chartyear = [2015,2016,2017,2018]

        return render_template(
           'DataQuery.html',
           img_under_construction = '/static/imgs/under_construction.png',
           chart = chart,
           form=form,
           height = "250" ,
           width = "600",
           year=datetime.now().year,
           chartyear = chartyear,
           message='Please enter the parameters you choose, to analyze the database'

    )