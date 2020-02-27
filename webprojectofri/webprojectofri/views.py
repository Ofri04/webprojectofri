"""
Routes and views for the flask application.
"""

from datetime import datetime
from flask import render_template
from webprojectofri import app
from webprojectofri.Models.LocalDatabaseRoutines import create_LocalDatabaseServiceRoutines


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


from webprojectofri.Models.QueryFormStructure import QueryFormStructure 
from webprojectofri.Models.QueryFormStructure import LoginFormStructure 
from webprojectofri.Models.QueryFormStructure import UserRegistrationFormStructure 

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

