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
day_or_night = input("Day or Night: ")
next_day = datetime.strptime(fname1, "%Y-%m-%d")
modified_date = next_day + timedelta(days=1)
fname2 = datetime.strftime(modified_date, "%Y-%m-%d")#month+"-"+next_day+"-"+year
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
titles = [fname1+" BVP", fname1+" BVP", fname1+" EDA", fname1+" EDA", fname1+" TEMP", fname1+" TEMP" ]
fig, ax1 = plt.subplots(6, sharex = True)
i = 0
for item in ['BVP', 'EDA', 'TEMP']:
    df = rcf(item, fname1, day_or_night)
    df1 = rcf(item, fname2, day_or_night)
    fnum2 = np.array(df.iloc[:,1]).astype(float)
    fnum1 = np.array(df["UTCTimeStamp"]).astype(float)
    fnum_nxt2 = np.array(df1.iloc[:,1]).astype(float)
    fnum_nxt1 = np.array(df1["UTCTimeStamp"]).astype(float)
    if fnum1[-1]-fnum1[0]>3600:
        x_day = []
        x_night = []
        fnum2_day = []
        fnum2_night = []
#converting UTC time into HH/MM/SS
        for idx in range(len(fnum1)):
            d = datetime.utcfromtimestamp(fnum1[idx])
            if d.hour>=20:
                x_night.append(d)
                fnum2_night.append(fnum2[idx])
            elif d.hour<20 and d.hour>=8:
                x_day.append(d)
                fnum2_day.append(fnum2[idx])
                x_night.append(d)
                fnum2_night.append(np.NaN)
        fnum2_day.append(np.NaN)
        fnum2_night.append(np.NaN)
        x_day.append(x_day[-1])
        x_night.append(x_night[-1])
        for idx in range(len(fnum_nxt1)):
            d = datetime.utcfromtimestamp(fnum_nxt1[idx])
            if d.day == modified_date.day:
                if d.hour>=0 and d.hour<8:
                    x_night.append(d)
                    fnum2_night.append(fnum_nxt2[idx])
        fnum2_night.append(np.NaN)
        x_night.append(x_night[-1])
        ax1[i].plot(x_day, fnum2_day)
        ax1[i+1].plot(x_night, fnum2_night)
        plt.xlabel("Time")
        ax1[i].set_title(titles[i]+"_day")
        ax1[i+1].set_title(titles[i]+"_night")
        ax1[i].xaxis.set_major_formatter(DateFormatter('%d:%H:%M:%S'))
        ax1[i+1].xaxis.set_major_formatter(DateFormatter('%d:%H:%M:%S'))
        plt.setp(ax1[i].get_xticklabels(), rotation=30, ha="right")
        plt.setp(ax1[i+1].get_xticklabels(), rotation=30, ha="right")
        i = i+2
    else:
        print ("ERROR: more data expected for ", item)
        break
plt.suptitle("Subject "+ subjectid)
plt.show()
