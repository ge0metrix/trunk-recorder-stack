ARG IMAGE=robotastic/trunk-recorder:latest

FROM ${IMAGE}

# add requests to python
RUN apt update && export DEBIAN_FRONTEND=noninteractive && \ 
    apt install -y python3-pip && pip install requests  && rm -rf /var/lib/apt/lists/*

WORKDIR /app