#------------------------------------------------------------------------------------------#
'''
LIBRERIAS
'''
import sqlalchemy as sql
import pandas as pd
import numpy as np
import streamlit as st
import matplotlib.pylab as plt
import plotly.express as px
import datetime
from PIL import Image
import altair as alt
import pymysql
#------------------------------------------------------------------------------------------#
'''
CONEXION DataWarehouse
'''
engine = sql.create_engine(
    "mysql+pymysql://root:password@localhost:3307/data_warehouse_olist?charset=utf8mb4"
)
#------------------------------------------------------------------------------------------#