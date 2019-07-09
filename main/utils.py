# -*- coding: utf-8 -*-

import re
import pandas as pd


# 规范化招聘信息中的标签列表
def refined_job_tags(tags):
    refined_tags = [list(filter(None, re.split('/| ', i)))[0] for i in tags]
    return refined_tags

# 提取正确的职位发布时间，并转为时间格式
def calc_real_date(before_x_day):
    download_day = pd.to_datetime('2019-06-17')
    x = int(before_x_day.split('天前')[0])
    real_date = download_day - pd.DateOffset(x)
    
    return real_date