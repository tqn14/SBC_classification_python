import numpy as np 
import pandas as pd

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
        

def classify_series_helper(data, type ="SBC", plot = False): 
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

def sbc_class(data, type = 'SBC', plot=False):
    # check if input data is an array/list, etc: 
    if np.ndim(data) == 1 and not isinstance(data, pd.DataFrame): 
        target = np.array(data)
        target = target.reshape(len(target), -1)
        res = classify_series_helper(target, type, plot)
        print(f"Model use: {res.getModelUse()}")
        res.getCoefficients()
    elif np.ndim(data) == 1 and isinstance(data, pd.DataFrame): 
        # assume the first column to be the target
        target = np.array(data.iloc[:, 0])
        res = classify_series_helper(target, type, plot)
        print(f"Model use: {res.getModelUse()}")
        res.getCoefficients()
    elif np.ndim(data) >1 and isinstance(data, pd.DataFrame): 
        target = data.to_numpy().T
        p = [] 
        v = [] 
        model_use = [] 
        out_df = pd.DataFrame()
        for i in range(target.shape[0]): 
            res = classify_series_helper(target[i], type, plot)
            p.append(res.getDemandInterval())
            v.append(res.getCVSquared())
            model_use.append(res.getModelUse())
        out_df['target'] = data.columns.to_list()
        out_df['p'] = p 
        out_df['CV squared'] = v 
        out_df['model'] = model_use
        return out_df
    else: 
        raise ValueError('Please pass in a list/array (for 1 target) or a dataframe (multiple targets)')
    return (res.getModelUse(), [res.getDemandInterval(), res.getCVSquared()])

