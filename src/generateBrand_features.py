## generates brand features :click times,buy times and buy_per_click
## more features should be extracted and appended to brand features.
import os

Brand_features={'clic_times':0,'buy_times':0,'buy_per_clic':0}
Brand={}
def init_features(act_type):
	# Brand_features={'clic_times':0,'buy_times':0,'buy_per_clic':0}
	Brand_features['clic_times']=0
	Brand_features['buy_times']=0
	Brand_features['buy_per_clic']=0
	if act_type=='0':
		Brand_features['clic_times']=1
	elif act_type=='1':
		Brand_features['buy_times']=1
	else:
		pass

def ext_features(act_type):
	if act_type=='0':
		Brand_features['clic_times']+=1
	elif act_type=='1':
		Brand_features['buy_times']+=1
	else:
		pass		
	# Brand_features['buy_per_clic']=0	


#####generate Brand features######

path=os.path.abspath(os.path.dirname(os.path.dirname(__file__)))+'\\files'  
os.chdir(path)  ## change dir to '~/files'
t_all=open("t_all.csv")
t_Brand_features=open("Brand_features.csv",'w')
entrys=t_all.readlines()
entrys.sort(key=lambda x: x.split(",")[1])
for index,entry in enumerate(entrys):
    uid,bid,act_type,date = entry.strip().split(",")
    if index==0:
    	init_features(act_type)
    	Brand[bid]=Brand_features
    	cur_bid=bid
    elif cur_bid==bid:
    	ext_features(act_type)
    else :
    	if not Brand_features['clic_times']==0:
    		Brand_features['buy_per_clic']=float(Brand_features['buy_times'])/((Brand_features['clic_times']))
    	else:
    		if Brand_features['buy_times']>0 :
    			Brand_features['buy_per_clic']=1	
    		else :
	   			Brand_features['buy_per_clic']=-1	
    	t_Brand_features.write(cur_bid+','+str(Brand[cur_bid].values()).strip('[]')+'\n')
    	init_features(act_type)
    	Brand[bid]=Brand_features
    	cur_bid=bid


