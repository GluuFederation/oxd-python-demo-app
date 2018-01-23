#!/usr/bin/env bash

APP=oxd-demo
CGI_DIR=/usr/lib/cgi-bin/
APP_DIR=/var/log/$APP
APP_CONFIG=$APP_DIR/oxd-demo.cfg

echo "Welcome to oxd-python demo app deployment. This script will deploy the demo cgi application in the current machine."
read -p "Do you wish to continue? (y/n): " DEPLOY

if [ ! "$DEPLOY" == "y" ] && [ ! "$DEPLOY" == "y" ]; then
    echo "Deployment aborted."
    exit 1
fi

echo "Setting up $APP ..."
# Ensure the system has the CGI directory
if [ ! -d $CGI_DIR ]; then
    echo "CGI directory $CGI_DIR is absent in the system. Deployment aborted."
    exit 1
fi

echo "Copying cgi scripts to $CGI_DIR ..."
cp cgi-bin/*.cgi $CGI_DIR
cp cgi-bin/*.py $CGI_DIR

echo "Creating application directory $APP_DIR ..."
mkdir -p $APP_DIR

echo "Creating oxd-python config file for $APP ..."
echo ""
read -p "> Enter the hostname of this machine (localhost): " APP_HOSTNAME
if [ -z "$APP_HOSTNAME" ]; then
    APP_HOSTNAME="localhost"
fi
echo "Setting app hostname to $APP_HOSTNAME ..."
cp cgi-bin/oxd-demo.cfg $APP_CONFIG
sed -i -- 's/www.example.com/$APP_HOSTNAME/g' $APP_CONFIG

echo "Setting up log file ..."
touch $APP_DIR/app.log

echo "Setting file permissions ..."
chmod 555 $CGI_DIR/*.cgi
chmod 777 $APP_DIR/*

echo "Done. Now you can start the access the app by visiting https://$APP_HOSTNAME/cgi-bin/home.cgi"
