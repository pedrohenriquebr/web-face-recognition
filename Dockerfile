FROM base_face_recognition:latest
LABEL maintainer="PedroHenriqueBraga <pedrohenriquebraga735@gmail.com>"

EXPOSE 5000

COPY ./src /root/face_recognition
COPY ./modelset/ /modelset

WORKDIR /root/face_recognition

CMD python3 app.py