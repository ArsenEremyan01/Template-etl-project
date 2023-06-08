from airflow import DAG
from airflow.providers.postgres.hooks.postgres import PostgresHook
from airflow.operators.python import PythonOperator
from datetime import datetime

default_args = {
    'owner': 'airflow',
    'start_date': datetime(2023, 1, 1)
}

source_hook = PostgresHook(postgres_conn_id='source_db_conn')
target_hook = PostgresHook(postgres_conn_id='mrr_db_conn')


def copy_products_table():
    # Get last modified date
    last_modified_date = target_hook.get_records("SELECT COALESCE((SELECT last_modified FROM mrr_high_water_mark "
                                                 "WHERE source_table='products' and target_table='mrr_products'), "
                                                 "'1900-01-01 00:00:00'::timestamp)")

    # Extract data from source database table
    source_records = source_hook.get_records(f"SELECT id, name, group_name, NOW() "
                                             f"FROM products "
                                             f"WHERE created_at > '{last_modified_date[0][0].strftime('%Y-%m-%d %H:%M:%S')}'")

    # Insert the records into the target database
    for record in source_records:
        target_hook.run(
            "INSERT INTO mrr_products (id, name, group_name, created_at) "
            "VALUES (%(id)s, %(name)s, %(group_name)s, %(created_at)s)",
            parameters={
                'id': record[0],
                'name': record[1],
                'group_name': record[2],
                'created_at': record[3]
            }
        )

    # Update last modified date
    target_hook.run("INSERT INTO mrr_high_water_mark (source_table, target_table, last_modified) "
                    "VALUES ('products', 'mrr_products', (SELECT MAX(created_at) FROM mrr_products))  "
                    "ON CONFLICT (source_table, target_table) "
                    "DO UPDATE SET last_modified = EXCLUDED.last_modified;")


def copy_customers_table():
    # Get last modified date
    last_modified_date = target_hook.get_records("SELECT COALESCE((SELECT last_modified FROM mrr_high_water_mark "
                                                 "WHERE source_table='customers' and target_table='mrr_customers'), "
                                                 "'1900-01-01 00:00:00'::timestamp)")

    # Extract data from source database table
    source_records = source_hook.get_records(f"SELECT id, name, country, NOW() "
                                             f"FROM customers "
                                             f"WHERE created_at > '{last_modified_date[0][0].strftime('%Y-%m-%d %H:%M:%S')}'")

    # Insert the records into the target database
    for record in source_records:
        target_hook.run(
            "INSERT INTO mrr_customers (id, name, country, created_at) "
            "VALUES (%(id)s, %(name)s, %(country)s, %(created_at)s)",
            parameters={
                'id': record[0],
                'name': record[1],
                'country': record[2],
                'created_at': record[3]
            }
        )

    # Update last modified date
    target_hook.run("INSERT INTO mrr_high_water_mark (source_table, target_table, last_modified) "
                    "VALUES ('customers', 'mrr_customers', (SELECT MAX(created_at) FROM mrr_customers))  "
                    "ON CONFLICT (source_table, target_table) "
                    "DO UPDATE SET last_modified = EXCLUDED.last_modified;")


def copy_sales_table():
    # Get last modified date
    last_modified_date = target_hook.get_records("SELECT COALESCE((SELECT last_modified FROM mrr_high_water_mark "
                                                 "WHERE source_table='sales' and target_table='mrr_sales'), "
                                                 "'1900-01-01 00:00:00'::timestamp)")

    # Extract data from source database table
    source_records = source_hook.get_records(f"SELECT customer_id, product_id, qty, NOW() "
                                             f"FROM sales "
                                             f"WHERE created_at > '{last_modified_date[0][0].strftime('%Y-%m-%d %H:%M:%S')}'")

    # Insert the records into the target database
    for record in source_records:
        target_hook.run(
            "INSERT INTO mrr_sales (customer_id, product_id, qty, created_at) "
            "VALUES (%(customer_id)s, %(product_id)s, %(qty)s, %(created_at)s)",
            parameters={
                'customer_id': record[0],
                'product_id': record[1],
                'qty': record[2],
                'created_at': record[3]
            }
        )

    # Update last modified date
    target_hook.run("INSERT INTO mrr_high_water_mark (source_table, target_table, last_modified) "
                    "VALUES ('sales', 'mrr_sales', (SELECT MAX(created_at) FROM mrr_sales))  "
                    "ON CONFLICT (source_table, target_table) "
                    "DO UPDATE SET last_modified = EXCLUDED.last_modified;")


with DAG('source_to_mrr', default_args=default_args, schedule_interval=None) as dag:
    copy_products_table_task = PythonOperator(
        task_id='copy_products_table_task',
        python_callable=copy_products_table
    )

    copy_customers_table_task = PythonOperator(
        task_id='copy_customers_table_task',
        python_callable=copy_customers_table
    )

    copy_sales_table_task = PythonOperator(
        task_id='copy_sales_table_task',
        python_callable=copy_sales_table
    )

    copy_products_table_task >> copy_customers_table_task >> copy_sales_table_task
