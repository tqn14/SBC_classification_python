import numpy as np 
import pandas as pd
from python_sbc_classification import utils
import matplotlib.pyplot as plt

class Result: 
    def __init__(self, p, v, model_use):
        self.p = p 
        self.v = v 
        self.model_use = model_use
    def getDemandInterval(self): 
        return self.p 
    def getCVSquared(self): 
        return self.v
    def getCoefficients(self):
        print(f'p (demand interval), CV squared (coefficient of variation): {[self.p, self.v]}')
        return [self.p, self.v]
    def getModelUse(self): 
        return self.model_use
        

def classify_series_helper(data, type ="SBC"): 
    # check if input data is an array/list, etc: 
    data = data[~np.isnan(data)]
    nzd = np.where(data != 0)[0]
    k = len(nzd)
    z = data[nzd]
    x = np.diff(nzd, prepend=-1)
    p = np.mean(x)
    v = (np.std(z, ddof=1) / np.mean(z)) ** 2

    if type == 'SBC': 
        if p > 1.32 or v < 0.49: 
            model_use = 'SBA'
        else: 
            model_use = 'Croston'
    else: 
        print("Unsupported classification type")
    return Result(p, v, model_use)

def sbc_class(data, type = 'SBC', plot_type = None):
    # check if input data is an array/list, etc: 
    p = [] 
    v = [] 
    model_use = [] 
    out_df = pd.DataFrame()
    if np.ndim(data) == 1 and not isinstance(data, pd.DataFrame): 
        if len(data) != 0: 
            target = np.array(data)
            target = target.reshape(len(target), -1)
            res = classify_series_helper(target, type)
            p.append(res.getDemandInterval())
            v.append(res.getCVSquared())
            model_use.append(res.getModelUse())
            out_df['target'] = np.nan
            out_df['p'] = p 
            out_df['CV Squared'] = v 
            out_df['model'] = model_use
        else: 
            raise ValueError('Please check if data is empty')
    elif np.ndim(data) == 1 and isinstance(data, pd.DataFrame): 
        # assume the first column to be the target
        target = np.array(data.iloc[:, 0])
        res = classify_series_helper(target, type)
        p.append(res.getDemandInterval())
        v.append(res.getCVSquared())
        model_use.append(res.getModelUse())
        out_df['target'] = np.nan
        out_df['p'] = p 
        out_df['CV Squared'] = v 
        out_df['model'] = model_use
    elif np.ndim(data) >1 and isinstance(data, pd.DataFrame): 
        target = data.to_numpy().T
        p = [] 
        v = [] 
        model_use = [] 
        out_df = pd.DataFrame()
        for i in range(target.shape[0]): 
            res = classify_series_helper(target[i], type)
            p.append(res.getDemandInterval())
            v.append(res.getCVSquared())
            model_use.append(res.getModelUse())
        out_df['target'] = data.columns.to_list()
        out_df['p'] = p 
        out_df['CV Squared'] = v 
        out_df['model'] = model_use
    else: 
        raise ValueError('Please pass in a list, an array or a dataframe')
    if plot_type == 'bar': 
        d = utils.create_dict_plot_helper(out_df)
        print("test", d)
        out_plot = utils.bar_plot(d)
        plt.show()
    elif plot_type == 'summary': 
        out_plot = utils.summary_plot(out_df)
        plt.show()
    elif plot_type is not None: 
        raise ValueError('Please pass in a correct type of plot')
    return out_df

