FROM ubuntu:22.04

RUN apt update && apt install -y python3 python3-pip git ffmpeg && git clone https://github.com/TheGreatCodeholio/icad_tone_detection_api /icad

WORKDIR /icad

RUN pip3 install -r requirements.txt

EXPOSE 8002

CMD [ "python3", "app.py" ]
