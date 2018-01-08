from picamera import PiCamera
from gpiozero import Button, LED
from signal import pause
from time import sleep
import pickle

count = 1

newfile = 'cameraCount.pk'

with open(newfile, 'rb') as fi:
    count = pickle.load(fi)

count += 1

with open(newfile, 'wb') as fi:
    pickle.dump(count, fi)



camera = PiCamera()

button = Button(2)
led = LED(17)

pic = 1

sleep(5)


while True:
    if button.is_pressed:
        for i in range(2):
            led.off()
            sleep(0.5)
            led.on()
            sleep(0.5)
        while button.is_pressed:
            camera.capture('/home/pi/Desktop/pics/pic.%s.%s.jpg' % (count, pic))
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
        
