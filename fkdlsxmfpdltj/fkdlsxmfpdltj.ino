#include <Servo.h> 
int servoPin = 9;
Servo servo;
int angle = 0;
int l,r;
int led1 = 8;
int led2 = 7; 
int cds = A0;

 void setup() 
 {
   pinMode(10, OUTPUT);
   pinMode(11, OUTPUT);
   pinMode(12, OUTPUT);
   pinMode(13, OUTPUT);
   pinMode(led1,OUTPUT);
   pinMode(led2,OUTPUT);
   servo.attach(servoPin);
   
   pinMode(4,INPUT);
   pinMode(3,INPUT);
 }
 void forward()
 {
  digitalWrite(10,HIGH);
  digitalWrite(11,LOW);
  digitalWrite(12,HIGH);
  digitalWrite(13,LOW);
  delay(2);
  brake();
 }
 
  void L_turn()
  {
  digitalWrite(10,LOW);
  digitalWrite(11,LOW);
  digitalWrite(12,HIGH);
  digitalWrite(13,LOW);
  }
  void R_turn()
  {
  digitalWrite(10,LOW);
  digitalWrite(11,LOW);
  digitalWrite(12,HIGH);
  digitalWrite(13,LOW);
  }
void brake()
{
  digitalWrite(10,LOW);
  digitalWrite(11,LOW);
  digitalWrite(12,LOW);
  digitalWrite(13,LOW);
}

void loop()
{
  for(angle = 0; angle < 180; angle++)
  {
    servo.write(angle);
    delay(15);
  }
   for(angle = 180; angle > 0; angle--)
   {
    servo.write(angle);
    delay(15);
   }
  
  int cdsValue = analogRead(cds);
  Serial.print("cds=");
  Serial.println(cdsValue);
  if(cdsValue>220){
   digitalWrite(led1,HIGH);
   digitalWrite(led2,HIGH);
  }else{
    digitalWrite(led1,LOW);
    digitalWrite(led2,LOW);
  }
  
  r=digitalRead(4);
  l=digitalRead(3);


 if(r==LOW&&l==LOW)//if(r==LOW&&l==HIGH)
 {forward();}
 
 if(r==HIGH&&l==LOW)//if(r==LOW&&l==LOW)
 {L_turn();}
 
 if(r==LOW&&l==HIGH)//if(r==LOW&&l==LOW)
 {R_turn();}
 
 if(r==HIGH&&l==HIGH)//if(r==LOW&&l==LOW)
 {brake();}
}
