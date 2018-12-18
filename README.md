# SecLab Spotify Webpage

This is a [Flask](http://flask.pocoo.org) app to run the SecLab Spotify Webpage

===================

## Prerequisites
* A Raspberry Pi
* Python 3
* Pip3
* Raspotify (installed from https://github.com/dtcooper/raspotify)

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

1. Create a separate link for each file from etc/systemd/system/ into /etc/systemd/system/
```bash
sudo ln etc/systemd/system/spotipi.service /etc/systemd/system/spotipi.service
sudo ln etc/systemd/system/spotipi_script.service /etc/systemd/system/spotipi_script.service
sudo ln etc/systemd/system/spotipi_script.timer /etc/systemd/system/spotipi_script.timer
```
2. Edit the system service configuration files as needed to point to the correct directories and use the correct arguments to run script.sh.
3. Start and enable the services on boot with 
```bash
sudo systemctl start spotipi.service
sudo systemctl enable spotipi.service
sudo systemctl start spotipi_script.service
sudo systemctl enable spotipi_script.service
sudo systemctl start spotipi_script.timer
```
4. Create a link from etc/systemd/system/spotipi.service into /etc/nginx/sites-available/spotipi
```bash
sudo ln etc/nginx/sites-available/spotipi /etc/nginx/sites-available/spotipi
```
5. Create a symlink in sites-enabled to the site configuration file and reload nginx.
```bash
sudo ln -s /etc/nginx/sites-available/spotipi /etc/nginx/sites-enabled/spotipi
```
6. Edit the nginx configuration file as needed to have uwsgi pointing to the correct directory.
7. Add the following lines to your user crontab:
```bash
45 * * * * rm auth_token; authtoken
00 00 * * * rm raspotify.log; touch raspotify.log
```
8. The site should now be live at the ip of your pi.
