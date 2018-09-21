# SecLab Spotify Webpage

This is a [Flask](http://flask.pocoo.org) app to run the SecLab Spotify Webpage

===================

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

1. Copy spotipi.service to /etc/systemd/system/
2. Start and enable the service on boot with 
```bash
sudo systemctl start spotipi
sudo systemctl enable spotipi
```
3. Copy the nginx configuration file to /etc/nginx/sites-available/spotipi
4. Create a symlink in sites-enabled to the site configuration file and reload nginx.
5. The site should now be live at the ip of the pi/server.
