from airflow import DAG
from airflow.operators.empty import EmptyOperator
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
import random
import time


# Function to generate random IoT data
def generate_iot_data(**kwargs):
    data = []
    for _ in range(10):  # Reduced to 10 readings for testing
        data.append(random.choice([0, 1]))
        time.sleep(0.1)  # Reduced sleep time for testing
    print(f"Generated data: {data}")
    return data


# Function to aggregate the IoT data
def aggregate_machine_data(**kwargs):
    ti = kwargs['ti']
    data = ti.xcom_pull(task_ids='getting_iot_data')
    count_0 = data.count(0)
    count_1 = data.count(1)
    aggregated_data = {'count_0': count_0, 'count_1': count_1}
    print(f"Aggregated data: {aggregated_data}")
    return aggregated_data


# Function to print results (instead of email)
def print_results(**kwargs):
    ti = kwargs['ti']
    aggregated_data = ti.xcom_pull(task_ids='aggregate_machine_data')
    message = (f"Aggregated IoT Data:\n"
               f"Count of 0: {aggregated_data['count_0']}\n"
               f"Count of 1: {aggregated_data['count_1']}")
    print(message)
    return message


# Default arguments for the DAG
default_args = {
    'owner': 'airflow',
    'start_date': datetime(2024, 1, 1),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
}


with DAG(
    dag_id='iot_data_pipeline',
    default_args=default_args,
    description='IoT Data Processing Pipeline',
    schedule=None,
    catchup=False,
    tags=['iot', 'data-processing'],
) as dag:

    start_task = EmptyOperator(task_id='start_task')

    getting_iot_data = PythonOperator(
        task_id='getting_iot_data',
        python_callable=generate_iot_data,
    )

    aggregate_machine_data = PythonOperator(
        task_id='aggregate_machine_data',
        python_callable=aggregate_machine_data,
    )

    print_results_task = PythonOperator(
        task_id='print_results',
        python_callable=print_results,
    )

    end_task = EmptyOperator(task_id='end_task')

    # Define the task dependencies
    start_task >> getting_iot_data >> aggregate_machine_data >> print_results_task >> end_task