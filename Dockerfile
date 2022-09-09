FROM python:3.9

ENV PROJECT_DIR /python_module

WORKDIR ${PROJECT_DIR}

COPY ./requirements.txt .

RUN pip install -r ./requirements.txt

EXPOSE 8080
COPY . .

RUN chmod +x ${PROJECT_DIR}/startup.sh

CMD ./startup.sh

