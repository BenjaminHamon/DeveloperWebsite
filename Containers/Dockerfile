# cspell:words a2enmod  libapache2 venv virtualenv wsgi

FROM debian:12



# Install Apache web server (httpd)
RUN apt update && apt install --yes apache2 libapache2-mod-wsgi-py3

# Enable apache modules
RUN a2enmod headers proxy proxy_http ssl wsgi

# Copy apache configuration
COPY Containers/Configuration/apache2.conf /etc/apache2/apache2.conf

# Remove apache default websites
RUN rm /etc/apache2/sites-available/* /etc/apache2/sites-enabled/*

# Set up default website
COPY Containers/Configuration/default.conf /etc/apache2/sites-available/default.conf
RUN ln --symbolic /etc/apache2/sites-available/default.conf /etc/apache2/sites-enabled/default.conf

# Validate apache configuration
RUN apache2ctl -t -f /etc/apache2/apache2.conf



# Install Python
RUN apt update && apt install --yes python3 python3-pip python3-venv

# Copy the application sources
COPY Sources /srv/application

# Set up the python virtual environment
RUN python3 -m venv /srv/application/.venv
RUN /srv/application/.venv/bin/python -m pip install --upgrade pip wheel
COPY pip.conf /srv/application/.venv/pip.conf

# Install the application
RUN /srv/application/.venv/bin/python -m pip install --upgrade /srv/application/website

# Copy the application scripts
COPY Containers/Scripts /srv/scripts

# Copy the website configuration for apache
COPY Containers/Configuration/website.conf /etc/apache2/sites-available/default.conf

# Validate apache configuration
RUN apache2ctl -t -f /etc/apache2/apache2.conf



# Run apache
EXPOSE 80
CMD [ "apache2ctl", "-DFOREGROUND" ]
