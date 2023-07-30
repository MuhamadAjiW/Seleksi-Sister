import time
import cv2
import cupy
import threading as td
import multiprocessing as mp

# Librarynya rada ngecheat jadi bikin dua versi
# Cek versi cudanya cuy dijamin gacor
def grayscale(image, row, cols):
    for col in range(0, cols):
        image[row, col] = cupy.sum(image[row, col]) / 3

def contrast(image, row, cols, value):
    for col in range(0, cols):
        image[row, col] = cupy.clip(a=value * (image[row, col] - 128) + 128, a_min=0, a_max=255)

def saturation(image, row, cols, value):
    for col in range(0, cols):
        image[row, col] = cupy.clip(a=value * image[row, col], a_min=0, a_max=255)

def blur(image, targetimage, row, cols, intensity):
    for col in range(intensity, cols - intensity):
        # arr = cupy.asarray()
        result = (image[row - intensity:row + intensity+1, col - intensity:col + intensity+1]).mean(axis=(0, 1))
        targetimage[row, col] = result

# Note: cupy udah highly efficient soal pararelisasi di gpu, threading dari python malah ngelambatin
# ini dibuat algoritma pararel biar spesifikasi tugas, lebih lambat
def thread_img(image, command, value=1.0, use_threads=False):
    start_time = time.time()
    if command == "grayscale":
        if use_threads:
            height, width, channel = image.shape

            threads = []
            for i in range(0, height):
                thread = td.Thread(target=grayscale, args=(image, i, width))
                threads.append(thread)
                thread.start()

            for thread in threads:
                thread.join()

            array = image

        else:
            image_blue, image_green, image_red = cv2.split(image)
            blue = cupy.asarray(image_blue)
            green = cupy.asarray(image_green)
            red = cupy.asarray(image_red)

            array = cupy.floor_divide(red + green + blue, 3)

    elif command == "contrast":
        if use_threads:
            height, width, channel = image.shape

            threads = []
            for i in range(0, height):
                thread = td.Thread(target=contrast, args=(image, i, width, value))
                thread.start()
                threads.append(thread)

            for thread in threads:
                thread.join()

            array = image

        else:
            array = cupy.clip(a=value * (image - 128) + 128, a_min=0, a_max=255)

    elif command == "saturation":
        image = image.astype(cupy.uint8)
        image_hls = cv2.cvtColor(image, cv2.COLOR_BGR2HLS)
        image_saturation = image_hls[:, :, 2]

        if use_threads:
            height, width, channel = image.shape

            threads = []
            for i in range(0, height):
                thread = td.Thread(target=saturation, args=(image_saturation, i, width, value))
                thread.start()
                threads.append(thread)

            for thread in threads:
                thread.join()

        else:
            image_saturation = cupy.clip(a=value * image_saturation, a_min=0, a_max=255)

        image_hls[:, :, 2] = image_saturation

        image_hsv = image_hls.astype(cupy.uint8)
        array = cv2.cvtColor(image_hsv, cv2.COLOR_HLS2BGR)

    elif command == "blur":
        # box blur, gak handle pojok
        intensity = (int)(value)
        height, width, channel = image.shape

        empty_image = cupy.copy(image).astype(cupy.float64)

        if use_threads:
            threads = []
            for i in range(intensity, height - intensity):
                thread = td.Thread(target=blur, args=(image, empty_image, i, width, intensity))
                thread.start()
                threads.append(thread)

            for thread in threads:
                thread.join()

        else:
            for i in range(intensity, height - intensity):
                blur(image, empty_image, i, width, intensity)

        array = empty_image
        
    else:
        array = image

    result = cupy.asnumpy(array).astype(cupy.uint8)

    end_time = time.time()
    elapsed_time = end_time - start_time
    print("Elapsed time:", elapsed_time, "Seconds")

    cv2.imshow("Result", result)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

if __name__ == '__main__':
    path = 'C:/Users/Muhamad/Desktop/seleksisister/b/fotosop/pic.jpg'
    image = cv2.imread(path).astype(cupy.float64)

    command = "blur"
    use_threads = False
    value = 4.0

    thread_img(image, command, value, use_threads)