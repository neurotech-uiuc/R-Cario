unsigned char Bluetooth_val;       //defining variable val
#define Lpwm_pin  5     //adjusting speed  
#define Rpwm_pin  6    //adjusting speed  //
int pinLB=2;     // defining pin2 left rear
int pinLF=4;     // defining pin4 left front
int pinRB=7;    // defining pin7 right rear
int pinRF=8;    // defining pin8 right front
unsigned char Lpwm_val = 180;
unsigned char Rpwm_val = 180;
int Car_state=0;
void M_Control_IO_config(void)
{
  pinMode(pinLB,OUTPUT); // pin 2
  pinMode(pinLF,OUTPUT); // pin 4
  pinMode(pinRB,OUTPUT); // pin 7 
  pinMode(pinRF,OUTPUT); // pin 8
  pinMode(Lpwm_pin,OUTPUT); // pin 5 (PWM) 
  pinMode(Rpwm_pin,OUTPUT); // pin 6 (PWM)   
}
void Set_Speed(unsigned char Left,unsigned char Right)
{
  analogWrite(Lpwm_pin,Left);
  analogWrite(Rpwm_pin,Right);
}
void advance()     //  going forward
    {
     digitalWrite(pinRB,LOW);  // making motor move towards right rear
     digitalWrite(pinRF,HIGH);
     digitalWrite(pinLB,LOW);  // making motor move towards left rear
     digitalWrite(pinLF,HIGH); 
     Car_state = 1;    
    }
void turnR()        //turning right(dual wheel)
    {
     digitalWrite(pinRB,LOW);  //making motor move towards right rear
     digitalWrite(pinRF,HIGH);
     digitalWrite(pinLB,HIGH);
     digitalWrite(pinLF,LOW);  //making motor move towards left front
     Car_state = 4;
    }
void turnL()        //turning left(dual wheel)
    {
     digitalWrite(pinRB,HIGH);
     digitalWrite(pinRF,LOW );   //making motor move towards right front
     digitalWrite(pinLB,LOW);   //making motor move towards left rear
     digitalWrite(pinLF,HIGH);
     Car_state = 3;
    }    
void stopp()         //stop
    {
     digitalWrite(pinRB,HIGH);
     digitalWrite(pinRF,HIGH);
     digitalWrite(pinLB,HIGH);
     digitalWrite(pinLF,HIGH);
     Car_state = 5;
    }
void back()          //back up
    {
     digitalWrite(pinRB,HIGH);  //making motor move towards right rear
     digitalWrite(pinRF,LOW);
     digitalWrite(pinLB,HIGH);  //making motor move towards left rear
     digitalWrite(pinLF,LOW);
     Car_state = 2;   
    }
     
void setup() 
{ 
   M_Control_IO_config();
   Set_Speed(Lpwm_val,Rpwm_val);
   Serial.begin(9600);   //initialized serial port , using Bluetooth as serial port, setting baud at 9600 
   stopp(); 
}
void loop() 
{  
   if(Serial.available()) //to judge whether the serial port receives the data.
    {
     Bluetooth_val=Serial.read();  //reading (Bluetooth) data of serial port,giving the value of val;
    switch(Bluetooth_val)
     {
       case 'U':
       advance(); //UP
       Serial.println("UP");
       break;
       case 'D': back();   //back
       Serial.println("BACK");
       break;
       case 'L':turnL();   //Left
       Serial.println("LEFT");
       break;
       case 'R':turnR();  //Right
       Serial.println("RIGHT");
       break;
       case 'S':stopp();    //stop
       Serial.println("STOP");
       break;   
     }
    } 
}