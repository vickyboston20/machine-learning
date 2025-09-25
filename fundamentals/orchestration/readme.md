# smtp
```
docker exec -it orchestration-airflow-scheduler-1 airflow connections add 'mailpit_smtp' \
    --conn-type 'smtp' \
    --conn-host 'mailpit' \
    --conn-port 1025 \
    --conn-login '' \
    --conn-password '' \
    --conn-extra '{
    "from_email": "admin@example.com",
    "timeout": 30,
    "retry_limit": 5,
    "disable_tls": true,
    "disable_ssl": true,
    "subject_template": null,
    "html_content_template": null,
    "auth_type": "basic",
    "access_token": null,
    "client_id": null,
    "client_secret": null,
    "tenant_id": null,
    "scope": null
    }'
```

```
docker exec -it orchestration-airflow-scheduler-1 nc -zv mailpit 1025
```
```
docker exec -it orchestration-airflow-scheduler-1 python3 -c "import smtplib; s = smtplib.SMTP('mailpit', 1025); s.sendmail('from@example.com', 'to@example.com', 'Subject: Test\n\nHello from Airflow!'); s.quit()"
```