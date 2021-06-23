import sensor, image, time, pyb

enable_lens_corr = False # turn on for straighter lines...

sensor.reset()

sensor.set_pixformat(sensor.RGB565) # grayscale is faster

sensor.set_framesize(sensor.QQVGA)

sensor.skip_frames(time = 2000)

clock = time.clock()
RED_LED_PIN = 1
BLUE_LED_PIN = 3

# All lines also have `x1()`, `y1()`, `x2()`, and `y2()` methods to get their end-points

# and a `line()` method to get all the above as one 4 value tuple for `draw_line()`.

uart = pyb.UART(3,9600,timeout_char=1000)
uart.init(9600,bits=8,parity = None, stop=1, timeout_char=1000)
pyb.LED(RED_LED_PIN).on()
sensor.skip_frames(time = 2000) # Give the user time to get ready.
pyb.LED(RED_LED_PIN).off()
pyb.LED(RED_LED_PIN).on()
while(True):

   clock.tick()

   img = sensor.snapshot()


   if enable_lens_corr: img.lens_corr(1.8) # for 2.8mm lens...


   # `merge_distance` controls the merging of nearby lines. At 0 (the default), no

   # merging is done. At 1, any line 1 pixel away from another is merged... and so

   # on as you increase this value. You may wish to merge lines as line segment

   # detection produces a lot of line segment results.


   # `max_theta_d
   # iff` controls the maximum amount of rotation difference between

   # any two lines about to be merged. The default setting allows for 15 degrees.


   for l in img.find_line_segments(merge_distance = 0, max_theta_diff = 5):
      if l.y2() == 0:
        img.draw_line(l.line(), color = (255, 0, 0))
        # print("%d, %d, %d, %d" % l.line())
        print("{}, {}, {}, {}".format(l.x1(), l.x2(), l.y1(), l.y2()))
        print("{}".format(l.x1() - l.x2()-20))
        print("----------------")
        uart.write(chr(l.x1()))
        uart.write(chr(l.x2()))
        uart.write(chr(l.y1()))
        uart.write(chr(l.y2()))
        uart.write("\n")
        break
        # uart.write(("%d, %d, %d, %d\n" % l.line()).encode())

   # print("FPS %f" % clock.fps())
