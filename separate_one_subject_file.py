#!/usr/local/bin/python3
import os
import pandas as pd
from os import path
import numpy as np
import datetime
from matplotlib.dates import date2num, MINUTES_PER_DAY, SEC_PER_DAY
from matplotlib.dates import DateFormatter
from datetime import datetime, timedelta

subjectid = input("Subject ID: ")

def cleanfile(filename):
    df = pd.read_csv(filename)
    df.drop_duplicates(inplace = True)
    df.dropna(inplace = True)
    return df

def getdate(filename):
    wcsv = (filename.split("/")[-1])
    wtype = (wcsv.split(".")[0])
    date_only = (wtype.split("_")[0])
    return date_only

#get nxt_date
def getnxtdate(date_only):
    new_day = datetime.strptime(date_only, "%Y-%m-%d")
    nxt_date = new_day + timedelta(days=1)
    nxt_day = datetime.strftime(nxt_date, "%Y-%m-%d")
    return nxt_day

#get nxt path and file
def getnxtfile(filename, date_only, subdir):
    nxt_day = getnxtdate(date_only)
    wcsv = (filename.split("/")[-1])
    wtype = (wcsv.split(".")[0])
    filename1 = (nxt_day+"_"+(wtype.split("_")[1])+"."+(wcsv.split(".")[1]))
    nxt_filepath = subdir + os.path.sep + filename1
    return nxt_filepath

#read and write files
def rwf(filename, subdir,type):
    time_day = []
    time_night = []
    sec_col_day = []
    sec_col_night = []

    df = cleanfile(filename)
    date_only = getdate(filename)
    sec_col = np.array(df.iloc[:,1]).astype(float)
    ts_cur_file = np.array(df["UTCTimeStamp"]).astype(float)
    for idx in range(len(ts_cur_file)):
        d = datetime.utcfromtimestamp(ts_cur_file[idx])
        if d.hour>=20:
            time_night.append(ts_cur_file[idx])
            sec_col_night.append(sec_col[idx])
        elif d.hour<20 and d.hour>=8:
            time_day.append(ts_cur_file[idx])
            sec_col_day.append(sec_col[idx])

    nxt_filepath = getnxtfile(filename, date_only, subdir)
    if path.exists(nxt_filepath):
        nxt_day_df = cleanfile(nxt_filepath)
        sec_col_nxt_day = np.array(nxt_day_df.iloc[:,1]).astype(float)
        ts_nxt_day = np.array(nxt_day_df["UTCTimeStamp"]).astype(float)

        nxt_date = getnxtdate(date_only)
        new_day = datetime.strptime(nxt_date, "%Y-%m-%d")

        for idx in range(len(ts_nxt_day)):
            d = datetime.utcfromtimestamp(ts_nxt_day[idx])
            if d.day == new_day.day:
                if d.hour>=0 and d.hour<8:
                    time_night.append(ts_nxt_day[idx])
                    sec_col_night.append(sec_col_nxt_day[idx])


    title = df.columns
    daytime = pd.DataFrame({"UTCTimeStamp": time_day, title[1]: sec_col_day}, columns = ["UTCTimeStamp", title[1]])
    nighttime = pd.DataFrame({"UTCTimeStamp": time_night, title[1]: sec_col_night}, columns = ["UTCTimeStamp", title[1]])
    wcsv = (filename.split("/")[-1])
    wtype = (wcsv.split(".")[0])
    daytime.name = (date_only+"_"+(wtype.split("_")[1])+"_day.csv")
    nighttime.name = (date_only+"_"+(wtype.split("_")[1])+"_night.csv")

    new_day_file = subdir + os.path.sep + daytime.name
    new_night_file = subdir + os.path.sep + nighttime.name
    daytime.to_csv(new_day_file, index = False)
    nighttime.to_csv(new_night_file, index = False)
    print (daytime.name)



for subdir, dirs, files in os.walk(os.getcwd()+"/"+subjectid):
    for filename in files:
        filepath = subdir + os.path.sep + filename
        if path.exists(filepath):
            for type in ['_BVP.csv', '_EDA.csv', '_TEMP.csv']:#filtering out ACC data
                if filepath.endswith(type):
                    rwf(filepath, subdir,type)
