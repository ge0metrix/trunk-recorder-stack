ARG IMAGE=robotastic/trunk-recorder:latest

FROM ${IMAGE}

# add requests to python
RUN apt update && export DEBIAN_FRONTEND=noninteractive && \ 
    apt install -y python3-pip libpaho-mqtt-dev libpaho-mqtt1.3  libpaho-mqttpp-dev libpaho-mqttpp3-1 && \
    pip install requests  && \
    rm -rf /var/lib/apt/lists/*
    
WORKDIR /build

RUN git clone https://github.com/robotastic/trunk-recorder-mqtt-status.git

WORKDIR /build/trunk-recorder-mqtt-status/build

RUN cmake .. && make install

WORKDIR /app