# Alternative Microsoft SQL Server Hook for Airflow

A minimal Airflow [Hook](https://airflow.apache.org/docs/apache-airflow/stable/concepts.html?highlight=hook#hooks) for interacting with [Microsoft SQL Server](https://www.microsoft.com/pt-br/sql-server/)

Enables the usage of [DbApiHook](https://airflow.apache.org/docs/apache-airflow/stable/_modules/airflow/hooks/dbapi.html) methods that the [provided Hook for SQL Server](http://airflow.apache.org/docs/apache-airflow-providers-microsoft-mssql/stable/_modules/airflow/providers/microsoft/mssql/hooks/mssql.html#MsSqlHook) does not support, such as **.get_sqlalchemy_engine** and **.get_pandas_df**.


## Install 
```shell
python -m pip install git+https://github.com/Harduim/mssql_airflow.git
```

## Features
- Use SQLAlchemy Connections with `MsSQLHook.get_sqlalchemy_engine`
- Get a pandas dataframe from a query using `MsSQLHook.get_pandas_df`
- Multiline inserts with `MsSQLHook.batch_insert_rows`
- All other methods already implemented by [DbApiHook](https://airflow.apache.org/docs/apache-airflow/stable/_modules/airflow/hooks/dbapi.html)

## Instructions and sample usage

- Create a connection on **Admin** => **Conections**
  - **Conn Id**: Name of the conection, used on the parameter **mssql_conn_id**
  - **Conn Type**: Microsoft SQL Server
  - **Host**: The IP address or hostname of the server
  - **Schema**: The **Database** not actual schema. Not sure why there is no "database" field, I'm just following Airflow's convention
  - **Password**: The password
  - **Login**: The user name. Use 'domain\username' for Windows auth.


### Airflow 1.10
```python
from datetime import datetime, timedelta

from airflow import DAG
from airflow.hooks.alternative_mssql_hook import MsSQLHook
from airflow.operators.python_operator import PythonOperator


def sample_usage():
    # Schema is the database, not the actual schema.
    mssql = MsSQLHook(mssql_conn_id="my_conn", schema="some_database")

    # This method (get_pandas_df) does not work with the regular mssql plugin
    df = mssql.get_pandas_df("SELECT * FROM TABLE")

    # All the regular dbapihook methods works
    my_records = mssql.get_records("SELECT col1, col2 FROM THE_TABLE")
    mssql.run("DELETE FROM othet_staging_table_name")

    # Saving data to a staging table using pandas to_sql
    conn = mssql.get_sqlalchemy_engine()
    df.to_sql("staging_table_name", con=conn, if_exists="replace")


with DAG(
    "Sample_DAG",
    description="""Sample usage of the MSSQL plugin""",
    schedule_interval="00 00 * * *",
    default_args={
        "owner": "Arthur Harduim",
        "depends_on_past": False,
        "start_date": datetime(2020, 12, 1),
        "email": ["arthur@rioenergy.com.br"],
        "email_on_failure": False,
        "email_on_retry": False,
        "retries": 2,
        "retry_delay": timedelta(minutes=6),
    },
    catchup=False,
) as dag:
    some_db_tsk = PythonOperator(task_id="some_db_tsk", python_callable=sample_usage)
```

### Airflow 2.0

```python
from datetime import datetime, timedelta

from airflow import DAG

from alternative_mssql_hook import MsSQLHook
from airflow.operators.python import PythonOperator


def sample_usage():
    # Schema is the database, not the actual schema.
    mssql = MsSQLHook(mssql_conn_id="my_conn", schema="some_database")

    # This method (get_pandas_df) does not work with the regular mssql plugin
    df = mssql.get_pandas_df("SELECT * FROM TABLE")

    # All the default dbapihook methods works
    my_records = mssql.get_records("SELECT col1, col2 FROM THE_TABLE")
    mssql.run("DELETE FROM othet_staging_table_name")

    # Saving data to a staging table using pandas to_sql
    conn = mssql.get_sqlalchemy_engine()
    df.to_sql("staging_table_name", con=conn, if_exists="replace")


with DAG(
    "Sample_DAG",
    description="""Sample usage of the MSSQL plugin""",
    schedule_interval="00 00 * * *",
    default_args={
        "owner": "Arthur Harduim",
        "depends_on_past": False,
        "start_date": datetime(2020, 12, 1),
        "email": ["arthur@rioenergy.com.br"],
        "email_on_failure": False,
        "email_on_retry": False,
        "retries": 2,
        "retry_delay": timedelta(minutes=6),
    },
    catchup=False,
) as dag:
    some_db_tsk = PythonOperator(task_id="some_db_tsk", python_callable=sample_usage)
```
