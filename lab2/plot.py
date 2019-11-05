import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

x = [1000, 2000, 5000, 10000, 15000, 20000]
means = []

plt.figure(1)
data = pd.read_csv("data/queue-1000.csv")
meanQD = data['QD'].mean()
means.append(meanQD)
data = pd.read_csv("data/queue-2000.csv")
meanQD = data['QD'].mean()
means.append(meanQD)
data = pd.read_csv("data/queue-5000.csv")
meanQD = data['QD'].mean()
means.append(meanQD)
data = pd.read_csv("data/queue-10000.csv")
meanQD = data['QD'].mean()
means.append(meanQD)
data = pd.read_csv("data/queue-15000.csv")
meanQD = data['QD'].mean()
means.append(meanQD)
data = pd.read_csv("data/queue-20000.csv")
meanQD = data['QD'].mean()
means.append(meanQD)

plt.plot(x, means, 'r')

# x = np.linspace(0, 1, num=100)
# y = x/((2*(125))*(1-x))

plt.xlabel('window size')
plt.ylabel('queueing delay')
# f1.plot(x,y, 'g')
plt.gca().legend(('queueing delay'))

#--------------------------------------------------------------------------------
vals = []
plt.figure(2)

data = pd.read_csv("data/Throughput.csv")
vals = data['Throughput']

plt.plot(x, vals, 'r')

plt.xlabel('window size')
plt.ylabel('throughput')

#--------------------------------------------------------------------------------

plt.show()
#1000000 // (1000*8)
