# -*- coding: utf-8 -*-

import os
import re
from lxml import html

import pandas as pd

from utils import refined_job_tags


# 从文件夹中获得数据源列表
def get_file_list(dir_path):
    file_list = [i for i in os.listdir(dir_path) if bool(re.search('.html', i))] # 找到文件夹中所有含 html 的源文件
    return file_list

# 读取数据源列表的 html 文件并用 lxml 解析
def read_html(file_path):
    with open(file_path, 'r', encoding='utf-8-sig') as doc:
        html_text = doc.read()
        parsed_html_tree = html.fromstring(html_text)
    
    return parsed_html_tree

# 获得 html 中所需的字段信息
def parse_html(parsed_html_tree):
    company_id = parsed_html_tree.xpath('//div[@class="position-head"]/@data-companyid')[0]
    company = parsed_html_tree.xpath('//div[@class="company"]/text()')[0]
    job_name = parsed_html_tree.xpath('//div[@class="job-name"]/@title')[0]
    job_request = refined_job_tags(parsed_html_tree.xpath('//dd[@class="job_request"]/p/span/text()'))
    job_label = parsed_html_tree.xpath('//dd[@class="job_request"]/ul/li/text()')
    job_time = parsed_html_tree.xpath('//dd[@class="job_request"]/p[@class="publish_time"]/text()')[0].split('\xa0')[0]
    job_advantage = parsed_html_tree.xpath('//dd[@class="job-advantage"]/p/text()')[0]
    # job_bt = parsed_html_tree.xpath('//dd[@class="job_bt"]/div[@class="job-detail"]/p/text()')
    job_bt = parsed_html_tree.xpath('//dd[@class="job_bt"]/div[@class="job-detail"]')[0].text_content()
    job_address = parsed_html_tree.xpath('//dd[@class="job-address clearfix"]/div[@class="work_addr"]/a/text()')
    
    record = \
    dict(zip(['company_id', 'company', 'job_name', 'request', 'label', 'time', 'advantage', 'bt', 'address'],
             [company_id, company, job_name, job_request, job_label, job_time, job_advantage, job_bt, job_address]))
    
    return record
