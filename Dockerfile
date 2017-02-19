FROM ubuntu:latest

# Set the file maintainer (your name - the file's author)
MAINTAINER Ray Alez

# Set env variables used in this Dockerfile (add a unique prefix, such as DOCKYARD)
ENV DOCKYARD_SRC=nexus
# Directory in container for all project files
ENV DOCKYARD_SRVHOME=/home
# Directory in container for project source files
ENV DOCKYARD_SRVPROJ=/home/nexus
# Update the default application repository sources list

RUN apt-get update
RUN apt-get install -y python python-dev python-pip supervisor nginx libpq-dev libcurl4-openssl-dev
RUN apt-get install -y libtiff5-dev libjpeg8-dev zlib1g-dev libfreetype6-dev liblcms2-dev libwebp-dev tcl8.6-dev tk8.6-dev python-tk


# Create application subdirectories
WORKDIR $DOCKYARD_SRVHOME
RUN mkdir media static logs
VOLUME ["$DOCKYARD_SRVHOME/media/", "$DOCKYARD_SRVHOME/logs/"]

ENV SECRET_KEY 7-pwxu4=a0th_s$)8)#z5f-^jlsn_^rg@l+r6$b0)!yfji6m13
ENV ACCESS_TOKEN loyZ-Xv74V4AAAAAAAAHofK10zIpP3gK-p1tLJmpOLNFjtF10Q4w0pQYGk-AD2ly
ENV PG_USERNAME nexus
ENV PG_PASS nexus

COPY $DOCKYARD_SRC $DOCKYARD_SRVPROJ
# Install Python dependencies
RUN pip install -r $DOCKYARD_SRVPROJ/requirements.txt
RUN pip install uwsgi

RUN echo "daemon off;" >> /etc/nginx/nginx.conf
COPY nginx-app.conf /etc/nginx/sites-available/default
COPY supervisor-app.conf /etc/supervisor/conf.d/ 
COPY uwsgi.ini $DOCKYARD_SRVPROJ
COPY uwsgi_params $DOCKYARD_SRVPROJ
# Port to expose
EXPOSE 8000

# Copy entrypoint script into the image
WORKDIR $DOCKYARD_SRVPROJ

CMD ["supervisord", "-n"]
