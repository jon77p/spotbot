# SecLab Spotify Webpage

This is a [Flask](http://flask.pocoo.org) app to run the SecLab Spotify Webpage

===================

## Prerequisites
* Python 3
* Pip3
* Librespot

## Running the app (development environment)

To run the site, install virtualenv on your machine with

```bash
pip install virtualenv
```

create a new virtualenv in the root of the git repository and activate it with 

```bash
virtualenv .
source bin/activate
```

install the required pip packages with

```bash
pip install -r requirements.txt
```

And finally, run the app with

```bash
python app.py
```

then go to [localhost:3000](localhost:3000)

## For production

1. Create a separate symlink for each file from etc/systemd/system/ into /etc/systemd/system/
```bash
sudo ln -s etc/systemd/system/librespot.service /etc/systemd/system/librespot.service
sudo ln -s etc/systemd/system/spotbot.service /etc/systemd/system/spotbot.service
sudo ln -s etc/systemd/system/spotbot_script.service /etc/systemd/system/spotbot_script.service
sudo ln -s etc/systemd/system/spotbot_script.timer /etc/systemd/system/spotbot_script.timer
```
2. Edit the system service configuration files as needed to point to the correct directories and use the correct arguments to run script.sh.
3. Start and enable the services on boot with 
```bash
sudo systemctl start librespot.service
sudo systemctl enable librespot.service
sudo systemctl start spotbot.service
sudo systemctl enable spotbot.service
sudo systemctl start spotbot_script.service
sudo systemctl enable spotbot_script.service
sudo systemctl start spotbot_script.timer
```
4. Create a symlink from etc/nginx/sites-available/spotbot into /etc/nginx/sites-available/spotbot
```bash
sudo ln -s etc/nginx/sites-available/spotbot /etc/nginx/sites-available/spotbot
```
5. Create a symlink in sites-enabled to the site configuration file and reload nginx.
```bash
sudo ln -s /etc/nginx/sites-available/spotbot /etc/nginx/sites-enabled/spotbot
```
6. Edit the nginx configuration file as needed to have uwsgi pointing to the correct directory.
7. Add the following lines to your user crontab:
```bash
45 * * * * rm auth_token; authtoken
00 00 * * * rm raspotify.log; touch raspotify.log
```
8. The site should now be live at your machine's IP address.
