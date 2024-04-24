import aspose.ocr as ocr
import os
path_to_file = '/Users/a1234/Downloads/2.png'
assert os.path.exists(path_to_file)
# Instantiate Aspose.OCR API
api = ocr.AsposeOcr()

# Add image to the recognition batch
input = ocr.OcrInput(ocr.InputType.SINGLE_IMAGE)
input.add(path_to_file)

# Recognize the image
result = api.recognize_car_plate(input)

# Print recognition result
print(result[0].recognition_text)