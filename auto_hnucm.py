#!/usr/local/bin/python3
# -*- encoding: utf-8 -*-
'''
@Function   : 爬取【湖南中医药大学研究生院】最新招生公告
@Time       : 2022/09/03 01:26:09
@Author     : https://github.com/shujuecn
'''

import os
import re
import functools

import requests
from lxml import etree


# 最新通知的标题（此文件运行后会自动更新！！！）
OLD_TITLE = {
    # 通知公告
    'tzgg': '关于2023年博士研究生报考资格审查情况的说明',
    # 硕士生招生
    'ssszs': '湖南中医药大学2023年接收优秀应届本科毕业生免试攻读硕士学位研究生名单公示',
    # 招生简章
    'zsjz': 'None',
    # 博士生招生
    'bsszs': '湖南中医药大学关于2023年招收在职攻读中医博士专业学位研究生的通知'
}


def get_html(url):
    '''
    获取网页源代码
    url: 网页链接
    '''

    headers = {
        "User-Agent":
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36 Edg/105.0.1343.25",
        "Accept":
        "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6"
    }

    try:
        r = requests.get(url=url, headers=headers, timeout=1)
        r.raise_for_status()
        r.encoding = r.apparent_encoding
        # 返回html文本内容
        return r.text
    except Exception as e:
        print("\033[0;31m%s\033[0m" % "获取失败，请检查网络连接！")
        print(e)


def get_notice_info(html):
    """
    获取通知的标题、时间、链接
    html: 网页源代码
    """

    # 最新通知标题
    selector = etree.HTML(html)
    notice_title = selector.xpath('//div[@class="news_nr"]//li/a/text()')[0]

    # 最新通知时间
    selector = etree.HTML(html)
    notice_time = selector.xpath('//div[@class="news_nr"]//span/text()')[0]

    # 最新通知链接
    selector = etree.HTML(html)
    notice_url = selector.xpath('//div[@class="news_nr"]//li/a/@href')[0][2:]
    notice_url = "http://yjsy.hnucm.edu.cn" + notice_url

    return (notice_title, notice_time, notice_url)


def hnucm_notice(code, notice_type):
    """
    打印个页面的查询结果
    """
    if code == 1:
        if notice_type == 'tzgg':
            print("\033[1;34m查询【通知公告】...\033[0m")
        elif notice_type == 'ssszs':
            print("\033[1;34m查询【硕士生招生】...\033[0m")
        elif notice_type == 'zsjz':
            print("\033[1;34m查询【招生简章】...\033[0m")
        elif notice_type == 'bsszs':
            print("\033[1;34m查询【博士生招生】...\033[0m")
        else:
            print('请检查开关！')
            return

        notice_url = f'https://yjsy.hnucm.edu.cn/zsxx/{notice_type}.htm'
        notice_html = get_html(notice_url)

        if notice_html:

            # 新通知标题、时间、链接
            notice_title, notice_time, notice_url = get_notice_info(notice_html)

            print("最新通知：" + notice_title)
            print("更新日期：" + notice_time)

            # 判断置顶通知是否更新
            if notice_title != OLD_TITLE[notice_type]:
                print("查询结果：\033[1;31m%s\033[0m" % "有新通知，请速查看！")
                print("通知链接：\033[1;31m%s\033[0m" % notice_url)
            else:
                print("查询结果：\033[1;34m%s\033[0m" % "无新通知！")

            print()
            return notice_title
        else:
            print('获取失败...\n')


def update_title(file_path, new_title):
    """
    自动更新 auto_hnucm.py 中的 old_title
    """

    with open(file_path, 'r', encoding='utf-8') as file:
        file_data = file.read()

        for title_type, title in new_title.items():
            # 新旧标题不一致时，修改本文件全局变量
            if title and title != OLD_TITLE[title_type]:
                file_data = re.sub(
                    rf"'{title_type}': '(.*?)'",
                    f"'{title_type}': '{title}'",
                    file_data,
                    count=1
                )

    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(file_data)


def print_dotted_lines(func):
    '''
    打印分割线
    '''
    @functools.wraps(func)
    def inner(*args, **kwargs):
        print('-' * 40, '\n')   # 运行前
        result = func(*args, **kwargs)
        print('-' * 40)   # 运行后
        return result

    return inner


@print_dotted_lines
def main(tzgg: int, ssszs: int, zsjz: int, bsszs: int):

    # 获取各页面的最新通知，返回标题
    tzgg_title = hnucm_notice(tzgg, 'tzgg')
    ssszs_title = hnucm_notice(ssszs, 'ssszs')
    zsjz_title = hnucm_notice(zsjz, 'zsjz')
    bsszs_title = hnucm_notice(bsszs, 'bsszs')

    # 更新当前文件中的全局变量
    file_path = os.path.realpath(__file__)
    new_title = {
        'tzgg': tzgg_title,     # 通知公告
        'ssszs': ssszs_title,   # 硕士生招生
        'zsjz': zsjz_title,     # 招生简章
        'bsszs': bsszs_title    # 博士生招生
    }
    update_title(file_path, new_title)


if __name__ == '__main__':

    # 查询开关（1：开启  0：关闭）
    main(
        tzgg=1,     # 通知公告
        ssszs=1,    # 硕士生招生
        zsjz=0,     # 招生简章
        bsszs=0     # 博士生招生
    )
