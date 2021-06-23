import time

import serial

import sys,tty,termios

reverse_flag = 0
# d1 = 7.6
# d2 = 5.2
w = 11.5
# west = float(input('Enter West(0/1) : '))
# d1 = float(input('Enter d1 : '))
# d2 = float(input('Enter d2 : '))
west = 0
d1 = 7.6 #7.6 #13
#d2 = 5.6 # 5.6 #9 
#print(f"Setup: (d1, d2) ={d1, d2}")

depth = 18+d1-w
rv = 4
speed = 50
# print(cir_time, back_time1, back_time2) 
class _Getch:

    def __call__(self):

        fd = sys.stdin.fileno()

        old_settings = termios.tcgetattr(fd)

        try:

            tty.setraw(sys.stdin.fileno())

            ch = sys.stdin.read(1)

        finally:

            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)

        return ch


def get():

    inkey = _Getch()

    while(1):

        k=inkey()

        if k!='':break

    if k=='\x1b':

        k2 = inkey()

        k3 = inkey()

        print(k3)

        if k3=='A':

            print ("up")
            reverse_flag = 0
            s.write("/goStraight/run 80 \n".encode())
            time.sleep(1)
            s.write("/stop/run \n".encode())

        if k3=='B':

            print ("down")
            reverse_flag = 0
            s.write("/goStraight/run -80 \n".encode())
            time.sleep(1)
            s.write("/stop/run \n".encode())

        if k3=='C':

            print ("right")
            reverse_flag = 0
            s.write("/turn/run 80 -0.3 \n".encode())
            time.sleep(1)
            s.write("/stop/run \n".encode())

        if k3=='D':

            print ("left")
            reverse_flag = 0
            s.write("/turn/run 80 0.3 \n".encode())
            time.sleep(1)
            s.write("/stop/run \n".encode()) 

        if k3=='Q': # press f2
            # 
            west = float(input('Enter West(0/1) : '))
            d1 = float(input('Enter d1 : '))
            d2 = float(input('Enter d2 : '))

            back_time1 = (d2-1)/rv
            cir_time = 10/rv
            back_time2 = (depth-5)/rv # speed = 80
            print ("Backward")
            s.write(f"/goStraight/run -{speed} \n".encode())
            time.sleep(back_time1)
            s.write("/stop/run \n".encode())
            time.sleep(1)
            #---------------
            print ("Backturn")
            s.write(f"/turn/run -{speed} -0.00001\n".encode())
            time.sleep(cir_time)
            s.write("/stop/run \n".encode())
            time.sleep(1)
            #---------------
            s.write(f"/goStraight/run -{speed} \n".encode())
            time.sleep(back_time2)
            s.write("/stop/run \n".encode())
            time.sleep(1)
        
        if k3=='P': # press f1

            print ("LineFollowMode")
            
            s.write(f"/Line/run 15 -80\n".encode())


        if k3=='R': # press f3
            print ("TagFollowMode")
            s.write(f"/Tag/run \n".encode())
            
            
            
        
        
        print("End Command (Tag, Line may not finish yet)")
        # if reverse_flag == 1:
        #     reverse_flag = 0
        #     s.write("/goStraight/run -80 \n".encode())
        #     time.sleep(1)

        

    elif k=='q':

        print ("quit")

        return 0

    else:

        print ("not an arrow key!")

    return 1


if len(sys.argv) < 1:

    print ("No port input")

s = serial.Serial(sys.argv[1])

while get():

    i = 0