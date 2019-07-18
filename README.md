# "Wiener Linien Monitor" for Raspberry Pi
A Python 3 script for using your Raspberry Pi as a departure board for stations of your choice inside Vienna.

## Requirements
* Request an API key [here](https://www.wien.gv.at/formularserver2/user/formular.aspx?pid=3b49a23de1ff43efbc45ae85faee31db&pn=B0718725a79fb40f4bb4b7e0d2d49f1d1).  
* Get RBL numbers [here](https://till.mabe.at/rbl/).  (Special thanks to @mabe-at)
### Hardware
* Raspberry Pi&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;- Buy one [here](https://www.raspberrypi.org/products/).  
* Adafruit LCD Keypad Kit&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;- Buy one [here](https://www.adafruit.com/category/808).


## Usage
```
usage:
  python3 wl_monitor.py [-h] [-t time] -k apikey rbl [rbl ...]
  ./wl_monitor.py [-h] [-t time] -k apikey rbl [rbl ...]

arguments:
  -k, --key=    API key
  rbl           RBL number

optional arguments:
  -h, --help	  Show this help
  -t, --time=	  refresh time in seconds (Default: 10)
```

## Photos
| ![IMG_20190718_131042](https://user-images.githubusercontent.com/49726903/61454600-9d731e80-a961-11e9-85e0-5984d34a59e4.jpg) | ![IMG_20190718_131552](https://user-images.githubusercontent.com/49726903/61454625-ad8afe00-a961-11e9-9af5-cc08c08a1497.jpg) |
|---------------------------------------------------------------------------------------|:-------------------------------------------------------------------------------------:|
| ![IMG_20190718_132222](https://user-images.githubusercontent.com/49726903/61454637-ba0f5680-a961-11e9-959a-0beaeb0a1c9f.jpg) | ![IMG_20190718_131822](https://user-images.githubusercontent.com/49726903/61454662-c398be80-a961-11e9-9275-041177f99d5f.jpg) |



Data Source: City of Vienna (Stadt Wien) - https://data.wien.gv.at
