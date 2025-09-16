import pickle
import jieba
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import accuracy_score
import numpy as np

def train():
    #1.加载训练数据
    train_data = pickle.load(open("temp/清洗训练集.pkl", "rb"))
    emails = train_data['email']
    labels = train_data['label']
    #print(labels)

    #2.训练特征提取器
    with open('trec06c/trec06c/stopwords.txt', encoding='utf-8') as f:
        stopwords = [line.strip() for line in f if line.strip()]
    extractor = CountVectorizer(stop_words=stopwords, max_features=100000)  # 过滤频率低的特征词
    # 以稀疏的方式存储转换后的数据
    emails = extractor.fit_transform(emails)

    #3.训练算法模型
    estimator = MultinomialNB()
    estimator.fit(emails, labels)

    # 查看算法模型的准确率
    y_pred = estimator.predict(emails)
    acc = accuracy_score(labels, y_pred)
    #print(f"模型准确率: {acc:.4f}") #模型准确率: 0.9843

    #4.存储特征值提取器和算法模型
    pickle.dump(extractor, open('model/extractor.pkl', 'wb'))
    pickle.dump(estimator, open('model/estimator.pkl', 'wb'))

def evaluate():

    #1.加载特征提取器
    extractor = pickle.load(open('model/extractor.pkl', 'rb'))
    #2.加载算法模型
    estimator = pickle.load(open('model/estimator.pkl', 'rb'))
    #3.加载测试集
    test_data = pickle.load(open('temp/清洗测试集.pkl', 'rb'))
    emails = test_data['email']
    labels = test_data['label']
    #4.测试集的准确率
    emails = extractor.transform(emails)
    y_pred = estimator.predict(emails)
    acc = accuracy_score(labels, y_pred)
    #print(acc) #0.9816620241411328

if __name__ == '__main__':
    evaluate()