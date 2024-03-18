A school project that detects motion using a camera and visually alerts the user.
The implementation is done using OpenCV and code written in Python & Django.

![image](https://github.com/Radu-Maris/CameraDetectionSystem/assets/58084616/bce20c06-a6e7-41fc-be7f-42a783b50df1)

The implementation of the project was done by manipulating the recived video in 4 steps:
* First transformation to the image is a grayscale transformation in order to detect the light intensity of the image. In order to detect only relevant movement I used a gaussian blur to transform the first image.
* 
<p align="center">
![image](https://github.com/Radu-Maris/CameraDetectionSystem/assets/58084616/49009452-0481-408c-8661-fce71809de25)
</p>

* After that, I generate the difference frame. This is done by comparing the initial image with the current frame from the camera. If there is a difference in light values.

![image](https://github.com/Radu-Maris/CameraDetectionSystem/assets/58084616/718d4e77-8eb5-413e-bb9b-de824bc16559)

* The next transformation is the threshold generation. For this, we set a threshold and if there is a light value above that value, then it will be converted to white, thus having only 2 values to work with: black and white.

![image](https://github.com/Radu-Maris/CameraDetectionSystem/assets/58084616/4726b55e-bc06-45d4-8f54-ce01714a808d)

* The final transformation is applied in the current frame of the camera input. By using the threshold and OpenCV it detects the perimeter of all the white objects and generates bounding coordinates for that object. Then I draw rectangles at the coordinates from the threshold on the current frame of the input and get the final image that is shown to the user.

![image](https://github.com/Radu-Maris/CameraDetectionSystem/assets/58084616/cc4005a5-8705-4186-b3d7-fd6bbf89b4cc)
