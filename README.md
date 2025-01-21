# DataStream
Realtime Election Voting System
===============================

This repository contains the code for a realtime election voting system. The system is built using Python, Kafka, Spark Streaming, Postgres and Streamlit. The system is built using Docker Compose to easily spin up the required services in Docker containers.

## System Architecture
![system_architecture.jpg](images%2Fsystem_architecture.jpg)

## System Flow
![system_flow.jpg](images%2Fsystem_flow.jpg)

## System Components
- **createAndInsertDataToTable.py**: Creates the `votes`, `voter`, and `candidate` tables in the Postgres database. 
- **insertDataToDb.py**: Inserts data into the database and into Kafka topics.
- **insertDataToKafka.py**: Produces data directly into Kafka topics.
- **realtime_vote.py**: This file represents the script responsible for handling votes by storing each vote in a Kafka topic(`votes_topic`) and a Postgres database.
- **spark-streaming.py**: Consumes votes from the `votes_topic` Kafka topic, enriches data from Postgres, aggregates votes, and produces data to specific Kafka topics(`result_vote_per_candidate_topic`).
- **consume_data_to_results_per_vote_topic.py**: Consumes real-time data from `results_vote_per_candidate_topic`.
- **test.py** Verifies that the method performs as expected, ensuring its functionality through unit tests to check correctness and expected behavior.

## Setting up the System
This Docker Compose file simplifies the setup by spinning up Zookeeper, Kafka, and Postgres applications in Docker containers. 
We have configured our setup and installed it on a virtual machine running Linux (OS: Ubuntu). 
Inside the virtual machine, we used two Docker Compose files: 1. One for deploying Apache Spark and 3 worker nodes. 2.
Another for deploying the Kafka server and different brokers.


### Prerequisites
- Python 3.11.1 or above installed on your machine and apache spark 3.5.0
- Install Docker either on your local machine or on a virtual machine (VM) such as VirtualBox or VMware.
- Install Docker Compose for orchestrating the services. You can install it on your local machine or on a VM (e.g., VirtualBox or VMware).


### Steps to Run
1. Clone this repository.
2. Navigate to the root containing the Docker Compose file.
3. Run the following command:

```bash
docker-compose up -d
```
Starting Services

docker-compose up -d  
This command will start the following services:

Kafka:
Zookeeper1,2,3
broker1,2
restProxi
spark:
spark-master
spark-worker1,2,3
PostgreSQL
By default:

Kafka will be accessible at localhost:9092
PostgreSQL will be accessible at localhost:5432
If you are running Kafka and PostgreSQL in a virtual machine (VM), you need to replace localhost with the IP address of your VM. Ensure the ports exposed in the docker-compose.yml file are correctly mapped to the VM's network settings.

For example, if your VM IP address is 192.168.178.100, Kafka will be accessible at 192.168.178.100:9092, and PostgreSQL will be accessible at 192.168.178.100:5432.

### git action for CI/CD
To automate the testing and deployment of your application, you can use GitHub Actions. Below is an example of a GitHub Actions workflow configuration to ensure the application works as expected.
You can modify this workflow. yml file according to your specific needs or the stack you're using. For instance, I have configured it to work with an Ubuntu server that I deployed in my virtual machine (VM). If you use a different server or stack, you can adjust the setup steps accordingly.

### Tech Stack Used
- Data injection: API, Kafka
- Processing & Analysis: Python (Pandas, apache spark and sparkStreaming)
- Data Storage: Kafka,PostgresSQL
- Visualization: Power BI
- CI/CD: git action


## Screenshots
### Candidates and Parties information
![finalResult.png](image%2FfinalResult.png)
### Voters
![voters.png](image%2Fvoters.png)

### Voting
![votes_table.png](image%2Fvotes_table.png)

### Dashboard
![dashboard.png](image%2Fdashboard.png)

