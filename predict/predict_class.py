#!/usr/bin/env python
# @Project -> File  :intelligent-wastebin -> predict_class
# @Date     : 2020/5/22 17:58
# @Author   : ChenHaHa
# @Email:   :silidada@163.com

from tensorflow.keras.models import load_model
import sys
import numpy as np


class PredictRubbishClass:

    def __init__(self, path):
        """
        :param path: a str, the model path
        """

        assert (isinstance(path, str))

        print('loading model...')
        try:
            model = load_model(filepath=path)
        except Exception as e:
            print('some error were occur when loading the model',e)
            sys.exit('sorry goodbye')
        print('load model successfully')

        self.className = {}

        self.model = model

        self.history_path = 'history.txt'

        try:
            with open(self.history_path, 'r') as f:
                self.image_num = f.read(1)
        except OSError as e:
            self.image_num = 0

    def predict_class(self, image):
        """
        :param image: a numpy array, the image you want to predict
        :return: a int, the number the model output
        """

        result = self.model.predict(image)
        result = np.argmax(result)

        return result

    def get_image(self):
        image = None

        self.image_num += 1
        return image

    def send_message(self, class_num):
        pass

    def __del__(self):
        with open(self.history_path, 'w') as f:
            f.write(str(self.image_num))


if __name__ == '__main__':
    # path = ''
    # image = ''
    # test = PredictRubbishClass(path)
    # test.predict_class(image)
    with open('../1.txt', 'r') as f:
        a = f.read(1)
    print(int(a))
