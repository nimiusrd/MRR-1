import csv
from tensorflow.python.keras.models import load_model

def read_K(n,number_of_rings):                      #LKの読み込み
    file_name = "C:\\Users\\taipa\\Documents\\研究室\\プログラム\\MRR\\data\\K" + str(number_of_rings) + "_" + str(n) +".csv"
    with open(file_name) as file:
        reader = csv.reader(file,quoting =csv.QUOTE_NONNUMERIC)
        data = [row for row in reader]
    return data

def load_NN(n,number_of_rings):
    file_name = "C:\\Users\\taipa\\Documents\\研究室\\プログラム\\MRR\\data\\DNN" + str(number_of_rings) + "_" + str(n) +".h5"
    model_DNN = load_model(file_name)
    return model_DNN