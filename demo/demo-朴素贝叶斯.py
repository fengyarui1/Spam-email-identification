import pickle
from sklearn.naive_bayes import MultinomialNB #多项式朴素贝叶斯
import numpy as np
from sklearn.metrics import accuracy_score

def test():
    #训练数据加载
    train_data = pickle.load(open('train_data.pkl', 'rb'))
    labels = ['垃圾', '垃圾', '垃圾', '正常', '正常', '正常']
    #print(train_data)

    #1.初始化算法模型
    # alpha 表示拉普拉斯平滑系数
    # fit_prior 表示训练先验概率
    # class_prior 提供的各个类别的先验概率
    estimator = MultinomialNB(alpha=1.0)

    #2.训练算法模型(数据、标签）
    estimator.fit(train_data, labels)

    #3.评估算法模型
    #训练完成后，算法在新的数据集上进行预测，比较精确率
    y_preds=estimator.predict(train_data)
    print(y_preds)

    acc = accuracy_score(labels, y_preds)#使用训练的数据预测，准确率为100%
    print(acc)

    #4.保存算法模型
    pickle.dump(estimator, open('estimator.pkl', 'wb'))

if __name__ == '__main__':
    test()