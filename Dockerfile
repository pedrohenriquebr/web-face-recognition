FROM base_face_recognition:latest
LABEL maintainer="PedroBraga <pedrohenriquebraga735@gmail.com>"

EXPOSE 5000

RUN mkdir /modelset
RUN mkdir /dataset
VOLUME ["/dataset"]
VOLUME ["/modelset"]

COPY ./src /root/face_recognition
COPY ./requirements.txt /root/face_recognition/requirements.txt

WORKDIR /root/face_recognition

RUN pip3 install -r requirements.txt

CMD python3 app.py