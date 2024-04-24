from turbojpeg import TurboJPEG
import cv2
jpeg = TurboJPEG()
with open('image.jpg', 'rb') as in_file:
    img = jpeg.decode(in_file.read())
    (width, height) = (img.shape[1] // 2, img.shape[0] // 2)
    img = cv2.resize(img, [width, height], interpolation = cv2.INTER_AREA)