FROM base_face_recognition:latest
LABEL maintainer="PedroHenriqueBraga <pedrohenriquebraga735@gmail.com>"

EXPOSE 5000

COPY ./src /root/face_recognition
RUN mkdir /modelset
RUN mkdir /dataset
VOLUME /modelset
VOLUME /dataset

WORKDIR /root/face_recognition

CMD python3 app.py