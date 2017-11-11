#install.packages('matrixStats')
#source("http://bioconductor.org/biocLite.R")
#biocLite()
#biocLite("affy")
#biocLite("limma")
#biocLite("hgu133plus2.db")
#biocLite("annotate")
#biocLite("genefilter")
#install.packages("purrr")

require(data.table)
require(affy)
require(hgu133plus2.db)
require(annotate)
require(purrr)
require(genefilter)

#this will read in all the *.CEL files in the working directory 
affydata <- ReadAffy()
# Normalization
gene_expr_rma <- rma(affydata)

### Filter out probes with features exhibiting little variation, or a consistently low signal, across samples
gene_expr_filtered <-nsFilter(gene_expr_rma, require.extrez = F, remove.dupEntrez = F)


# Convert to data frame gene expresion rma data
dt_gene <- data.frame(exprs(gene_expr_filtered$eset))

# Look for gene expresion names
probe_names <- data.table(probe_names = row.names(dt_gene), A = 1:nrow(dt_gene))

gene_names <- data.table(gene_name = getSYMBOL(probe_names[, probe_names], "hgu133plus2"), 
                         A = 1:nrow(dt_gene))

probe_gene_names <- gene_names[probe_names, on = 'A']

# Number of duplicated genes
temp <- probe_gene_names[, .N, by = gene_name] %>%
  setorder(., -N)
temp

# Merge names with gene expression data
setDT(dt_gene)
dt_gene[, A := 1:.N]
dt_gene_names <- probe_gene_names[dt_gene, on = 'A' ]

# Melt DT
long_dt_gene_name<- melt(dt_gene_names, id.vars = c('gene_name', 'A', 'probe_names'),
                          variable.name = 'patient',
                          value.name = 'gene_expression')

# Calculate min, p25, median, p75, max
long_dt_gene_name[, `:=`(MIN = quantile(gene_expression)[[1]],
                         p25 = quantile(gene_expression)[[2]],
                         MEDIAN = quantile(gene_expression)[[3]],
                         p75 = quantile(gene_expression)[[4]],
                         MAX = quantile(gene_expression)[[5]],
                         Avg = mean(gene_expression) ),
                  by = gene_name]

# 12,132 unique genes
quantiles_gene<- unique(long_dt_gene_name[, .(gene_name,
                                               MIN,
                                               p25,
                                               MEDIAN,
                                               p75,
                                               MAX)])


# Plot distribution ###
layout(mat = matrix(c(1,2),2,1, byrow=TRUE),  height = c(1,8))
par(mar=c(0, 3.1, 1.1, 2.1))
boxplot(long_dt_gene_name$MEDIAN, horizontal=TRUE, ylim=c(2.5,14), xaxt="n" ,col=rgb(0.8,0.8,0,0.5) , frame=F, outcex=0.5)
par(mar=c(4, 3.1, 1.1, 2.1))
hist(long_dt_gene_name$MEDIAN,xaxt='n',xlab='median expression level of genes',ylab='frequency',main='histogram of median gene expression level')
axis(side=1, at=seq(2.5,13.5, 0.5))
abline(v=median(long_dt_gene_name$MEDIAN),col='red')
text(4.77, y=0, '4.77',pos=4, cex=0.8) 

layout(mat = matrix(c(1,2),2,1, byrow=TRUE),  height = c(1,8))
par(mar=c(0, 3.1, 1.1, 2.1))
boxplot(long_dt_gene_name$Avg, horizontal=TRUE, ylim=c(2.5,14), xaxt="n" ,col=rgb(0.8,0.8,0,0.5) , frame=F, outcex=0.5)
par(mar=c(4, 3.1, 1.1, 2.1))
hist(long_dt_gene_name$Avg,xaxt='n',xlab='average expression level of genes',ylab='frequency',main='histogram of average gene expression level')
axis(side=1, at=seq(2.5,13.5, 0.5))
abline(v=median(long_dt_gene_name$Avg),col='red')
text(4.93, y=0, '4.93',pos=4, cex=0.8) 


# Read clinical data ####
require(readxl)

clinical_key <- read_excel('TARGET_ALL_GeneExpressionArray_Phase1_20160812.xlsx', sheet = 2) %>%
  setDT(.) %>%
  .[, c(1,36)] %>%
  setnames(., c('patient_id', 'cel_file')) %>%
  unique(.)

clinical <- read_excel('TARGET_ALL_ClinicalData_Phase1_20160714.xlsx', sheet = 1) %>%
  setDT(.) %>%
  .[, c(1:8,13:15,18)] %>%
  setnames(., c('patient_id', 'gender', 'race', 'ethnicity', 'age_diagnosis_days',
                'first_event', 'event_free_survival_time_days', 'vital_status',
                'wbc_diagnosis', 'cns_status', 'testicular_involment', 'mrd_29')) %>%
  clinical_key[., on = 'patient_id'] %>%
  .[!is.na(cel_file),]


# Creat categorical values of key clinical features####
require(purrr)
require(data.table)

clinical[, `:=` (snc_teste_involve = 0,
                 latino_black = 0,
                 under_1_over_10_year = 0,
                 wbc_over_50k = 0,
                 mrd_29_positive = 0,
                 dead = 0)] %>%
  .[cns_status %in% c('CNS 2', 'CNS 3') | testicular_involment == 'Yes',
         snc_teste_involve := 1] %>%
  .[cns_status == 'CNS 1' & testicular_involment == 'Unknown',
         snc_teste_involve := NA] %>%
  .[race == 'Black or African American' | ethnicity == 'Hispanic or Latino',
         latino_black := 1] %>%
  .[race == 'Unknown' & ethnicity == 'Unknown',
         latino_black := NA] %>%
  .[age_diagnosis_days < 365 | age_diagnosis_days > 3650,
         under_1_over_10_year := 1] %>%
  .[wbc_diagnosis > 50, wbc_over_50k := 1] %>%
  .[mrd_29 > 0, mrd_29_positive := 1] %>%
  .[is.na(mrd_29), mrd_29_positive := NA] %>%
  .[vital_status == 'Dead', dead := 1] %>%
  .[vital_status %in% c('Unknown', 'Unspecified'), dead := NA] %>%

  # Make key for join with gene expression data set
  .[, B := 1:.N]

clinical <- clinical[, c(1:3,7:9,14:20)]
# Join clinical data with gene expression data ####

# Disable package purrr, so you can use data.table transpose function
#detach('package:purrr', unload = T)

# Prefered to explicit call a function from a package
cda <- data.table::transpose(dt_gene_names)

cda[, B := -2:.N]

join <- clinical[cda, on = 'B']

fwrite(join, 'clinical_gene.csv', sep = '|')



