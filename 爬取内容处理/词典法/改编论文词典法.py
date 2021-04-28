import jieba
import pandas as pd
import re
inversedict=open('inversedict.txt')
ishdict=open('ishdict.txt')
moredict=open('moredic.txt')
mostdict=open('mostdic.txt')
negdict=open('negdic.txt')
overdict=open('overdic.txt')
posdict=open('postdic.txt')
verydict=open('verydic.txt')
insufficientlydict=open('insufficientlydict.txt')
pos_neg_dict=open('pos_neg_dict.txt')
class SentimentAnalysis():

# """Sentiment Analysis with some dictionarys"""

    def sentiment_score_list(self,file_path,seg_sentence):
        names = ['增长', '提升', '增加', '下降', '上涨', '提高', '加快', '减少', '涨幅', '降低', '突破', '持有', '盈利',
                 '亏损', '收益', '压力', '有望', '购买', '持股', '下滑', '下跌', '补贴', '改善', '增强', '买入', '减值',
                 '更好', '助力', '平稳', '新高', '下行', '增幅', '回落', '损失', '下调', '扩张', '跌幅', '增速', '减持',
                 '反弹', '增持', '冲击', '助力', '暴跌', '带动', '熔断', '大跌', '回落', '恐慌', '复苏', '降幅', '净流入',
                 '流出', '涨停', '利好', '高位', '大涨', '牛市', '增量', '流入', '收窄', '恢复', '卖出', '回升', '看好',
                 '上行', '回暖', '受益', '跌停']
        df=pd.read_excel(file_path)
        for text in df['content']:
            results_list = []
            for name in names:
                results = re.findall(r'[^。]*?{}[^。]*?。'.format(name), text)
                results_list = results_list + results

        # seg_sentence = tool.sentence_split_regex(dataset)
        seg_sentence =['我觉得今天股票不大可能会大涨']
        count1,count2 = [],[]

        for sentence in seg_sentence:

            words = jieba.lcut(sentence, cut_all=False)

            i = 0

            a = 0

            for word in words:

# """poscount 积极词的第一次分值;poscount2 积极反转后的分值;poscount3 积极词的最后分值(包括叹号的分值)"""

                poscount,negcount,poscount2,negcount2,poscount3,negcount3 = 0,0,0,0,0,0 #

                if word in posdict:

                    if word in ['好','真','实在'] and words[min(i+1,len(words)-1)] in pos_neg_dict and words[min(i+1,len(words)-1)] != word:

                        continue

                    else:

                        poscount +=1

                        c = 0

                        for w in words[a:i]: # 扫描情感词前的程度词

                            if w in mostdict:

                                poscount *= 4

                            elif w in verydict:

                                poscount *= 3

                            elif w in moredict:

                                poscount *= 2

                            elif w in ishdict:

                                poscount *= 0.5

                            elif w in insufficientlydict:

                                poscount *= -0.3

                            elif w in overdict:

                                poscount *= -0.5

                            elif w in inversedict:

                                c+= 1

                            else:

                                poscount *= 1

                        # if tool.is_odd(c) == 'odd': # 扫描情感词前的否定词数
                        #
                        #     poscount *= -1.0
                        #
                        #     poscount2 += poscount
                        #
                        #     poscount = 0
                        #
                        #     poscount3 = poscount + poscount2 + poscount3
                        #
                        #     poscount2 = 0
                        #
                        # else:
                        #
                        #     poscount3 = poscount + poscount2 + poscount3
                        #
                        #     poscount = 0
                        #
                        #     a = i+1

                elif word in negdict: # 消极情感的分析，与上面一致

                    if word in ['好','真','实在'] and words[min(i+1,len(words)-1)] in pos_neg_dict and words[min(i+1,len(words)-1)] != word:

                        continue

                    else:

                        negcount += 1

                        d = 0

                        for w in words[a:i]:

                            if w in mostdict:

                                negcount *= 4

                            elif w in verydict:

                                negcount *= 3

                            elif w in moredict:

                                negcount *= 2

                            elif w in ishdict:

                                negcount *= 0.5

                            elif w in insufficientlydict:

                                negcount *= -0.3

                            elif w in overdict:

                                negcount *= -0.5

                            elif w in inversedict:

                                d += 1

                            else:

                                negcount *= 1

                        # if tool.is_odd(d) == 'odd':
                        #
                        #     negcount *= -1.0
                        #
                        #     negcount2 += negcount
                        #
                        #     negcount = 0
                        #
                        #     negcount3 = negcount + negcount2 + negcount3
                        #
                        #     negcount2 = 0
                        #
                        # else:
                        #
                        #     negcount3 = negcount + negcount2 + negcount3
                        #
                        #     negcount = 0
                        #
                        #     a = i + 1
                        #
                        #     i += 1
                        #
                        #     pos_count = poscount3
                        #
                        #     neg_count = negcount3
                        #
                        #     count1.append([pos_count,neg_count])

                    if words[-1] in ['!','！']:# 扫描感叹号前的情感词，发现后权值*2

                        count1 = [[j*2 for j in c] for c in count1]

                        for w_im in ['但是','但']:

                            if w_im in words : # 扫描但是后面的情感词，发现后权值*5

                                ind = words.index(w_im)

                                count1_head = count1[:ind]

                                count1_tail = count1[ind:]

                                count1_tail_new = [[j*5 for j in c] for c in count1_tail]

                                count1 = []

                                count1.extend(count1_head)

                                count1.extend(count1_tail_new)

                        break

                    if words[-1] in ['?','？']:# 扫描是否有问好，发现后为负面

                        count1 = [[0,2]]

                        count2.append(count1)

                        count1=[]

        return count2
try1=SentimentAnalysis()
try2=try1.sentiment_score_list('我觉得今天股票不大可能会大涨!')
print(try2)