ARG IMAGE=robotastic/trunk-recorder:latest

FROM ${IMAGE}

# add requests to python
RUN apt update && export DEBIAN_FRONTEND=noninteractive && \ 
    apt install -y python3-pip libpaho-mqtt-dev libpaho-mqtt1.3  libpaho-mqttpp-dev libpaho-mqttpp3-1 && \
    pip install requests paho-mqtt  && \
    rm -rf /var/lib/apt/lists/*
    
WORKDIR /build

RUN git clone https://github.com/taclane/trunk-recorder-mqtt-status

# ugly hack to build the plugin. the path in the container isnt in the sub directory /usr/local/lib/trunk-recorder
# instead its in /usr/local/lib so we just surgically remove the path from the CMakeLists
WORKDIR /build/trunk-recorder-mqtt-status
RUN sed -i 's!trunk-recorder/!!g' CMakeLists.txt

WORKDIR /build/trunk-recorder-mqtt-status/build
RUN cmake .. && make install

#cleanup
WORKDIR /
RUN rm -rf /build

WORKDIR /app