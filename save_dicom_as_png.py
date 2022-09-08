import os
import cv2
from pydicom import dcmread

def check_image_type(folder_4):
    """ This function check if image is
        * full mammogram (side view)
        * cropped (upper view)
        * ROI mask (segmentation)
    Args:
        folder_4: (str) level 4 in deeper from folder
    Returns:
        (str) type image
    """
    if "full mammogram" in folder_4:
        return "full_mammogram"
    elif "cropped" in folder_4:
        return "cropped"
    elif "ROI mask" in folder_4:
        return "ROI_mask"
    else:
        return  ""

def create_directories(dataset_directory):
    os.mkdir(dataset_directory)
    for train_test in ["train","test"]:            
        path_train_test = dataset_directory+f"/{train_test}"
        os.mkdir(path_train_test)
        print(f"Path {path_train_test} created")
        for calc_mass in ["calc","mass"]:
            path_calc_mass = dataset_directory+f"/{train_test}/{calc_mass}"
            os.mkdir(path_calc_mass)
            print(f"Path {path_calc_mass} created")
            for full_cropped_roi in ["full_mammogram","cropped","ROI_mask"]:
                full_path = dataset_directory+f"/{train_test}/{calc_mass}/{full_cropped_roi}" 
                os.mkdir(full_path)
                print(f"Path {full_path} created")
    return


if __name__ == "__main__":
    """
    Example:
    manifest-1657064287305\CBIS-DDSM\Calc-Test_P_00038_LEFT_CC\08-29-2017-DDSM-NA-96009\1.000000-full mammogram images-63992\1-1.dcm
            level 0     /    level 1      /   level 2              /     level 3            /          level 4       /       level 5
    """
    
    # Create directory to Dataset
    dataset_directory = "Dataset-DDSM-png"
    create_directories(dataset_directory)
    print(" -------------------------------------")
    print("Start Extraction")
    for folder_0 in os.listdir(): # manifest-1657064287305 
        if folder_0 != "env-dicom" and os.path.isdir(folder_0):
            for folder_1 in os.listdir(folder_0): # CBIS-DDSM
                path_level1 = f"{folder_0}/{folder_1}"
                if os.path.isdir(path_level1):
                    for folder_2 in os.listdir(path_level1): #  Calc-Test_P_00038_LEFT_CC
                        path_level2 = f"{folder_0}/{folder_1}/{folder_2}"
                        if os.path.isdir(path_level2):
                            for folder_3 in os.listdir(path_level2): # 08-29-2017-DDSM-NA-96009
                                path_level3 = f"{folder_0}/{folder_1}/{folder_2}/{folder_3}"
                                if os.path.isdir(path_level3):
                                    for folder_4 in os.listdir(path_level3): # 1.000000-full mammogram images-63992
                                        path_level4 = f"{folder_0}/{folder_1}/{folder_2}/{folder_3}/{folder_4}"
                                        if os.path.isdir(path_level4):
                                            for dcm_file in os.listdir(path_level4): # 1-1.dcm   
                                                if dcm_file.endswith(".dcm"):    
                                                    path_level5 = f"{folder_0}/{folder_1}/{folder_2}/{folder_3}/{folder_4}/{dcm_file}"
                                                    ds = dcmread(path_level5) # Read file
                                                    type_image = check_image_type(folder_4) # Check type
                                                    train_or_test = "train" if "Training" in folder_2 else "test"
                                                    calc_or_mass = "calc" if "Calc" in folder_2 else "mass"
                                                    path_image_in_dataset = f"{dataset_directory}/{train_or_test}/{calc_or_mass}/{type_image}/{folder_2}.png"
                                                    cv2.imwrite(path_image_in_dataset, ds.pixel_array) # Write as a png
                                                    print(f"Write {path_image_in_dataset}")                                                                  