'''
Input Data: DataFrame and flag for writing change usage memory
Output Data: DataFrame with changed type data
'''
import numpy as np
import pandas as pd
def optimize_memory_usage(df, print_size=False):
    # Function optimizes memory usage in dataframe.
    # Types for optimization.
    numerics = ['int16', 'int32', 'int64', 'float16', 'float32', 'float64']
    # Memory usage size before optimize (Mb).
    before_size = df.memory_usage(deep=True).sum() / 1024**2

    for column in df.columns:
        column_type = df[column].dtypes
#Converting to an effectve numeric type
        if column_type in numerics:
            column_min = df[column].min()
            column_max = df[column].max()
            if str(column_type).startswith('int'):
                if column_min > np.iinfo(np.int8).min and column_max < np.iinfo(np.int8).max:
                    df[column] = df[column].astype(np.int8)
                elif column_min > np.iinfo(np.int16).min and column_max < np.iinfo(np.int16).max:
                    df[column] = df[column].astype(np.int16)
                elif column_min > np.iinfo(np.int32).min and column_max < np.iinfo(np.int32).max:
                    df[column] = df[column].astype(np.int32)
                elif column_min > np.iinfo(np.int64).min and column_max < np.iinfo(np.int64).max:
                    df[column] = df[column].astype(np.int64)
            else:
                if column_min > np.finfo(np.float32).min and column_max < np.finfo(np.float32).max:
                    df[column] = df[column].astype(np.float32)
                else:
                    df[column] = df[column].astype(np.float64)
#Converting object to category
        elif column in ['mutation', 'pdb', 'start_amino', 'end_amino']:
            num_unique_values = len(df[column].unique())
            num_total_values = len(df[column])
            if num_unique_values / num_total_values < 0.5:
                df.loc[:,column] = df[column].astype('category')
            else:
                df.loc[:,column] = df[column]
    # Memory usage size after optimize (Mb).
    after_size = df.memory_usage(deep=True).sum() / 1024**2
    if print_size:
        print('Memory usage size: before {:5.4f} Mb - after {:5.4f} Mb ({:.1f}%).'.format(before_size, after_size, 100 * (before_size - after_size) / before_size))
    return df
