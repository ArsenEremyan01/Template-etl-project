# Databases

This section provides a list of databases used in the project along with their descriptions:
 * **source_db**: This database contains the source tables that serve as the initial data for the project.
 * **mrr_db**: The mirrored version of the source tables is stored in this database. It allows for analysis and processing without affecting the original data.
 * **staging_db**: This database contains staging tables where data can be temporarily stored during the ETL (Extract, Transform, Load) process.
 * **dwh_db**: The dimensions and facts tables, essential components of the data warehouse, are stored in this database. These tables provide structured and organized data for analytical purposes.

## Running the Databases
To create and run a Docker container with a PostgreSQL database server that includes all the necessary databases and tables, follow these steps:

1. Make sure you have Docker installed on your system.
2. Open a terminal or command prompt.
3. Navigate to the project's **./databases** directory.
4. Execute the following command to start the Docker container: <br> ```docker-compose -f ./postgres-docker-compose.yaml up -d``` <br> This command will read the postgres-docker-compose.yaml file and launch the container in detached mode (-d flag).
5. Wait for the container to initialize and the databases to be set up. This may take a few moments.

Once the command completes and the container is running, you will have the PostgreSQL database server up and ready with all the required databases and tables. You can now proceed to use these databases for your project.


## Database Backup
To ensure the safety and integrity of your databases, it's important to regularly back them up. Follow the steps below to perform a backup:

1. Open a terminal or command prompt.
2. Navigate to the project directory.
3. Execute the following Bash command to initiate the backup process: <br>
```bash db_backup.sh``` <br>
This command will trigger the backup script (db_backup.sh) and start the backup procedure.
4. Wait for the backup process to complete. The duration may vary depending on the size and complexity of your databases.

Once the backup is finished, you will have a secure copy of your databases, which can be used for restoration or archival purposes. It's recommended to store these backups in a safe and separate location to ensure data redundancy and disaster recovery.

## Initial Tables
To view the list of databases along with their initial table structures, navigate to the **./db** folder and refer to the provided SQL file. The SQL file contains the necessary statements to create the tables with their respective schemas.

## Notes
    1. Remove db volumes and stop DB: ```docker-compose -f postgres-docker-compose.yaml down --volumes --rmi all```
