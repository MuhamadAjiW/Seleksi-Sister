result = cupy.asnumpy(array).astype(cupy.uint8)

cv2.imshow("Result", result)
cv2.waitKey(0)
cv2.destroyAllWindows()
