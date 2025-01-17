import pandas as pd
import numpy as np
import os
from tensorflow import keras
from matplotlib import pyplot as plt
from tensorflow.keras.models import Model
from tensorflow.keras import layers
from tensorflow.keras import Input
from sklearn.metrics import confusion_matrix,roc_curve, auc,recall_score,precision_score,f1_score


plt.rcParams['font.sans-serif'] = ['SimHei'] # 指定默认字体
plt.rcParams['axes.unicode_minus'] = False



begin_date='2016-01-01'
end_date='2021-09-30'



wenben_back=20
total_day=1338
train_num=1204

long_term_back=10
short_term_back=5
wenben_sort=3
batch_size=64

epochs=20

LSTM_num=124
dense_num=20
drop_num=0.2

# mix_file='666777-2.xlsx'
mix_file='加入东方财富网股吧评论数据777888.xlsx'
first_columns='search_index'



test_num=total_day-train_num


class Data_maker:
    def __init__(self,train_num,test_num,fif_back,daily_back,wenben_back,long_term_back,short_term_back):
        self.train_num=train_num
        self.test_num=test_num
        self.fif_back=fif_back
        self.daily_back=daily_back
        self.wenben_back = wenben_back
        self.long_term_back=long_term_back
        self.short_term_back = short_term_back

    def daily_train_data(self,data):
        while True:
            rows = list(range(self.train_num - self.wenben_back)) #总共1489个数据，由于扣除前面20个数据，所以为1469
            samples = np.zeros((len(rows),
                                 self.daily_back,
                                 4))
            for j in rows:

                samples[j] = data.loc[
                                  (data.index >= j) & (data.index < self.daily_back + j),
                                  'open':'close']
            print('日频训练array：',samples.shape)
            print(samples)
            return samples
    def fif_train_data(self,data):
        while True:
            rows = list(range(self.train_num - self.wenben_back))
            samples = np.zeros((len(rows),
                                 self.fif_back,
                                 4))
            for j in rows:

                samples[j] = data.loc[
                              (data.index >= 18* self.fif_back+j * self.fif_back) & (data.index <18*self.fif_back+ (j+1) * self.fif_back),
                              'open':'low']
            print('十五分钟训练array：',samples.shape)
            print(samples)
            return samples
    def wenben_long_term_train_data(self,data):
        while True:
            rows = list(range(self.train_num - self.wenben_back)) #总共1489个数据，由于扣除前面20个数据，所以为1469
            samples = np.zeros((len(rows),
                                 self.long_term_back,
                                 wenben_sort))
            for j in rows:

                samples[j] = data.loc[
                                  (data.index >= self.daily_back+j-self.long_term_back) & (data.index < self.daily_back + j),
                                  first_columns:]
            print('文本长期训练array：',samples.shape)
            return samples
    def wenben_short_term_train_data(self,data):
        while True:
            rows = list(range(self.train_num - self.wenben_back)) #总共1489个数据，由于扣除前面20个数据，所以为1469
            samples = np.zeros((len(rows),
                                 self.short_term_back,
                                wenben_sort))
            for j in rows:

                samples[j] = data.loc[
                                  (data.index >=self.daily_back+j-self.short_term_back) & (data.index < self.daily_back + j),
                                  first_columns:]
            print('文本短期训练array：',samples.shape)
            print(samples)
            return samples
    def daily_test_data(self,data):
        while True:
            rows = list(range(self.test_num - self.wenben_back))
            samples = np.zeros((len(rows),
                                self.daily_back,
                                 4))
            for j in rows:


                samples[j] = data.loc[
                                  (data.index >=j+self.train_num) & (data.index <  j+self.daily_back+self.train_num ),
                                  'open':'close']
            print('日测试array：',samples.shape)
            print(samples)

            return samples

    def wenben_long_term_test_data(self, data):
        while True:
            rows = list(range(self.test_num - self.wenben_back))
            samples = np.zeros((len(rows),
                                self.long_term_back,
                                wenben_sort))
            for j in rows:
                # print(j) ##j从0开始
                samples[j] = data.loc[
                             (data.index >= self.train_num + j+self.daily_back- self.long_term_back ) & (data.index < self.train_num + j+self.daily_back),
                             first_columns:]
            print('长期文本测试array：', samples.shape)        #改正samples[j] = data.loc[(data.index >= self.train_num + j) & (data.index < self.train_num + self.long_term_back + j),first_columns:]
            return samples
    def wenben_short_term_test_data(self, data):
        while True:
            rows = list(range(self.test_num - self.wenben_back))
            samples = np.zeros((len(rows),
                                self.short_term_back,
                                wenben_sort))
            for j in rows:
                samples[j] = data.loc[
                             (data.index >= self.train_num + j+self.daily_back- self.short_term_back) & (data.index < self.train_num + j+self.daily_back),
                             first_columns:]
            print('短期文本测试array：', samples.shape)   #改正samples[j] = data.loc[(data.index >= self.train_num + j) & (data.index < self.train_num + self.short_term_back + j),first_columns:]
            return samples
    def fif_test_data(self,data):
        while True:
            rows = list(range(self.test_num - self.wenben_back))
            samples = np.zeros((len(rows),
                                self.fif_back,
                                 4))
            for j in rows:


                samples[j] = data.loc[
                                 (data.index >=18* self.fif_back+16*self.train_num+(j) * self.fif_back) & (data.index < 18* self.fif_back+16*self.train_num+(j+1) * self.fif_back),
                                 'open':'low']
            print('十五分钟测试array：',samples.shape)
            return samples
    def target_train_data(self,data):
        while True:
            rows = list(range(self.train_num-self.wenben_back))
            targets = np.zeros((len(rows),))
            for j in rows:


                targets[j] = data.loc[data.index == j+self.wenben_back, 'target']
            print('训练标签array',targets.shape)
            print('训练targets',targets)
            return targets
    def target_test_data(self,data):
        while True:
            rows = list(range(self.test_num-self.wenben_back))
            targets = np.zeros((len(rows),))
            for j in rows:


                targets[j] = data.loc[data.index == self.train_num+j+self.wenben_back, 'target'] ##出问题：应该是。而不是***：data.index == self.train_num+j
            print(targets.shape)
            print('验证targets',targets)
            return targets


origin_data=Data_maker(train_num=train_num,test_num=test_num,fif_back=16,daily_back=20,wenben_back=wenben_back,long_term_back=long_term_back,short_term_back=short_term_back)

new_dir='/Users/ccmac/Documents/毕业论文数据/数据二合为一'
dir='/Users/ccmac/Documents/毕业论文数据/数据区间试验'
wenben_dir='/Users/ccmac/Documents/毕业论文数据/每日均值'
daily_df=pd.read_excel(os.path.join(new_dir,mix_file))
fif_df=pd.read_excel(os.path.join(dir,'fif_data.xlsx'))
target_df=pd.read_excel(os.path.join(dir,'target.xlsx'))
wenben_df=pd.read_excel(os.path.join(new_dir,mix_file))

begin=pd.to_datetime(begin_date)
end=pd.to_datetime(end_date)

daily_df=daily_df.loc[(daily_df['trade_time']>=begin)&(daily_df['trade_time']<=end),:].reset_index()
fif_df=fif_df.loc[(fif_df['trade_time']>=begin)&(fif_df['trade_time']<=end),:].reset_index()
target_df=target_df.loc[(target_df['trade_time']>=begin)&(target_df['trade_time']<=end),:].reset_index()
wenben_df=wenben_df.loc[(wenben_df['trade_time']>=begin)&(wenben_df['trade_time']<=end),:].reset_index()

print('数据长度',daily_df.shape)
print('数据索引',daily_df.index)


print('前几行',daily_df.head())
print('后几行',daily_df.tail())
print('切分数据位置',daily_df.loc[daily_df.index>=train_num,:])

print('fif_df',fif_df.head())
print('fif_df_tail',fif_df.tail())
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
def wenben_norm(df):
    x=df.copy()
    sector_score_mean_value = df['sector_score'].mean(axis=0)
    search_index_mean_value = df['search_index'].mean(axis=0)
    dongfang_mean_value = df['score'].mean(axis=0)

    sector_score_std_value = df['sector_score'].std()
    search_index_std_value = df['search_index'].std()
    dongfang_std_value = df['score'].std()


    x['sector_score']=(df['sector_score']-sector_score_mean_value)/sector_score_std_value
    x['search_index'] = (df['search_index'] - search_index_mean_value) / search_index_std_value
    x['score'] = (df['score'] - dongfang_mean_value) / dongfang_std_value

    df=x
    return df



def split_data(train_num=train_num,wenben_back=wenben_back):
    # print(daily_df.loc[daily_df.index<train_num])
    daily_train_df=daily_df.loc[daily_df.index<train_num]
    daily_test_df=daily_df.loc[daily_df.index>=train_num]
    fif_train_df=fif_df.loc[fif_df.index<16*train_num]
    fif_test_df=fif_df.loc[fif_df.index>=16*train_num]
    wenben_train_df=wenben_df.loc[wenben_df.index<train_num]
    wenben_test_df=wenben_df.loc[wenben_df.index>=train_num]

    target_train_df=target_df.loc[target_df.index<train_num] ##错target_train_df=target_df.loc[target_df.index<train_num-wenben_back]不应该减wenben_back
    target_test_df=target_df.loc[target_df.index>=train_num]

    daily_train_df=norm(daily_train_df)
    daily_test_df=norm(daily_test_df)
    fif_train_df=norm(fif_train_df)
    fif_test_df=norm(fif_test_df)
    wenben_train_df=wenben_norm(wenben_train_df)
    wenben_test_df = wenben_norm(wenben_test_df)


    return {'daily_train_df':daily_train_df,
            'daily_test_df':daily_test_df,
            'fif_train_df':fif_train_df,
            'fif_test_df':fif_test_df,
            'target_train_df':target_train_df,
            'target_test_df':target_test_df,
            'wenben_train_df':wenben_train_df,
            'wenben_test_df': wenben_test_df
            }



###二、读入数据先切分
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
print(target_train_df)
target_test_df=split_data()['target_test_df']
print('测试目标切分：',target_test_df.shape)
print(target_test_df)
wenben_norm_train_df=split_data()['wenben_train_df']
wenben_norm_test_df=split_data()['wenben_test_df']


DM=origin_data

daily_train=DM.daily_train_data(daily_train_df)
daily_test=DM.daily_test_data(daily_test_df)
fif_train=DM.fif_train_data(fif_train_df)
fif_test=DM.fif_test_data(fif_test_df)
target_train=DM.target_train_data(target_train_df)
target_test=DM.target_test_data(target_test_df)


wenben_long_term_train=DM.wenben_long_term_train_data(wenben_norm_train_df)
wenben_short_term_train=DM.wenben_short_term_train_data(wenben_norm_train_df)
wenben_long_term_test=DM.wenben_long_term_test_data(wenben_norm_test_df)
wenben_short_term_test=DM.wenben_short_term_test_data(wenben_norm_test_df)


print('文本数据',wenben_long_term_train)
print('交易数据',daily_train)



def my_model(long_term_back,short_term_back,wenben_sort):
    ##### 一、模型搭建
    wenben_short_term_input = Input(shape=(short_term_back, wenben_sort), dtype='float32',
                                    name='wenben_short_term_input')
    Conv1D_fif = layers.Conv1D(16, 1, strides=1)(wenben_short_term_input)
    LSTM_short_term = layers.LSTM(LSTM_num)(Conv1D_fif)
    # 15分钟频输入训练(!!!卷积滤镜行列先后)
    fif_min_input=Input(shape=(16,4),dtype='float32',name='fif_min_input')
    # fif_min_input=(8,16,4,1)
    Conv1D_fif=layers.Conv1D(16,1,strides=1)(fif_min_input)
    LSTM_fif=layers.LSTM(LSTM_num)(Conv1D_fif)

    # 日频输入训练
    daily_input=Input(shape=(20,4),dtype='float32',name='daily_input')
    # daily_input=(8,16,4,1)
    Conv1D_daily=layers.Conv1D(16,1,strides=1)(daily_input)
    LSTM_daily=layers.LSTM(LSTM_num)(Conv1D_daily)
    # 15分钟频训练结果和日频训练结果合并
    concatenated = layers.concatenate([LSTM_fif, LSTM_daily, LSTM_short_term], axis=-1)  # axis=-1按照最后一个轴粘合

    alloy = layers.Dense(dense_num, activation='relu')(concatenated)  # 将粘合结果再接一个全连接层
    dropout = layers.Dropout(0.2)(alloy)
    output = layers.Dense(1, activation='sigmoid')(dropout)
    model = Model([fif_min_input, daily_input, wenben_short_term_input], output)  # 八股文：将输入和输出圈起来

    print(model.summary())
    model.compile(optimizer=keras.optimizers.Adam(lr=1e-3), loss='binary_crossentropy', metrics=['acc'])
    return model
    # reduce_lr = ReduceLROnPlateau(monitor='val_loss', patience=5, mode='auto')


model = my_model(long_term_back=long_term_back, short_term_back=short_term_back, wenben_sort=wenben_sort)

history = model.fit(x=[fif_train, daily_train, wenben_short_term_train], y=target_train, batch_size=batch_size,
                    validation_split=0.1,epochs=epochs)

loss, accuracy = model.evaluate([fif_test, daily_test, wenben_short_term_test], y=target_test)
print(loss, accuracy)


def gen_y_pred():
    y_predict = model.predict([fif_test, daily_test, wenben_short_term_test], batch_size=1).reshape(
        test_num - wenben_back).tolist()  ###batch_size要设为1，不然evaluate和predict结果不同
    y_pred = []
    for i, v in enumerate(y_predict):
        if v > 0.5:
            y_pred.append(1)
        if v < 0.5:
            y_pred.append(0)
    return y_pred


y_pred = gen_y_pred()
print(y_pred)


# 回测代码试写

class Back_tes_trader:  ###第二步
    def __init__(self, train_num, daily_back, wenben_back):
        self.train_num = train_num
        self.daily_back = daily_back
        self.wenben_back = wenben_back

    def daily_test_data(self, data):
        while True:
            samples = data.loc[
                data.index >= self.train_num + self.wenben_back - 1,
                ['open', 'close']]  ##改了-1
            print(data.index)
            return samples


back_tes_trader = Back_tes_trader(train_num=train_num, daily_back=20,
                                  wenben_back=wenben_back)  ##获取回测期数据df["open","close"]


def split_back_trader(train_num=train_num):  ###第一步

    daily_test_df = daily_df.loc[daily_df.index >= train_num]

    return {'daily_test_df': daily_test_df}


back_df = split_back_trader()['daily_test_df']  ##1、获取回测期df，还需传入Back_tes_trader
# print('日频测试切分：',back_df.shape)


backtrader_df = back_tes_trader.daily_test_data(back_df)  ###2、传入

# print(backtrader_df.shape)
# print(backtrader_df)

backtrader_df['rate_of_return'] = backtrader_df['close'].rolling(2).apply(lambda x: x[1] / x[0] - 1, raw=True)
backtrader_df['day_rate_of_return'] = backtrader_df['close'] / backtrader_df['open'] - 1

clo_1 = backtrader_df.loc[(backtrader_df.index < total_day - 1), "close"].tolist()

backtrader_df.loc[(backtrader_df.index >= train_num + 20), 'last_close'] = clo_1  ##改
backtrader_df['sale_rate_of_return'] = backtrader_df['open'] / backtrader_df['last_close'] - 1

print(backtrader_df)
print(backtrader_df.shape)
trade_day_return_list = []
return_list = []
every_day_return_list = []


def backtrader(list, df):  ###第三步
    a = 0

    rate_of_return = 1
    for i, v in enumerate(list):
        if (v == 1) & (a == 0):  ##从无到有，a是持股状态
            b = (1 + df.loc[train_num + 20 + i, 'day_rate_of_return'])  ###day_rate_of_return日内收益率
            rate_of_return = rate_of_return * b  ###rate_of_return是当前收益率
            a = 1
            trade_day_return_list.append(b - 1)  ##交易日收益率
            return_list.append(rate_of_return)
            every_day_return_list.append(b - 1)  ##每一天收益率（包括0）

        elif (v == 1) & (a == 1):
            b = (1 + df.loc[train_num + 20 + i, 'rate_of_return'])  ###rate_of_return日间收益率
            rate_of_return = rate_of_return * b
            a = a
            trade_day_return_list.append(b - 1)
            return_list.append(rate_of_return)
            every_day_return_list.append(b - 1)
        elif (v == 0) & (a == 0):
            rate_of_return = rate_of_return
            a = a
            every_day_return_list.append(0)

        elif (v == 0) & (a == 1):
            a = 0
            b = (1 + df.loc[train_num + 20 + i, 'sale_rate_of_return'])
            rate_of_return = rate_of_return * b
            trade_day_return_list.append(b - 1)
            every_day_return_list.append(b - 1)
            return_list.append(rate_of_return)
    return a, trade_day_return_list, rate_of_return, return_list, every_day_return_list


result = backtrader(y_pred, backtrader_df)

# final_list=[]
# for i in result[3]:
#     final_list.append(i-1)
# print(final_list)

print(result[1])  ###交易收益统计列表
print(result[2])  ### rate_of_return是当前收益率
print(result[3])  ###每一天本金列表

pingjun_nian_jiaoyi_ri = 240 * len(result[1]) / (len(y_pred))
sharp = (np.mean(result[1])) / (np.std(result[1], ddof=1)) * np.sqrt(pingjun_nian_jiaoyi_ri)

# sharp1=(np.mean(result[4]))/(np.std(result[4]))
# print('夏普比率--：',sharp1)
print('夏普比率：', sharp)
print('收益率：', result[2] - 1)
backtest_list = []

return_right_now = result[3]
for i, v in enumerate(return_right_now):
    if i < len(return_right_now) - 1:
        min = np.min(return_right_now[i + 1:])
        if v > min:
            backtest = (v - min) / (v)
            backtest_list.append(backtest)

backtest = np.max(backtest_list)

print('最大回测：', backtest)

# 检查数据
print('每日收益率', result[1])
target_test_ddf = pd.Series(target_test)
# print('目标数据标签',target_test_ddf)
print('预测结果', y_pred)

print('目标测试数据标签', target_test)

target_counts = target_test_ddf.value_counts()
print('目标数据标签统计', target_counts)
y_p = pd.Series(y_pred)
print('统计预测结果个数', y_p.value_counts())


# fpr,tpr,threshold = roc_curve(target_test, y_pred) ###计算真正率和假正率
# print(fpr,tpr,threshold)
# roc_auc = auc(fpr,tpr)

def paint():
    acc = history.history['acc']
    val_acc = history.history['val_acc']
    loss = history.history['loss']
    val_loss = history.history['val_loss']

    epochs = range(len(acc))
    plt.plot(epochs, acc, 'bo', label='Training acc')
    plt.plot(epochs, val_acc, 'b', label='Validation acc')
    plt.title('Training and validation accuracy')
    plt.legend()

    plt.figure()

    plt.plot(epochs, loss, 'bo', label='Training loss')
    plt.plot(epochs, val_loss, 'b', label='Validation loss')
    plt.title('Training and validation loss')
    plt.legend()
    return plt


my_paint = paint()
my_paint.show()
# 混淆矩阵绘制
confusion_matrix = confusion_matrix(target_test, y_pred, labels=[1, 0])
precision_score = precision_score(target_test, y_pred)
recall_score = recall_score(target_test, y_pred)
f1_score = f1_score(target_test, y_pred)

print('混淆矩阵：', confusion_matrix)
print('查准率：', precision_score)
print('查全率：', recall_score)
print('f1-score:', f1_score)

# plt.matshow(confusion_matrix)
# plt.title('Confusion matrix')
# plt.colorbar()
# plt.ylabel('True label')
# plt.xlabel('Predicted label')
# plt.show()


# ROC曲线绘制
y_predict = model.predict([fif_test, daily_test, wenben_short_term_test]).reshape(test_num - wenben_back).tolist()
fpr, tpr, threshold = roc_curve(target_test, y_predict)  ###计算真正率和假正率
# print(fpr,tpr,threshold)
roc_auc = auc(fpr, tpr)

lw = 2
plt.figure()
plt.plot(fpr, tpr, color='darkorange',
         lw=lw, label='ROC curve (area = %0.2f)' % roc_auc)  ###假正率为横坐标，真正率为纵坐标做曲线
plt.plot([0, 1], [0, 1], color='navy', lw=lw, linestyle='--')
plt.xlim([0.0, 1.0])
plt.ylim([0.0, 1.05])
plt.xlabel('False Positive Rate')
plt.ylabel('True Positive Rate')
plt.title('Receiver operating characteristic example')
plt.legend(loc="lower right")
plt.show()
