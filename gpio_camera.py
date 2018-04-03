import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import picamera
import numpy as np
from gpiozero import Button, LED
from signal import pause
from time import sleep
import pickle

def NDVI_Capture():
    with picamera.PiCamera() as camera:
        camera.resolution = (320, 240)
        #camera.awb_mode = 'off'
        #camera.awb_gains = ((1.2),(1))
        sleep(2)
        output = np.empty((240, 320, 3), dtype=np.uint8)
        camera.capture(output, 'rgb')

    red = 0
    nir = 2

    output32 = output.astype(np.float32)

    a = (output32[:, :, nir] - output32[:, :, red])
    b = (output32[:, :, red] + output32[:, :, nir])

    ndvi = np.divide(a, b, out=np.zeros_like(a), where=b!=0)

    print(ndvi)
    plt.figure(1)
    plt.imshow(ndvi, cmap = "nipy_spectral", vmin = -1, vmax = 1)
    plt.colorbar()
    plt.savefig('/home/pi/Desktop/pics/NDVI.%s.%s.png' % (count, pic))
    plt.close()
    print("Saved NDVI")

    print(output)
    plt.figure(2)
    plt.imshow(output)
    plt.savefig('/home/pi/Desktop/pics/RGB.%s.%s.png' % (count, pic))
    plt.close()
    print("Saved RGB")

count = 1

save = '/home/pi/camera/cameraCount.pk'

with open(save, 'rb') as fi:
    count = pickle.load(fi)

count += 1

with open(save, 'wb') as fi:
    pickle.dump(count, fi)

button = Button(2)
led = LED(17)
pic = 1

sleep(2)

while True:
    if button.is_pressed:
        for i in range(2):
            led.off()
            sleep(0.5)
            led.on()
            sleep(0.5)
        while button.is_pressed:
            NDVI_Capture()
            led.off()
            sleep(1)
            led.on()
            pic += 1
            sleep(5)
    else:
        for i in range(2):
            led.on()
            sleep(0.5)
            led.off()
            sleep(5)
        led.off()
