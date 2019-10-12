# omega-omion-lPS331AP
Python library to use lPS331AP chip with Omega Onion

Official docs https://files.amperka.ru/datasheets/LPS331AP-barometer.pdf

Software guidelines https://www.pololu.com/file/0J623/LPS331AP_AN4159_Hardware_and_software_guidelines.pdf

# Overview

This library contains a class lPS331AP with 3 public methods:
* <b>get_temperature</b> in Celsius degrees
* <b>get_pressure</b> in millibars
* <b>custom</b> for custom interaction with the chip
And a dictionary <b>r_a_m</b> with registers adresses map
# How to use

Firstly, You need to install i2c
opkg update
opkg install pyOnionI2C

Secondly, you need to download <b>LPS331AP.py</b> to your project folder

Thirdly, you need to import LPS331AP class from LPS331AP.py, for example
<p>from LPS331AP import LPS331AP as lps

By default, an object of LPS331AP is initialized with address <b>0x5c</b> and with high precision.
