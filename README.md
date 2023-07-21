# Demand Patterns SBC (Syntetos Boylan Croston) method of Categorizations

## Description
This method helps classify different demand patterns (time-series patterns) into groups in order to fit the most appropriate model. More info could be found [here](https://www.researchgate.net/publication/28578603_On_the_categorization_of_demand_patterns) and [here](https://robjhyndman.com/papers/SBC-categorization.pdf) 

This is a Python version of the tsintermittent package in R. At the moment, only the SBC method is available 

## 

```
project
│   README.md
│
└───tests
│   │   test_SBCclass.py
│   │
│   └───data
│       │   sales_train_clean.csv
│   
└───sbc
    │   sbc_class.py
    │   util.py
```

## Test Data

Test data is the clean version of the data from M5 Forecasting Challenge competition on Kaggle. Details can be found [here](https://www.kaggle.com/competitions/m5-forecasting-accuracy/data)