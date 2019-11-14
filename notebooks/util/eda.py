from tabulate import tabulate
import pandas as pd
pd.options.display.width=None
pd.options.display.max_columns = None

def inspect_columns(df):
    '''
    Prints number of columns and column names
    :param df:
    '''

    print(f'number of columns {len(list(df))}')
    print(list(df))


def inspect_rows(df):
    '''
    Prints number of rows and first row as example
    :param df:
    '''
    # number of rows
    print(f'number of rows {len(df)}')
    print(tabulate(df.head(), headers='firstrow'))


def eda(dataframe):
    '''
    Prints exploratory data analysis basics
    * dataframe shape
    * dataframe data types
    * dataframe index range
    * dataframe sum of missing values per column
    * dataframe statistics
    * dataframes number of unique values per column
    :param df:
    '''
    print(f'dataframe shape:\n {dataframe.shape}\n')
    print(f'dataframe types:\n {dataframe.dtypes}\n')
    print(f'dataframe index:\n {dataframe.index}\n')
    print(f'missing values:\n {dataframe.isnull().sum()}\n')
    print(f'dataframe describe:ń {dataframe.describe()}\n')
    print(f'unique values:\n')
    for item in dataframe:
        print(f"item: {item} - {dataframe[item].nunique()}")


def boxplot(df, col_name):
    '''
    Prints boxplot for numerical values of column
    :param df:
    :param col_name: numerical column of dataframe
    :return:
    '''
    import seaborn as sns
    sns.set(style="whitegrid")
    ax = sns.boxplot(x=df[col_name])

def dtypes_and_ranges(df, display_theshold=200, num_only=False):
    '''
    Prints data types
    * ranges for numeric values
    * up to <threshold> examples for string values
    :param df:
    :param display_theshold:
    :param num_only:
    '''
    dtypes =  df.dtypes
    print(dtypes)

    print("NUMERIC VALUES and RANGES\n")
    for index, value in dtypes.items():
        if value in (int, float, complex):
            distinct_entries = df[index].unique()
            entry_count = len(distinct_entries)
            print(f"NUMERIC {index}:    {entry_count} different values from:    {min(distinct_entries)} to {'{0:,.0f}'.format(max(distinct_entries)) }")

    print("\nSTRING VALUES and UNIQUES\n")
    if not num_only:
        for index, value in dtypes.items():
            if value == object:
                distinct_entries = df[index].unique()
                entry_count = len(distinct_entries)
                print(f"STRING: {index} has {entry_count} entries\n")
                if entry_count < display_theshold:
                    print(distinct_entries)
                    print('\n')
                else:
                    print(distinct_entries[:200])
                    print('\n')


def uniques(df, col_name, ret=False):
    '''
    Prints unique values of a specific column
    :param df:
    :param col_name:
    :param ret: returns values if set to True
    '''
    unique = df[col_name].unique()
    count = len(unique)
    print(f"count: {count}")
    print(unique)
    if ret:
        return unique


def dropping_duplicates(df):
    # raw count
    '''
    Drops duplicates and prints how many values where dropped
    :param df:
    :return: returns df without duplicates
    '''
    print(f"dataset count: {count}")
    df_no_duplicates = df.drop_duplicates()
    count_no_duplicates = len(df_no_duplicates)
    print(f"dataset no dup count: {count_no_duplicates}")
    return df_no_duplicates