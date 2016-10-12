FROM python:3.5

WORKDIR /sigma
ADD requirements.txt requirements.txt
RUN pip install -r requirements.txt
ADD . .

ENTRYPOINT ["python3", "sigma.py"]
