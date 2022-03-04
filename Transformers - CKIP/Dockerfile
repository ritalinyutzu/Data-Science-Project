FROM python:3.8-buster
#建置初始容器:https://hub.docker.com/_/python

#以你在容器最外層思考，你要放什麼東西
WORKDIR /root
ADD pipeline/01.tagging_transformer.py /root
ADD data data/
ADD docs docs/
ADD model model/
ADD src src/

#東西尻進去後，開始裝套件
#opencc install:https://www.796t.com/article.php?id=10422
RUN pip install opencc-python-reimplemented
RUN pip install ckip-transformers
RUN pip install pandas
RUN pip install gensim==3.7.0
RUN apt update
RUN apt install vim


#--給一個變數叫xterm--#
#ENV TERM xterm 
ENV TZ 'Asia/Taipei'

#--entry command line--#
ENTRYPOINT [ "/bin/bash" ] 
##ENTRYPOINT [ "python",'./notebook/01.tagging_transformer.py' ] 