# About project
The ultimate objective of this project is to furnish the analytics team with a comprehensive dashboard for analyzing the quantity of sold products categorized by product name and product group. The project is comprised of three key components: databases, data pipelines, and business intelligence (BI). Please refer to the information provided below for a more detailed description of each component.

# Project structure
## Databases
The databases component is responsible for providing a robust collection of databases, complete with all the necessary tables. 
Additionally, it includes backup tool to ensure the safety and integrity of the data.

## Data Pipelines
The data pipelines component is responsible for creating efficient data pipelines that extract data from the initial source, transform it, and ultimately load it in the required format for the data warehouse. Apache Airflow is utilized for orchestrating this entire process. All the Extract, Transform, Load (ETL) operations are implemented as Airflow DAGs (Directed Acyclic Graphs) within this module. The module encompasses the following ETLs:

1. source-to-mrr
2. mrr-to-staging
3. staging-to-datawarehouse

## BI
The business intelligence (BI) component of the project utilizes the open-source tool Apache Superset. This component is responsible for providing the necessary information on SQL queries required to build metrics. It also includes a Docker file that simplifies the setup of the dashboard. Furthermore, this component offers additional documentation on configuring the dashboard to provide the analytics team with visualized metrics. Specifically, it focuses on the quantity of sold products categorized by both product name and product group.


# Project Setup Steps

To properly set up the project, follow these steps:
1. **Set up databases**: Navigate to the **/databases** folder and refer to the README file for detailed instructions on configuring the databases.
2. **Run Apache Airflow with data pipelines**: Access the **/data_pipelines** directory and follow the instructions outlined in the README file to execute Apache Airflow, which includes all the necessary pipelines for data extraction, transformation, and loading.
3. **Configure the Dashboard with metrics**: Once the databases are up and running, and the pipelines have successfully moved the data from the source to the final data warehouse, proceed to the **/bi** folder. In the README file provided, you will find instructions on setting up the Dashboard, complete with all the relevant metrics.
