#include "mbed.h"
#include "bbcar.h"
#include "bbcar_rpc.h"


Ticker servo_ticker;

PwmOut pin5(D5), pin6(D6);
DigitalInOut pin8(D8);

BufferedSerial xbee(D1, D0);
BufferedSerial uart(D10, D9); //tx,rx
BBCar car(pin5, pin6, servo_ticker);
parallax_ping ping1(pin8);

void Line(Arguments *in, Reply *out);
void Tag(Arguments *in, Reply *out);
void mystop(Arguments *in, Reply *out);
RPCFunction rpcLine (&Line, "Line");
RPCFunction rpcTag (&Tag, "Tag");


void track(int deg){
   int speed = -80;
   //deg = 0;
   if(deg <1 && deg >-1){
      car.goStraight(speed);
      printf("straight\r\n");
   }
   else if(deg<0){
      car.turn(speed, 0.6);
      printf("left\r\n");
   }
   else {
      car.turn(speed, -0.6);
      printf("right\r\n");
   }
   ThisThread::sleep_for(300ms);
   car.stop();
   ThisThread::sleep_for(500ms);
}

void line_track(int end, int speed){
   char o = '1';
   uart.write(&o, 1);
   int step = 0;
   int x[4];
   while (step<end) {
      if(uart.readable()){
         x[0] = 0;
         while(uart.readable()){
            for (int i=0;;i++){
               char recv[1];
               uart.read(recv, sizeof(recv));
               x[i] = recv[0];
               if(recv[0] =='\n'){
                  //printf("\r\n");
                  break;
               }
               // printf("%d, ", recv[0]);
            }
         }
         int rho = x[0] - 85;
         printf("Current rho %d, %d \r\n", x[0], rho);
         if(rho<50 && rho>-50){
            if(rho<1 && rho>-1)
               car.goStraight(speed);
            else if(rho>0){
               car.turn(speed, -0.6);
               printf("left\r\n");
            }
            else{
               car.turn(speed, 0.6);
               printf("right\r\n");
            }
            ThisThread::sleep_for(500ms);
            car.stop();
            ThisThread::sleep_for(500ms);
            step++;
         }
      }
   }
}
void tag_track(int limit){
   char o = '0';
   uart.write(&o, 1);
   int distance = 0;
   int degree = -1;
   int first =0;
   int x[2];
   char recv[1];
   while (1){
      if(uart.readable()){
         degree = -1;
         first = 0;
         while(uart.readable()){
            for (int i=0;;i++){
               uart.read(recv, sizeof(recv));
               if(recv[0] =='\n')
                  break;
               else{
                  x[0] = recv[0];
                  // printf("%d, ", recv[0]);
               }  
            }
            degree = x[0] - 180;
         }
         // printf("=== %d\r\n", degree);
         
         distance = (float)ping1;
         if(degree<30 && degree> -30){
            printf("Current Status (deg, dist): %d, %d\r\n", degree, distance);
            if(distance>limit){
               printf("--> run track ");
               track(degree);
            }
            else{
               printf("--> stop at limit\r\n");
               break;
            }

         }
         else
            car.stop();            
      }    
   }
}

void Line(Arguments *in, Reply *out){
   int in0 = in->getArg<int>();
   int in1 = in->getArg<int>();
   line_track(in0, in1);
}

void Tag(Arguments *in, Reply *out){
   tag_track(25);
}

int main() {
   char buf[256], outbuf[256];
   
   FILE *devin = fdopen(&xbee, "r");
   FILE *devout = fdopen(&xbee, "w");
   uart.set_baud(9600);
   printf("Board !!!! im here\r\n");
   //line_track(15, -80);
   //tag_track(25);
   while(1){
      memset(buf, 0, 256);
      for( int i = 0; ; i++ ) {
         char recv = fgetc(devin);
         if(recv == '\n') {
            printf("\r\n");
            break;
         }
         buf[i] = fputc(recv, devout);
      }
      RPC::call(buf, outbuf);
   }
   // ------------ track line
   // line_track(20);
   // ------------ track Tag
   // tag_track(25);
}

