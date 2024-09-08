# syntax=docker/dockerfile:1.4
FROM --platform=$BUILDPLATFORM python:3.12-bullseye AS builder

WORKDIR /app

# RUN apk add gcc 
# RUN apk add curl
# RUN apk add cargo

RUN apt install gcc curl 
#RUN curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh
RUN curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- --help


COPY requirements.txt /app
RUN --mount=type=cache,target=/root/.cache/pip \
    pip3 install -r requirements.txt

COPY . /app

RUN echo "Running python"

ENTRYPOINT ["python3"]
CMD ["-u", "polars_test.py"]
