import pickle
import jieba

def test():

    #待预测数据
    inputs=['点击链接领取您的百万大奖']

    #1.文本数据化
    extractor=pickle.load(open('extractor.pkl','rb'))   #特征提取器
    inputs = [' '.join(jieba.lcut(text)) for text in inputs]
    print(inputs)
    inputs = extractor.transform(inputs).toarray()  #将文本转换为数值
    print(inputs)


    #2.算法模型推理
    estimator=pickle.load(open('estimator.pkl','rb'))   #算法模型
    y_preds = estimator.predict(inputs)
    print(y_preds)


if __name__ == '__main__':
  test()
