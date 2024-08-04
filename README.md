# RetroFreak Toolkit

This is a toolkit intended to help players root their RetroFreak console to get more features out of it.

The RetroFreak has an rk3066 SoC and uses the Rockchip image format for updates; these updates can be modified and repackaged using imgRePackerRK.

##### Requirements:
* Python 3
* Pycryptodomex >= 3.9.0

##### RetroFreak.py
A script to unpack updates for the RetroFreak that you can download from the official website [here](https://www.cybergadget.co.jp/support/retrofreak/en/update.html).

##### RetroFreakROM.py
This file is used to encrypt/decrypt ROM's so you can play them on your RetroFreak or PC.

##### An example to enable ADB (build.prop inside system.img):
```
persist.service.adb.enable=1                                                    
persist.service.debuggable=1
persist.sys.usb.config=adb
```

##### RetroFreakROM.py Usage:
```
usage: RetroFreakROM.py [-h] [-o O] [-s SERIAL] ifile

A script to encrypt/decrypt ROM's to/from the RetroFreak

positional arguments:
  ifile                 The ROM to read from

optional arguments:
  -h, --help            show this help message and exit
  -o O                  The ROM file to write to
  -s SERIAL, --serial SERIAL
                        The serial number you want to use
```

##### Credits:
> [RedScoripoXDA](https://forum.xda-developers.com/member.php?u=4582467) for [imgRePackerRK](https://forum.xda-developers.com/showthread.php?t=2257331)
