from airflow import DAG
from airflow.providers.postgres.hooks.postgres import PostgresHook
from airflow.operators.postgres_operator import PostgresOperator
from airflow.operators.python import PythonOperator
from datetime import datetime

default_args = {
    'owner': 'airflow',
    'start_date': datetime(2023, 1, 1)
}

source_hook = PostgresHook(postgres_conn_id='mrr_db_conn')
target_hook = PostgresHook(postgres_conn_id='stg_db_conn')


def copy_products_table():
    # Extract data from source database table
    source_records = source_hook.get_records(f"SELECT id, name, group_name, NOW() FROM mrr_products ")

    # Insert the records into the target database
    for record in source_records:
        target_hook.run(
            "INSERT INTO stg_products (id, name, group_name, created_at) "
            "VALUES (%(id)s, %(name)s, %(group_name)s, %(created_at)s)",
            parameters={
                'id': record[0],
                'name': record[1],
                'group_name': record[2],
                'created_at': record[3]
            }
        )


def copy_sales_table():
    # Extract data from source database table
    source_records = source_hook.get_records(f"SELECT customer_id, product_id, qty, NOW() FROM mrr_sales ")

    # Insert the records into the target database
    for record in source_records:
        target_hook.run(
            "INSERT INTO stg_sales (customer_id, product_id, qty, created_at) "
            "VALUES (%(customer_id)s, %(product_id)s, %(qty)s, %(created_at)s)",
            parameters={
                'customer_id': record[0],
                'product_id': record[1],
                'qty': record[2],
                'created_at': record[3]
            }
        )


def fill_dim_product_name_table():
    # Extract data from mrr_db database table
    source_records = source_hook.get_records(f"SELECT id, name FROM mrr_products")

    # Insert the records into the target database
    for record in source_records:
        target_hook.run(
            "INSERT INTO stg_dim_product_name (id, name) VALUES (%(id)s, %(name)s)",
            parameters={
                'id': record[0],
                'name': record[1],
            }
        )


def fill_dim_product_group_table():
    # Extract data from mrr_db database table
    source_records = source_hook.get_records(f"SELECT id, group_name FROM mrr_products  ")

    # Insert the records into the target database
    for record in source_records:
        target_hook.run(
            "INSERT INTO stg_dim_product_group (id, group_name) "
            "VALUES (%(id)s, %(group_name)s)",
            parameters={
                'id': record[0],
                'group_name': record[1],
            }
        )


def fill_fact_sales_table(**context):
    sql_query = (
        f"WITH new_products_table AS (SELECT p.id as product_id, pc.id as product_group_id, pd.id as product_name_id "
        f"FROM stg_products p LEFT JOIN stg_dim_product_group pc ON p.group_name = pc.group_name "
        f"LEFT JOIN stg_dim_product_name pd ON p.name = pd.name)"
        f"SELECT npt.product_group_id, npt.product_name_id, sum(qty) as total_qty "
        f"FROM stg_sales s LEFT JOIN new_products_table npt ON s.product_id = npt.product_id "
        f"GROUP BY npt.product_group_id, npt.product_name_id;")

    postgres_hook = PostgresHook(postgres_conn_id='stg_db_conn')
    results = postgres_hook.get_records(sql=sql_query)

    for result in results:
        product_group_id = result[0]
        product_name_id = result[1]
        total_qty = result[2]
        insert_query = f"INSERT INTO stg_fact_sales (product_group_id, product_name_id, total_qty) " \
                       f"VALUES ({product_group_id}, {product_name_id}, {total_qty})"
        postgres_hook.run(insert_query)


with DAG('mrr_to_staging', default_args=default_args, schedule_interval=None) as dag:
    copy_stg_products_task = PythonOperator(
        task_id='copy_stg_products_task',
        python_callable=copy_products_table
    )
    copy_stg_sales_task = PythonOperator(
        task_id='copy_stg_sales_task',
        python_callable=copy_sales_table
    )
    fill_dim_product_name_table_task = PythonOperator(
        task_id='fill_dim_product_name_table_task',
        python_callable=fill_dim_product_name_table
    )
    fill_dim_product_group_table_task = PythonOperator(
        task_id='fill_dim_product_group_table_task',
        python_callable=fill_dim_product_group_table
    )
    fill_stg_fact_sales_task = PythonOperator(
        task_id='fill_stg_fact_sales_task',
        provide_context=True,
        python_callable=fill_fact_sales_table
    )

    copy_stg_products_task >> copy_stg_sales_task >> fill_dim_product_name_table_task >> fill_dim_product_group_table_task >> fill_stg_fact_sales_task
