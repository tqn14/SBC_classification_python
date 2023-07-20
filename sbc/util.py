import numpy as np 
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

def create_dict_plot_helper(input_df): 
    d = {}
    d['Erratic'] = 0 
    d['Lumpy'] = 0
    d['Smooth'] = 0
    d['Intermittent'] = 0
    d['No group'] = 0
    if len(input_df) == 1: 
        if input_df['p'].values[0] >= 1.32:
            if input_df['CV Squared'].values[0] >= 0.49: 
                d['Lumpy'] = 1
            else: 
                d['Intermittent'] = 1
        elif input_df['p'].values[0] < 1.32: 
            if input_df['CV Squared'].values[0] >= 0.49: 
                d['Erratic'] = 1
            else: 
                d['Smooth'] = 1
        else: 
            d['No group'] = 1 
    else: 
        d['Erratic'] = len(input_df[(input_df['p'] < 1.32) & (input_df['CV Squared'] >= 0.49)])
        d['Lumpy'] = len(input_df[(input_df['p'] >= 1.32) & (input_df['CV Squared'] >= 0.49)])
        d['Smooth'] = len(input_df[(input_df['p'] < 1.32) & (input_df['CV Squared'] < 0.49)])
        d['Intermittent'] = len(input_df[(input_df['p'] >= 1.32) & (input_df['CV Squared'] < 0.49)])
        d['No group'] = len(input_df) - sum(d.values())
    return d 

def bar_plot(input_dict): 
    fig, ax = plt.subplots(figsize = (12,6))
    labels = ['Erratic', 'Lumpy', 'Smooth', 'Intermittent', 'No group']
    values = list(input_dict.values())

    bar_colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd']

    out = ax.bar(labels, values, color=bar_colors)
    ax.bar_label(out, labels = values, padding = 0.5)
    ax.set_ylabel('Number of demand patterns')
    ax.set_title('Number of demand patterns by category')
    return ax

def summary_plot(input_df): 
    sba_count = 0 
    croston_count = 0
    if len(input_df) == 1: 
        model = input_df['model'].values[0]
        if model == 'SBA': 
            sba_count = 1 
        else: 
            croston_count = 1
    else:
        sba_count = len(input_df[input_df['model'] == 'SBA'])
        croston_count = len(input_df[input_df['model'] == 'Croston'])
    fig,ax = plt.subplots(figsize = (8,8))
    currentAxis = plt.gca()
    currentAxis.add_patch(Rectangle((1,0), width = 0.64, height = 0.98, facecolor='none'))
    currentAxis.add_patch(Rectangle((1,0), width = 0.32, height = 0.49, facecolor='grey', alpha = 0.5))
    ax.set_yticks(np.arange(0, 0.98, 0.49))
    ax.set_xlim(1, 1.64)
    ax.set_xticks(np.arange(1, 1.64, 0.32))
    ax.axvline(x = 1.32, color = 'grey', alpha = 0.5, linestyle = 'dotted')
    ax.axhline(y = 0.49, color = 'grey', alpha = 0.5, linestyle = 'dotted')
    ax.text((1 + 1.32) /2, (0.49 + 0.98)/2, 'Erratic', ha = 'center', va = 'center', alpha = 0.7)
    ax.text((1.32 + 1.64) /2, (0.49 + 0.98)/2, 'Lumpy', ha = 'center', va = 'center', alpha = 0.7)
    ax.text(1.64, 0.98, f'SBA: {sba_count}', ha = 'right', va = 'top', alpha = 0.9)
    ax.text((1 + 1.32) /2, (0 + 0.49)/2, 'Smooth', ha = 'center', va = 'center', alpha = 0.7)
    ax.text(1, 0, f'Croston: {croston_count}', ha = 'left', va = 'bottom', alpha = 0.9)
    ax.text((1.32 + 1.64) /2, (0 + 0.49)/2, 'Intermittent', ha = 'center', va = 'center', alpha = 0.7)
    ax.set_ylabel("CV\u00b2")
    ax.set_xlabel("p")
    ax.set_title("SBC Classification")
    return ax