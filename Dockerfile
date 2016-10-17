FROM python:3.5

ENV USER sigma

RUN apt-get update -qq \
 && apt-get install -y --no-install-recommends \
    sqlite3 \
    lsof \
 && useradd -m -s /bin/bash -u 1000 ${USER}

WORKDIR /sigma
ADD ./requirements.txt ./requirements.txt
RUN pip install -r requirements.txt
ADD . .
RUN chown -R ${USER}:${USER} /sigma

USER ${USER}

ENTRYPOINT ["python3", "run.py"]
