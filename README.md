# Correlation-analysis-between-mutations
# Abstract 
&emsp; Predicting the consequences of mutations is one of the existing problems in which machine learning and deep learning are applied. One of the stages of their application is the division of data into training and test sets, which, among other things, determines the accuracy of the constructed model. We propose an a priori method for separating mutations in samples based on considering the correlation between mutations as a measure of proximity and further clustering. 

# Introduction 

&emsp;In December 2022, the article "Mega-scale experimental analysis of protein folding stability in biology and protein design" was published. Within its framework, the largest number of measured effects of mutations was obtained. Based on the obtained data, we attempted to build a model for predicting the effects of mutations within the framework of kaggle-competition https://www.kaggle.com/competitions/novozymes-enzyme-stability-prediction. One of the problems of assessing the accuracy of the constructed models is splitting the dataset into training and test sets. We propose to divide mutations into equivalence classes and train on some classes and test on others. 
# Method 

&emsp;To solve the problem, we will consider single mutations in proteins no longer than 100 amino acids. Then we need to cluster 19*20 = 380 possible mutations. We will use hierarchical clustering, in which we will use the Spearman correlation as the distance between mutations (the method of its calculation will be described below): $sqrt(2(1-|p|))$

&emsp;Now we will tell how we will calculate the correlation. Consider a pair of mutations, for example, WQ and AE (total 19*20 = 380 possible mutations). We construct a sequence of pairs of these two mutations, where each pair satisfies the following conditions: 

&emsp;&emsp;occurred in the same protein 

&emsp;&emsp;happened close in space(distance less than 6 Angstrem) 


&emsp;Next, we calculate the Spearman correlation for each pair mutations. The choice of Spearman's correlation instead of Pearson's is due to the fact that the distribution does not obey the normal law.

&emsp; As a clustering quality metric, we used Silhouette(https://en.wikipedia.org/wiki/Silhouette_(clustering))
# Result

```console
./run.sh mutation_data.scv <path_output_scv_file> 
```
