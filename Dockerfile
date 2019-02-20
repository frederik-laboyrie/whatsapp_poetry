FROM python:2.7

COPY . /opt/app
WORKDIR /opt/app

RUN pip install -r requirements.txt

ENTRYPOINT ["python", "/opt/app/model.py"]