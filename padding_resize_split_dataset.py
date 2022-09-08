"""
maximum dimensions of an image was (5386,6631)
add padding to make img become square
resize img 
"""
import os
import sys
import cv2
import pandas as pd

df_train_mass = pd.read_csv('mass_case_description_train_set.csv')
df_test_mass  = pd.read_csv('mass_case_description_test_set.csv')
df_train_calc = pd.read_csv('calc_case_description_train_set.csv')
df_test_calc  = pd.read_csv('calc_case_description_test_set.csv')

def padding(img):
    """ Make an image become square 
        get maximum dimension, subtract from dimension
        and apply padding 
    """
    h, w = img.shape[:2]
    max_dimension = max(w,h)
    padding_upper = max_dimension - h
    padding_down  = max_dimension - w    
    return cv2.copyMakeBorder(img, 
                              int(padding_upper/2), 
                              int(padding_upper/2),                                   
                              int(padding_down/2), 
                              int(padding_down/2), 
                              cv2.BORDER_CONSTANT, 
                              0)

def resize(img):    
    """ Resize image """
    width = int(sys.argv[2])
    height = int(sys.argv[3])
    h, w = img.shape[:2]
    ratio = w / h
    if h > height or w > width:
        # shrinking image algorithm
        interp = cv2.INTER_AREA
    else:
        # stretching image algorithm
        interp = cv2.INTER_CUBIC
    w = width
    h = round(w / ratio)
    if h > height:
        h = height
        w = round(h * ratio)
    return cv2.resize(img, (w, h), interpolation=interp)

def define_field_search(full_mammogram_or_cropped_or_ROI_mask:str):
    """ Define field to search in csv reference """
    if full_mammogram_or_cropped_or_ROI_mask == 'full_mammogram':
        return 'image file path'
    elif full_mammogram_or_cropped_or_ROI_mask == 'cropped':
        return 'cropped image file path'
    elif full_mammogram_or_cropped_or_ROI_mask == 'ROI_mask':
        return 'ROI mask file path'

def pathology_type(train_or_test:str, 
                mass_or_calc:str, 
                filename:str,
                full_mammogram_or_cropped_or_ROI_mask:str):
  """ Returns pathology type based on filename """
  field_to_search = define_field_search(full_mammogram_or_cropped_or_ROI_mask) 

  if mass_or_calc == 'calc' and train_or_test == 'train':
    return df_train_calc.loc[df_train_calc[field_to_search].str.contains(filename.split('.')[0]),
              'pathology'].array[0]

  elif mass_or_calc == 'calc' and train_or_test == 'test': 
    return df_test_calc.loc[df_test_calc[field_to_search].str.contains(filename.split('.')[0]),
              'pathology'].array[0]
              
  elif mass_or_calc == 'mass' and train_or_test == 'train':
    return df_train_mass.loc[df_train_mass[field_to_search].str.contains(filename.split('.')[0]),
              'pathology'].array[0]   

  elif mass_or_calc == 'mass' and train_or_test == 'test':  
    return df_test_mass.loc[df_test_mass[field_to_search].str.contains(filename.split('.')[0]),
              'pathology'].array[0]
              
def create_directories_one_view(dataset_directory:str):    
    os.makedirs(dataset_directory, exist_ok=True)
    os.makedirs(f'{dataset_directory}/train', exist_ok=True)
    os.makedirs(f'{dataset_directory}/train/benign', exist_ok=True)
    os.makedirs(f'{dataset_directory}/train/malignant', exist_ok=True)
    os.makedirs(f'{dataset_directory}/test', exist_ok=True)
    os.makedirs(f'{dataset_directory}/test/benign', exist_ok=True)
    os.makedirs(f'{dataset_directory}/test/malignant', exist_ok=True)
    print(f'Created {dataset_directory}')
    
def one_view_dataset():
    """ Make dataset based in full mammograms """
    dataset_directory = f'Dataset-DDSM-One-View_{sys.argv[2]}-{sys.argv[3]}'
    create_directories_one_view(dataset_directory)
    path_dataset_ddsm_png = 'Dataset-DDSM-png'
    print('Start split dataset One View')
    count_train = 0
    count_test  = 0
    for train_or_test in ['train','test']:
        for mass_or_calc in ['mass','calc']:
            images_path = f'{path_dataset_ddsm_png}/{train_or_test}/{mass_or_calc}/full_mammogram'                                                                          
            for filename in os.listdir(images_path):
                if filename.endswith(".png"): 
                    try:
                        fullpath = f'{images_path}/{filename}'
                        image = cv2.imread(fullpath)
                        image_padding = padding(image)
                        image_resized = resize(image_padding)
                        pathology = pathology_type(train_or_test,
                                                mass_or_calc,
                                                filename,
                                                'full_mammogram')                     
                        if pathology == 'BENIGN_WITHOUT_CALLBACK': 
                            pathology = 'BENIGN'                                                                   
                        path_img_OV = f'{dataset_directory}/{train_or_test}/{pathology.lower()}/{filename}' 

                        cv2.imwrite(path_img_OV, image_resized)
                        print(f'Writing {path_img_OV}')
                        del image
                        del image_padding
                        del image_resized         
                        if train_or_test == 'train': 
                            count_train=+1
                        else: 
                            count_test=+1  
                    except Exception as e:
                        print(e)
                        print(filename)          
    print('Finish')    
    print(f'Num train files: {count_train}')
    print(f'Num test files: {count_test}')

if __name__ == "__main__":
    """python padding_resize_split_dataset oneView 640 640"""
    dataset_type = sys.argv[1]
    if dataset_type == 'oneView':
        print(dataset_type)
        one_view_dataset()