# DEVELOPMENT LOG

This file contains info sources and tricks

## Open Issues and Recherche

### Using Spark and Airflow on AWS

Sources:
* [https://aws.amazon.com/de/blogs/big-data/build-a-concurrent-data-orchestration-pipeline-using-amazon-emr-and-apache-livy/]
* [https://github.com/aws-samples/aws-concurrent-data-orchestration-pipeline-emr-livy]
* [https://livy.apache.org/examples/]


### Merging Dimension Table from different sources:
* Use a Join (Inner or Left?)
* Maybe use fuzzy matching
* Maybe keep different dimensions and introduce a mapping table between different dims?

Sources:
* search-term: 'medium merge dimensions from different data sets'
* https://medium.com/holistics-software/combining-data-sources-in-reporting-approaches-considerations-23be8c3b4c57
* https://medium.com/@mrpowers/adding-structtype-columns-to-spark-dataframes-b44125409803
* https://www.youtube.com/watch?v=fPufVcItDzs

## Knowledge:

### AWS
* About IAM, VPC, Networks etc: https://www.youtube.com/watch?v=W_eu0rJN0yU&list=PLv2a_5pNAko0Mijc6mnv04xeOut443Wnk&index=9


### EDA
Geo-spatial analysis
* https://www.kaggle.com/learn/geospatial-analysis
* Maps: https://www.kaggle.com/amelinvladislav/map-of-temperatures-and-analysis-of-global-warming

Time-series:
* https://medium.com/@NickDoesData/visualizing-time-series-change-86322a42cf51
* https://scentellegher.github.io/programming/2017/07/15/pandas-groupby-multiple-columns-plot.html

Profiling / Make Pandas quicker:
* https://towardsdatascience.com/speed-up-jupyter-notebooks-20716cbe2025


## Tricks:

Spark
* Remove null values form dataframe:
```
df.where(df.FirstName.isNotNull())

# or for strings only  
df.where(df.FirstName != '').
``` 

other Syntax:
```
df.where(col("FirstName").isNull())
```

* multiple Filter conditions:
```
# and
df.filter((col("act_date") >= "2016-10-01") & (col("act_date") <= "2017-04-01"))

# or
at_least_one_factual_values = df.filter( df['trade_usd'].isNotNull() | df['weight_kg'].isNotNull() | df['quantity'].isNotNull())
```

* get list of column names from pyspark dataframe:
```
col_names = df.columns
```

*  check if a column contains a value:
```
df.filter(df.name.contains('o')).collect()
```

* remove duplicates:
```
df.dropDuplicates()

# or only based on a specific column/s
df.dropDuplicates(['col_name_a'])
df.dropDuplicates(['col_name_a', 'col_name_b'])
```