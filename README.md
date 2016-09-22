# RaspberryEcho

Turn your raspberry pi into a client for Amazon's Alexa service.

This is compatible with Raspberry Pi 3 (and probably 2).

# Hardware requirements

* A Raspberry Pi 3 (or 2)
* An SD Card with a fresh install of Raspbian Jessie
* An External Speaker with 3.5mm Jack
* A USB Microphone
* A push to make button connected to GPIO 26 and ground

# Software requirements

You need to obtain a set of credentials from Amazon to use the Alexa Voice service.
 
 1. login at http://developer.amazon.com/login.html
 2. Go to Alexa then Alexa Voice Service.
 3. Create a new product type as a Device and give it a name. 
 4. Create a new security profile,
 5. Under the web settings allowed origins put http://localhost:5000 and/or http://my_ip_address:5000
 6. Under return URL put http://localhost:5000/code and/or http://my_ip_address:5000

## Install Required Packages

```
sudo apt-get update
sudo apt-get upgrade
sudo apt-get install python-pip python-dev
sudo apt-get install python-alsaaudio libasound2-dev mpg123 python-alsaaudio
sudo pip install -r requirements.txt
```

## Setup the service
```
chmod +x service_raspberryecho.sh
sudo cp service_raspberryecho.sh /etc/init.d/RaspberryEcho
sudo update-rc.d RaspberryEcho defaults
touch /var/log/raspberryecho.log
```

## Authenticate
Open the *amazon.ini* and fill out the values with your credentials.

Then run,

```
python ./authenticate.py
```

## Verify

Get your IP
```
echo $(hostname -I)
```

Then, Open http://my_ip_address:5000/code

# Test it

Installation completed. At this point you can either reboot or start the service manually.

Then, press the button and talk with Alexa, she will reply back!