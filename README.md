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
#### Required flags:
  * -1: detector (image): isolate objects in an image
  * -2: detector (video): isolate objects in real time camera feed or video
  * -3: mapper: object detection in a general location or address using randomized sampling methods and streetview images.
#### Additional flags:
  * -s: search for only a specific type of object
  * -h: for more accurate, but slower detection (only for video detection)

### Detector (image)
  Welcome to Detector (image). This program can take in an image and use ML based object detection methods to find and label objects within an image. Possible object types are found within labels.txt. The image can be stored in either in a mongod database or locally  in a specified directory.
  Methods related to this program can be found in item_detector.py.
  Example usage:
  ```
  $ python3 scouter.py -1
  $ python3 scouter.py -1 -s
  ```
### Detector (video)
  Welcome to Detector (video). This program is similar to Detector (image), using ML based object detection methods to find and label objects within an image. The difference is that this program detects image throughout a video, which can be in real time or a video file.
  Methods related to this program can be found in item_detector.py.
  Example usage:
  ```
  $ python3 scouter.py -2 -s
  $ python3 scouter.py -2 -sh
  ```
### Mapper:
  Welcome to Mapper. This program is a combination of the object detection methods, a mongod db, and location/streetview apis. When a user  queries for a location, a map of all possible locations matching the query are shown with dots displayed at each location where some object was detected. The map can also be configured to show only places where specific object types were found. Images of each match are shown as well and all found data is securely stored in a mongodb.
  Methods related to this program can be found in map.py, streetview.py, item_detector.py.
  Example usage:
  ```
  $ python3 scouter.py -3
  $ python3 scouter.py -3 -s
  ```

  Database object keys:
     * location
     * type
     * confidence
     * image
     * shape
     * dtype
     * meta
     * direction
     * object_count
     * date_requested
     * author

### Authors
* Joshua Ren

### Acknowledgments:
[arunponnusamy](https://github.com/arunponnusamy/cvlib) for his work on cvlib, which was one of the object detection methods utilitized.
