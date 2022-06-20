FROM debian:latest

RUN apt update

RUN apt install -y python3 python3-dev python3-pip python3-setuptools build-essential libssl-dev libffi-dev git

WORKDIR /tmp

RUN git clone https://github.com/radareorg/radare2

RUN radare2/sys/install.sh

# COPY radare2_5.3.1_amd64.deb /tmp

# RUN dpkg -i /tmp/radare2_5.3.1_amd64.deb

COPY requirements.txt /tmp

RUN python3 -m pip install -r requirements.txt

RUN useradd -ms /bin/bash coquilleur

USER coquilleur
WORKDIR /home/coquilleur/

COPY . coquilleur/

WORKDIR /home/coquilleur/coquilleur

ENTRYPOINT [ "python3", "coquilleur.py"]
