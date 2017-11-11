# adjust clinical_gene.csv path.
import pandas as pd

# Add this code to change the columns names to probes_names
with open('clinical_gene.csv', 'r') as file:
    wrong_col_names = file.readline().split('|')
    gene_names = file.readline().split('|')
    third_line = file.readline().split('|')
    probes_names = file.readline().split('|')

# Create a dictionary with old columns as key and the probes names as the values.
col_dictionary = dict(zip(wrong_col_names[13:], probes_names[13:]))

# Create a dictionary Key = probe ; value = gene
probe_gene_dic = dict(zip(probes_names[13:], gene_names[13:]))

del third_line, probes_names, file, gene_names


# Some columns are float because pandas integer cant represent NA values
clinical_gene_df = pd.read_csv('clinical_gene.csv',
                            sep = '|',
                            skiprows = 4,
                            header = None,
                            names = wrong_col_names)
                            
# Change names from V1 to probe names using a dictionary
clinical_gene_df.rename(columns= col_dictionary, inplace=True)

# Drop columns not required for the analysis
# 1 = cel_file ; 2 = gender ; 5 = vital_status ; 6 = snc_teste_involve ; 7 = latino_black
# 12 = B
clinical_gene_df.drop(clinical_gene_df.columns[[1,2,5,6,7,12]], axis=1, inplace=True)



