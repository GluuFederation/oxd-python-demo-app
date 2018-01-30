This document outlines the instructions required for running the demo using the development
versions of oxd-server (3.1.2) and oxd-python (3.1.2-alpha)

### Install oxd-server

```sh
# install oxd-server
echo "deb https://repo.gluu.org/ubuntu/ xenial main" > /etc/apt/sources.list.d/gluu-repo.list
curl https://repo.gluu.org/ubuntu/gluu-apt.key | apt-key add -
apt-get update
apt-get install oxd-server
wget https://ox.gluu.org/maven/org/xdi/oxd-server/3.1.2.Final/oxd-server-3.1.2.Final-distribution.zip
mkdir oxd-312
mv oxd-server-3.1.2.Final-distribution.zip oxd-312/
cd oxd-312/
apt install unzip
unzip oxd-server-3.1.2.Final-distribution.zip
rm /opt/oxd-server/lib/oxd-server-jar-with-dependencies.jar
mv lib/oxd-server-jar-with-dependencies.jar /opt/oxd-server/lib/
/etc/init.d/oxd-server start
tail /var/log/oxd-server.log
```

### Edit the configuration files

Edit `/opt/oxd-server/conf/oxd-conf.json`

```
vim /opt/oxd-server/conf/oxd-conf.json
```
* Enter server name
* Enter oxd license details.
* Set `uma2_auto_register_claims_gathering_endpoint_as_redirect_uri_of_client` to `false`.

Edit `/opt/oxd-server/conf/oxd-default-site-conf.json`

```
vim /opt/oxd-server/conf/oxd-default-site-config.json
```
 
* Enter the value for `op_host` pointing to your Gluu Server 3.1.2

### Install Python, oxd-python and other dependencies

```
apt install python-pip
pip install flask pyOpenSSL
wget https://github.com/GluuFederation/oxd-python/archive/master.zip
mv master.zip oxd-python-312.zip
unzip oxd-python-312.zip
cd oxd-python-master/
python setup.py install
```

### Install Apache and configure CGI and SSL

```
apt install apache2
a2enmod cgi
a2enmod ssl
a2dissite 000-default
a2ensite default-ssl
service apache2 restart
exit
```

### Get the demo application

As non-root user

```sh
git clone https://github.com/GluuFederation/oxd-python-demo-app.git
cd oxd-python-demo-app/
cd cgi-bin/

# Enter the hostname of your application
vim constants.py

sudo python setupDemo.py
cd ../uma_rs/
nohup python app.py > uma_rs.log 2>&1 &

curl -k https://localhost:8085/api/
exit
```
