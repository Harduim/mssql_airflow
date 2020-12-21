from airflow.hooks.dbapi_hook import DbApiHook
from airflow.plugins_manager import AirflowPlugin
from sqlalchemy import create_engine
from typing import Iterable, Optional


class MsSQLHook(DbApiHook):
    """Interact with Microsoft SQL Server using sqlalchemy instead of raw pymssql"""

    conn_name_attr = "mssql_conn_id"
    default_conn_name = "mssql_default"

    def __init__(self, *args, **kwargs):
        super(MsSQLHook, self).__init__(*args, **kwargs)
        self.schema = kwargs.pop("schema", "master")

    def get_conn(self):
        """Returns a mssql sqlalchemy raw connection"""

        return self.get_sqlalchemy_engine().raw_connection()

    def get_sqlalchemy_engine(self):
        """Returns a mssql sqlalchemy engine object"""

        conn = self.get_connection(self.mssql_conn_id)
        engine = create_engine(
            f"mssql+pymssql://{conn.login}:{conn.password}@{conn.host}/{self.schema}?charset=utf8"
        )
        return engine

    def batch_insert_rows(
        self,
        table: str,
        rows: Iterable,
        target_fields: Optional[Iterable] = None,
        insert_every: int = 1000,
    ):
        """Insere na os valores de um iterador na tabela desejada

        Args:
            table (str): Nome da tabela destino
            rows (Iterable): Iterador com as linhas
            target_fields (Union[None, Iterable], optional): Relação de colunas da tabela. Defaults to None.
            insert_every (int, optional): Define quantas linhas serão adicionadas a cada insert. Defaults to 1000.
        """
        if target_fields:
            target_fields = ", ".join(target_fields)
            target_fields = "({})".format(target_fields)
        else:
            target_fields = ""

        sql_header = f"INSERT INTO {table} {target_fields} VALUES\n"
        sql_vals = ""
        con = self.get_sqlalchemy_engine()
        i = 1
        for i, row in enumerate(rows, 1):
            cells = [f"'{cell}'" if cell != "NULL" else f"{cell}" for cell in row]
            sql_vals += "({}),".format(",".join(cells))

            if i % insert_every == 0:
                stmt = sql_header + sql_vals[:-1]
                try:
                    con.execute(stmt)
                except Exception:
                    self.log.error(f"ERROR sql stamement:{stmt[:200]}")
                    raise
                sql_vals = ""
                self.log.info(f"Loaded {i} into {table} rows so far")

        if sql_vals:
            stmt = sql_header + sql_vals[:-1]
            try:
                con.execute(stmt)
            except Exception:
                self.log.error(f"ERROR sql stamement:{stmt[:200]}")
                raise
        self.log.info(f"Done loading. Loaded a total of {i} rows")


class AltMsSqlPlugin(AirflowPlugin):
    name = "alt_mssql_hook"
    hooks = [MsSQLHook]
