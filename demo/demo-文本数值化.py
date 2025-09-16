import jieba
from sklearn.feature_extraction.text import CountVectorizer
import pickle
def test():
    texts = ['您中奖了！点击链接领取您的百万大奖。',
             '免费试用我们的产品，不满意全额退款。',
             '您的银行账户需要紧急验证，请点击以下链接。',
             '会议通知：下周的会议安排。',
             '我在超市买了一些食物。',
             '明天我们将一起庆祝生日。']

    #jieba分词,使用空格隔开
    words = [' '.join(jieba.lcut(text)) for text in texts]
    #加载停用词
    with open('../trec06c/trec06c/stopwords.txt', encoding='utf-8') as f:
        stopwords = [line.strip() for line in f if line.strip()]
    #初始化特征提取器,即去除停用词
    extractor = CountVectorizer(stop_words=stopwords)
    extractor.fit(words)#构建特征词词表
    print(extractor.get_feature_names_out())

    #将文本转换为数值
    inputs=extractor.transform(words).toarray()
    print(inputs)

    #存储特征提取器
    pickle.dump(extractor,open('extractor.pkl', 'wb'))
    #存储数值文本
    pickle.dump(inputs,open('train_data.pkl', 'wb'))

if __name__ == '__main__':
    test()