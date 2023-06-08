# Setting up Apache Superset for Dashboard Creation
The 'bi' module of this project utilizes Apache Superset as the chosen BI tool for building interactive dashboards based on the data in the data warehouse. 
Follow the instructions below to set up Apache Superset locally and create a dashboard using the predefined metrics SQL queries from the 'queries.sql' file.
To get an idea of the dashboard's appearance and functionality, refer to the 'dashboard_example.png' image included in this module. 
It showcases an example of a dashboard created using Apache Superset with the provided metrics.


## Apache Superset setup
To set up Apache Superset for your local development environment, follow the steps below:
1. **Pull Apache Superset Docker Image**: Pull the Apache Superset Docker image from the official repository by executing the following command: <br> ```docker pull apache/superset```
2. **Run Apache Superset Container**: Run the Apache Superset container with the necessary configurations using the following command: <br> ```docker run -d -p 8081:8088 --network=etl_network -e "SUPERSET_SECRET_KEY=192b9bdd22ab9ed4d12e236c78afcb9a393ec15f71bbf5dc987d54727823bcbf" --name superset apache/superset```
3. **Create Admin User**: Set up the admin user account for Apache Superset by executing the following commands: <br> ```docker exec -it superset superset fab create-admin \
              --username admin \
              --firstname Superset \
              --lastname Admin \
              --email admin@superset.com \
              --password admin```
4. **Upgrade Database**: Perform a database upgrade for Apache Superset by executing the following command: ```docker exec -it superset superset db upgrade```
5. **Initialize Superset**: Initialize Apache Superset by executing the following command: <br> ```docker exec -it superset superset init```
6. **Access Apache Superset**: To access the Apache Superset web interface, navigate to **http://localhost:8081/login/** in your web browser. Use the following login credentials: <br> ```Username: admin Password: admin```

With these setup steps, you will have Apache Superset up and running on your local environment. You can now proceed with creating dashboards, configuring connections to your data sources, and exploring the rich features of Apache Superset for data visualization and analysis.


## Connecting Apache Superset to Postgresql Data Warehouse (DWH_DB)
To connect Apache Superset to your Postgresql data warehouse (DWH_DB), follow the steps below:
1. **Open Apache Superset**: Access the Apache Superset web interface by navigating to the appropriate URL in your web browser (e.g., **http://localhost:8081/login/**).
2. **Create Dataset**: Go to the "Data" section in the navigation menu and select "Create Dataset".
3. **Select Database Type**: In the "Create Dataset" page, select the database type as "SqlLite". ""docker network create etl_network""
4. **Configure Connection**: Provide the necessary details to configure the connection to your Postgresql data warehouse. URI: In the "URL" field, enter the SQLAlchemy URI for your Postgresql connection. Use the following format: <br> ```postgresql+psycopg2://postgres:postgres@172.17.0.1:5432/dwh_db```

## Links:
https://hub.docker.com/r/apache/superset









