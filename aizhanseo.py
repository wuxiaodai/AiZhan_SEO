# _*_ encoding:utf-8 _*_
___author___ = 'wuxiaodai'
___date___ = '2020/5/27 11:34'

import re
import os
import time
import argparse
import requests
from multiprocessing import Process


def args():
    """
    命令行参数以及说明
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('-r', '--read', dest='read', help='input domains file path')
    parse_args = parser.parse_args()

    # 参数为空 输出--help命令
    if parse_args.read is None:
        parser.print_help()
        os._exit(0)

    return parse_args.read


def seo(domain_url):
    """
    利用爱站接口查询权重信息
    """
    url = f'https://www.aizhan.com/seo/{domain_url}/'
    headers = {
        'Host': 'www.aizhan.com',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.13; rv:61.0) Gecko/20100101 Firefox/61.0',
        'Content-Type': 'application/x-www-form-urlencoded',
    }
    r = requests.get(url=url, headers=headers, timeout=6)
    html = r.text

    #公司名称正则
    company_name = re.compile(r'<li>.*?id="icp_company">(.*?)</span></li>')
    company = company_name.findall(html)[0]

    # 百度权重正则
    baidu_pattern = re.compile(r'<li>百度权重.*?alt="(.*?)"/>')
    baidu = baidu_pattern.findall(html)[0]

    # 站点备案号正则
    beian_rules = re.compile(r'<li>.*?id="icp_icp">(.*?)</a></li>')
    beian_name = beian_rules.findall(html)[0]

    print(str(domain_url).ljust(20), '\t', company.rjust(15), '\t', baidu.ljust(10), '\t', beian_name)


def main():
    start = time.time()
    file_path = args()
    try:
        #  读取文件所有行
        with open(file_path, "r", encoding='utf-8') as f:
            print('域名'.ljust(20), '公司名称\t'.rjust(20), '权重\t'.rjust(10), '备案号'.rjust(12))
            for line in f.readlines():
                line = line.strip("\n")
                if "http://" in line:
                    line = line[7:]
                elif 'https://' in line:
                    line = line[8:]
                seo(line)

        end = time.time()
        print(f'\n耗时: {end - start:.4f} 秒')

    except Exception as e:
        print('文件读取异常，请检查文件路径是否正确！')
        print(e)


if __name__ == '__main__':
    main()
