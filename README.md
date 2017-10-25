# Programming_I_Leukemia_analysis
## Course project bioinformatics programming I

### Files description
  * `read_data.py` is for read in data;
  * `getcox.py` is to calculate the cox-score of each gene when the dataset is given; also report the histogram of the cox-scores of genes; 
  * `f.py` will get the cox-regression result in the test dataset, while the PCA model is built on train dataset with the qualified genes; those genes have cox-score > or equal than the given threshold
  * `change_col_names` created a dictionary using V columns names as key and probes names as values.
  * `sampling_the_data.py` will get the balanced 5 train/test folds based on key feature: MRD day 29; Age; WBC at diagnosis.
  * `1_gene_expression.md` testing R Markdown
  * `project_notebook.ipynb` jupyter notebook showing the the read in dataframe and the cox-score histogram based on the 207 patients.
  * `get_5_testfolds.ipynb` jupyter notebook showing how to do stratified resampling to get balanced 5 train/test datasets. 
