FROM debian:latest

RUN apt-get -y update && apt-get install -y python python-pip

ADD . /GetCet
WORKDIR /GetCet

RUN pip install -r requirements.txt

ENTRYPOINT ["python", "GetCET.py"]
EXPOSE 8081
CMD ["--address=0.0.0.0", "--port=8081"]
