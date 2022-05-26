import os
import datetime
import numpy as np
import pandas as pd
import streamlit as st


# project settings
VERSION = 'version_2'
METRIC = 'mape'
PRED_DATE = '2022-05-25'

#task settings
BASELINE = False  #if True compare the current day wrt the current prediction of the baseline
DATA1 = datetime.datetime(2021,4,1)
DATA2 = None
# ID_LIST = ["03377_181000.008", "05284_110077.004", "05285_110044.001", "74016_081000.012"]
ID_LIST = None

# project directories settings
ROOT = os.getcwd()
DATA_DIR = os.path.join(ROOT,'../voltaine/data/')
PRED_DIR = os.path.join(DATA_DIR,'prediction/',VERSION)
TRAIN_PRED = os.path.join(PRED_DIR,'train',PRED_DATE)
TEST_PRED = os.path.join(PRED_DIR,'test',PRED_DATE)


# graph settings
blu_ammagamma = 'rgba(0,71,92,'
red = 'rgba(199,75,55,'
orange = 'rgba(240,129,22,'
dark_blue = 'rgba(0,60,80,'
yellow = 'rgba(235,185,10,'
green = 'rgba(72,118,42,'
grey = 'rgba(124,145,146,'
antique_pink = 'rgba(144,98,95,'
alpha = 0.3
