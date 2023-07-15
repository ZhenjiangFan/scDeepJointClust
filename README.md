# scDeepJointClust


The proposed method proceeds in four steps. 
Firstly, a DNN model is constructed and trained (see Figure. 1A below). 
Secondly, the representation data is retrieved from the trained DNN model and a clustering algorithm is performed on it (see Figure. 1B). 
After that, the clustering result is annotated using SingleR (16) (see Figure. 1C). 
Lastly, the method's performance is evaluated by considering the true positive rate and false positive rate (see Figure. 1D).
<!-- 
![An overview of scDeepJointClust.](Images/Fig1.png "An overview of scDeepJointC
-->
<div align="center">
    <img src="Images/Fig1.png" height="265px" width="605px" />
    <div style="width: 200px; text-align: center;">Figrue. 1. An overview of scDeepJointClust.</div>
</div>

# Run scDeepJointClust
'''
#Construct a model.
celltypeModel = buildModel(numInputCols,numOutputsCellType,numOutputsRorNR);

#Train the model.
celltypeModel = trainPhase1Model(celltypeModel,trainDataset,Configurations.numOfEpochs,Configurations.batchSize,Configurations.celltypeLossWeight, Configurations.RorNRLossWeight);
    
representationLayerModel = tf.keras.models.Model(inputs=celltypeModel.input,outputs=celltypeModel.get_layer("hiddenLayer3").output);
representationLayterOutput = representationLayerModel.predict(XTensor);

kmeans = KMeans(n_clusters=curK, random_state=0).fit(representationLayterOutput);

'''

