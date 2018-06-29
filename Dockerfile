FROM python:3.6.2
RUN sed -i 's/deb.debian.org/mirrors.ustc.edu.cn/g' /etc/apt/sources.list
RUN mkdir /code
WORKDIR /code
RUN pip install scrapy -i https://pypi.mirrors.ustc.edu.cn/simple
