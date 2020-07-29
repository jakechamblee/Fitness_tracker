FROM python:3.7.8-buster

COPY . /django_project_may

WORKDIR /django_project_may

RUN pip install -r requirements.txt

EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]