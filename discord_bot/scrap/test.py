from transformers import BertTokenizer, BertModel
import torch
import sqlite3
import pandas as pd
from scipy.spatial.distance import cosine
from db_init import db_get_df

