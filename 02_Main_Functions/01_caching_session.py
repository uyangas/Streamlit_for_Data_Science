import streamlit as st
import pandas as pd
import numpy as np
import os
import json
import sys

import matplotlib.pyplot as plt
import seaborn as sns

with open("../utils/config.json","r") as f:
    config = json.load(f)

PATH = config['DATA_PATH']

@st.cache_data
def load_data():
    df = pd.read_excel(os.path.join(PATH, "Coffee Shop Sales.xlsx"))

    return df

coffee_df = load_data()

st.write(coffee_df.head())