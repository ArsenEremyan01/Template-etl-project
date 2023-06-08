# Data Pipelines

## Description
To facilitate the creation and management of data pipelines, as well as monitoring and logging the execution of these pipelines, we have utilized the powerful tool Apache Airflow. This folder contains all the essential files required to set up the Apache Airflow interface and the corresponding DAGs (Directed Acyclic Graphs) that define the pipelines.
Please refer to the information provided below for detailed instructions on setting up and configuring Apache Airflow to run smoothly within your project environment.

## Running the Airflow Project

To run the Airflow project, follow the steps below:
1. Open a terminal or command prompt.
2. Create the necessary directories for Airflow by executing the following commands: <br> ```mkdir -p ./dags ./logs ./plugins``` <br> ```chmod -R 777 ./dags ./logs ./plugins``` <br> These commands will create the *dags*, *logs*, and *plugins* directories and provide appropriate permissions.
3. Set the environment variables by sourcing the **.env** file: ```source .env```
4. Initialize Airflow by running the following command: <br>```docker-compose -f airflow-docker-compose.yaml up airflow-init```
5. Start Airflow in detached mode by running the following command: <br> ```docker-compose -f airflow-docker-compose.yaml up -d``` <br> This command launches Airflow, and it will continue running in the background.
<br>
Once you have completed the previous steps, the Airflow project should be up and running. To access the Airflow interface and start configuring and managing your data pipelines, follow these instructions:
1. Open a web browser and navigate to the following URL: http://localhost:8080/home.
2. You will be prompted to log in to the Airflow interface. Use the following credentials: <br> ```Username: airflow Password: airflow```
3. After logging in, you will gain access to the Airflow interface, where you can configure, schedule, and monitor your data pipelines.

From the Airflow interface, you can explore the provided DAGs and customize them to suit your specific requirements. Additionally, you can monitor the execution of your pipelines, view logs, and manage various aspects of the Airflow environment.

## DAG's
To ensure the proper execution and orchestration of your data pipeline, you need to run the DAGs (Directed Acyclic Graphs) in the following sequence:

1. **source_to_mrr**: This DAG is responsible for copying data from the **source_db** database tables to the **mrr_db** database tables. It facilitates the initial data transfer and synchronization between these two databases.
2. **mrr_to_staging**: The next DAG in the sequence is responsible for copying selected tables from the **mrr_db** to the **staging_db**. It also involves transforming the data as necessary and populating the staging dimension and fact tables. This DAG plays a crucial role in preparing the data for further processing.
3. **staging_to_dwh**: The final DAG in the sequence is responsible for moving the transformed and prepared data from the staging database tables to the **dwh_db**, which represents the data warehouse. This DAG ensures that the data is loaded into the appropriate dimensions and facts tables within the data warehouse for further analysis and reporting.

By running these DAGs in the specified sequence, you can ensure a streamlined and controlled flow of data through your pipeline, from the source databases to the final data warehouse.


