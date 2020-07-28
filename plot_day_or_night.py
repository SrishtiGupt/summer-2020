#!/usr/local/bin/python3
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os
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
def rcf(subjectid,type,fname,day_or_night):
    filepath1 = os.getcwd()+"/"+subjectid+"/"+fname+"_"+type+"_"+day_or_night+".csv"
    if path.exists(filepath1):
        df = pd.read_csv(filepath1)
        df.drop_duplicates(inplace = True)
        df.dropna(inplace = True)
    else:
        print(fname, " does not exist")
        exit()
    return df

i = 0
titles = [fname1+" BVP",fname1+" EDA",fname1+" TEMP"]
fig, ax1 = plt.subplots(3, sharex = True)
for item in ['BVP', 'EDA', 'TEMP']:
    df = rcf(subjectid,item, fname1,day_or_night)
    fnum2 = np.array(df.iloc[:,1]).astype(float)
    fnum1 = np.array(df["UTCTimeStamp"]).astype(float)
    time = []
    data = []
    for idx in range(len(fnum1)):
        d= datetime.utcfromtimestamp(fnum1[idx])
        time.append(d)
        data.append(fnum2[idx])
    ax1[i].plot(time,data)
    plt.xlabel("Time")
    ax1[i].set_title(titles[i]+" "+day_or_night)
    ax1[i].xaxis.set_major_formatter(DateFormatter('%d:%H:%M:%S'))
    plt.setp(ax1[i].get_xticklabels(), rotation=30, ha="right")
    print (item + " plotted")
    i=i+1
plt.suptitle("Subject "+ subjectid)
plt.show()
