# -*- coding: utf-8 -*-
import csv
import os
import codecs

def find_row_by_name(target_name, name_key,target_column = None ):
    current_dir = os.path.dirname(__file__)
    two_levels_up = os.path.abspath(os.path.join(current_dir, '..', '..'))
    csv_path = os.path.join(two_levels_up, 'data','familydata.csv')
    data = []
    with codecs.open(csv_path, 'r', 'utf-8', 'ignore') as csv_file:
        reader = csv.DictReader(csv_file)

        for row in reader:
            if row[name_key] == target_name:
                if target_column:
                    # 特定の列のみを追加
                    data.append(row[target_column])
                else:
                    # 全ての列を追加
                    data.append(row)

    return data

print(find_row_by_name('Desk','BlockName'))