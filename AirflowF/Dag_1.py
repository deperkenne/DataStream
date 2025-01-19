from datetime import datetime

from airflow.example_dags.example_bash_operator import dag
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator
from KafkaTest import Tweeter,tweeter_consumer,producer



default_args = {
    'owner': 'airflow',
    'start_date': datetime(2024, 12, 19),
    'retries': 1,
}

@dag(
    default_args=default_args,
    description='A DAG to send and consume data from brokers',
    schedule_interval='*/5 * * * *',
    catchup=False,
)




def yelp_data_pipeline():
    send_data = PythonOperator(
        task_id='send_data',
        python_callable = producer.producer_init_and_send_data
    )
    consume_data = PythonOperator(
        task_id='consume_data',
        python_callable = tweeter_consumer.consume_data
    )

    send_data  >> consume_data

dag = yelp_data_pipeline()
