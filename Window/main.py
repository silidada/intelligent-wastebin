#!/usr/bin/env python
# @Project -> File  :intelligent-wastebin -> main
# @Date     : 2020/5/22 18:01
# @Author   : ChenHaHa
# @Email:   :silidada@163.com

from Window.window import Window
from Window.history import read, draw_in_html, draw_in_image
import threading


def deal_with_history():
    path = {'csv_path': '',
            'last_week_path': '',
            'last_month_path': '',
            'last_year_path': ''}
    data_last_week, data_last_month, data_last_year = read(path=path['csv_path'])
    draw_in_image(data=data_last_week, path=path['last_week_path'], name='last_week')
    draw_in_image(data=data_last_month, path=path['last_month_path'], name='last_month')
    draw_in_image(data=data_last_year, path=path['last_year_path'], name='last_year')
    draw_in_html(data=data_last_week, path=path['last_week_path'], name='last_week')
    draw_in_html(data=data_last_month, path=path['last_month_path'], name='last_month')
    draw_in_html(data=data_last_year, path=path['last_year_path'], name='last_year')


def main():
    pie_path = {'last_week': r'..\lalala.png',
                'last_month': '',
                'last_year': ''}
    window = Window(pie_path=pie_path)
    history_thread = threading.Thread(target=deal_with_history, name='deal_with_history')
    window()
    history_thread.start()
    window.root.mainloop()


if __name__ == '__main__':
    main()
