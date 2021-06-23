# mbedFinal

## Setup and run the Program 

   1. Copy the code in hw4/openMV code_hw4.txt into IDE
    
   2.  Compile the program
   
   `$ cd mbedFinal/13_7_Control_BBCar_by_Xbee/`
   
   `$ sudo mbed compile --source . --source ~/ee2405/mbed-os-build/ -m B_L4S5I_IOT01A -t GCC_ARM -f`
   
   3.  Execute the python code to control BBCar
   
   `$ cd mbedFinal/13_6_Python_PRC`
   
   `$ sudo python3 car_control.py /dev/ttyACM0`
   
### Scenario

  1. Press F5 to let the bb car start auto mode
  2. Run until green light (blob detection)
  3. Follow lane (line detection)
   - Simulate self-drive under navigation
   - Assumes that the lane leads to parking slot
  4. Position Calibration for Parking Mode: April tag + Ping
  5. Parking: Pre-coded route + Ping
  
###   Execution Flow

  1. Python RPC UI: enter auto mode (F5)
   - Mbed send UART to trigger blob detection
   - Mbed receive blob color code
   - if green light received -> Next step
  2. Follow lane 
   - Mbed send UART to trigger line detection
   - Mbed enter line track for 20 steps -> Next step
  3.  Position Calibration
   - Mbed send UART to trigger April tag track
   - Face to Tag with distance of 5cm -> Next step
  4.  Reverse Parking
   - Mbed perform reverse turn
   - Mbed reverse parking augmented with Ping sensor
   
## Execution Results

1.Traffic Light Sample
![image](https://user-images.githubusercontent.com/79574056/123037360-1ff39b00-d421-11eb-9f5f-ad33046b89cd.png)

2. The apriltag used in this homework
![tag_36h11](https://user-images.githubusercontent.com/79574056/123038376-d906a500-d422-11eb-9af4-3a965d9f4890.png)

3. demo video:
    https://drive.google.com/file/d/1cKarCdNoDI-se3LtDhSXPAxc65iFe4K1/view?usp=sharing
    
