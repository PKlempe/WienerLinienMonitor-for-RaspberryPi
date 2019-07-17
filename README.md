# "Wiener Linien Monitor" for Raspberry Pi
A Python 3 script for using your Raspberry Pi as a departure board for stations of your choice inside Vienna.

## Requirements
* Request an API key [here](https://www.wien.gv.at/formularserver2/user/formular.aspx?pid=3b49a23de1ff43efbc45ae85faee31db&pn=B0718725a79fb40f4bb4b7e0d2d49f1d1).  
* Get RBL numbers [here](https://till.mabe.at/rbl/).
### Hardware
* Raspberry Pi&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;- Buy one [here](https://www.raspberrypi.org/products/).  
* Adafruit LCD Keypad Kit&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;- Buy one [here](https://www.adafruit.com/category/808).

## Usage
```
python3 wl_monitor.py [-h] [-t time] -k apikey rbl [rbl ...]

arguments:
  -k, --key=	  API key
  rbl           RBL number

optional arguments:
  -h, --help	  Show this help
  -t, --time=	  refresh time in seconds (Default: 10)
```


## Photos
![](https://raw.githubusercontent.com/mabe-at/WL-Monitor-Pi/master/PHOTOS/photo1.jpg)
![](https://raw.githubusercontent.com/mabe-at/WL-Monitor-Pi/master/PHOTOS/photo2.jpg)
![](https://raw.githubusercontent.com/mabe-at/WL-Monitor-Pi/master/PHOTOS/photo3.jpg)



Data Source: City of Vienna (Stadt Wien) - https://data.wien.gv.at
