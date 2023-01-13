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
    'zsjz': 'test',
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
            notice_url = "https://yjsy.hnucm.edu.cn/zsxx/tzgg.htm"
        elif notice_type == 'ssszs':
            print("\033[1;34m查询【硕士生招生】...\033[0m")
            notice_url = "https://yjsy.hnucm.edu.cn/zsxx/ssszs.htm"
        elif notice_type == 'zsjz':
            print("\033[1;34m查询【招生简章】...\033[0m")
            notice_url = "https://yjsy.hnucm.edu.cn/zsxx/zsjz.htm"
        elif notice_type == 'bsszs':
            print("\033[1;34m查询【博士生招生】...\033[0m")
            notice_url = "https://yjsy.hnucm.edu.cn/zsxx/bsszs.htm"
        else:
            return

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


def update_title(**kwargs):
    """
    自动更新 auto_hnucm.py 中的 old_title
    """

    # 当前文件路径
    filepath = kwargs['current_file_path']

    # 最新通知标题
    new_ssszs_title = kwargs['new_ssszs_title']
    new_tzgg_title = kwargs['new_tzgg_title']
    new_zsjz_title = kwargs['new_zsjz_title']
    new_bsszs_title = kwargs['new_bsszs_title']

    # 打开当前文件
    with open(filepath, 'r', encoding='utf-8') as file:
        file_data = file.read()

        if new_tzgg_title and new_tzgg_title != OLD_TITLE['tzgg']:
            # 更新【通知公告】旧标题
            file_data = re.sub(
                r"'tzgg': '(.*?)'",
                f"'tzgg': '{new_tzgg_title}'",
                file_data,
                count=1
            )

        # 更新【硕士生招生】旧标题
        if new_ssszs_title and new_ssszs_title != OLD_TITLE['ssszs']:
            file_data = re.sub(
                r"'ssszs': '(.*?)'",
                f"'ssszs': '{new_ssszs_title}'",
                file_data,
                count=1
            )

        if new_zsjz_title and new_zsjz_title != OLD_TITLE['zsjz']:
            # 更新【招生简章】旧标题
            file_data = re.sub(
                r"'zsjz': '(.*?)'",
                f"'zsjz': '{new_zsjz_title}'",
                file_data,
                count=1
            )

        if new_bsszs_title and new_bsszs_title != OLD_TITLE['bsszs']:
            # 更新【招生简章】旧标题
            file_data = re.sub(
                r"'bsszs': '(.*?)'",
                f"'bsszs': '{new_bsszs_title}'",
                file_data,
                count=1
            )

    # 写入当前文件
    with open(filepath, 'w', encoding='utf-8') as file:
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
def main(**kwargs):

    # 查询【通知公告】的最新通知
    tzgg_title = hnucm_notice(kwargs['tzgg'], 'tzgg')
    # 查询【硕士生招生】的最新通知
    ssszs_title = hnucm_notice(kwargs['ssszs'], 'ssszs')
    # 查询【招生简章】的最新通知
    zsjz_title = hnucm_notice(kwargs['zsjz'], 'zsjz')
    # 查询【博士生招生】的最新通知
    bsszs_title = hnucm_notice(kwargs['bsszs'], 'bsszs')

    # 更新当前文件中的全局变量
    new_title = {
        'current_file_path': os.path.realpath(__file__),
        'new_ssszs_title': ssszs_title,
        'new_tzgg_title': tzgg_title,
        'new_zsjz_title': zsjz_title,
        'new_bsszs_title': bsszs_title
    }
    update_title(**new_title)


if __name__ == '__main__':

    # 查询开关（1：开启  0：关闭）
    code = {
        'tzgg': 1,      # 通知公告
        'ssszs': 1,     # 硕士生招生
        'zsjz': 0,      # 招生简章
        'bsszs': 1      # 博士生招生
    }

    main(**code)
