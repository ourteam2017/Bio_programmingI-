1. #we need to see the cross-table of 'Age at Diagnosis in years', 'MRD Day 29','WBC at Diagnosis'
print(pd.crosstab(merged_df['MRD Day 29'],merged_df['WBC at Diagnosis']))
print(pd.crosstab(merged_df['MRD Day 29'],merged_df['Age at Diagnosis in years']))

#see the summary of the three features, because later on we need to use the three features 
#to do stratified random sampling 
print(merged_df['WBC at Diagnosis'].value_counts())
print(merged_df['MRD Day 29'].value_counts())
print(merged_df['Age at Diagnosis in years'].value_counts())


#from here we need to set 8 stratum 
#strata 1  (Age, WBC, MRD)=(0,0,0)
#strata 2  (Age, WBC, MRD)=(0,0,1)
#strata 3  (Age, WBC, MRD)=(0,1,0)
#strata 4  (Age, WBC, MRD)=(0,1,1)
#strata 5  (Age, WBC, MRD)=(1,0,0)
#strata 6  (Age, WBC, MRD)=(1,0,1)
#strata 7  (Age, WBC, MRD)=(1,1,0)
#strata 8  (Age, WBC, MRD)=(1,1,1)

2. #the strata size: 
for i in range(2):
    for j in range(2):
        for k in range(2):
            print('strata(mrd={MRD29},wbc={WBC},age={AGE}):n={count}'.format(MRD29=i,WBC=j,AGE=k,count=len(merged_df[(merged_df['MRD Day 29']==i)&(merged_df['WBC at Diagnosis']==j)&(merged_df['Age at Diagnosis in years']==k)])))

#output in python : 
#strata(mrd=0,wbc=0,age=0):n=4
#strata(mrd=0,wbc=0,age=1):n=14
#strata(mrd=0,wbc=1,age=0):n=47
#strata(mrd=0,wbc=1,age=1):n=60
#strata(mrd=1,wbc=0,age=0):n=0
#strata(mrd=1,wbc=0,age=1):n=7
#strata(mrd=1,wbc=1,age=0):n=24
#strata(mrd=1,wbc=1,age=1):n=51
            

3. # get the number in each strata in count_list; get the patient id (the row index in merged_df: range from 0 to 206) in each strata    
# key features for balancing: 'MRD 29 day',  'WBC at Diagnosis', 'Age at Diagnosis in years'
  
count_list=[]
id_list=[]

for i in range(2):
    for j in range(2):
        for k in range(2):
            count_list.append(len(merged_df[(merged_df['MRD Day 29']==i)&(merged_df['WBC at Diagnosis']==j)&(merged_df['Age at Diagnosis in years']==k)]))
            id_list.append(merged_df[(merged_df['MRD Day 29']==i)&(merged_df['WBC at Diagnosis']==j)&(merged_df['Age at Diagnosis in years']==k)].index.tolist())
            
print(count_list)
print(id_list)


4. # we will do the stratified random sampling by sampling_the_data.py and map the sample id to the patient id to get blanced test and train dataset

            
            