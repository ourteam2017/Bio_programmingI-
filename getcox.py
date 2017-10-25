#this is the debugged version of getting the cox-score 
import pandas as pd
import numpy as np
from scipy import stats
import matplotlib.pyplot as plt


def h(inputdata,n_bins):
    n_bins=int(n_bins)
#1. get inputdata
#2. get event time
    event_time=inputdata[inputdata['death']==1]['event_free_survival_time_days'].sort_values().unique()
    cols = ['V{0}'.format(element) for element in range(1,21149)] #has 21148 genes generate the genenames
    
    ls=[]
    for i in event_time:
        m=(inputdata['event_free_survival_time_days']>i).sum()
        d=(inputdata['event_free_survival_time_days']==i).sum()
        who=inputdata.index[inputdata['event_free_survival_time_days']==i].tolist()
        ls.append([m,d,who])
        
    #the index of at risk set 
    indx=[]
    for i in range(len(event_time)):
        indx.append(inputdata[inputdata['event_free_survival_time_days']>event_time[i]].index.values.tolist())
 

 #get Xik
    sum_gene_val=[]
    for i in range(len(event_time)): 
        sum_gene_val.append(inputdata.loc[indx[i],cols].sum())
        
#get Xik_bar
    ser1=[item[0] for item in ls]
    avg_gene_val=[]
    for i in range(len(sum_gene_val)):
        avg_gene_val.append(sum_gene_val[i]/ser1[i])
        
        
#get X*ik
    subj_time=[item[2] for item in ls]
    subj_gene_val=[]

    for i in range(len(event_time)):    
        subj_gene_val.append(inputdata.loc[subj_time[i],cols].sum())     
        
        
 #get dk*Xik_bar
    davg_gene_val=[]
    ser2=[item[1] for item in ls]
    for i in range(len(ser2)):
        davg_gene_val.append(avg_gene_val[i]*ser2[i])
        
 #get ri
    r=pd.DataFrame(0,index=cols,columns=np.array(range(len(event_time))))
    for i in range(len(ser2)):
        r.loc[:,i]=(subj_gene_val[i]-davg_gene_val[i])
        
    ri=r.sum(axis=1)
    
 #get Si
    Tempi=[]
    for i in range(len(event_time)): 
        Tempi.append(inputdata.loc[indx[i],cols])
    series_avg_gene_val=pd.Series(avg_gene_val[0])
    S_gene_val=pd.DataFrame(0,index=cols,columns=np.array(range(len(event_time))))
    for i in range(len(event_time)):
        S_gene_val.loc[:,i]=(Tempi[i].sub(series_avg_gene_val)**2).sum()*ser2[i]/ser1[i]
        
    si=S_gene_val.sum(axis=1)**(1/2)
    s0=si.median()
 
 #get hi   
    hi=ri.div(si+s0)
    hi=np.absolute(hi)
    
    plt.hist(hi,bins=n_bins)
    plt.title("Histogram of absolute value of cox-score")
    plt.show()


  
    return hi






