import random
import numpy
from matplotlib import pyplot as plt

datas = [
    [random.randint(i+10, i+20), random.randint(i+50, i+100)] for i in range(random.randint(10, 50))
]

fig, axs = plt.subplots(nrows=1, ncols=1, figsize=(7, 7))

fig = plt.figure(1)	#identifies the figure 
plt.title("Y vs X", fontsize='16')	#title
plt.plot([i[0] for i in datas], [i[1] for i in datas], color='gray')	#plot the points
plt.xlabel("X",fontsize='13')	#adds a label in the x axis
plt.ylabel("Y",fontsize='13')	#adds a label in the y axis
plt.legend(('YvsX'),loc='best')	#creates a legend to identify the plot
# plt.savefig('Y_X.png')	#saves the figure in the present directory
plt.grid()	#shows a grid under the plot
plt.show()

print(datas)









