#!/bin/sh
if [ `whoami` != root ]; then
    echo Please run this script as root or using sudo
    exit
fi

APP_HOME="/var/www/app"
echo "Application home is $APP_HOME"

apt-get update;
#install nginx
apt-get -y install nginx  sed python-pip python-dev uwsgi-plugin-python supervisor
#install motion
apt-get -y install motion
echo "Motion installed"

apt-get --no-install-recommends install -y python-setuptools build-essential libpq-dev ca-certificates -y;
easy_install pip;
echo "Pip installed"
#install requirements
pip install -r $APP_HOME/requirements.txt;
echo "Installed requirements"

#install rabbit-mq
apt-get install rabbitmq-server -y
echo "RabbitMQ installed"
#download from url

#copy motion config
cp $APP_HOME/motion/motion.conf /etc/motion/motion.conf
chmod 777 /etc/motion/motion.conf
sed -i "s/=no/=yes/g" /etc/default/motion

mkdir -p /var/log/app

#configure web server
rm /etc/nginx/sites-enabled/default
cp $APP_HOME/config/flask.conf /etc/nginx/sites-available/
ln -s /etc/nginx/sites-available/flask.conf /etc/nginx/sites-enabled/flask.conf

#configure supervisor
mkdir -p /var/log/supervisor
sed -i "s#APP_HOME#$APP_HOME#g" $APP_HOME/config/supervisord.conf

cp $APP_HOME/config/supervisord.conf /etc/supervisor/conf.d/supervisord.conf

service motion restart
service supervisor restart
service nginx restart

echo "Done"