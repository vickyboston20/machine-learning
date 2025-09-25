from airflow import DAG
from airflow.operators.empty import EmptyOperator  # Fixed: DummyOperator -> EmptyOperator
from airflow.operators.python import PythonOperator
from airflow.operators.email import EmailOperator
from datetime import datetime, timedelta  # Fixed: replaced days_ago import
import random
import time


# Function to generate random IoT data
def generate_iot_data(**kwargs):
    data = []
    for _ in range(60):  # 60 readings (1 per second) over one minute
        data.append(random.choice([0, 1]))
        time.sleep(1)  # simulate a 1-second interval
    return data


# Function to aggregate the IoT data
def aggregate_machine_data(**kwargs):
    ti = kwargs['ti']
    data = ti.xcom_pull(task_ids='getting_iot_data')
    count_0 = data.count(0)
    count_1 = data.count(1)
    aggregated_data = {'count_0': count_0, 'count_1': count_1}
    return aggregated_data


# Email content generation
def create_email_content(**kwargs):
    ti = kwargs['ti']
    aggregated_data = ti.xcom_pull(task_ids='aggregate_machine_data')
    return (f"Aggregated IoT Data:\n"
            f"Count of 0: {aggregated_data['count_0']}\n"
            f"Count of 1: {aggregated_data['count_1']}")


# Default arguments for the DAG
default_args = {
    'owner': 'airflow',
    'start_date': datetime(2024, 1, 1),  # Fixed: days_ago(1) -> datetime(2024, 1, 1)
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
}


with DAG(
    dag_id='iot_data_pipeline',
    default_args=default_args,
    schedule=None,  # Fixed: schedule_interval -> schedule
    catchup=False,
) as dag:

    start_task = EmptyOperator(task_id='start_task')  # Fixed: DummyOperator -> EmptyOperator

    getting_iot_data = PythonOperator(
        task_id='getting_iot_data',
        python_callable=generate_iot_data,
    )

    aggregate_machine_data = PythonOperator(
        task_id='aggregate_machine_data',
        python_callable=aggregate_machine_data,
    )

    # Generate email content as a separate task (Fixed: EmailOperator content issue)
    generate_email_content = PythonOperator(
        task_id='generate_email_content',
        python_callable=create_email_content,
    )

    # Fixed: EmailOperator using templated content and mailpit SMTP
    send_email = EmailOperator(
        task_id='send_email',
        to='technician@example.com',
        subject='IoT Data Aggregation Results',
        html_content="{{ ti.xcom_pull(task_ids='generate_email_content') }}",
        conn_id='mailpit_smtp',  # Added: specify SMTP connection
    )

    end_task = EmptyOperator(task_id='end_task')  # Fixed: DummyOperator -> EmptyOperator

    # Define the task dependencies (Fixed: added generate_email_content in the chain)
    start_task >> getting_iot_data >> aggregate_machine_data >> generate_email_content >> send_email >> end_task