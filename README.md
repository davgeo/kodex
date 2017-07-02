# Kodex
A web browser UI for Kodi which allows easy control of multiple Kodi instances from a single location.

Kodex is ideal for Kodi setups which have multiple instances that share a common library.

e.g. A kodi setup where there is one kodi instance in the main living room and one instance in the kitchen sharing a common MySQL library database.

Kodex should be hosted on the same location that hosts the MySQL library and/or the Kodi media files. This could either be one of the Kodi instances or on a separate device (e.g. Network Attached Storage machine).

## Deployment
### Docker
The simplest deployment is to run the containerised version from Docker. To do this install Docker (see https://www.docker.com/ for more info) and execute the follow:
- docker run -d -p &lt;PORT>:8000 -v &lt;HOST_DIR>:/app/kodex/persistent davgeo/kodex:v1.0

where &lt;PORT> should be replaced with the port you want to use and &lt;HOST_DIR> a folder on the host filesystem where the kodex container will store persistent files.

### Manual
Alternatively you can deploy manually by following these steps:
- Ensure your target host server has python 3.4 or later installed.
- Download Kodex source onto host server.
- Install third party python packages using the requirements file: `pip install -r requirements.txt`
- In kodex directory run "python manage.py migrate"
- Host Kodex using appropriate web server or run "python manage.py runserver 0.0.0.0:8000" to use the django dev server on port 8000.
- Navigate to web host IP, add Kodi servers and enjoy!

A helper script exists in kodex/helper which provides boot start, stop and status functionality for running kodex using Gunicorn as the web server (http://gunicorn.org/).

_Note: If pip is not available in your python install it can be downloaded using the get-pip script (google python pip to find this and for more info)_

## Hotkeys
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
On top of the tools and packages listed above Kodex is making use of a number of other third-party libraries.

- jQuery
- bootstrap
- jquery ui
- Font awesome
- Python Django package
- Python dj_static package
- Python requests package

A massive thank you to all those who have worked on any of the supporting libraries or tools used for this project.

## Screenshots

### TV panel
![](https://raw.githubusercontent.com/davgeo/kodex/master/screenshots/kodex_tv.jpg "TV panel")

### Config
![](https://raw.githubusercontent.com/davgeo/kodex/master/screenshots/kodex_config.jpg "Config")
