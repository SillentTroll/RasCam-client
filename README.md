# RasCam-client
Client part of RasCam project.

Does all work of detecting the motion and uploading the image to the main server.

##Whats inside?
 - [Motion](http://www.lavrsen.dk/foswiki/bin/view/Motion/WebHome) for motion detection and image capturing
 - [flask](http://flask.pocoo.org), [nginx](http://nginx.org) and [uwsgi](http://uwsgi-docs.readthedocs.org/en/latest/) doing the web server stuff
 - [Celery](http://www.celeryproject.org) and [RabbitMQ](https://www.rabbitmq.com) for background tasks (image upload)
 - [Supervisor](http://supervisord.org) for process control
 
##Installation
Once you have your Raspberry Pi up and running, ssh into your device and execute:
```
mkdir /var/www/
cd /var/www/
git clone https://github.com/SillentTroll/rascam_client.git
mv rascam_client app
cd app
./install.sh
```
It might take some time to install. When finished, open the browser and go to your Raspberry Pi IP address.
You should see a screen like this:
![](https://raw.githubusercontent.com/SillentTroll/rascam_client/master/images/first_config.png)

It means the installation went well and now your are required to configure your device with:

 - **The server URL** is the url of your server, where all the images are going to be uploaded
 - **Username and password** of the admin user, created on the main server
 - **Camera name** ig going to be the identification of this device

If successful, the device is going to be registered and server will generate a key, that is going to be used for communication with the server.
![](https://raw.githubusercontent.com/SillentTroll/rascam_client/master/images/configured.png)

And that is pretty much it for the client side.

##Testing
You can test the installation process on your dev machine by running the installation in a [Vagrant](https://www.vagrantup.com) box:
```
vagrant up
```

