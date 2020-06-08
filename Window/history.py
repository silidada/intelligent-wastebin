#!/usr/bin/env python
# @Project -> File  :intelligent-wastebin -> history
# @Date     : 2020/5/22 18:00
# @Author   : ChenHaHa
# @Email:   :silidada@163.com

from PIL import Image
import pandas as pd
import time
import os
import pyecharts
from pyecharts.charts import Pie
import matplotlib.pyplot as plt


def save(path, image, classname):
    """
    保存垃圾的图片并且将该垃圾类名和储存路径存到对应的CSV文件里面
    :param path: a str, the dir used to save image and csv
    :param image: a numpy array
    :param classname: str, the image's name, it can be a Chinese
    :return: None
    """

    assert (isinstance(path, str))
    assert (isinstance(classname, str))
    assert (os.path.exists(path))

    try:
        # 保存垃圾照片
        image = Image.fromarray(image)
        t = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
        path = path + '/' + t + '.jpg'
        image.save(path)

        # 保存类别记录的路径
        path = path.split('.', 1)[0]
        path = path + '.csv'

        # 构建DataFrame
        data = {'classname': classname,
                'time': t.split(' ', 1)[0],
                'path': path}
        data = pd.DataFrame(data=data)

        # 如果是第一次写文件就写上头
        if not os.path.exists(path):
            header = True
            data.to_csv(path, header=header)
        else:
            header = False
            data.to_csv(path, mode='a', header=header)
    except Exception as e:
        print('some error occur when save the history', e)


def read(path):
    """
    读取CSV文件, 以字典的形式返回最近7天, 最近30天, 最近356天的数据
    :param path: a str, the path csv file have save
    :return: three dict, data_last_week, data_last_month, data_last_year
    """

    assert (isinstance(path, str))
    # assert (os.path.exists(path))
    while not os.path.exists(path):
        pass

    data = pd.read_csv(path, usecols=[0, 2])
    td = data['time']
    Time = pd.to_datetime(td)
    Now = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())).split(' ', 1)[0]
    Now = time.strptime(Now, '%Y-%m-%d')
    day = Now - Time
    data['Day'] = day
    data_last_week = data['Day'][data['Day'] < 8]
    data_last_month = data['Day'][data['Day'] < 31]
    data_last_year = data['Day'][data['Day'] < 366]
    del data
    data_last_week = data_last_week.groupby('classname')
    data_last_month = data_last_month.groupby('classname')
    data_last_year = data_last_year.groupby('classname')

    data_last_week = data_last_week.count()
    data_last_week = data_last_week['Day']
    data_last_week= data_last_week.to_dict()

    data_last_month = data_last_month.count()
    data_last_month = data_last_month['Day']
    data_last_month = data_last_month.to_dict()

    data_last_year = data_last_year.count()
    data_last_year = data_last_year['Day']
    data_last_year = data_last_year.to_dict()

    return data_last_week, data_last_month, data_last_year


def dive_data(data):
    """
    将字典的键放到一个列表当中, 将字典的值放到另一个列表当中
    :param data: a dict
    :return:
    """

    assert (isinstance(data, dict))
    # 储存data中的key
    label = []
    # 储存data中的value
    nums = []
    # 将data中的数据分成label和数量
    for key, value in data.items():
        label.append(key)
        nums.append(value)

    return label, nums


def draw_in_html(data, path, name):
    """
    根据所给的data在HTML中画出圆饼图
    :param data: a dict
    :param path: a str, the html dir
    :param name: a str, the html's name
    :return: None
    """

    assert (isinstance(data, dict))
    assert (isinstance(path, str))
    assert (isinstance(name, str))

    # 获取名字和数量
    label, nums = dive_data(data)

    pie = Pie()
    # 添加元素
    pie.add('垃圾类型', [list(z) for z in zip(label, nums)]).set_global_opts(
        title_opts=pyecharts.options.TitleOpts(title="垃圾分布")).set_series_opts(
        label_opts=pyecharts.options.LabelOpts(formatter="{b}: {c}"))
    pie.render(path + '/' + name + '.html')


def draw_in_image(data, path, name):
    """
    根据所给的data画出圆饼图
    :param data: a dict
    :param path: a str, the image save dir
    :param name: a str, the image's name
    :return: None
    """

    assert (isinstance(data, dict))
    assert (isinstance(path, str))
    assert (isinstance(name, str))

    # 获取名字和数量
    label, nums = dive_data(data)

    # 保证正常显示中文
    plt.rcParams['font.sans-serif'] = ['SimHei']
    plt.pie(nums, labels=label, autopct='%1.1f%%', startangle=150, labeldistance=1.1)
    plt.title('垃圾分布')
    # 画成圆形
    plt.axis('equal')
    plt.savefig(path + '/' + name + '.png')


if __name__ == '__main__':
    d = {'classname': ['可回收', '有害', '可回收', '其他', '有害', '可回收'],
         'Day': [1, 2, 3, 1, 2, 3],
         'path': ['lala', 'aaad', 'dakljfl', 'ajsdlfk', 'ajdlfkj', 'ajfla']}
    d = pd.DataFrame(d)
    print(d)
    d = d.groupby(['classname'])
    d = d.count()
    d = d['Day']
    d = d.to_dict()
    # names = []
    # nums = []
    # for key, value in d.items():
    #     names.append(key)
    #     nums.append(value)

    names, nums = dive_data(d)

    # pie = pyecharts.charts.Pie()
    # pie.add('垃圾类型', [list(z) for z in zip(names, nums)])
    # pie.set_global_opts(title_opts=pyecharts.options.TitleOpts(title="垃圾分布"))
    # pie.set_series_opts(label_opts=pyecharts.options.LabelOpts(formatter="{b}: {c}"))
    # pie.render('Pie-weather.html')

    plt.rcParams['font.sans-serif'] = ['SimHei']
    plt.pie(nums, labels=names, autopct='%1.1f%%', startangle=150, labeldistance=1.1)
    plt.title('垃圾分布')
    plt.axis('equal')
    plt.savefig('lalala.png')

    draw_in_html(d, '../', 'lalal')
