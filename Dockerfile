FROM python:3

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install -r requirements.txt

COPY . .

ENTRYPOINT ["gunicorn", "-w", "4", "-b", "0.0.0.0:8000", "python-executor-controller:app"]
