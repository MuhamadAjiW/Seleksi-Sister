import time
import pycuda.driver as cuda
import pycuda.autoinit
from pycuda.compiler import SourceModule
import numpy as np
import cv2

# Librarynya rada ngecheat jadi bikin dua versi
# kaya kurang kalo ga nyentuh kernel cuda
# maximum(minimum(a, a_max), a_min)

cuda_kernel = """
__global__ void grayscale(const float* input, float* output, uint64_t size) {
    int idx = blockIdx.x * blockDim.x + threadIdx.x;
    if (idx < size) {
        int chidx = idx * 3;
        float gray = (input[chidx] + input[chidx + 1] + input[chidx + 2]) / 3.0;
        output[chidx] = gray;
        output[chidx + 1] = gray;
        output[chidx + 2] = gray;
    }
}

__global__ void contrast(const float* input, float* output, float value, uint64_t size) {
    int idx = blockIdx.x * blockDim.x + threadIdx.x;
    if (idx < size) {
        float calculated = value * (input[idx] - 128) + 128;
        if(calculated > 255){
            calculated = 255;
        }
        else if(calculated < 0){
            calculated = 0;
        }
        output[idx] = calculated;
    }
}

__global__ void saturation(const float* input, float* output, float value, uint64_t size) {
    int idx = blockIdx.x * blockDim.x + threadIdx.x;
    if (idx < size) {
        output[idx] = input[idx] * value;
    }
}

__global__ void blur(const float* input, float* output, int value, int width, int height, uint64_t size) {
    int idx = blockIdx.x * blockDim.x + threadIdx.x;
    int limitval = value * 3;

    if (idx < size) {
        int x = idx % width;
        int y = idx / width;

        if (x < limitval || x >= (width - limitval)) {
            int sum = 0;
            for(int i = -value; i <= value; i++){
                for(int j = -limitval; j <= limitval; j += 3){
                    if(y + i >= 0){
                        sum += input[idx + (i * width - j) * 3];                        
                    }                    
                }
            }            
            output[idx] = sum / (1 + value*2) / (1 + value*2);
        }
        else if(y < value || y >= (height - value)){
            int sum = 0;
            for(int i = -value; i <= value; i++){
                for(int j = -limitval; j <= limitval; j += 3){
                    if(x + j < 0){
                        sum += input[idx + ((-1)*i * width - j) * 3];
                    }
                    else{
                        sum += input[idx + ((-1)*i * width + j) * 3];                        
                    }
                }
            }
            output[idx] = sum / (1 + value*2) / (1 + value*2);
        }
        else{
            int sum = 0;
            for(int i = -value; i <= value; i++){
                for(int j = -limitval; j <= limitval; j += 3){
                    sum += input[idx + (i * width + j) * 3];
                }
            }
            output[idx] = sum / (1 + value*2) / (1 + value*2);
        }    
    }
}
"""
module = SourceModule(cuda_kernel)

def process_image(image: np.ndarray, command:str, value:float=0):
    height, width, channel = image.shape

    size = len(image.flatten())
    if(command == "grayscale"):
        image_gpu_input = cuda.mem_alloc(image.nbytes)
        image_gpu_output = cuda.mem_alloc(image.nbytes)

        size //= 3
        block_size = 256
        grid_size = (size + block_size - 1) // block_size
        grayscale = module.get_function("grayscale")

        cuda.memcpy_htod(image_gpu_input, image)
        grayscale(image_gpu_input, image_gpu_output, np.int64(size), block=(block_size, 1, 1), grid=(grid_size, 1))
        cuda.Context.synchronize()
        cuda.memcpy_dtoh(image, image_gpu_output)

    elif(command == "contrast"):
        image_gpu_input = cuda.mem_alloc(image.nbytes)
        image_gpu_output = cuda.mem_alloc(image.nbytes)

        block_size = 256
        grid_size = (size + block_size - 1) // block_size
        contrast = module.get_function("contrast")

        cuda.memcpy_htod(image_gpu_input, image)
        contrast(image_gpu_input, image_gpu_output, np.float32(value), np.int64(size), block=(block_size, 1, 1), grid=(grid_size, 1))
        cuda.Context.synchronize()
        cuda.memcpy_dtoh(image, image_gpu_output)

    elif(command == "saturation"):
        image = image.astype(np.uint8)
        image_hls = cv2.cvtColor(image, cv2.COLOR_BGR2HLS)
        image_saturation = image_hls[:, :, 2].astype(np.float32)

        image_gpu_input = cuda.mem_alloc(image_saturation.nbytes)
        image_gpu_output = cuda.mem_alloc(image_saturation.nbytes)

        size //= 3
        block_size = 256
        grid_size = (size + block_size - 1) // block_size
        saturation = module.get_function("saturation")

        cuda.memcpy_htod(image_gpu_input, image_saturation)
        saturation(image_gpu_input, image_gpu_output, np.float32(value), np.int64(size), block=(block_size, 1, 1), grid=(grid_size, 1))
        cuda.Context.synchronize()
        cuda.memcpy_dtoh(image_saturation, image_gpu_output)

        image_hls[:, :, 2] = image_saturation
        image_hls = image_hls.astype(np.uint8)
        image = cv2.cvtColor(image_hls, cv2.COLOR_HLS2BGR)

    elif(command == "blur"):
        image_gpu_input = cuda.mem_alloc(image.nbytes)
        image_gpu_output = cuda.mem_alloc(image.nbytes)

        block_size = 256
        grid_size = (size + block_size - 1) // block_size
        blur = module.get_function("blur")

        cuda.memcpy_htod(image_gpu_input, image)
        blur(image_gpu_input, image_gpu_output, np.uint32(value), np.int32(width) * 3, np.int32(height), np.int64(size), block=(block_size, 1, 1), grid=(grid_size, 1))
        cuda.Context.synchronize()
        cuda.memcpy_dtoh(image, image_gpu_output)

    else:
        pass

    image_gpu_input.free()
    image_gpu_output.free()

    image_result = image.reshape(height, width, channel).astype(np.uint8)

    return image_result

if __name__ == "__main__":
    path = 'C:/Users/Muhamad/Desktop/seleksisister/b/fotosop/pic.jpg'
    image = cv2.imread(path).astype(np.float32) 
    command = "blur"
    value = 4
    
    start_time = time.time()

    processed_image = process_image(image, command, value)

    end_time = time.time()
    elapsed_time = end_time - start_time
    print("Elapsed time:", elapsed_time, "Seconds")

    cv2.imshow("Result", processed_image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()