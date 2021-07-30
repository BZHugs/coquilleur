FROM debian:latest

RUN apt update

RUN apt install -y python3 python3-dev python3-pip python3-setuptools build-essential libssl-dev libffi-dev

COPY radare2_5.3.1_amd64.deb /tmp

RUN dpkg -i /tmp/radare2_5.3.1_amd64.deb

RUN useradd -ms /bin/bash coquilleur

USER coquilleur
WORKDIR /home/coquilleur/

# RUN mkdir coquilleur

COPY . coquilleur/

WORKDIR /home/coquilleur/coquilleur

RUN python3 -m pip install -r requirements.txt

ENTRYPOINT [ "python3", "coquilleur.py"]
