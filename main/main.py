# -*- coding: utf-8 -*-

import os
import pandas as pd
from parse import get_file_list, read_html, parse_html
from clean import clean_data


def main():
    
    dir_path = './raw_html'
    #dir_path = input("Input data file path: ")
    
    df_record = []
    
    file_list = get_file_list(dir_path)
    #print(file_list)
    

    for file_name in file_list:
        file_path = os.path.join(dir_path, file_name)
        tree = read_html(file_path)

        record = parse_html(tree)
        df_record.append(record)
    
    df = pd.DataFrame(df_record)

    lagou = clean_data(df)
    #print(df.head())
    print(lagou)
    
    lagou.to_csv('./output/lagou.csv', encoding='gbk')

if __name__ == '__main__':
    main()
