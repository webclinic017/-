import pandas as pd
import numpy as np
import os
from matplotlib import pyplot as plt
from keras.models import Model
from keras import layers
from keras import Input
from sklearn.metrics import confusion_matrix,roc_curve,auc,recall_score,precision_score,f1_score


plt.rcParams['font.sans-serif'] = ['SimHei'] # 指定默认字体
plt.rcParams['axes.unicode_minus'] = False
import keras

import keras.losses




class Data_maker:
    def __init__(self,train_num,test_num,fif_back,daily_back):
        self.train_num=train_num
        self.test_num=test_num
        self.fif_back=fif_back
        self.daily_back=daily_back

    def daily_train_data(self,data):
        while True:
            rows = list(range(self.train_num - self.daily_back)) #总共1489个数据，由于扣除前面20个数据，所以为1469
            samples = np.zeros((len(rows),
                                 self.daily_back,
                                 5))
            for j in rows:

                samples[j] = data.loc[
                                  (data.index >= j) & (data.index < self.daily_back + j),
                                  'open':]
            print('日频训练array：',samples.shape)
            return samples
    def fif_train_data(self,data):
        while True:
            rows = list(range(self.train_num - self.daily_back))
            samples = np.zeros((len(rows),
                                 self.fif_back,
                                 5))
            for j in rows:

                samples[j] = data.loc[
                              (data.index >= j * self.fif_back ) & (data.index < (j+1) * self.fif_back),
                              'open':]
            print('十五分钟训练array：',samples.shape)
            return samples

    def daily_test_data(self,data):
        while True:
            rows = list(range(self.test_num - self.daily_back))
            samples = np.zeros((len(rows),
                                self.daily_back,
                                 5))
            for j in rows:


                samples[j] = data.loc[
                                  (data.index >= self.train_num+j) & (data.index < self.train_num+self.daily_back + j),
                                  'open':]
            print('日测试array：',samples.shape)
            return samples
    def fif_test_data(self,data):
        while True:
            rows = list(range(self.test_num - self.daily_back))
            samples = np.zeros((len(rows),
                                self.fif_back,
                                 5))
            for j in rows:


                samples[j] = data.loc[
                                 (data.index >= 16*self.train_num+(j) * self.fif_back) & (data.index < 16*self.train_num+(j+1) * self.fif_back),
                                 'open':]
            print('十五分钟测试array：',samples.shape)
            return samples
    def target_train_data(self,data):
        while True:
            rows = list(range(self.train_num-self.daily_back))
            targets = np.zeros((len(rows),))
            for j in rows:


                targets[j] = data.loc[data.index == j, 'target']
            print('训练标签array',targets.shape)
            return targets
    def target_test_data(self,data):
        while True:
            rows = list(range(self.test_num-self.daily_back))
            targets = np.zeros((len(rows),))
            for j in rows:


                targets[j] = data.loc[data.index == self.train_num+j, 'target']
            print(targets.shape)
            return targets


origin_data=Data_maker(train_num=1650,test_num=413,fif_back=16,daily_back=20)

dir='F:\\newstart\software\category\\tool\category\deal_with_data\武汉金融数据\标准化处理数据基础\数据区间试验'

daily_df=pd.read_excel(os.path.join(dir,'daily_data.xlsx'))
fif_df=pd.read_excel(os.path.join(dir,'fif_data.xlsx'))
target_df=pd.read_excel(os.path.join(dir,'target.xlsx'))



# def shuffle_data(fif_data,daily_data,target,train_num,test_num,fif_back,daily_back):
#
#     a = list(range(train_num-daily_back))
#     # shuffle_list = np.random.choice(a, train_num-test_num, replace=False)
#     shuffle_list=a[:train_num-test_num]
#     rows = list(range(train_num-daily_back)) #总共1489个数据，由于扣除前面20个数据，所以为1469
#     val_list = list(set(rows)-set(shuffle_list))
#     daily_train_samples = np.zeros((len(shuffle_list),
#                          daily_back,
#                          5))
#     fif_train_samples = np.zeros((len(shuffle_list),
#                         fif_back,
#                         5))
#     daily_val_samples = np.zeros((train_num-daily_back-len(shuffle_list),
#                                     daily_back,
#                                     5))
#     fif_val_samples = np.zeros((train_num-daily_back-len(shuffle_list),
#                                   fif_back,
#                                   5))
#     train_targets = np.zeros((train_num-test_num,))
#     val_targets = np.zeros((test_num-daily_back,))
#
#     for i,v in enumerate(shuffle_list):
#
#         fif_train_samples[i] = fif_data[v]
#         daily_train_samples[i] = daily_data[v]
#         train_targets[i] = target[v]
#     for i,v in enumerate(val_list):
#         daily_val_samples[i] = daily_data[v]
#         fif_val_samples[i] = fif_data[v]
#         val_targets[i] = target[v]
#     print('打乱十五分钟频训练:' ,fif_train_samples.shape)
#     print('打乱日频训练；', daily_train_samples.shape)
#     print('打乱十五分钟频验证：',fif_val_samples.shape)
#     print('打乱日频验证：',daily_val_samples.shape)
#     print('打乱训练标签：',train_targets.shape)
#     print('打乱验证标签：',val_targets.shape)
#
#     return {'fif_train_samples':fif_train_samples,
#             'daily_train_samples':daily_train_samples,
#             'train_targets':train_targets,
#             'fif_val_samples':fif_val_samples,
#             'daily_val_samples':daily_val_samples,
#             'val_targets':val_targets}




# 标准化
def norm(df):
    x=df.copy()
    open_mean_value = df['open'].mean(axis=0)
    high_mean_value = df['high'].mean(axis=0)
    low_mean_value = df['low'].mean()
    close_mean_value = df['close'].mean()
    volumerate_mean_value = df['volume_rate'].mean()

    open_std_value = df['open'].std()
    high_std_value = df['high'].std()
    low_std_value = df['low'].std()
    close_std_value = df['close'].std()
    volumerate_std_value = df['volume_rate'].std()

    x['open']=(df['open']-open_mean_value)/open_std_value
    x['high'] = (df['high'] - high_mean_value) / high_std_value
    x['low'] =  (df['low'] - low_mean_value) / low_std_value
    x['close'] =  (df['close'] - close_mean_value) / close_std_value
    x['volume_rate'] = (df['volume_rate'] - volumerate_mean_value) / volumerate_std_value
    df=x
    return df

# # 零一化
# def norm(df):
#     x=df.copy()
#     open_min_value = df['open'].min(axis=0)
#     high_min_value = df['high'].min(axis=0)
#     low_min_value = df['low'].min()
#     close_min_value = df['close'].min()
#     volumerate_min_value = df['volume_rate'].min()
#
#     open_max_value = df['open'].max()
#     high_max_value = df['high'].max()
#     low_max_value = df['low'].max()
#     close_max_value = df['close'].max()
#     volumerate_max_value = df['volume_rate'].max()
#
#     x['open']=(df['open']-open_min_value)/(open_max_value-open_min_value)
#     x['high'] = (df['high'] - high_min_value) / (high_max_value-high_min_value)
#     x['low'] =  (df['low'] - low_min_value) / (low_max_value-low_min_value)
#     x['close'] =  (df['close'] - close_min_value) / (close_max_value-close_min_value)
#     x['volume_rate'] = (df['volume_rate'] - volumerate_min_value) / (volumerate_max_value-volumerate_min_value)
#     df=x
#     return df


def split_data(train_num=1650,daily_back=20):
    daily_train_df=daily_df.loc[daily_df.index<train_num]
    daily_test_df=daily_df.loc[daily_df.index>=train_num]
    fif_train_df=fif_df.loc[fif_df.index<16*train_num]
    fif_test_df=fif_df.loc[fif_df.index>=16*train_num]
    target_train_df=target_df.loc[target_df.index<train_num-daily_back]
    target_test_df=target_df.loc[target_df.index>=train_num]

    daily_train_df=norm(daily_train_df)
    daily_test_df=norm(daily_test_df)
    fif_train_df=norm(fif_train_df)
    fif_test_df=norm(fif_test_df)



    return {'daily_train_df':daily_train_df,
            'daily_test_df':daily_test_df,
            'fif_train_df':fif_train_df,
            'fif_test_df':fif_test_df,
            'target_train_df':target_train_df,
            'target_test_df':target_test_df}

daily_train_df=split_data()['daily_train_df']
print('日频训练切分：',daily_train_df.shape)
daily_test_df=split_data()['daily_test_df']
print('日频测试切分：',daily_test_df.shape)
fif_train_df=split_data()['fif_train_df']
print('十五分钟频训练切分：',fif_train_df.shape)
fif_test_df=split_data()['fif_test_df']
print('十五分钟频测试切分：',fif_test_df.shape)
target_train_df=split_data()['target_train_df']
print('训练目标切分：',target_train_df.shape)
target_test_df=split_data()['target_test_df']
print('测试目标切分：',target_test_df.shape)




DM=origin_data

daily_train=DM.daily_train_data(daily_train_df)
daily_test=DM.daily_test_data(daily_test_df)
fif_train=DM.fif_train_data(fif_train_df)
fif_test=DM.fif_test_data(fif_test_df)
target_train=DM.target_train_data(target_train_df)
target_test=DM.target_test_data(target_test_df)


# data=shuffle_data(fif_data=fif_train,daily_data=daily_train,
#                   target=target_train,train_num=1650,
#                   test_num=413,fif_back=16,daily_back=20)

# fif_train=data.get('fif_train_samples')
# daily_train=data.get('daily_train_samples')
# daily_val=data.get('daily_val_samples')
# fif_val=data.get('fif_val_samples')
# val_targets=data.get('val_targets')
# train_targets=data.get('train_targets')



def my_model():
    ##### 一、模型搭建
    # 15分钟频输入训练(!!!卷积滤镜行列先后)
    fif_min_input=Input(shape=(16,5),dtype='float32',name='fif_min_input')
    # fif_min_input=(8,16,4,1)
    Conv1D_fif=layers.Conv1D(16,1,strides=1)(fif_min_input)
    LSTM_fif=layers.LSTM(100)(Conv1D_fif)

    # 日频输入训练
    daily_input=Input(shape=(20,5),dtype='float32',name='daily_input')
    # daily_input=(8,16,4,1)
    Conv1D_daily=layers.Conv1D(16,1,strides=1)(daily_input)
    LSTM_daily=layers.LSTM(100)(Conv1D_daily)
    # 15分钟频训练结果和日频训练结果合并
    concatenated=layers.concatenate([LSTM_fif,LSTM_daily],axis=-1) # axis=-1按照最后一个轴粘合

    alloy=layers.Dense(20,activation='relu')(concatenated) #将粘合结果再接一个全连接层
    dropout=layers.Dropout(0.2)(alloy)
    output=layers.Dense(1,activation='sigmoid')(dropout)
    model=Model([fif_min_input,daily_input],output) #八股文：将输入和输出圈起来

    print(model.summary())
    model.compile(optimizer=keras.optimizers.adam(lr=1e-3),loss='binary_crossentropy',metrics=['acc'])
    return model
    # reduce_lr = ReduceLROnPlateau(monitor='val_loss', patience=5, mode='auto')

model=my_model()

history=model.fit(x=[fif_train,daily_train],y=target_train,batch_size=8,validation_split=0.2,epochs=20)


loss,accuracy = model.evaluate([fif_test,daily_test],y=target_test)
print(loss,accuracy)

def gen_y_pred():
    y_predict=model.predict([fif_test,daily_test]).reshape(393).tolist()
    y_pred=[]
    for i,v in enumerate(y_predict):
        if v>0.5:
            y_pred.append(1)
        if v<0.5:
            y_pred.append(0)
    return y_pred






y_pred=gen_y_pred()


def paint():
    acc=history.history['acc']
    val_acc=history.history['val_acc']
    loss=history.history['loss']
    val_loss=history.history['val_loss']

    epochs=range(len(acc))
    plt.plot(epochs,acc,'bo',label='Training acc')
    plt.plot(epochs,val_acc,'b',label='Validation acc')
    plt.title('Training and validation accuracy')
    plt.legend()

    plt.figure()

    plt.plot(epochs,loss,'bo',label='Training loss')
    plt.plot(epochs,val_loss,'b',label='Validation loss')
    plt.title('Training and validation loss')
    plt.legend()
    return plt
my_paint=paint()
my_paint.show()

confusion_matrix = confusion_matrix(target_test, y_pred,labels=[1,0])
precision_score=precision_score(target_test, y_pred)
recall_score=recall_score(target_test, y_pred)
f1_score=f1_score(target_test, y_pred)

print('混淆矩阵：',confusion_matrix)
print('查准率：',precision_score)
print('查全率：',recall_score)
print('f1-score:',f1_score)

#ROC曲线绘制
y_predict=model.predict([fif_test,daily_test]).reshape(393).tolist()
fpr,tpr,threshold = roc_curve(target_test, y_predict) ###计算真正率和假正率
print(fpr,tpr,threshold)
roc_auc = auc(fpr,tpr)


lw = 2
plt.figure()
plt.plot(fpr, tpr, color='darkorange',
         lw=lw, label='ROC curve (area = %0.2f)' % roc_auc) ###假正率为横坐标，真正率为纵坐标做曲线
plt.plot([0, 1], [0, 1], color='navy', lw=lw, linestyle='--')
plt.xlim([0.0, 1.0])
plt.ylim([0.0, 1.05])
plt.xlabel('False Positive Rate')
plt.ylabel('True Positive Rate')
plt.title('Receiver operating characteristic example')
plt.legend(loc="lower right")
plt.show()



#混淆矩阵绘制
# plt.matshow(confusion_matrix)
# plt.title('Confusion matrix')
# plt.colorbar()
# plt.ylabel('True label')
# plt.xlabel('Predicted label')
# plt.show()