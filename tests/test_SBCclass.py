import numpy as np 
import pandas as pd 
import pytest
import os
import sys

current_path = os.path.dirname(os.path.abspath(__file__))
new_path = os.path.join(current_path, "..")
sys.path.append(new_path)

from sbc import sbc_class 

data = pd.read_csv("data/sales_train_clean.csv")

def test_raise_empty_data_df(): 
    ## ndim == 2 
    input_data = pd.DataFrame()
    with pytest.raises(ValueError):
        sbc_class.sbc_class(input_data)

def test_raise_empty_data_list():
    ## ndim == 1
    input_data = []
    with pytest.raises(ValueError):
        sbc_class.sbc_class(input_data)

def test_null_object(): 
    input_data = None 
    with pytest.raises(ValueError):
        sbc_class.sbc_class(input_data)

def test_plot_value(): 
    df = data.iloc[:,1:3]
    type = ['line_plot']
    with pytest.raises(ValueError):
        sbc_class.sbc_class(df, plot_type=type)

def test_reproducible(): 
    df = data.iloc[:, 1]
    df1 = data.iloc[:,1]
    out1 = sbc_class.sbc_class(df)
    out2 = sbc_class.sbc_class(df1)
    
    assert out1.equals(out2)


