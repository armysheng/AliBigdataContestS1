# segment original data file "t_alibaba_data.csv"
# to training set and test set, using parameter SEPERATEDAY
# original code by oilbeater.
#

import os
from datetime import *

########preprocess rawdate###############

def parse_date(raw_date):
    # entry_date = raw_date.decode("gbk")
    entry_date = raw_date
    month = int(entry_date[0])
    if len(entry_date) == 8:
        day = 10 * int(entry_date[3]) + int(entry_date[4])
    else:
        day = int(entry_date[3])
    return 2013, month, day

# save orignal data to t_all and seprate it to  t_train and t_validation

def split_file(raw_file, seperate_day, begin_date): 
    t_train=open("t_train_temp.csv",'w')
    t_validation=open("t_validation_temp.csv",'w')
    t_all=open("t_all_temp.csv",'w')
    raw_file.readline()
    for line in raw_file.readlines():
        entry = line.split(",")
        entry_date = date(*parse_date(entry[3]))
        date_delta = (entry_date - begin_date).days
        if date_delta <=(seperate_day-begin_date).days:
            t_train.write(",".join(entry[:3]) + "," + str(date_delta) + "\n")
        else:
            t_validation.write(",".join(entry[:3]) + "," + str(date_delta) + "\n")
        t_all.write(",".join(entry[:3]) + "," + str(date_delta) + "\n")
    t_all.close()
    t_validation.close()
    t_train.close()
    originfile=open("t_train_temp.csv")
    generate_sortedfile(originfile,"t_train.csv")
    originfile=open("t_validation_temp.csv")
    generate_sortedfile(originfile,"t_validation.csv")
    originfile=open("t_all_temp.csv")
    generate_sortedfile(originfile,"t_all.csv")

#sort file accroding to entrys in line
def generate_sortedfile(originfile,filename):
    entrys = originfile.readlines()
    entrys.sort(key=lambda x: x.split(","))
    sortedfile = open(filename, "w")
    for i in entrys:
        sortedfile.write(i)
    sortedfile.close()

#############data prepocessing ###############

SEPERATEDAY =date(2013, 7, 15)
BEGINDAY = date(2013, 4, 15)
path=os.path.abspath(os.path.dirname(os.path.dirname(__file__)))+'\\files'  
os.chdir(path)  ## change dir to '~/files'
raw_file = open("t_alibaba_data.csv")
split_file(raw_file, SEPERATEDAY, BEGINDAY)
raw_file.close()
