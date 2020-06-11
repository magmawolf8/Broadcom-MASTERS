from sklearn.cluster import KMeans;
import matplotlib.pyplot as plt;
import numpy as np;
import smbus;
import time;
import os;
import gpiozero as gpio;

#variable initialization to prevent errors

clear = lambda: os.system("clear");
bus = smbus.SMBus(1);
address = 0x48;
starttime = time.time();
elapsedtime = 0;
mtrcurrent = 0;
lhtcurrent = 0;
masterlist = [];
iterate_one = 0;
iterate_two = 0;

#define motorcurrent and lightcurrent

def motorcurrent():
    #time.sleep(0.1);
    mcurrent = bus.read_byte_data(address,3);
    mcurrent = 255 - mcurrent;
    return mcurrent;
    
def lightcurrent():
    #time.sleep(0.1);
    lcurrent = bus.read_byte_data(address,3);
    lcurrent = 255 - lcurrent;
    return lcurrent;

while elapsedtime < 10:
    print("prep phase");
    print(elapsedtime);
    print(mtrcurrent);
    print(lhtcurrent);
    mtrcurrent = motorcurrent();
    lhtcurrent = lightcurrent();
    elapsedtime = time.time() - starttime;
    clear();

starttime = time.time();
elapsedtime = 0;

#logging current values into masterlist

while elapsedtime < 70:
    print(elapsedtime);
    print(mtrcurrent);
    print(lhtcurrent);
    mtrcurrent = motorcurrent();
    lhtcurrent = lightcurrent();
    elapsedtime = time.time() - starttime;
    if mtrcurrent > 100:
        masterlist.append([elapsedtime*100,mtrcurrent]);
    clear();
    
#delete extraneous values and errors in masterlist 
    
while iterate_one < len((masterlist)):
    tempmaster = masterlist[iterate_one][1];
    iterate_one += 1;
    iterate_two = iterate_one;
    while masterlist[iterate_two][1] == tempmaster and iterate_two <= len(masterlist):
        del masterlist[iterate_two];
        iterate_two += 1;
        
#setting up matplotlib        
    
print(masterlist);
fig, axs = plt.subplots(7);
axs[0].set_xlim(0,1000);
axs[1].set_xlim(1000,2000);
axs[2].set_xlim(2000,3000);
axs[3].set_xlim(3000,4000);
axs[4].set_xlim(4000,5000);
axs[5].set_xlim(5000,6000);
axs[6].set_xlim(6000,7000);

axs[0].set_ylim(0,500);
axs[1].set_ylim(0,500);
axs[2].set_ylim(0,500);
axs[3].set_ylim(0,500);
axs[4].set_ylim(0,500);
axs[5].set_ylim(0,500);
axs[6].set_ylim(0,500);

#more variable initialization

fig.suptitle('Energy Consumption per Day of Week');
mondaylist = [];
tuesdaylist = [];
wednesdaylist = [];
thursdaylist = [];
fridaylist = [];
saturdaylist = [];
sundaylist = [];

#separating masterlist into lists by day of week

for i in range(len(masterlist)):
    if masterlist[i][0] < 1000:
        mondaytemp = masterlist[i];
        mondaylist.append(mondaytemp);
    if masterlist[i][0] > 999 and masterlist[i][0] < 2000:
        tuesdaytemp = masterlist[i];
        tuesdaylist.append(tuesdaytemp);
    if masterlist[i][0] > 1999 and masterlist[i][0] < 3000:
        wednesdaytemp = masterlist[i];
        wednesdaylist.append(wednesdaytemp);
    if masterlist[i][0] > 2999 and masterlist[i][0] < 4000:
        thursdaytemp = masterlist[i];
        thursdaylist.append(thursdaytemp);
    if masterlist[i][0] > 3999 and masterlist[i][0] < 5000:
        fridaytemp = masterlist[i];
        fridaylist.append(fridaytemp);
    if masterlist[i][0] > 4999 and masterlist[i][0] < 6000:
        saturdaytemp = masterlist[i];
        saturdaylist.append(saturdaytemp);
    if masterlist[i][0] > 5999 and masterlist[i][0] < 7000:
        sundaytemp = masterlist[i];
        sundaylist.append(sundaytemp);

#convert python arrays into numpy arrays for use in KMeans

np.array(masterlist);
np.array(mondaylist);
np.array(tuesdaylist);
np.array(wednesdaylist);
np.array(thursdaylist);
np.array(fridaylist);
np.array(saturdaylist);
np.array(sundaylist);

#console logging

print("mondaylist: ",mondaylist);
print("tuesdaylist: ",tuesdaylist);
print("wednesdaylist: ",wednesdaylist);
print("thursdaylist: ",thursdaylist);
print("fridaylist: ",fridaylist);
print("saturdaylist: ",saturdaylist);
print("sundaylist: ",sundaylist);

#evaluation of lists by KMeans

kmonday = KMeans(n_clusters=2, random_state=0).fit(mondaylist);
print(kmonday.labels_);
print(kmonday.cluster_centers_);

ktuesday = KMeans(n_clusters=2, random_state=0).fit(tuesdaylist);
print(ktuesday.labels_);
print(ktuesday.cluster_centers_);

kwednesday = KMeans(n_clusters=2, random_state=0).fit(wednesdaylist);
print(kwednesday.labels_);
print(kwednesday.cluster_centers_);

kthursday = KMeans(n_clusters=2, random_state=0).fit(thursdaylist);
print(kthursday.labels_);
print(kthursday.cluster_centers_);

kfriday = KMeans(n_clusters=2, random_state=0).fit(fridaylist);
print(kfriday.labels_);
print(kfriday.cluster_centers_);

ksaturday = KMeans(n_clusters=2, random_state=0).fit(saturdaylist);
print(ksaturday.labels_);
print(ksaturday.cluster_centers_);

ksunday = KMeans(n_clusters=2, random_state=0).fit(sundaylist);
print(ksunday.labels_);
print(ksunday.cluster_centers_);

#logging values into matplotlib

for i in range(len(mondaylist)):
    axs[0].scatter(mondaylist[i][0],mondaylist[i][1]);
for i in range(len(tuesdaylist)):
    axs[1].scatter(tuesdaylist[i][0],tuesdaylist[i][1]);
for i in range(len(wednesdaylist)):
    axs[2].scatter(wednesdaylist[i][0],wednesdaylist[i][1]);
for i in range(len(thursdaylist)):
    axs[3].scatter(thursdaylist[i][0],thursdaylist[i][1]);
for i in range(len(fridaylist)):
    axs[4].scatter(fridaylist[i][0],fridaylist[i][1]);
for i in range(len(saturdaylist)):
    axs[5].scatter(saturdaylist[i][0],saturdaylist[i][1]);
for i in range(len(sundaylist)):
    axs[6].scatter(sundaylist[i][0],sundaylist[i][1]);    
    
plt.show();

#initializing gpio devices

dlcCharge = gpio.DigitalOutputDevice(17);
dlcDischarge = gpio.DigitalOutputDevice(23);
motor = gpio.DigitalOutputDevice(22);
led = gpio.DigitalOutputDevice(27);

starttime = time.time();
elapsedtime = 0;

#charging and discharging of supercapacitors based on the KMeans algorithm

while True:
    if elapsedtime  > 70:
        elapsedtime -= 70;
    if elapsedtime * 100 > kmonday.cluster_centers[0][0] - 2 or elapsedtime * 100 > kmonday.cluster_centers[1][0] - 2:
        dlcCharge.on();
    if elapsedtime * 100 > kmonday.cluster_centers[0][0] - 0.5 or elapsedtime * 100 > kmonday.cluster_centers[1][0] - 0.5:
        dlcCharge.off();
        dlcDischarge.on();
        sleep(1);
        dlcDischarge.off();
    if elapsedtime * 100 > ktuesday.cluster_centers[0][0] - 2 or elapsedtime * 100 > ktuesday.cluster_centers[1][0] - 2:
        dlcCharge.on();
    if elapsedtime * 100 > ktuesday.cluster_centers[0][0] - 0.5 or elapsedtime * 100 > ktuesday.cluster_centers[1][0] - 0.5:
        dlcCharge.off();
        dlcDischarge.on();
        sleep(1);
        dlcDischarge.off();
    if elapsedtime * 100 > kwednesday.cluster_centers[0][0] - 2 or elapsedtime * 100 > kwednesday.cluster_centers[1][0] - 2:
        dlcCharge.on();
    if elapsedtime * 100 > kwednesday.cluster_centers[0][0] - 0.5 or elapsedtime * 100 > kwednesday.cluster_centers[1][0] - 0.5:
        dlcCharge.off();
        dlcDischarge.on();
        sleep(1);
        dlcDischarge.off();
    if elapsedtime * 100 > kthursday.cluster_centers[0][0] - 2 or elapsedtime * 100 > kthursday.cluster_centers[1][0] - 2:
        dlcCharge.on();
    if elapsedtime * 100 > kthursday.cluster_centers[0][0] - 0.5 or elapsedtime * 100 > kthursday.cluster_centers[1][0] - 0.5:
        dlcCharge.off();
        dlcDischarge.on();
        sleep(1);
        dlcDischarge.off();
    if elapsedtime * 100 > kfriday.cluster_centers[0][0] - 2 or elapsedtime * 100 > kfriday.cluster_centers[1][0] - 2:
        dlcCharge.on();
    if elapsedtime * 100 > kfriday.cluster_centers[0][0] - 0.5 or elapsedtime * 100 > kfriday.cluster_centers[1][0] - 0.5:
        dlcCharge.off();
        dlcDischarge.on();
        sleep(1);
        dlcDischarge.off();
    if elapsedtime * 100 > ksaturday.cluster_centers[0][0] - 2 or elapsedtime * 100 > ksaturday.cluster_centers[1][0] - 2:
        dlcCharge.on();
    if elapsedtime * 100 > ksaturday.cluster_centers[0][0] - 0.5 or elapsedtime * 100 > ksaturday.cluster_centers[1][0] - 0.5:
        dlcCharge.off();
        dlcDischarge.on();
        sleep(1);
        dlcDischarge.off();
    if elapsedtime * 100 > ksunday.cluster_centers[0][0] - 2 or elapsedtime * 100 > ksunday.cluster_centers[1][0] - 2:
        dlcCharge.on();
    if elapsedtime * 100 > ksunday.cluster_centers[0][0] - 0.5 or elapsedtime * 100 > ksunday.cluster_centers[1][0] - 0.5:
        dlcCharge.off();
        dlcDischarge.on();
        sleep(1);
        dlcDischarge.off();
    
