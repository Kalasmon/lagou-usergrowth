# -*- coding: utf-8 -*-

import numpy as np
import pandas as pd

from utils import calc_real_date


# main
def clean_data(df):

    df['publish_time'] = df.loc[~df.time.str.contains('天前'), 'time'].apply(lambda x: pd.to_datetime(x))

    df.loc[df.publish_time.isnull(), 'publish_time'] = \
    df.loc[df.publish_time.isnull(), 'time'].apply(calc_real_date)

    # 将公司地址的列表转为数据框并加入到数据中
    # 部分公司地址的具体区位是缺少的，因此先统一判断是否缺少，若缺少则在列表对应位置插入空值
    df.address.apply(lambda x: x.insert(2, np.nan) if len(x) == 3 else x)

    # 统一将地址的列表提取为数据框
    df = df.join(pd.DataFrame(df.address.tolist(), columns=['city', 'district', 'area', 'map']))

    # 主要将职位要求的列表进行拆分
    df = df.join(pd.DataFrame(df.request.tolist(), columns=['salary', 'location', 'experience', 'education', 'working_time']))

    # 进一步整理
    ordered_column = \
    ['company_id', 'company', 'job_name', 'label', 'advantage', 'bt', 'publish_time',
    'salary', 'salary_min', 'salary_max', 'salary_mean', 'experience', 'education', 'working_time',
    'city', 'district', 'area']

    lagou = df\
    .assign(salary_min = lambda x: x.salary.str.split('-').str[0].apply(lambda y: int(y.split('k')[0]) * 1000))\
    .assign(salary_max = lambda x: x.salary.str.split('-').str[1].apply(lambda y: int(y.split('k')[0]) * 1000))\
    .eval('salary_mean = (salary_min + salary_max)/2')\
    .assign(experience = lambda x: x.experience.apply(lambda y: y.split('经验')[1].split('年')[0]))\
    .assign(bt = lambda x: x.bt.str.replace('\xa0|\n| ', ''))\
    .assign(label = lambda x: x.label.apply(lambda x: ','.join(x)))\
    .drop(['request', 'time', 'address', 'location', 'map'], axis=1)\
    .reindex(columns = ordered_column)

    return lagou
