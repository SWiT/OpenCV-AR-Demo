QRGifAR: QR codes overlayed with animated Gifs as an Augmented Reality demo.
==============
Copyright (C) 2015 Matthew Gary Switlik

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.

###About
This is a demo of an augmented reality concept using OpenCV, Zbar, and Python.  It scans the video source for QR codes and replaces them with animated gifs. The QR codes can then be used to play a simple game of "pong".

###Setup
You will want the OpenCV 2.4+ and Zbar 0.10+ packages installed along with their python packages. Add the animated gifs you want to the gifs/ subdirectory.

sudo apt-get install python-zbar libzbar-dev zbar-tools libopencv-dev


###Run
```
python qrgifar.py
```
