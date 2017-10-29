FROM tiangolo/uwsgi-nginx-flask:python3.6

ENV JAVA_VER 8
ENV JAVA_HOME /usr/lib/jvm/java-8-oracle

RUN echo 'deb http://ppa.launchpad.net/webupd8team/java/ubuntu trusty main' >> /etc/apt/sources.list && \
    echo 'deb-src http://ppa.launchpad.net/webupd8team/java/ubuntu trusty main' >> /etc/apt/sources.list && \
    apt-key adv --keyserver keyserver.ubuntu.com --recv-keys C2518248EEA14886 && \
    apt-get update && \
    echo oracle-java${JAVA_VER}-installer shared/accepted-oracle-license-v1-1 select true | sudo /usr/bin/debconf-set-selections && \
    apt-get install -y --force-yes --no-install-recommends oracle-java${JAVA_VER}-installer oracle-java${JAVA_VER}-set-default && \
    apt-get clean && \
    rm -rf /var/cache/oracle-jdk${JAVA_VER}-installer

RUN update-java-alternatives -s java-8-oracle

RUN echo "export JAVA_HOME=/usr/lib/jvm/java-8-oracle" >> ~/.bashrc

COPY htpasswd /etc/nginx/htpasswd
COPY ./nginx.conf /etc/nginx/conf.d/

COPY ./app /app

COPY requirements.txt /app/
RUN pip install -r /app/requirements.txt

WORKDIR /app

COPY w2g_entrypoint.sh /w2g_entrypoint.sh
RUN chmod +x /w2g_entrypoint.sh

ENTRYPOINT ["/w2g_entrypoint.sh"]

CMD ["/usr/bin/supervisord"]