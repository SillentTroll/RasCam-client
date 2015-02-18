# RasCam-client
Client part of RasCam project.

Does all work of detecting the motion and uploading the image to the main server.

##Whats inside?
 - [Motion](http://www.lavrsen.dk/foswiki/bin/view/Motion/WebHome) for motion detection and image capturing
 - [flask](http://flask.pocoo.org), [nginx](http://nginx.org) and [uwsgi](http://uwsgi-docs.readthedocs.org/en/latest/) doing the web server stuff
 - [Celery](http://www.celeryproject.org) and [RabbitMQ](https://www.rabbitmq.com) for background tasks (like image upload)
 - [Supervisor](http://supervisord.org) for process control

##How does it work?
Nothing special actually. When [Motion](http://www.lavrsen.dk/foswiki/bin/view/Motion/WebHome) detects the movement, it saves a picture and executes a python script witch is going to schedule a [Celery](http://www.celeryproject.org) task for upload.
On a slow device it might take a while for image to be uploaded, as the Motion process takes all the resources.

Also Celery periodically (30 sec) checks the state of the camera, that can be changed on the [server](https://github.com/SillentTroll/rascam_server).
If the camera is deactivated on the server, then the motion detection will be paused. Activate the camera, and motion detection will resume.

##Installation
Once you have your Raspberry Pi up and running with latest [Raspbian](http://raspbian.org) release, ssh into your device and execute:
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

It means the installation went well and now your are required to configure your device.
This step must be done only after configuring the [server side](https://github.com/SillentTroll/rascam_server).
The configuration parameters are:

 - **The server URL** is the url of your server, where all the images are going to be uploaded
 - **Username and password** of the admin user, created on the main server
 - **Camera name** is going to be the unique identification of this device

If successful, the device is going to be registered and server will generate a key, that is going to be used for communication with the server.
![](https://raw.githubusercontent.com/SillentTroll/rascam_client/master/images/configured.png)

And that is pretty much it for the client side.

##Testing
You can test the installation process on your dev machine by running the installation in a [Vagrant](https://www.vagrantup.com) box:
```
vagrant up
```

