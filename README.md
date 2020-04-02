# Scouter
Hi! Welcome to Scouter.

### What can I do with Scouter?
Use object detection to identify over 80 types of objects in images, video, or real time using your device's camera. Plot trends using data of these objects (e.g. see where a type of object tends to go).


### Cloning from git
Navigate into the directory on your computer where you would like to place the project folder. Then type the following command to download the project.

```
$ git clone https://github.com/visininjr/scouter.git
```

### Options flags:
Example: python3 scouter.py -1 -sh
#### Main flags:
  * -1: isolate and write images of an input
  * -2: isolate images of an input type in real time or video
  * -3: write streetview images from a latitude/longitude or address
#### Additional flags:
  * -s: search for only a specific type of object
  * -h: for more accurate, but slower detection

### Authors
* Joshua Ren

### Acknowledgments:
[arunponnusamy](https://github.com/arunponnusamy/cvlib) for his work on cvlib, which was one of the object detection methods utilitized.
