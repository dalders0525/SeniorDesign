import matplotlib.pyplot as plt
import sounddevice as sd
import numpy as np
import time as tm
import scipy as sp
from scipy import signal
from numpy.fft import fft, fftshift

sd.default.samplerate=48000
duration = .2
i = 0 #initialized counter variable
x1=[0] #initialized DUT1 array variable for data after filtering
x2=[0] #initialized DUT2 array variable for data after filtering
x1a=[0] #initialized DUT1 array variable for data after filtering
x2a=[0] #initialized DUT2 array variable for data after filtering

while i <=50: #collect data from source 1
    sd.default.device ='USB PnP Sound Device'
    dataset_2 = sd.rec(int(duration*sd.default.samplerate),channels=1)
    i+=1
    
i=0 #reinitialize counter to zero
tm.sleep(.2) #200 ms non-blocking delay

while i <=50: #collect data from source 2
    sd.default.device = 'USB Audio Device'
    dataset_1 = sd.rec(int(duration*sd.default.samplerate),channels=1)
    i +=1

i=0 #reinitialize counter to zero
tm.sleep(.2) #200 ms non-blocking delay

x1 = np.amax(dataset_1)
x2 = np.amax(dataset_2)
x1a = np.average(dataset_1)
x2a = np.average(dataset_2)
##print(x1)
##print(x2)
##print(x1a)
##print(x2a)

x=np.linspace(0,11580,num = 9600); #generates plot of dataset 1 in frequency domain


w1=signal.savgol_filter(dataset_1, 501, 2,0,1.0,0)
plt.plot(x,w1,'b')
plt.show()

w2=signal.savgol_filter(dataset_2, 501, 2,0,1.0,0)
plt.plot(x,w2,'b')
plt.show()
print('Average Power Draw on Outlet One:' , np.average(w1))
print('Average Power Draw on Outlet Two:' , np.average(w2))


print('Working load defined as either motor or heat generating.')
f1 = np.average(w1)
f2 = np.average(w2)


if f1 <= 0.007:
    print('Nothing Running or Power Draw Insubstantial on Outlet One')
elif 0.007 <= f1 < 0.0076:
    if 0.0073 < f1 < 0.0076:
        print('Working Load Detected on Outlet One: UNot in Use')
    else:
        print('Non-Working Load Detected on Outlet One')
elif 0.00765 <= f1:
    print('Working Load Detected on Outlet One: Use Caution')

if f2 <= 0.001:
    print('Nothing Running or Power Draw Insubstantial on Outlet Two')
elif 0.001 <= f2 <= 0.002:
    print('Non-Working Load Detected on Outlet Two')
elif 0.002 < f2 < 0.0072:
    print('Working Load Detected on Outlet Two: Not in Use')
elif 0.00722 < f2:
    print('Working Load in Use on Outlet Two: Use Caution')
