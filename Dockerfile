FROM python:3.11-bullseye

RUN apt update

RUN apt install -y build-essential libssl-dev libffi-dev git

WORKDIR /tmp

RUN git clone https://github.com/radareorg/radare2

RUN radare2/sys/install.sh

# COPY radare2_5.3.1_amd64.deb /tmp

# RUN dpkg -i /tmp/radare2_5.3.1_amd64.deb

RUN useradd -ms /bin/bash coquilleur

USER coquilleur
WORKDIR /home/coquilleur/

COPY . coquilleur/

WORKDIR /home/coquilleur/coquilleur

RUN pip3 install --no-cache-dir -r requirements.txt

ENTRYPOINT [ "python3", "coquilleur.py"]
