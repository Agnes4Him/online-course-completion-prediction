FROM python:3.12.4

RUN pip install -U pip
RUN pip install pipenv 

WORKDIR /app

COPY [ "Pipfile", "Pipfile.lock", "./" ]

RUN pipenv install --system --deploy

COPY [ "predict.py", "./" ]

EXPOSE 9696

ENTRYPOINT [ "gunicorn", "predict:app", "-b", "0.0.0.0:9696", "-w", "4" ]