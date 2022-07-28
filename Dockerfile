FROM circleci/python:3.8.2

WORKDIR /app

ADD . /app
RUN sudo chown -R circleci:circleci /app
RUN python3 -m venv venv_docker
RUN . venv_docker/bin/activate && pip install -r requirements.txt
RUN rm -f database.db

EXPOSE 5000
ENTRYPOINT ["/app/entrypoint.sh"]
