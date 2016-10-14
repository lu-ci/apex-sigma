FROM python:3.5

WORKDIR /sigma
ADD requirements.txt requirements.txt
RUN pip install -r requirements.txt
ADD . .

ENV USER sigma
RUN useradd -m -s /bin/bash -u 1000 ${USER} \
 && chown -R ${USER}:${USER} /sigma
USER ${USER}

ENTRYPOINT ["python3", "sigma.py"]
