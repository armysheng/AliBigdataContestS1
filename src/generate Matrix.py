features={'clic_times':0,'buy_times':0,'favor_times':0, \
'Addcart_times':0,'total_dates':0,'mean_date':0,'score_day':-1.0,\
'score_week':-1.0,'user_active':-1,'date':-1,'days':-1,'Brand_features':-1,'label':-1}
# print features
total_times=0
rate={'0':0.2,'1':1,'2':0.5,'3':0.5}
rate_week={'0':0.2,'1':1,'2':0.5,'3':0.5}

###########generate activeuser #####
active_user={}
f_active_user=open("User_features.csv")
entrys=f_active_user.readlines()
entrys.sort(key=lambda x: x.split(","))
for index,entry in enumerate(entrys):
    uid,clic_per_buy,clic_times,buy_times=entry.strip().split(',')
    active_user[uid]=[float(clic_per_buy),int(clic_times),int(buy_times)]


###########generate Hotbrand #####
Hotbrand={}
f_Hotbrand=open("Brand_features.csv")
entrys=f_Hotbrand.readlines()
entrys.sort(key=lambda x: x.split(",")[1])
for index,entry in enumerate(entrys):
    bid,clic_per_buy,clic_times,buy_times=entry.strip().split(',')
    Hotbrand[bid]=[float(clic_per_buy),int(clic_times),int(buy_times)]

##initial features
def iniitialFeatures(uid,bid,act_type,dates):
    features['clic_times']=0
    features['buy_times']=0
    features['favor_times']=0
    features['Addcart_times']=0
    features['days']=1
    if act_type=='0':
        features['clic_times']=1
        # features['label']=0
    elif act_type=='1':
        features['buy_times']=1
        # features['label']=1
    elif act_type=='2':
        features['favor_times']=1
        # features['label']=0
    elif act_type=='3':
        features['Addcart_times']=1
        # features['label']=0   
    features['score_day']=((float(dates)+1)/123)*float(rate[act_type])
    features['score_week']=((int(dates)+1)/7+1)*float(rate_week[act_type])
    total_times=features['clic_times']+features['buy_times']+features['favor_times']+features['Addcart_times']
    features['total_dates']=int(dates)
    features['mean_date']=int(dates)
    features['date']=int(dates)
    if not uid =='99999999999999999':
        features['User_features']=active_user[uid]
    if not bid =='999999':
        features['Brand_features']=Hotbrand[bid]


##extract features from lines
def extractFeatures(uid,bid,act_type,dates):
    # uid,bid,act_type,date = entry.strip().split(",")
    if act_type=='0':
        features['clic_times']+=1
        # features['label']=0
    elif act_type=='1':
        features['buy_times']+=1
        # features['label']=+1
    elif act_type=='2':
        features['favor_times']+=1
        # features['label']=0
    elif act_type=='3':
        features['Addcart_times']+=1
        # features['label']=0
    features['score_day']+=((float(dates)+1)/123)*float(rate[act_type])
    features['score_week']=((int(dates)+1)/7+1)*float(rate_week[act_type])   
    total_times=features['clic_times']+features['buy_times']+features['favor_times']+features['Addcart_times']
    features['total_dates']+=int(dates)
    features['mean_date']=features.get('total_dates') / total_times
    features['User_features']=active_user[uid]
    features['Brand_features']=Hotbrand[bid]
    if not date==features['date']:
        features['days']+=1
    features['date']=date        



#####generate buy dict of 4th month for label marking of the trainning dataset
test=open("t_validation.csv")
label_temp=open("label_temp.csv",'w')
label_4th_month={}
entrys=test.readlines()
entrys.sort(key=lambda x: x.split(","))
for index,entry in enumerate(entrys):
    uid,bid,act_type,date = entry.strip().split(",")
    if act_type=='1':
        label_4th_month[uid+','+bid]=1
        label_temp.write(uid+','+bid+','+'1\n')  

#####generate buy dict of 3rd month for label marking of the trainning dataset
test=open("t_3rd_month.csv")
label_3rd_temp=open("label_3rd_temp.csv",'w')
label_3rd_month={}
entrys=test.readlines()
entrys.sort(key=lambda x: x.split(","))
for index,entry in enumerate(entrys):
    uid,bid,act_type,date = entry.strip().split(",")
    if act_type=='1':
        label_3rd_month[uid+','+bid]=1
        label_3rd_temp.write(uid+','+bid+','+'1\n')                   

############main body#################
path=os.path.abspath(os.path.dirname(os.path.dirname(__file__)))+'\\files'  
os.chdir(path)  ## change dir to '~/files'
train=open("t_all.csv")
# score_week=open('score_week.csv','w')
Matrix = open("Matrix.csv","w")
# Matrix.write(','.join(['uid','Bid','clic_times','buy_times','favor_times','Addcart_times','mean_date','score_day','score_week','User_features','days','Brand_features','label'])+'\n')
entrys=train.readlines()
entrys.sort(key=lambda x: x.split(","))
for index,entry in enumerate(entrys):
    uid,bid,act_type,date = entry.strip().split(",")
    if index==0:
        cur_uid=uid
        cur_bid=bid
        # result=((float(date)+1)/123)*float(rate[act_type])
        iniitialFeatures(uid,bid,act_type,date)
        features['label']=(1 if uid+','+bid in label_4th_month else 0 )
        # features['label']=(1 if uid+','+bid in label_3rd_month else 0 )       
    elif cur_uid==uid:
        if cur_bid==bid:
            extractFeatures(uid,bid,act_type, date)
        else:
            if (not features['User_features'][2]==0)&(not features['Brand_features'][2]==0):
                Matrix.write(cur_uid+','+cur_bid+','+str(features.get('clic_times'))+',' \
                    +str(features.get('buy_times'))+','+str(features.get('favor_times'))+',' \
                    +str(features.get('Addcart_times'))+','+str(features.get('mean_date'))+',' \
                    +str(features.get('score_day'))+','+str(features.get('score_week'))+','\
                    +str(features.get('User_features')).strip('[]')+','+str(features.get('days'))+','\
                    +str(features.get('Brand_features')).strip('[]')+','+str(features.get('label'))+'\n')
            cur_bid=bid
            iniitialFeatures(uid,bid,act_type,date)
            features['label']=(1 if uid+','+bid in label_4th_month else 0 )
            # features['label']=(1 if uid+','+bid in label_3rd_month else 0 )       
    else:
        if (not features['User_features'][2]==0)&(not features['Brand_features'][2]==0):
            Matrix.write(cur_uid+','+cur_bid+','+str(features.get('clic_times'))+',' \
                +str(features.get('buy_times'))+','+str(features.get('favor_times'))+',' \
                +str(features.get('Addcart_times'))+','+str(features.get('mean_date'))+',' \
                +str(features.get('score_day'))+','+str(features.get('score_week'))+','\
                +str(features.get('User_features')).strip('[ ]')+','+str(features.get('days'))+','\
                +str(features.get('Brand_features')).strip('[ ]')+','+str(features.get('label'))+'\n')
        iniitialFeatures(uid,bid,act_type,date)
        features['label']=(1 if uid+','+bid in label_4th_month else 0 )  
        # features['label']=(1 if uid+','+bid in label_3rd_month else 0 )       
        cur_uid=uid
        cur_bid=bid
# print features        
Matrix.close()    
