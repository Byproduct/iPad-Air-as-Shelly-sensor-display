# iPad Air as Shelly sensor display

Displays shelly H&T (humidity & temperature) sensor information on a html page.  
Page layout made for my 1st gen iPad Air.

Requires Python 3.

How to use:

Font (optional): download this to the same folder and rename it to "MyriadProRegular.otf"  
* https://www.fontpalace.com/font-details/myriadpro-regular/

Put the contents of this script on a server and set sensors.py to run every 10 minutes or so, for example using crontab.  

Point your tablet's browser to the generated sensors.html file.  
* The page will automatically refresh every 10 minutes. Can be adjusted in template.html.
* On an ipad you can get a full-screen browser window by first opening the page in Safari normally, then adding the page (as a shortcut) to the home screen, and then using this shortcut.

![photo](https://github.com/Byproduct/iPad-Air-as-Shelly-sensor-display/blob/main/sensors.jpg)
