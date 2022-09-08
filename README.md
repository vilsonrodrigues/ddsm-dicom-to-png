# DDSM TO PNG
This script help to convert DDSM Dataset DICOM (medical format) to .png 

## Download Database

Following steps in https://wiki.cancerimagingarchive.net/display/Public/CBIS-DDSM 

The files are storages in directories. A common structure is:

manifest-1657064287305\CBIS-DDSM\Calc-Test_P_00038_LEFT_CC\08-29-2017-DDSM-NA-96009\1.000000-full mammogram images-63992\1-1.dcm

## Execute Script

#### Clone

> git clone https://github.com/vilsonrodrigues/ddsm-dicom-to-png.git

> cd ddsm-dicom-to-png

#### Isolate Enviroment

> pip install virtualenv

> virtualenv env-ddsm

###### Windows CMD case:

> cd env-ddsm

> cd Scripts

> activate

###### Linux Terminal case:

> source env-ddsm/bin/activate

#### Install Requirements

> pip install -r requirements.txt

#### Convert

> python save_dicom_as_png.py

# Make Dataset with One View

From Dataset-DDSM-png this script make a dataset using full mammograms. He apply zero-padding and resize. Split in malignant and benign. 

> python padding_resize_split_dataset.py oneView <hidth> <weight>


