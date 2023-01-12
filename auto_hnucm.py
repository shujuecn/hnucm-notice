#!/usr/local/bin/python3
# -*- encoding: utf-8 -*-
'''
@Function	: 爬取【湖南中医药大学研究生院】最新招生公告
@Create-Time: 2022/09/03 01:26:09
@Author		: https://github.com/shujuecn
'''

import os
import re
import functools

import requests
from lxml import etree


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
        # print("1.获取网页成功！\n")
        return r.text
    except Exception as e:
        print("\033[0;31m%s\033[0m" % "获取失败，请检查网络连接！")
        print(e)
        print("\n", "-" * 40)


def get_notice_title(html):
    '''
    获取网页标题
    html: 网页源代码
    '''
    selector = etree.HTML(html)
    notice_title = selector.xpath('//div[@class="news_nr"]//li/a/text()')
    # print("2.获取标题成功！")
    return notice_title[0]


def get_notice_time(html):
    '''
    获取网页时间
    html: 网页源代码
    '''
    selector = etree.HTML(html)
    notice_time = selector.xpath('//div[@class="news_nr"]//span/text()')
    # print("3.获取时间成功！")
    return notice_time[0]


def get_notice_url(html):
    '''
    获取最新通知链接
    html: 网页源代码
    '''
    selector = etree.HTML(html)
    notice_url = selector.xpath('//div[@class="news_nr"]//li/a/@href')[0][2:]
    # print("4.获取链接成功！")
    new_notice_url = "http://yjsy.hnucm.edu.cn" + notice_url
    return new_notice_url


# 不执行
"""
def hnucm_zsjz_main():
    '''
    查询【招生简章】页面相关通知
    '''

    print("\n正在查询【湖南中医药大学2023招生简章】...\n")

    # 招生简章
    zsjz_url = "https://yjsy.hnucm.edu.cn/zsxx/zsjz.htm"
    zsjz_html = get_html(zsjz_url)

    if zsjz_html:

        # 获取最新通知标题
        notice_title = get_notice_title(zsjz_html)
        # 获取最新通知时间
        notice_time = get_notice_time(zsjz_html)
        # 获取最新通知链接
        notice_url = get_notice_url(zsjz_html)

        print("最新通知：" + notice_title)
        print("更新日期：" + notice_time)

        # 判断置顶通知是否更新
        if "2023" in notice_title and "简章" in notice_title:
            print("查询结果：\033[0;31m%s\033[0m" % "已发布，请速查看！")
            print("通知链接：\033[0;31m%s\033[0m" % notice_url)
        else:
            print("查询结果：\033[0;31m%s\033[0m" % "暂未发布！")
"""


def hnucm_ssszs_main():
    """
    查询【硕士生招生】页面相关通知
    """

    print("\033[1;34m查询【硕士生招生】...\033[0m")

    ssszs_url = "https://yjsy.hnucm.edu.cn/zsxx/ssszs.htm"
    ssszs_html = get_html(ssszs_url)

    if ssszs_html:

        # 旧通知标题
        old_ssszs_title = '湖南中医药大学2023年接收优秀应届本科毕业生免试攻读硕士学位研究生名单公示'

        # 获取最新通知标题
        ssszs_title = get_notice_title(ssszs_html)
        # 获取最新通知时间
        ssszs_time = get_notice_time(ssszs_html)
        # 获取最新通知链接
        ssszs_url = get_notice_url(ssszs_html)

        print("最新通知：" + ssszs_title)
        print("更新日期：" + ssszs_time)

        # 判断置顶通知是否更新
        if ssszs_title != old_ssszs_title:
            print("查询结果：\033[1;31m%s\033[0m" % "有新通知，请速查看！")
            print("通知链接：\033[1;31m%s\033[0m" % ssszs_url)
        else:
            print("查询结果：\033[1;34m%s\033[0m" % "无新通知！")

    print()
    return ssszs_title


def hncum_tzgg_main():
    """
    查询【通知公告】页面相关通知
    """

    print("\033[1;34m查询【通知公告】...\033[0m")

    tzgg_url = "https://yjsy.hnucm.edu.cn/zsxx/tzgg.htm"
    tzgg_html = get_html(tzgg_url)

    if tzgg_html:

        # 旧通知标题
        old_tzgg_title = '关于2023年博士研究生报考资格审查情况的说明'

        # 获取最新通知标题
        tzgg_title = get_notice_title(tzgg_html)
        # 获取最新通知时间
        tzgg_time = get_notice_time(tzgg_html)
        # 获取最新通知链接
        tzgg_url = get_notice_url(tzgg_html)

        print("最新通知：" + tzgg_title)
        print("更新日期：" + tzgg_time)

        # 判断置顶通知是否更新
        if tzgg_title != old_tzgg_title:
            print("查询结果：\033[1;31m%s\033[0m" % "有新通知，请速查看！")
            print("通知链接：\033[1;31m%s\033[0m" % tzgg_url)
        else:
            print("查询结果：\033[1;34m%s\033[0m" % "无新通知！")

    print()
    return tzgg_title


def update_title(filepath, new_ssszs_title, new_tzgg_title):
    """
    自动更新 auto_hnucm.py 中的 old_title
    """
    with open(filepath, 'r') as file:
        file_data = file.read()

        # 更新【硕士生招生】旧标题
        new_ssszs_data = re.sub(
            r"old_ssszs_title = '(.*?)'",
            f"old_ssszs_title = '{new_ssszs_title}'",
            file_data,
            count=1
        )

        # 更新【通知公告】旧标题
        new_data = re.sub(
            r"old_tzgg_title = '(.*?)'",
            f"old_tzgg_title = '{new_tzgg_title}'",
            new_ssszs_data,
            count=1
        )

    with open(filepath, 'w') as file:
        file.write(new_data)


def print_decorator(func):

    @functools.wraps(func)
    def inner(*args, **kwargs):
        print('-' * 40, '\n')   # 运行前
        result = func(*args, **kwargs)
        print('-' * 40, '\n')   # 运行后
        return result

    return inner


@print_decorator
def main():

    # 查询【通知公告】的最新通知
    tzgg_title = hncum_tzgg_main()
    # 查询【硕士生招生】的最新通知
    ssszs_title = hnucm_ssszs_main()

    # 更新当前文件中的 old_ssszs_title 和 tzgg_title
    current_file_path = os.path.realpath(__file__)
    update_title(
        filepath=current_file_path,
        new_ssszs_title=ssszs_title,
        new_tzgg_title=tzgg_title
    )


if __name__ == '__main__':
    main()
