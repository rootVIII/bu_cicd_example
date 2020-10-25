FROM ubuntu:18.04


# Build the Dockerfile from within the project's directory:
# docker build -t bu_cicd_example:latest .


# Run the container with the webapp:
# docker run -d -it -p 80:80 bu_cicd_example


# visit http://<hostname> or http://<hostname>:80 from
# browser or any device's browser on your network


# To enter the running container for troubleshooting
# and logs (/var/log/apache2/error.log)
# docker exec -it <container id> /bin/bash


RUN apt-get update && apt-get install -y apache2 \
    libapache2-mod-wsgi-py3 \
    build-essential \
    python3 \
    python3-dev \
    python3-pip \
    vim

RUN apt-get clean

# Declare the working directory inside container
WORKDIR /var/www/bu_cicd_example

# Copy over and install the requirements
COPY . /var/www/bu_cicd_example/
RUN pip3 install --proxy http://proxy.statestr.com -r /var/www/bu_cicd_example/requirements.txt

# Copy over the apache configuration file and enable the site
COPY ./flask_apache.conf /etc/apache2/sites-available/flask_apache.conf

# Remove symlink from sites-enabled/ for default config: 000-default.conf
RUN a2dissite 000-default.conf

# Add a symlink flask_apache.config from sites-enabled/ to sites-available/
RUN a2ensite flask_apache.conf

EXPOSE 80

# Make all project files owned by user:group www-data:www-data
# (CentOS/RH uses user:group apache:apache)
RUN chown -R www-data:www-data /var/www/bu_cicd_example


# Start the Apache webserver in fg for Docker only
# (use 'service apache2 start|stop|restart' inside container when troubleshooting)
CMD  /usr/sbin/apache2ctl -D FOREGROUND


# USEFUL COMMANDS


# View or remove current images:
# docker image ls | rm


# View running containers:
# docker container ls


# Stop/Remove a running container:
# docker container stop <container ID>
# docker container rm <container ID>


# Clean up a unused and dangling images or stopped containers
# docker system prune
# docker container prune
