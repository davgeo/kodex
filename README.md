# Kodex
A web-based control interface for Kodi which allows easy control of multiple Kodi instances
from a single point.

Kodex is ideal for Kodi setups which have multiple instances that share a common library.

e.g. A kodi setup where there is one kodi instance in the main living room and one instance in
the kitchen sharing a common MySQL library database.

Kodex should be hosted on the same location that hosts the MySQL library and/or the Kodi media files.
This could either be one of the Kodi instances or on a separate device (e.g. Network Attached Storage machine).

## Requirements
This is a python django based web application and requires the following packages:
- Python 3.4+
- Python Django package
- Python Requests package
- Python jsonrpcclient package
- Python dj_static package

The django runserver can be used to temporarily test this application however
a proper web sever should be used for final depoyment. I recommend using Gunicorn:
- Python Gunicorn (http://gunicorn.org/)

And of course to have a purpose at least one Kodi instance is required:
- Kodi v13 or later

## Deployment
- Ensure your target host server has python 3.4 or later installed.
- Install third party python packages (see below for more info on doing this)
- Download Kodex source onto host server
- In kodex directory run "python manage.py migrate"
- Host Kodex using appropriate web server (e.g. gunicorn)
- Navigate to web host IP, add Kodi servers and enjoy!

A helper script exists in kodex/helper which provides boot start/stop/status
functionality for running kodex on Gunicorn.

The third-party package can be installed using pip
  e.g. python -m pip install jsonrpcclient

If pip is not available in your python install it can be downloaded
using the get-pip.py script (google python pip to find this and for more info)

### Hotkeys
When a Kodi server is selected in the web interface various keyboard controls
can be used:

| key           | function         |
|:-------------:|:----------------:|
| spacebar      | play/pause       |
| +             | volume up        |
| -             | volume down      |
| m             | mute             |
| s             | toggle subtitles |


## Requests, Issues, Bugs or Suggestions
Add any feature requests, issues, bugs or suggestions here: https://github.com/davgeo/kodex/issues

Please give as much detail as possible.

## Third-party credit
On top of the additional python packages listed above Kodex is making use of a
number of other third-party libraries.

- jQuery
- bootstrap
- jquery ui
- Font awesome

A massive thank you to all those who have worked on any of the supporting libraries
for this project.

Also thanks to other Kodi web interface projects (e.g. Chorus) which gave inspiration to this project.

## Screenshots
