from random import weibullvariate

import matplotlib.pyplot as plt

data = [weibullvariate(0.1, 1) for _ in range(100000)]
plt.hist(data, bins=1000)

plt.show()

#%%
# Import the required Python libraries
import matplotlib.pyplot as plt
from scipy import interpolate
import numpy as np
  
# Initialize input values x and y
x = np.arange(0, 10)
y = x**2
  
# Interpolation
temp = interpolate.interp1d(x, y)
xnew = np.arange(0, 9, 0.2)
ynew = temp(xnew)
  
plt.title("1-D Interpolation")
plt.plot(x, y, '*', xnew, ynew, '-', color="green")
plt.show()
# %%
# Import the required Python libraries
import numpy as np
import matplotlib.pyplot as plt
from scipy import interpolate
  
# Initialize the input values
x = np.arange(0, 10)
y = np.cos(x**3)



# Interpolation
# To find the spline representation of a 
# curve in a 2-D plane using the function 
# splrep

temp = interpolate.splrep(x, y, s=0)
xnew = np.arange(0, np.pi**2, np.pi/100)
ynew = interpolate.splev(xnew, temp, der=0)
  
plt.figure()
  
plt.plot(x, y, '*', xnew, ynew, xnew, np.cos(xnew),
         x, y, 'b', color="green")
  
plt.legend(['Linear', 'Cubic Spline', 'True'])
plt.title('Cubic-spline Interpolation in Python')

plt.show()
# %%
# Import the required libraries
import numpy as np
from scipy.interpolate import Rbf
import matplotlib.pyplot as plt


# setup the data values
x = np.linspace(0, 10, 9)
y = np.cos(x/2)

x = [ 0.0, 20.0, 210.0, 240.0, 300.0, 340.0, 360.0,]
y = [ 0.0, 2.0, 2.0, 4.5, 17.5, 20.0, 20.0,]  


xi = np.linspace(0, 360, 10)
  
# Interpolation using RBF
rbf = Rbf(x, y)
fi = rbf(xi)
  
plt.subplot(2, 1, 2)
plt.plot(x, y, '*', color="green")
plt.plot(xi, fi, 'green')
plt.plot(xi, np.sin(xi), 'black')
plt.title('Radial basis function Interpolation')
plt.show()

# %%
