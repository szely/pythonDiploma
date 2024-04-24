# importing the required modules
import pytesseract
import matplotlib.pyplot as plt
import cv2
import glob
import os
path_to_file = '/Users/a1234/Downloads/1.png'
assert os.path.exists(path_to_file)
# specifying the path to the number plate images folder as shown below
file_path = path_to_file
NP_list = []
predicted_NP = []

for file_path in glob.glob(file_path, recursive=True):
    NP_file = file_path.split("/")[-1]
    number_plate, _ = os.path.splitext(NP_file)
    ''' 
    Here we will append the actual number plate to a list 
    '''
    NP_list.append(number_plate)

    ''' 
    Reading each number plate image file using openCV 
    '''
    NP_img = cv2.imread(file_path)

    ''' 
    We will then pass each number plate image file 
    to the Tesseract OCR engine utilizing the Python library 
    wrapper for it. We get back predicted_res for 
    number plate. We append the predicted_res in a 
    list and compare it with the original number plate 
    '''
    predicted_res = pytesseract.image_to_string(NP_img, lang='eng',
                                                config='--oem 3 --psm 6 -c tessedit_char_whitelist = ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789')

    filter_predicted_res = "".join(predicted_res.split()).replace(":", "").replace("-", "")
    predicted_NP.append(filter_predicted_res)

print("Original Number Plate", "\t", "Predicted Number Plate", "\t", "Accuracy")
print("--------------------", "\t", "-----------------------", "\t", "--------")


def estimate_predicted_accuracy(ori_list, pre_list):
    for ori_plate, pre_plate in zip(ori_list, pre_list):
        acc = "0 %"
        number_matches = 0
        if ori_plate == pre_plate:
            acc = "100 %"
        else:
            if len(ori_plate) == len(pre_plate):
                for o, p in zip(ori_plate, pre_plate):
                    if o == p:
                        number_matches += 1
                acc = str(round((number_matches / len(ori_plate)), 2) * 100)
                acc += "%"
        print(ori_plate, "\t", pre_plate, "\t", acc)


estimate_predicted_accuracy(NP_list, predicted_NP)