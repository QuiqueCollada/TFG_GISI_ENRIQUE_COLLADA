# syntax=docker/dockerfile:1

FROM python:3.8

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip3 install --no-cache-dir -r requirements.txt

USER root

ARG DEBIAN_FRONTEND=noninteractive

RUN	apt-get update && \
	apt-get -y install  wkhtmltopdf \
						openssl \
						build-essential \
						xorg \ 
						libssl-dev


ENV WKHTML2PDF_VERSION='0.12.4'

WORKDIR /home
RUN wget "https://github.com/wkhtmltopdf/wkhtmltopdf/releases/download/${WKHTML2PDF_VERSION}/wkhtmltox-${WKHTML2PDF_VERSION}_linux-generic-amd64.tar.xz"
RUN tar -xJf "wkhtmltox-${WKHTML2PDF_VERSION}_linux-generic-amd64.tar.xz"
WORKDIR /home/wkhtmltox
RUN chown root:root bin/wkhtmltopdf
RUN cp -r * /usr/

WORKDIR /usr/src/app

COPY . .

CMD python3 main.py
