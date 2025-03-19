import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

'''
a = np.random.choice([0, 1], size=4, p=(0.4, 0.6))
print(np.mean(a))
# różne wyniki [0.25, 0.5, 0.75, 1]
a = np.random.choice([0, 1], size=1000, p=(0.4, 0.6))
print(np.mean(a))
# 0.599
'''

n = 10
pr = 0.5
def perfectEstimation(n, pr):
    i = 0
    while True:
        i+=1
        a = np.random.choice([0,1], size = n, p=(1-pr, pr))
        if sum(a) == n * pr:
            return i
        
# print(perfectEstimation(n, pr))

list_of_n = [2, 4, 6, 8, 10, 14, 20, 30, 50, 70, 100, 150, 200, 300]

def dataGeneration(n_list, l_eksp, pr):
    data = {}
    for n in n_list:
        suma = 0
        for _ in range(l_eksp):
            suma += perfectEstimation(n, pr)
        data[n] = suma/l_eksp
    return data

def showScatter(list_of_n):
    data = dataGeneration(list_of_n, 100, 0.5)
    df = pd.DataFrame({'l_prob': list(data.keys()), 'srednia': list(data.values())})
    # print(df)
    plt.figure(figsize=(10, 5))
    sns.scatterplot(data=df, x='l_prob', y='srednia')
    plt.show()

showScatter(list_of_n)






