# Kodex
A web browser UI for Kodi which allows easy control of multiple Kodi instances from a single location.

Kodex is ideal for Kodi setups which have multiple instances that share a common library.

e.g. A kodi setup where there is one kodi instance in the main living room and one instance in the kitchen sharing a common MySQL library database.

Kodex should be hosted on the same location that hosts the MySQL library and/or the Kodi media files. This could either be one of the Kodi instances or on a separate device (e.g. Network Attached Storage machine).

## Requirements
This is a python django based web application and requires the following packages:
- Python 3.4+
- Python Django package
- Python dj_static package
- Python requests package
- Python kodicontroller package

The django runserver can be used to test this application however Gunicorn is recommended for final deployment:
- Python Gunicorn (http://gunicorn.org/)

And of course to have a purpose at least one Kodi instance is required:
- Kodi v13 or later

## Deployment
- Ensure your target host server has python 3.4 or later installed.
- Download Kodex source onto host server
- Install third party python packages using the requirements file: `pip install -r requirements.txt`
- In kodex directory run "python manage.py migrate"
- Host Kodex using appropriate web server (e.g. gunicorn)
- Navigate to web host IP, add Kodi servers and enjoy!

A helper script exists in kodex/helper which provides boot start, stop and status functionality for running kodex on Gunicorn.

_Note: If pip is not available in your python install it can be downloaded using the get-pip script (google python pip to find this and for more info)_

### Hotkeys
When a Kodi server is selected in the web interface various keyboard controls can be used:

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
On top of the additional python packages listed above Kodex is making use of a number of other third-party libraries.

- jQuery
- bootstrap
- jquery ui
- Font awesome

A massive thank you to all those who have worked on any of the supporting libraries for this project.

## Screenshots

### TV panel
![alt text](https://raw.githubusercontent.com/davgeo/kodex/master/screenshots/kodex_tv.jpg "TV panel")

### Config
![alt text](https://raw.githubusercontent.com/davgeo/kodex/master/screenshots/kodex_config.jpg "Config")
