#!/usr/bin/env bash

# Installs the package passed in if it's not installed
install () {
	package=$1
	dpkg-query -l $package &> /dev/null
	if [ $? -ne 0 ]; then
	apt-get -y install $package
	fi
}

apt-get update

# Install git
install git-core
install git

# Install Python
apt-get install -y python \
python-pip \
python-dev \
python-software-properties \
libpq-dev
apt-get update

# Install SQLite
apt-get install -y sqlite3
apt-get install -y libsqlite3-dev
	
# Install Python libraries
pip install -r /vagrant/config/requirements.txt
pip install flake8 # For local testing
pip install SQLAlchemy # Install SQLAlchemy
pip install flask-restful # Request parsing

# Install Vim
apt-get install vim

