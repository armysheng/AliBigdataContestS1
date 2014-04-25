## generates user features :click times,buy times and buy_per_click
## more features should be extracted and appended to user features.
import os

User_features={'clic_times':-1,'buy_times':-1,'buy_per_clic':-1}
user={}

def init_features(act_type):
    User_features['buy_times']=0
    User_features['clic_times']=0
    if act_type=='0':
        User_features['clic_times']=1
    elif act_type=='1':
        User_features['buy_times']=1
    else:
        pass
    User_features['buy_per_clic']=0

def ext_features(act_type):
    if act_type=='0':
        User_features['clic_times']+=1
    elif act_type=='1':
        User_features['buy_times']+=1
    else:
        pass        
    # User_features['buy_per_clic']=0   

###########generate user features############## 


path=os.path.abspath(os.path.dirname(os.path.dirname(__file__)))+'\\files'  
os.chdir(path)  ## change dir to '~/files'
t_all=open("t_all.csv")
t_User_features=open("User_features.csv",'w')
entrys=t_all.readlines()
entrys.sort(key=lambda x: x.split(","))
for index,entry in enumerate(entrys):
    uid,bid,act_type,date = entry.strip().split(",")
    if index==0:
        init_features(act_type)
        user[uid]=User_features
        cur_uid=uid
    elif uid in user:
        ext_features(act_type)
    else :
        if not User_features['clic_times']==0:
            User_features['buy_per_clic']=float(User_features['buy_times'])/(User_features['clic_times'])
        else:
            if User_features['buy_times']>0 :
                User_features['buy_per_clic']=1       #mark buy without click user as 1
            else :User_features['buy_per_clic']=-1    #mark other action without click as -1        
        t_User_features.write(cur_uid+','+str(user[cur_uid].values()).strip('[ ]')+'\n')
        init_features(act_type)
        user[uid]=User_features
        cur_uid=uid


