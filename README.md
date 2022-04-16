# Virtual Painter
## What it does
An AI-based virtual painter that can be used to draw on screen with RGB colors.

## How it works
* Detects the **Index & Middle fingers**
* Detects which finger pointing up
* If **Index Finger Up (☝)** => *Draw Operation :* Draw on screen w.r.t finger's positon
* If **Index & Middle Finger Up (✌)** => *Select Operation :* Select another color from the pallete

## How to install
* Install Python 3 in you system from https://www.python.org/.
* Install the following libraries using the command : **pip install _packageName_**
  1. cv2
  2. mediapipe
  3. math
  4. numpy
  5. os
* Keep both the files along with the *pallet* folder in same directory.
* Execute the **main.py** to run the program.

## How is it built
* **Hand Detection Module** : Class containing the *methods to detect hands & hand's postion*. 
* Python's **cv2 and mediapipe** libraries : Provide the *modules and methods to get hand landmarks and draw shapes* to mark them. 

