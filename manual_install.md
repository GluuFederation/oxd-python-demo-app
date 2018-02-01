# Manual installation

```
$ sudo su -
# add-apt-repository ppa:openjdk-r/ppa
# apt update
# apt install libssl-dev openjdk-8-jre openjdk-8-jre-headless openjdk-8-jdk openjdk-8-jdk-headless
# apt install python-pip python-dev libffi-dev git python-openssl
# pip install --upgrade setuptools
# pip install flask
# wget https://repo.gluu.org/ubuntu/pool/main/trusty-devel/oxd-server_3.1.2-9~trusty+Ub14.04_all.deb
# dpkg -i oxd-server_3.1.2-9~trusty+Ub14.04_all.deb
# exit; cd
# echo "EDIT files in /opt/oxd-server/conf/ : oxd-conf.json  oxd-default-site-config.json"
# service oxd-server start
# tail /var/log/oxd-sever.log
$ git clone https://github.com/GluuFederation/oxd-python.git
$ cd oxd-python
$ sudo python setup.py install
$ cd ..
$ git clone https://github.com/GluuFederation/oxd-python-demo-app.git
$ cd oxd-python-demo-app/uma_rs
$ sudo su -
# apt install apache2
# a2enmod cgi
# a2enmod ssl
# a2dissite 000-default
# a2ensite default-ssl
# service apache2 restart
```
