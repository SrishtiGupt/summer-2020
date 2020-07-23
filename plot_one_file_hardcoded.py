#!/usr/local/bin/python3
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from os import path
import datetime
from matplotlib.dates import date2num, MINUTES_PER_DAY, SEC_PER_DAY
from matplotlib.dates import DateFormatter
from datetime import datetime, timedelta


#subjectid = #input("Subject ID: ")
fname1 = "2018-08-24"#input("Date: ")
#day_or_night = #input("Day or Night: ")
next_day = datetime.strptime(fname1, "%Y-%m-%d")
modified_date = next_day + timedelta(days=1)
fname2 = datetime.strftime(modified_date, "%Y-%m-%d")#month+"-"+next_day+"-"+year
#read and clean a file
def rcf(type,fname):
    filepath1 = "/Users/srishtigupta/Documents/summer2020/20/2018-08-24_BVP_day.csv"#+fname+"_"+type+"_"+day_or_night+".csv"
    print (filepath1)
    if path.exists(filepath1):
        df = pd.read_csv(filepath1)
        df.drop_duplicates(inplace = True)
        df.dropna(inplace = True)
    else:
        print(fname, " does not exist")
        exit()
    return df


titles = [fname1+" BVP"]
fig, ax1 = plt.subplots(1, sharex = True)
for item in ['BVP']:
    df = rcf(item, fname1)
    print("got_df")
    fnum2 = np.array(df.iloc[:,1]).astype(float)
    fnum1 = np.array(df["UTCTimeStamp"]).astype(float)
    time = []
    data = []
    for idx in range(len(fnum1)):
        d= datetime.utcfromtimestamp(fnum1[idx])
        time.append(d)
        data.append(fnum2[idx])
    ax1.plot(time, data)
    plt.xlabel("Time")
    ax1.xaxis.set_major_formatter(DateFormatter('%d:%H:%M:%S'))
    plt.setp(ax1.get_xticklabels(), rotation=30, ha="right")
plt.show()
