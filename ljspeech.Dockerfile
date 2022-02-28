FROM tensorflow/tensorflow:1.8.0-py3
RUN apt-get update && apt-get install -y python3 python3-pip git llvm-8
RUN ln -s /usr/bin/llvm-config-8 /usr/bin/llvm-config

RUN git clone https://github.com/keithito/tacotron /root/tacotron
WORKDIR /root/tacotron
RUN pip3 install -r requirements.txt

RUN mkdir /root/tacotron_models
RUN curl https://data.keithito.com/data/speech/tacotron-20180906.tar.gz -k --output /root/tacotron_models/tacotron-20180906.tar.gz
WORKDIR /root/tacotron_models
RUN tar x --file /root/tacotron_models/tacotron-20180906.tar.gz
WORKDIR /root/tacotron

CMD python3 /root/tacotron/demo_server.py --checkpoint /root/tacotron_models/tacotron-20180906/model.ckpt