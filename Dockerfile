FROM python:3.10.4-alpine
LABEL maintainer="Kosaaaaa"

ENV PYTHONUNBUFFERED 1

COPY ./requirements.txt /tmp/requirements.txt
COPY ./scrapper /scrapper
WORKDIR /scrapper


# install required build packages
RUN apk add --update --no-cache gcc libc-dev libffi-dev libxml2-dev libxslt-dev

# install requirements.txt. After it remove /tmp
RUN python -m venv /py && \
    /py/bin/pip install --upgrade pip && \
    /py/bin/pip install -r /tmp/requirements.txt && \
    rm -rf /tmp

ENV PATH="/py/bin:$PATH"
