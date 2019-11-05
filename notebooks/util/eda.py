from tabulate import tabulate
import pandas as pd
pd.options.display.width=None
pd.options.display.max_columns = None
import seaborn as sns

def inspect_columns(df):
    # number of columns
    print(f'number of columns {len(list(df))}')
    print(list(df))


def inspect_rows(df):
    # number of rows
    print(f'number of rows {len(df)}')
    print(tabulate(df.head(), headers='firstrow'))
    #print(df.head())


# pandas function creates a report from several common EDA commands
def eda(dataframe):
    print(f'missing values:\n {dataframe.isnull().sum()}\n')
    print(f'dataframe index:\n {dataframe.index}\n')
    print(f'dataframe types:\n {dataframe.dtypes}\n')
    print(f'dataframe shape:\n {dataframe.shape}\n')
    print(f'dataframe index:\n {dataframe.index}\n')
    print(f'dataframe describe:ń {dataframe.describe()}\n')
    print(f'unique values:\n')
    for item in dataframe:
        print(f"item: {item} - {dataframe[item].nunique()}")

def boxplot(df, col_name):
    import seaborn as sns
    sns.set(style="whitegrid")
    ax = sns.boxplot(x=df[col_name])

def dtypes_and_ranges(df, display_theshold=200, num_only=False):
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
    unique = df[col_name].unique()
    count = len(unique)
    print(f"count: {count}")
    print(unique)
    if ret:
        return unique


def dropping_duplicates(df):
    # raw count
    count = len(df)
    print(f"dataset count: {count}")
    df_no_duplicates = df.drop_duplicates()
    count_no_duplicates = len(df_no_duplicates)
    print(f"dataset no dup count: {count_no_duplicates}")
    return df_no_duplicates