FROM fnndsc/ubuntu-python3
COPY sources.list /etc/apt/sources.list
RUN apt-get update && apt-get install -y nginx libmysqlclient-dev
COPY nginx/default.conf /etc/nginx/conf.d/default.conf
RUN mkdir /server
COPY ./ /server
WORKDIR /server
RUN ls && pip install uwsgi -i https://pypi.tuna.tsinghua.edu.cn/simple \
    && pip install -r requirements.prod.txt -i https://pypi.tuna.tsinghua.edu.cn/simple \
    && chmod +x start.sh 
COPY nginx/default.conf /etc/nginx/conf.d/default.conf
ENTRYPOINT [ "" ]
CMD ./start.sh
EXPOSE 80
