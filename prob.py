import random
import math
# import matplotlib.pyplot as plt

lam = 3
mu = 4
MAX = 100
alfa = lam/mu
T = 0
N = (((alfa)**2)+((alfa)*MAX - MAX - 1)*((alfa)**(MAX+2)))/((1-alfa))*(1-((alfa)**(MAX+2)))
print ('Средняя длина очереди заявок: N = ',N, '\n')
p0 = (1 - alfa)/(1-(alfa**(MAX+2)))
M = N + 1 - p0
t = M / lam
print('Среднее время пребывания в системе t = ', t,'\n')
print('Среднее время простоя обслуживающего устройства ta = ','\n')
#for T to 1
# ta = p0*T
tta=[]
for T in range(10):
ta = p0*T

print(ta,'\n')