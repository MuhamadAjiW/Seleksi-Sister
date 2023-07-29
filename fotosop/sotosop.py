import cv2
import cupy
import threading

# Librarynya rada ngecheat buat sekarang, tar buat threadingnya aja walaupun lebih lama
# Prinsipnya harusnya sederhana


path = 'C:/Users/Muhamad/Desktop/seleksisister/b/fotosop/pic.jpg'
image = cv2.imread(path).astype(cupy.float64)

command = "saturation"

if command == "grayscale":
    image_blue, image_green, image_red = cv2.split(image)
    blue = cupy.asarray(image_blue)
    green = cupy.asarray(image_green)
    red = cupy.asarray(image_red)

    array = cupy.floor_divide(red + green + blue, 3)

elif command == "contrast":
    value = 5.0

    array = cupy.clip(a=value * (image - 128) + 128, a_min=0, a_max=255)

elif command == "saturation":
    image = cv2.imread(path).astype(cupy.uint8)

    value = 5.0

    image_hls = cv2.cvtColor(image, cv2.COLOR_BGR2HLS)

    image_saturation = image_hls[:, :, 2]
    
    saturation_arr = cupy.clip(a=value * image_saturation, a_min=0, a_max=255)

    image_hls[:, :, 2] = saturation_arr

    image_hsv = image_hls.astype(cupy.uint8)
    array = cv2.cvtColor(image_hsv, cv2.COLOR_HLS2BGR)

elif command == "gaussian blur":
    image = cv2.imread(path).astype(cupy.uint8)

    value = 5.0

    image_hls = cv2.cvtColor(image, cv2.COLOR_BGR2HLS)

    image_saturation = image_hls[:, :, 2]
    
    saturation_arr = cupy.clip(a=value * image_saturation, a_min=0, a_max=255)

    image_hls[:, :, 2] = saturation_arr

    image_hsv = image_hls.astype(cupy.uint8)
    array = cv2.cvtColor(image_hsv, cv2.COLOR_HLS2BGR)

else:
    array = image



result = cupy.asnumpy(array).astype(cupy.uint8)

cv2.imshow("Result", result)
cv2.waitKey(0)
cv2.destroyAllWindows()
