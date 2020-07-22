#!/usr/bin/python3
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from os import path
import datetime
from matplotlib.dates import date2num, MINUTES_PER_DAY, SEC_PER_DAY
from matplotlib.dates import DateFormatter
from datetime import datetime, timedelta


subjectid = input("Subject ID: ")
fname1 = input("Date: ")
day_or_night = input("day or night: ")
#read and clean a file
def rcf(type,fname, day_or_night):
    filepath1 = "/home/agmfamily/Tutorial/"+subjectid+"/"+fname+"_"+type+"_"+day_or_night+".csv"
    if path.exists(filepath1):
        df = pd.read_csv(filepath1)
        df.drop_duplicates(inplace = True)
        df.dropna(inplace = True)
    else:
        print(fname, " does not exist")
        exit()
    return df
titles = [fname1+" BVP", fname1+" EDA", fname1+" TEMP"]
fig, ax1 = plt.subplots(3, sharex = True)
i = 0
for item in ['BVP', 'EDA', 'TEMP']:
    df = rcf(item, fname1, day_or_night)
    fnum2 = np.array(df.iloc[:,1]).astype(float)
    fnum1 = np.array(df["UTCTimeStamp"]).astype(float)
    if fnum1[-1]-fnum1[0]>3600:
        time = []
        data = []
#converting UTC time into HH/MM/SS
        for idx in range(len(fnum1)):
            d = datetime.utcfromtimestamp(fnum1[idx])
            if day_or_night == "day":
                if d.hour<20 and d.hour>=8:
                    time.append(d)
                    data.append(fnum2[idx])
            #    ax1[i].plot(time, data)
            #    plt.xlabel("Time")
            #    ax1[i].set_title(titles[i]+"_"+day_or_night)
            #    ax1[i].xaxis.set_major_formatter(DateFormatter('%d:%H:%M:%S'))
            #    plt.setp(ax1[i].get_xticklabels(), rotation=30, ha="right")
            elif day_or_night == "night":
                if d.hour>=20 and d.hour<8:
                    time.append(d)
                    data.append(fnum2[idx])
        ax1[i].plot(time, data)
        plt.xlabel("Time")
        ax1[i].set_title(titles[i]+"_"+day_or_night)
        ax1[i].xaxis.set_major_formatter(DateFormatter('%d:%H:%M:%S'))
        plt.setp(ax1[i].get_xticklabels(), rotation=30, ha="right")
    else:
        print ("ERROR: more data expected for ", item)
        break
    i = i+1
    print(i)
plt.suptitle("Subject "+ subjectid)
plt.show()
