import numpy as np
import matplotlib.pyplot as plt
from tensorflow.keras.layers import Dense, Dropout
from tensorflow.keras.models import Sequential  
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.callbacks import ModelCheckpoint
import tensorflow as tf
import random
import os
from mymath import minus_and_round
from transfer_function import TransferFunction
from control_data import read_K


number_of_rings = 4                                 #リング数
n = 100000                                          #データ数
data_K = np.array(read_K(n,number_of_rings))        #Kの格納先　DNNの教師データ
input_data = []                                     #DNNの入力データ
L=np.array([82.4e-6,82.4e-6,55.0e-6,55.0e-6])
xaxis = np.arange(1540e-9,1560e-9,0.01e-9)          #シミュレーション範囲1.54µ~1.56µ
epochs = 100                                        #訓練回数
batch_size = 1024                                   #学習時に一度に計算するデータ数


#データセットの用意
for i in range(n):
    trans_data = TransferFunction(L,data_K[i],config={'center_wavelength':1550e-9,'eta':0.996,'n_eff':2.2,'n_g':4.4,'alpha':52.96})
    input_data.append(list(map(minus_and_round,trans_data.simulate(xaxis))))
train_X = np.reshape(input_data,(n,len(xaxis)))
train_Y = np.reshape(data_K,(n,number_of_rings+1))

#シード値の固定
seed = 1
tf.random.set_seed(seed)
np.random.seed(seed)
random.seed(seed)
os.environ["PYTHONHASHSEED"] = str(seed)

#モデルの構造
model_DNN = Sequential()
model_DNN.add(Dense(len(xaxis), input_shape = (len(xaxis),), activation='linear'))
model_DNN.add(Dropout(0.2))
model_DNN.add(Dense(1000,activation='linear'))
model_DNN.add(Dropout(0.2))
model_DNN.add(Dense(1000,activation='linear'))
model_DNN.add(Dropout(0.1))
model_DNN.add(Dense(500,activation='linear'))
model_DNN.add(Dropout(0.1))
model_DNN.add(Dense(500,activation='linear'))
model_DNN.add(Dropout(0.1))
model_DNN.add(Dense(number_of_rings+1, activation='linear'))
model_DNN.compile(optimizer = Adam(lr=0.001), loss="mean_squared_error", metrics="accuracy")

#モデルの構造を表示する
print(model_DNN.summary())

#CallBacks
filename = "C:\\Users\\taipa\\Documents\\研究室\\プログラム\\MRR\\DNN" + str(number_of_rings) + "_" + str(n) +".h5"
checkpoint = ModelCheckpoint(filepath=filename, monitor="loss",verbose=0,save_best_only=True,save_weights_only=False,mode="min",period=1)


#学習開始
history = model_DNN.fit(train_X, train_Y, batch_size=batch_size, epochs=epochs, verbose=1, validation_split=0.01,callbacks=[checkpoint])

#グラフ表示
plt.plot(range(epochs),history.history["loss"],label="loss")
plt.plot(range(epochs),history.history["val_loss"],label="val_loss")
plt.xlabel("epoch")
plt.ylabel("loss")
plt.ylim(0,20)
plt.legend(bbox_to_anchor=(1,0),loc="lower right")
plt.show()
plt.savefig("C:\\Users\\taipa\\Documents\\研究室\\プログラム\\MRR\\figure.jpg")

#予測開始
pre_number = 10                                 #予測個数
pre_data_K = read_K(pre_number,number_of_rings) #予測用のK
for i in range(pre_number):
    pre_data = TransferFunction(L,pre_data_K[i],config={'center_wavelength':1550e-9,'eta':0.996,'n_eff':2.2,'n_g':4.4,'alpha':52.96})
    temp = np.array(list(map(minus_and_round,pre_data.simulate(xaxis))))
    pred_Y = model_DNN.predict(temp.reshape(1,len(xaxis)))
    print(pred_Y,pre_data_K[i])