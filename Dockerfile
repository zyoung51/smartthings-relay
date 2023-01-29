FROM ubuntu:22.04
RUN apt-get update; apt-get install -y --no-install-recommends ca-certificates netbase tzdata
RUN apt-get update; apt-get install -y --no-install-recommends \
    python3 python3-prometheus-client python3-requests
ADD temp-probe.py /root/

ENTRYPOINT ["python3", "/root/temp-probe.py"]
