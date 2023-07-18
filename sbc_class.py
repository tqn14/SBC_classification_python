import numpy as np 
import pandas as pd

class Result: 
    def __init__(self, name, p, v, use_sba, use_croston):
        self.name = name 
        self.p = p 
        self.v = v 
        self.use_croston = use_croston 
        self.use_sba = use_sba
    def getDemandInterval(self): 
        return self.p 
    def getCVSquared(self): 
        return self.v
    def getCoefficients(self):
        return f'p (demand interval), CV squared (coefficient of variation): {[self.p, self.v]}'
    def getModelUsed(self): 
        if self.use_sba: 
            return "SBA"
        if self.use_croston: 
            return "Croston" 
        

def classify_series(data, col_name, type ="SBC", plot = True): 
    # check if input data is an array/list, etc: 
    if np.ndim(data) == 1 and not isinstance(data, pd.DataFrame): 
        data = np.array(data)
        data = data.reshape(len(data), -1)
    elif isinstance(data, pd.DataFrame): 
        try: 
            data = np.array(data[col_name])
        except: 
            print("Please check column name")
    else: 
        print("please pass in a list or array")

    nzd = np.where(data != 0)[0]
    k = len(nzd)
    z = data[nzd]
    x = np.diff(nzd, prepend=0)
    p = np.mean(x)
    v = (np.std(z) / np.mean(z)) ** 2

    use_sba = False
    use_croston = False
    if type == 'SBC': 
        if p > 1.32 or v < 0.49: 
            use_sba = True 
        else: 
            use_croston = True
    else: 
        print("Unsupported classification type")

    return Result(col_name, p, v, use_sba, use_croston)

