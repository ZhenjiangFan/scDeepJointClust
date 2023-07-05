import numpy as np
import pandas as pd
import gc

from sklearn.datasets import make_regression
from sklearn.datasets import make_multilabel_classification
from sklearn.datasets import make_classification
from sklearn.model_selection import StratifiedKFold
from sklearn.decomposition import PCA

import tensorflow as tf

import Configurations as Configurations



def loadRawLeaderSelectedPatientsData():
    dataPath = "/zfs1/hpark/zhf16/data/";
    patientID = "695";
    dataset = pd.read_csv(dataPath+"SelectedPatient"+patientID+"Integrated.csv",index_col=0).T;
    
    numComponents=2000;
    pcaResult = PCA(n_components=numComponents).fit_transform(dataset);
    dataset = pd.DataFrame(pcaResult,index=dataset.index)

    clusterInfo = pd.read_csv(dataPath+"SelectedPatient"+patientID+"IntegratedClusterIDs.csv",index_col=0);
    sampleTypeInfo = pd.read_csv(dataPath+"SelectedPatient"+patientID+"IntegratedSampleTypes.csv",index_col=0);
    
    cellTypeData = clusterInfo["ClusterID"].values;#filteredCelltypes["Celltype"].values;
    RorNRData = sampleTypeInfo["SampleTypeFlag"].values;
    return dataset,cellTypeData,RorNRData;

def splitLeaderSelectedPatientsDataForCV(dataset,cellTypeData,RorNRData,randomState):
    
    #Splitting iterations in the cross-validator.
    kfold = StratifiedKFold(n_splits=Configurations.numOfKFolds, shuffle=True, random_state=randomState);
    KFoldIterIndices = kfold.split(dataset,cellTypeData);
    
    XTensor = tf.convert_to_tensor(dataset);
    
    #The classes starts at 0, so we need to minus 1 to all the class values
    celltypeYTensor = tf.keras.utils.to_categorical(cellTypeData-1);
    celltypeYTensor = tf.convert_to_tensor(celltypeYTensor);

    
    RorNRYTensor = tf.keras.utils.to_categorical(RorNRData);
    RorNRYTensor = tf.convert_to_tensor(RorNRYTensor);


    trainDataset = tf.data.Dataset.from_tensor_slices((XTensor, celltypeYTensor,RorNRYTensor));
    numInputRows = XTensor.shape[0];
    numInputCols = XTensor.shape[1];
    numOutputsCellType = celltypeYTensor.shape[1];
    numOutputsRorNR = RorNRYTensor.shape[1];
    
    return XTensor,celltypeYTensor,RorNRYTensor,numInputRows,numInputCols,numOutputsCellType,numOutputsRorNR,KFoldIterIndices;