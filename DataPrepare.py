import multiprocessing
import os
from collections import Counter
from multiprocessing.pool import worker
from sklearn.model_selection import train_test_split
from joblib import Parallel, delayed
from tqdm import tqdm
import pickle
import jieba


#在/full/index文件中包含了各个文件的索引，其中spam为垃圾邮件，ham为正常邮件
#读取所有邮件内容整合到一个数据集中
def read_mail_data():
    labels,fnames=[],[]
    for line in open('./trec06c/trec06c/full/index'):
        label,fname=line.strip().split()
        #将../data/000/000转换为trec06c/trec06c/data/000/000
        fname=fname.replace('..','trec06c/trec06c')
        # print(open(fname,encoding='gbk',errors='ignore').read())
        # break
        labels.append(label)
        fnames.append(fname)

    #根据文件路径读取所有文件内容
    emails=[open(fname,encoding='gbk',errors='ignore').read() for fname in fnames]
    # print(emails[0]) #是否正常读取
    #数据分布，垃圾邮件和正常邮件有多少
    # print(Counter(labels)) #Counter({'spam': 42854, 'ham': 21766}) 显然垃圾文本更多

    #数据分割训练集、测试集，从原始数据中分出一小部分作为测试数据集
    x_train,x_test,y_train,y_test=train_test_split(emails,labels,test_size=0.2,random_state=22) #原始数据集20%的数据作为测试集
    # print(Counter(y_train),Counter(y_test)) #Counter({'spam': 34326, 'ham': 17370}) Counter({'spam': 8528, 'ham': 4396})

    #存储相关数据
    pickle.dump({'email':x_train,'label':y_train},open('temp/原始训练集.pkl','wb'))
    pickle.dump({'email': x_test, 'label': y_test}, open('temp/原始测试集.pkl', 'wb'))

#清洗邮件内容，这里只进行了分词处理
def clean_email(email):
    jieba.setLogLevel(0)

    #分词处理
    email=' '.join(jieba.cut(email))
    #繁简体转换
    #去除非中文字符
    #...
    return email

#for循环处理数据集
def process_email(emails,labels):

    result_emails=[]
    result_labels=[]

    #进度条
    progress=tqdm(total=len(labels),desc='进度')

    #遍历所有邮件内容
    for email,label in zip(emails,labels):
        email=clean_email(email)
        progress.update()
        if len(email)==0:
            continue
        result_emails.append(email)
        result_labels.append(label)
    progress.close()

    return {'email':result_emails,'label':result_labels}


#使用简单的循环处理6万多个邮件显然非常耗时
#这里采用了joblib并发执行
def process_email_parallel(emails,labels,cpu_cnt=None):

    #分配任务
    worker_count = multiprocessing.cpu_count() if cpu_cnt is None else cpu_cnt
    emails_count=len(labels)
    every_worker_count=int(emails_count/worker_count)
    task_range=list(range(0,emails_count+1,every_worker_count))
    #print(task_range)

    #创建并发对象
    parallel =Parallel(n_jobs=worker_count)

    #创建并发任务
    def task(s,e):
        #截取任务需要处理区间的数据
        my_emails=emails[s:e]
        my_labels=labels[s:e]
        #开始处理邮件数据
        result_emails = []
        result_labels = []
        progress=tqdm(total=len(my_labels),desc=f'进程{os.getpid()}')
        for email,label in zip(my_emails,my_labels):
            email=clean_email(email)
            progress.update()
            if len(email)==0:
                continue
            result_emails.append(email)
            result_labels.append(label)
        progress.close()

        return {'email':result_emails,'label':result_labels}


    tasks=[]
    for s,e in zip(task_range[:-1],task_range[1:]):
        my_task=delayed(task)(s,e)
        tasks.append(my_task)

    #执行合并结果
    results=parallel(tasks)
    clean_emails=[]
    clean_labels=[]
    for result in results:
        clean_emails.append(result['email'])
        clean_labels.append(result['label'])

    return {'email':clean_emails,'label':clean_labels}

def prepare_email_data():
    #读取数据
    train_data = pickle.load(open('temp/原始训练集.pkl', 'rb'))
    test_data = pickle.load(open('temp/原始测试集.pkl','rb'))
    #处理每一封邮件
    #使用joblib并发方式,显然运行速度很快
    #然而在训练数据集的部分报错显示email长度和label长度不匹配，所以在这里又使用了普通的方法
    train_data=process_email(train_data['email'],train_data['label'])
    test_data=process_email(test_data['email'],test_data['label'])
    #存储处理好的邮件数据
    pickle.dump(train_data,open('temp/清洗训练集.pkl','wb'))
    pickle.dump(test_data,open('temp/清洗测试集.pkl','wb'))


if __name__ == '__main__':
    prepare_email_data()