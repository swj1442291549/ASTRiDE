# ASTRiDE (Automated Streak Detection for Astronomical Images)

<div align="center">
<img src="https://github.com/dwkim78/ASTRiDE/blob/master/astride/datasets/images/ASTRiDE.png">
</div>

<br/>
This package is the Python version of the streak detection pipeline ([Kim+ 2005](http://adsabs.harvard.edu/abs/2005JASS...22..385K) and [https://sites.google.com/site/dwkim78/streak-detection](https://sites.google.com/site/dwkim78/streak-detection)) originally programmed in C.

Basic idea is same with the C version, which uses a border of each object (i.e. a contour of a certain level) in a fits image to detect streaks. Nevertheless, the Python version has improved algorithm for determining whether each border  is a streak or not. For details, see the section "[How to Use ASTRiDE](#4-how-to-use-astride)".
 
The published paper title includes "High Velocity Objects", which means relatively long streaks. ASTRiDE, however, is able to detect any kind of streaks whose lengths are either short or long. That is why the acronym, ASTRiDE, does not include "High Velocity Objects". 


## Index
1. [Dependency](#1-dependency)
2. [Installation](#2-installation)
3. [Test the Installation](#3-test)
4. [How to Use ASTRiDE](#4-how-to-use-astride)
5. [Test with Crowded Field Image](#5-test-with-crowded-field-image)
6. [Application](#6-application-to-astronomical-images)

- [System Requirement](#system-requirement)
- [ChangeLog](#changelog)
- [Citation](#citation)
- [Contact](#contact)

## 1. Dependency

[Python 2.7+](https://www.python.org/) 

 * Not tested with Python 3.0+

[Numpy 1.9+](http://www.numpy.org/)
 
 * Numerical Python library.

[Scikit-image 0.11.3+](http://scikit-image.org/)
 
 * To get contour map of a fits image.

[Astropy 1.1.1+](http://www.astropy.org/)

 * For reading fits file and some utility functions.

[Matplotlib 1.5.1+](http://matplotlib.org/)

 * For plotting figures of detected streaks.

[Phoutils 0.2.1+](http://photutils.readthedocs.org/en/latest/index.html)

 * For calculating background map of a fits image.

## 2. Installation

The easiest way to install the ASTRiDE package is:

```python
pip install astride
```

Or,

```python
pip install git+https://github.com/dwkim78/ASTRiDE
```

If you do not want to install/upgrade the dependencies, execute the above commend with the ```--no-deps``` option. ASTRiDE possibly works with older version of Python and other libraries. 


Alternatively, you can download the ASTRiDE package from the Git repository as:

```python
git clone https://github.com/dwkim78/ASTRiDE

cd ASTRiDE
python setup.py install
```

You can edit ```setup.py```, if you do not want to update your own Python libraries (i.e. edit the ```install_requires``` variable).


## 3. Test

To check if ASTRiDE is correctly installed, type following commands in your Python console.

```python
from astride import test

test()
```

The command will print messages like:
```
2016-02-15 16:16:18,239 INFO - Start.
2016-02-15 16:16:18,241 INFO - Read a fits file..
2016-02-15 16:16:18,272 INFO - Search streaks..
2016-02-15 16:16:19,027 INFO - Save figures and write outputs to ./long/
2016-02-15 16:16:20,048 INFO - Done.
```

The test module will also save figures and write information of detected streaks under the "./long/" folder. In the folder, you can find two images and one text file. The two images are:

| Image name | Description |
|----:|:------------|
| all.png |  A full image with detected streaks (shown below) |
| 1.png | A zoomed image for each linked streak |

<div align="center">
<img src="https://github.com/dwkim78/ASTRiDE/blob/master/astride/datasets/images/all.png">
[ all.png ]</div>

<br/><br/>
The output text file named as "streaks.txt" contains following information.

| Column | Description |
|----:|:------------|
| ID  | Index |
| x_center, y_center  | Coordinate of the center  |
| area  | Area inside a streak  |
| perimeter  | Length of the perimeter of a streak  |
| shape_factor  | 4 * PI * area / perimeter^2 |
| radius_deviation  | Parameter to check roundness  |
| slope  | Slope of a linear line fitted to a streak  |
| intercept  | Intercept of a linear line fitted to a streak  |
| connectivity  | ID of another streak that is likely to be linked to the current streak  |


These information are accessible using the ASTRiDE Streak instance. For details, see [this section](#accessible-information-inside-the-streak-instance).


## 4. How to Use ASTRiDE? 

In this section, I will show how to use ASTRiDE to detect streaks. I will use the fits image shown in the previous section.

### Create Streak Instance

We first need to create ASTRiDE Streak instance as:

```python
from astride import Streak

streak = Streak('long.fits')
```

You can replace "long.fits" with your own fits filename. There are many options customizing the Streak instance such as:

| Options | Description |
|----:|:------------|
| bkg_box_size  | Box size for calculating a background map of a fits image. Default is 50. |
| contour_threshold  | Threshold to extract a contour map. If this value is high, then only bright streaks will be detected. Default is 3. |
| min_points  | The minimum number of data points (i.e. pixels) of each border. Default is 10. |
| shape_cut  | Empirical cut for shape factor. Default is 0.2. |
| area_cut | Empirical cut for area inside each contour |
| radius_dev_cut  | Empirical cut for radius deviation. Default is 10. |
| connectivity_angle | The maximum angle to link each streak. Default is 3. |
| output_path  | Output path to save figures and outputs. Default is the 'None', which will create a folder of the input filename. |

Although you can customize pretty much everything of the Streak instance, I recommend to leave them as they are. Some of these options are explained in the following sections.

### Detect Streaks

We can detect streaks in the fits image as:

```python

streak.detect()
```

That's it! The above one-line command will do everything needed to detect streaks, which is:

  * Background removal
    * ASTRiDE first removes background from the fits image. The background map is derived using [Phoutils](http://photutils.readthedocs.org/en/latest/index.html). It calculates the map by sigma-clipping method within the box of the size "bkg_box_size". 
  
  * Contour map
    * Using the [scikit-image](http://scikit-image.org/), ASTRiDE derives the contour map of the fits image. The level of the contour is controlled by the "contour_threshold" value, such as: contour_threshold * background standard deviation (calculated when deriving the background map). Default "contour_threshold" is 3. The following images shows all the <b>borders</b> detected using the contour map.
    
    <div align="center">
    <img src="https://github.com/dwkim78/ASTRiDE/blob/master/astride/datasets/images/all_borders.png">
    [ All the borders (color-coded) extracted using the contour map ]</div>
  
  <br/>
  * Streak determination based on the morphologies of each  border
    * As you can see from the above figure, there are many borders of star-like sources that are definitely <b>not</b> streaks. ASTRiDE removes such star-like sources by using the morphologies of each border such as:
    
| Morphology | Description |
|----:|:------------|
| Shape Factor | [Circularity](https://goo.gl/Z0Jy9z). The circularity of a circle is 1, and streak-like shape has much smaller circularity than 1. The default threshold is 0.2 (i.e. option "shape_cut") |
| Radius Deviation | An approximated deviation from roundness. Since the center of each border can be calculated, ASTRiDE calculates distances to each data point from the center. A radius is defined as the median value of the distances. ASTRiDE then calculates "roundness_deviation" as std(distances - radius) / radius. "std()" is the standard deviation. For a circle, the value is 0. The default threshold is 0.5 (i.e. option "radius_dev_cut"). |
| Area | The area inside an border must be larger than 10 pixels (i.e. option "area_cut"). |

The following figure shows the remaining two streak after these cut.
 
<div align="center">
<img src="https://github.com/dwkim78/ASTRiDE/blob/master/astride/datasets/images/two_streaks.png">
[ Two streaks after the morphology cut. The numbers are their IDs. ]</div>
  
  <br/><br/>
  * Link streaks by their slopes
    * As shown in the above image, ASTRiDE finally detected two streaks. However, these two streaks are not really separated two streaks. They seem to be one streak, but separately detected since the middle part of the streak is disconnected. This can happen for any kind of fast moving objects (e.g. meteor, satellites, etc). ASTRiDE connects (i.e. link) such streaks by their slopes derived using the linear line fitting. If their slopes are within the "connectivity_angle", and also the slope between the two centers of the two streaks are within the "connectivity_angle" with each streak, ASTRiDE determines that the two streaks are connected. This is why the "all.png" shown in the [section "Test"](#3-test) has only one red dashed-line box surrounding the two streaks. If one streak (i.e. s1) is determined to be linked with another streak (i.e. s2), s1's "connectivity" value is the index of s2. If s2 is again linked with s3, then again s2's "connectivity" is the index of s3. If s3 is not linked with any other streaks, s3's "connectivity" is -1.
     
     
Note that all the information derived during the streak detection procedures are accessible using the Streak instance 
(See [this section](#accessible-information-inside-the-streak-instance)).

### Plot Figures and Write Outputs
    
ASTRiDE provides functions to write outputs and plot figures as:

```python
streak.write_outputs()

streak.plot_figures()
```

```streak.write_outputs()``` will write an output text file, "streaks.txt", which is explained in the [section "Test"](#3-test).


```streak.plot_figures()``` will generate figures including "all.png", and an individual figure for each linked streak. A Filename of each individual file is the first index among the indices of the linked streak such as "1.png" (shown below)

<div align="center">
<img src="https://github.com/dwkim78/ASTRiDE/blob/master/astride/datasets/images/1.png"></div>


### Accessible Information Inside the Streak Instance

The streak instance - after calling "detect()" function - contains many information such as:

| Variable | Description |
|----:|:------------|
| streak.raw_image | Raw image before background removal |
| streak.background_map | Derived background map |
| streak.image | Background removed image |
| streak.raw_borders | All borders detected using a contour map |
| streak.streaks | The final list of streaks after excluding star-like sources and also after the linking (i.e. see Section [Detect Streaks](#detect-streaks)) |


Among these, ```streak.streaks``` contains a list of detected streaks. Each element has all the information that "streaks.txt" has. It also contains additional information such as:

| Variable | Description |
|----:|:------------|
| x | X coordinates of a streak |
| y | Y coordinates of a streak |
| x_min and x_max | The minimum and maximum x coordinates of a streak |
| y_min and y_max | The minimum and maximum y coordinates of a streak |

Using the above information, you can make your own figures if needed.


### 5. Test with Crowded Field Image

The example shown above used a less-crowded field image. If there are many stars in the field (i.e. crowded field), it is possible that some stars' borders are attached to other stars, which makes their borders long so that eventually look like a streak. We applied ASTRiDE to a relatively crowded field image to check how ASTRiDE works for such crowded field image. The following images show the results.
 
 <div align="center">
<img src="https://github.com/dwkim78/ASTRiDE/blob/master/astride/datasets/images/crowded_field.png">
[ Streak detection test using the crowded field image ]</div>

All the three images shown above are automatically generated by ASTRiDE. As you can see, ASTRiDE successfully excluded all the stars and detected two very short streaks that are quite hard to detect even by eyes.


### 6. Application to Astronomical Images

The following images show the application results of ASTRiDE. 

| [ESO DSS2](http://archive.eso.org/dss/dss) image | The Horsehead Nebular |
|---|---|
| <div align="center"> <img src="https://github.com/dwkim78/ASTRiDE/blob/master/astride/datasets/images/dss2.png" width="500"><br/>[ Three streaks are detected. ]</div> | <div align="center"> <img src="https://github.com/dwkim78/ASTRiDE/blob/master/astride/datasets/images/HorseHead.png" width="580"><br/>[ No streak is detected. ]</div> |


In the case of the ESO DSS2 image (left panel), ASTRiDE detected three streaks. However, only one streak (i.e. ID=2) looks like a real streak. In the following table, we show some parameters derived by ASTRiDE.

| ID | Area | Perimeter | Shape Factor | Radius Deviation |
|---:|------|-----------|--------------|------------------|
|1   | 75.1 |   74.4    | 0.17         |  0.57            |
|2   | 640.3|   360.9   | 0.06         |  0.60            |
|3   | 21.6 |   38.8    | 0.18         |  0.52            |
  
As you can clearly see, the streak with ID=2 is longer than two others, and also has a smaller shape factor than others. All these variables are accessible using the Streak instance, so you can define your own criteria according to the property and quality of your images. You can also set the threshold cut for some of these parameters when creating the Streak instance. For details, see [this section](#create-streak-instance).


In the case of the Horsehead Nebular image (right panel), it seems natural that ASTRiDE does not detect any streaks in the image.


### System Requirement
 
Any decent or even relatively old machines can run ASTRiDE as long as the machines are capable of running general Python libraries. Runtime for streak detection (i.e. wall-clock time) varies according to the size of fit images and the crowdedness of the images. In the cases of the two examples shown in the previous sections (i.e. less-crowded and crowded images), it took 0.6 sec and 2.6 sec to detect streaks using Macbook Pro 13'' equipped with 2.7 GHz Intel Core i5, 8 GB memory, and 256 GB SSD.


### Note

As you might notice, ASTRiDE does not use any source detection algorithm (e.g. Source Extractor) to distinguish stars from streaks. This is because such algorithms often find star-like-sources <b>inside</b> a streak. For instance, see the following figure.

<div align="center">
<img src="https://github.com/dwkim78/ASTRiDE/blob/master/astride/datasets/images/source_detection.png">
[ Red circles are the sources detected by a source detection algorithm (i.e. DAOFIND-like algorithm) ]</div>

<br/><br/>
Thus such source detection algorithms are not suitable to distinguish streaks from stars. One might think using the detected sources to construct streaks by somehow connecting them. Such methods, however, might not be very efficient either for 1) short streaks, or 2) crowded field.


### Logger

If you want to write log messages either to console or to disk, you can use the ASTRiDE Logger class as:

```python
from astride import Logger

logger = Logger().getLogger()

logger.debug('debug message')
logger.info('info message')
logger.warn('warn message')
logger.error('error message')
logger.critical('critical message')
```

Keep in mind that you need to generate only one logger instance through the whole processes, but not many. If you want to save log messages to a file, generate a logger instance as follows:
 
 ```python
 logger = Logger('/PATH/TO/FILE.log').getLogger()
 ```

This will send log messages to both console and a log file. Note that the path must be the absolute path.

## ChangeLog

### v0.2
 - Beta version released. 

### v0.1
 - initiate the GitHub repository.

## Citation

If you use this package for science publication, we will appreciate a citation to the paper [Kim+ 2005](http://adsabs.harvard.edu/abs/2005JASS...22..385K) and also to the current [github repository](https://github.com/dwkim78/ASTRiDE).

## Contact

If you have questions, send an email to dwkim78 at gmail. My official webpage is [sites.google.com/site/dwkim78](https://sites.google.com/site/dwkim78/).