FROM tensorflow/tensorflow:1.8.0-py3
RUN apt-get update && apt-get install -y python3 python3-pip git llvm-8
RUN ln -s /usr/bin/llvm-config-8 /usr/bin/llvm-config

RUN git clone https://github.com/keithito/tacotron /root/tacotron
WORKDIR /root/tacotron
RUN git reset --hard 8edcd55b3f08f0492340e8b3ee60a693138f5473
RUN pip3 install -r requirements.txt

RUN git clone https://github.com/ArkaneCow/tacotron-models  /root/tacotron_models

CMD python3 /root/tacotron/demo_server.py --checkpoint /root/tacotron_models/mxgray_nancy/model.ckpt-250000