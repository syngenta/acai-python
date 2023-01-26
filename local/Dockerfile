FROM python:3.9-slim

# set the working directory
WORKDIR /acai

# install dependencies
COPY ./requirements.txt ./
RUN pip install --no-cache-dir --upgrade -r requirements.txt

# copy the src to the folder
COPY ./acai ./
