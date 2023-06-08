from airflow import DAG
from airflow.providers.postgres.hooks.postgres import PostgresHook
from airflow.operators.python import PythonOperator
from datetime import datetime

default_args = {
    'owner': 'airflow',
    'start_date': datetime(2023, 1, 1)
}

source_hook = PostgresHook(postgres_conn_id='stg_db_conn')
target_hook = PostgresHook(postgres_conn_id='dwh_db_conn')


def copy_product_name_to_dwh():
    # Extract data from stg_db database table
    source_records = source_hook.get_records(f"SELECT id, name FROM stg_dim_product_name ")

    # Insert the records into the target database
    for record in source_records:
        target_hook.run(
            "INSERT INTO dim_product_name (id, name) "
            "VALUES (%(id)s, %(name)s)",
            parameters={
                'id': record[0],
                'name': record[1],
            }
        )


def copy_product_group_to_dwh():
    # Extract data from stg_db database table
    source_records = source_hook.get_records(f"SELECT id, group_name FROM stg_dim_product_group ")

    # Insert the records into the target database
    for record in source_records:
        target_hook.run(
            "INSERT INTO dim_product_group (id, group_name) VALUES (%(id)s, %(group_name)s)",
            parameters={
                'id': record[0],
                'group_name': record[1],
            }
        )


def copy_stg_fact_sales_table():
    # Extract data from stg_db database table
    source_records = source_hook.get_records(
        f"WITH new_products_table AS (SELECT p.id as product_id, pc.id as product_group_id, pd.id as product_name_id "
        f"FROM stg_products p LEFT JOIN stg_dim_product_group pc ON p.group_name = pc.group_name "
        f"LEFT JOIN stg_dim_product_name pd ON p.name = pd.name)"
        f"SELECT npt.product_group_id, npt.product_name_id, sum(qty) as total_qty "
        f"FROM stg_sales s LEFT JOIN new_products_table npt ON s.product_id = npt.product_id "
        f"GROUP BY npt.product_group_id, npt.product_name_id;")

    # Insert the records into the target database
    for record in source_records:
        target_hook.run(
            "INSERT INTO fact_sales (product_group_id, product_name_id, total_qty) "
            "VALUES (%(product_group_id)s,%(product_name_id)s, %(total_qty)s)",
            parameters={
                'product_group_id': record[0],
                'product_name_id': record[1],
                'total_qty': record[2]
            }
        )


with DAG('staging_to_dwh', default_args=default_args, schedule_interval=None) as dag:
    copy_product_name_task = PythonOperator(
        task_id='copy_product_name_task',
        python_callable=copy_product_name_to_dwh
    )
    copy_product_group_task = PythonOperator(
        task_id='copy_product_group_task',
        python_callable=copy_product_group_to_dwh
    )

    copy_stg_fact_sales_to_dwh_task = PythonOperator(
        task_id='copy_stg_fact_sales_to_dwh_task',
        python_callable=copy_stg_fact_sales_table
    )

    copy_product_name_task >> copy_product_group_task >> copy_stg_fact_sales_to_dwh_task
