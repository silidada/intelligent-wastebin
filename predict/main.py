#!/usr/bin/env python
# @Project -> File  :intelligent-wastebin -> main
# @Date     : 2020/5/22 17:57
# @Author   : ChenHaHa
# @Email:   :silidada@163.com

from predict.predict_class import PredictRubbishClass
from Window.history import save
import os


def main(model_path, history_path):
    # 传入model_path实例化对象
    p = PredictRubbishClass(model_path=model_path)
    while True:
        # 获取单片机返回的图片
        image = p.get_image()
        # 预测图片中垃圾的类别序号
        result = p.predict_class(image)
        # 将类别序号翻译成类别名称
        classname = p.className(result)
        # 将类别序号发送给单片机
        p.send_message(result)

        save(path=history_path, image=image, classname=classname)


if __name__ == '__main__':
    root_path = os.path.abspath('..')
    model_dir = root_path + '/model'
    path = os.listdir(model_dir)
    model_name = []
    for p in path:
        if p.split('.', 1)[1] == 'h5':
            model_name.append(p)
    print(model_name)

    # history_path = ''
    # main(model_path=model_path, history_path=history_path)
