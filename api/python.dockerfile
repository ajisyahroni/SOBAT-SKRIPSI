FROM python:3.9

# set the working directory
WORKDIR /app

# install dependencies
COPY requirements.txt /app/api/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /app/api/requirements.txt

# copy the scripts to the folder
COPY . /app/api
