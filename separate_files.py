#!/usr/bin/python3
import os
import pandas as pd
from os import path
import numpy as np
import datetime
from matplotlib.dates import date2num, MINUTES_PER_DAY, SEC_PER_DAY
from matplotlib.dates import DateFormatter
from datetime import datetime, timedelta


#read and write files
def rwf(filename, subdir,type):
    df = pd.read_csv(filename)
    df.drop_duplicates(inplace = True)
    df.dropna(inplace = True)
    wcsv = (filename.split("/")[5])
    wtype = (wcsv.split(".")[0])
    date_only = (wtype.split("_")[0])
    new_day = datetime.strptime(date_only, "%Y-%m-%d")
    modified_date = new_day + timedelta(days=1)
    next_day = datetime.strftime(modified_date, "%Y-%m-%d")
    filename1 = (next_day+"_"+(wtype.split("_")[1])+"."+(wcsv.split(".")[1]))
    abs_filepath = subdir + os.path.sep + filename1
    if path.exists(abs_filepath):
        df1 = pd.read_csv(abs_filepath)
        df1.drop_duplicates(inplace = True)
        df1.dropna(inplace = True)
        fnum2 = np.array(df.iloc[:,1]).astype(float)
        fnum1 = np.array(df["UTCTimeStamp"]).astype(float)
        fnum_nxt2 = np.array(df1.iloc[:,1]).astype(float)
        fnum_nxt1 = np.array(df1["UTCTimeStamp"]).astype(float)
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
        for idx in range(len(fnum_nxt1)):
            d = datetime.utcfromtimestamp(fnum_nxt1[idx])
            if d.day == modified_date.day:
                if d.hour>=0 and d.hour<8:
                    x_night.append(d)
                    fnum2_night.append(fnum_nxt2[idx])
        title = df.columns
        daytime = pd.DataFrame({"UTCTimeStamp": x_day, title[1]: fnum2_day}, columns = ["UTCTimeStamp", title[1]])
        nighttime = pd.DataFrame({"UTCTimeStamp": x_night, title[1]: fnum2_night}, columns = ["UTCTimeStamp", title[1]])
        daytime.name = date_only+"_"+(wtype.split("_")[1])+"_day."+(wcsv.split(".")[1])
        nighttime.name = date_only+"_"+(wtype.split("_")[1])+"_night."+(wcsv.split(".")[1])
        print (nighttime.name)
        new_filepath = subdir + os.path.sep + daytime.name
        new_filepath1 = subdir + os.path.sep + nighttime.name
        df.to_csv(new_filepath, index = False)
        df.to_csv(new_filepath1, index = False)

for subdir, dirs, files in os.walk("/home/agmfamily/Tutorial"):
    for filename in files:
        filepath = subdir + os.path.sep + filename
        if path.exists(filepath):
            for type in ['_BVP.csv', '_EDA.csv', '_TEMP.csv']:#filtering out ACC data
                if filepath.endswith(type):
                    print (subdir)
                    rwf(filepath, subdir,type)
