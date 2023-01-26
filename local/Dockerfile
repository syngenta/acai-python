FROM python:3.9-slim

# set the working directory
WORKDIR /code

# install dependencies
COPY ./local/pip.conf pip.conf
COPY ./local/requirements_dev.txt ./requirements.txt
ENV PIP_CONFIG_FILE pip.conf
RUN pip install --no-cache-dir --upgrade -r requirements.txt

## copy the working files to the folder
COPY ./acai ./acai
COPY ./tests ./tests
COPY ./.pylintrc ./.pylintrc
COPY ./setup.cfg ./setup.cfg
COPY ./setup.py ./setup.py
