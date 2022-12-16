"""
Class: CS230--Section 4
Name: Wayne Ng
Description: Final Program
I pledge that I have completed the programming assignment independently.
I have not copied the code from a student or any source.
I have not given my code to any student.
"""

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import re

st.set_page_config(layout="wide") #Wide page width

DATA_URL = "Used_cars.csv"

REGEX = "^(\w|\.|\_|\-)+[@](\w|\_|\-|\.)+[.]\w{2,3}$"

# ---------------------------------------------------------
# Load Data Functions
# ---------------------------------------------------------

def load_data(): #Read CSV file to lists
    data = pd.read_csv(DATA_URL, delimiter=",")
    data = data.dropna(subset=['model', 'state', 'lat', 'long', 'manufacturer'])
    data['model'] = data['model'].astype('string')
    data['manufacturer'] = data['manufacturer'].astype('string')
    data['posting_date'] = pd.to_datetime(data['posting_date'])
    return data

# ---------------------------------------------------------
# Pages
# ---------------------------------------------------------

def homePage(): #Home page
    st.image("https://drive.google.com/uc?export=view&id=1BSJLKaIigquicNUgN6bPcELapk1JGMXI") # Image from drive

    st.header("Introduction to my Final Project")

    st.markdown('''Welcome everyone to my final project for my Python class!
    In this in this assignment, we are expected to develop an interactive data-driven 
    web-based Python application that shows our mastery of many coding concepts as we interact 
    with data real world data. The data set I chose to use for this assignment is the National 
    Parks in New York data. Below are some of the coding skills I have demonstrated in this assignment:
    
    • Coding Fundamentals: data types, if statements, loops, formatting, etc. 
    • Data Structures: Interact with lists, tuples, dictionaries (keys, values, items)
    • Funct ions:  passing positional and optional arguments,  returning values
    • Files: Reading data from a CSV file into a DataFrame
    • Pandas: Module functions and DataFrames to manipulate large data sets
    • MatPlotLib or pandas: Creating different types of charts
    • StreamLit.io: Displaying interactive widgets and charts
    ''')

def understandingPage(data):
    st.header("Average Price of Different Models of Cars")
    st.markdown("Find the average price of each model of car in the state you live in!")
    col1, space, col2 = st.columns([14,1,15]) # define width for columns

    with col1: #column 1 containing checkboxes
        state = st.selectbox('State', getUniqueState(data))
        cars = st.multiselect('Cars', getUniqueModel(data, state))

    with col2:
        prices = getMeanCarPrice(data, cars, state)
        bar_chart(prices)

def comparisonPage(data):
    st.header("Where to get?")
    st.markdown("Which state to get the car for the lowest price!")
    col1, space, col2 = st.columns([14,1,15]) # define width for columns

    with col1: #column 1 containing checkboxes
        brand = st.selectbox('Car Brand', getUniqueCarBrand(data))
        carModel = st.multiselect('Car Model', getUniqueModelFromBrand(data, brand))

    with col2:
        #map stuff
        pass

# ---------------------------------------------------------
# Helper functions
# ---------------------------------------------------------
def getUniqueState(data):
    stateValues = data['state'].unique()
    stateValues.sort()
    return stateValues

def getUniqueModel(data, state):
    return sorted(data[data['state'] == state]['model'].unique())

def getUniqueCarBrand(data):
    return sorted(data['manufacturer'].unique())

def getUniqueModelFromBrand(data, brand):
    return sorted(data[data['manufacturer'] == brand]['model'].unique())

def getMeanCarPrice(data, cars, state):
    dataState = data[data['state'] == state] #filter by selected state
    dataStateCar = dataState[dataState['model'].isin(cars)]
    return dataStateCar.groupby('model')['price'].mean()

def bar_chart(prices): #Plots bar chart of cars by state
    fig, ax = plt.subplots()
    ax.bar(prices.keys(), prices , width=0.45, label="Frequency") #Plot bar chart
    ax.grid(axis="y", color = "lightgray",linestyle="-.", linewidth= .25)

    st.pyplot(fig)
    st.set_option('deprecation.showPyplotGlobalUse', False) #Dismiss warning on streamlit

# ---------------------------------------------------------
# Streamlit Navigation
# ---------------------------------------------------------

st.title("CS230 Final Project")
st.text("By: Wayne Ng Chia Hao")

data = load_data()

st.sidebar.title("Navigation")
selection = st.sidebar.radio("Go to", ["Home", "Understanding", "Comparison", "Best Option Available"])
if selection == "Home":
    homePage()
if selection == "Understanding":
    understandingPage(data)
if selection == "Comparison":
    comparisonPage(data)
if selection == "Best Option Available":
    pass