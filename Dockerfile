FROM python:3.5

ENV PORT=29090
ENV COUNT=3
ENV SPEED=15000
ENV READ=false
ENV PROMETHEUS=127.0.0.1:29999
ENV READ_PERIOD=15000
ENV JOB_NAME=stress
ENV INSTANCE=127.0.0.1:29090

# make workdir
RUN mkdir -p /data/stress-tool
WORKDIR /data/stress-tool

COPY . /data/stress-tool

# updgrade pip and install tool
RUN pip install --upgrade pip \
    && pip install -Ur requirements.txt \
    && python ./setup.py install

ADD docker-entrypoint.sh /docker-entrypoint.sh
RUN chmod a+x /docker-entrypoint.sh

CMD ["/docker-entrypoint.sh"]
