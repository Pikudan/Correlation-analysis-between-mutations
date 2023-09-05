# Correlation-analysis-between-mutations
# Abstract 
&emsp; Predicting the consequences of mutations is one of the existing problems in which machine learning and deep learning are applied. One of the stages of their application is the division of data into training and test sets, which, among other things, determines the accuracy of the constructed model. We propose an a priori method for separating mutations in samples based on considering the correlation between mutations as a measure of proximity and further clustering. 

# Introduction 

&emsp;In December 2022, the article "Mega-scale experimental analysis of protein folding stability in biology and protein design" was published. Within its framework, the largest number of measured effects of mutations was obtained. Based on the obtained data, we attempted to build a model for predicting the effects of mutations within the framework of kaggle-competition https://www.kaggle.com/competitions/novozymes-enzyme-stability-prediction. One of the problems of assessing the accuracy of the constructed models is splitting the dataset into training and test sets. We propose to divide mutations into equivalence classes and train on some classes and test on others. 
# Method 

&emsp;To solve the problem, we will consider single mutations in proteins no longer than 100 amino acids. Then we need to cluster 19*20 = 380 possible mutations. We will use hierarchical clustering, in which we will use the Spearman correlation as the distance between mutations (the method of its calculation will be described below): $sqrt(1-|p|)$ or $1 - |p|$ 

&emsp;Now we will tell how we will calculate the correlation. Consider a pair of mutations, for example, WQ and AE (total 19*20 = 380 possible mutations). We construct a sequence of pairs of these two mutations, where each pair satisfies the following conditions: 

&emsp;&emsp;occurred in the same protein 

&emsp;&emsp;happened close in space(distance less than 6 Angstrem) 


&emsp;Next, we calculate the Spearman correlation for each pair mutations. The choice of Spearman's correlation instead of Pearson's is due to the fact that the distribution does not obey the normal law.

&emsp; As a clustering quality metric, we used Silhouette(https://en.wikipedia.org/wiki/Silhouette_(clustering))
# Result

&emsp;We implemented the calculation of correlations in Python. To reproduce the results, unzip correlation_between_mutations.zip and run the following command from the console:

```console
./run.sh mutation_data.scv <path_output_scv_file> 
```
&emsp;Our resulting correlations are in correlation_between_mutation.csv 

&emsp;Clustering can be seen in hierarchy_clattering_python.html. We used Ward/Average/Complete Linkage method for combining clusters in agglomerative approach. The best silhouette metric was obtained if the model was obtained using Ward Linkage and a distance of $1 - |p|$. 
&emsp;Dendogram of best clustering 

<img width="983" alt="image" src="https://github.com/Pikudan/Correlation-analysis-between-mutations/assets/89961174/40587489-a9a6-4776-bd1c-de127fd13dab">
&emsp;An example part of clustering, where red is a high correlation, green is a correlation close to zero 

<img width="1286" alt="image" src="https://github.com/Pikudan/Correlation-analysis-between-mutations/assets/89961174/d6e6a8f0-cd63-4a7f-b70a-bbd4012fc113">



  &emsp;It can be seen that the classes are formed according to the initial amino acids and, with better clustering, 19-20 clusters are formed. 
  # Conclusion
&emsp;19-20 clusters were obtained, which can be identified with amino acids. Such a quite logical division can be used to make a decision when dividing into samples. The researcher can select two clusters in the test and training data, and take the averaged value as the accuracy of the model.
