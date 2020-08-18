#!/usr/local/bin/python3
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os
from os import path
import heartpy as hp
import datetime
from matplotlib.dates import date2num, MINUTES_PER_DAY, SEC_PER_DAY
from matplotlib.dates import DateFormatter
from datetime import datetime, timedelta

subjectid = "20"#input("Subject ID: )
#year month day
ymd = input("Date: ")

def rcf(subjectid,ymd):
    filepath1 = os.getcwd()+"/"+subjectid+"/"+ymd+"_BVP_night.csv"
    if path.exists(filepath1):
        df = pd.read_csv(filepath1)
        df.drop_duplicates(inplace = True)
        df.dropna(inplace = True)
    else:
        print(ymd, "_BVP_night.csv does not exist")
        exit()
    return df

i = 0
titles = ["Subject " + subjectid+ "bpm","Subject " + subjectid+ "rmssd"]
fig, ax = plt.subplots(2, sharex = True)


date = []
bpm = []
rmssd = []
df = rcf(subjectid, ymd)
time = np.array(df["UTCTimeStamp"]).astype(float)
ppgdata = np.array(df["PhotoplethysmographReading"]).astype(float)


if len(ppgdata)>15:
    datapt_per_night = 240*60*12
    cur_duration = 0
    time_duration = 120
    while cur_duration < datapt_per_night:
        filtered = hp.filtering.filter_signal(ppgdata[cur_duration:cur_duration+240], cutoff = [0.2,5], sample_rate = 64.0, order=2, filtertype='bandpass')
        working_data, measures = hp.process(filtered, 64.0)
        rmssd.append(measures['bpm'])
        bpm.append(measures['rmssd'])
        d = datetime.utcfromtimestamp(time[time_duration])
        date.append(d)
        cur_duration += 240
        time_duration += 240
else:
    print("more data expected")

ax[i].plot(date,bpm)
ax[i+1].plot(date,rmssd)
plt.xlabel("Date")
ax[i].set_title("Subject " + subjectid+ " bpm")
ax[i+1].set_title("Subject " + subjectid+ " rmssd")
ax[i].set_ylabel("BPM")
ax[i+1].set_ylabel("RMSSD")
plt.setp(ax[i].get_xticklabels(), rotation=30, ha="right")
plt.setp(ax[i+1].get_xticklabels(), rotation=30, ha="right")
plt.suptitle("Subject "+ subjectid)
plt.show()
