#%%
import argparse
import importlib
import pandas as pd
import numpy as np

#%%
def get_args(debug):
    parser = argparse.ArgumentParser('parameters')
    
    parser.add_argument('--embedding_type', type=str, default='openai', 
                        help='embedding type (options: openai, huggingface)')    
    parser.add_argument('--threshold', type=float, default=0.9, 
                        help='consine similarity threshold between question and word')  

    if debug:
        return parser.parse_args(args=[])
    else:    
        return parser.parse_args()
    
#%% 
config = vars(get_args(debug=True))
#%%
"""dataset"""

# %%
