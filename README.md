```python
from datetime import datetime, timedelta

from airflow import DAG
from airflow.hooks.alternative_mssql_hook import MsSQLHook
from airflow.operators import python_operator


def sample_usage():
    mssql = MsSQLHook(mssql_conn_id="my_conn", schema="some_database")

    # This method (get_pandas_df) does not with the regular mssql plugin
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
    some_db_tsk = python_operator(task_id="some_db_tsk", python_callable=sample_usage)

```
