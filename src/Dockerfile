# pull official base image
FROM python:3.10.12

# set work directory
WORKDIR /usr/src

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# copy requirements file
COPY /requirements.txt /usr/src/requirements.txt

# install dependencies
RUN set -eux \
    && pip install -r /usr/src/requirements.txt \
    && rm -rf /root/.cache/pip

# copy project
COPY . .

CMD [ "./docker_entry_point.sh" ]
