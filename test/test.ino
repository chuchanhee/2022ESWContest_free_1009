#include <MsTimer2.h> 
#include<SoftwareSerial.h>
#include<Servo.h>

Servo servo;

#define LEFT_A1 10 //왼쪽 바퀴
#define LEFT_B1 11 //왼쪽 바퀸
#define RIGHT_A2 12 //오른쪽 바퀴
#define RIGHT_B2 13 //오른쪽 바퀴

#define BLUE_TX 5
#define BLUE_RX 8 //블루투스 송신

SoftwareSerial bluetooth(BLUE_TX, BLUE_RX); //시리얼 통신을 위한 객체선언
char cmd; //블루투스에서 받는 값

volatile boolean state = true;
int piezoPin = 2;  //부저 핀
int angle = 100;   //서보모터 초기위치
int rot_angle = 0;  // 서보모터 함수 
int state2 = 0; 
//int cds = A0;    
//int led1 = 6;
//int led2 = 7;

int l,r;

void forward() //전진 함수
{
 digitalWrite(LEFT_A1, HIGH);
 digitalWrite(LEFT_B1, LOW);
 digitalWrite(RIGHT_A2, HIGH);
 digitalWrite(RIGHT_B2, LOW);
 
}
void backward() //후진 함수
{
 digitalWrite(LEFT_A1, LOW);
 digitalWrite(LEFT_B1, HIGH);
 digitalWrite(RIGHT_A2, LOW);
 digitalWrite(RIGHT_B2, HIGH);
}
void left() //좌회전 함수
{
 digitalWrite(LEFT_A1, LOW);
 digitalWrite(LEFT_B1, HIGH);
 digitalWrite(RIGHT_A2, HIGH);
 digitalWrite(RIGHT_B2, LOW);
}

void right() //우회전 함수
{
 digitalWrite(LEFT_A1, HIGH);
 digitalWrite(LEFT_B1, LOW);
 digitalWrite(RIGHT_A2, LOW);
 digitalWrite(RIGHT_B2, HIGH);
}
void sLeft()//약 좌회전 함수
{
 digitalWrite(LEFT_A1, LOW);
 digitalWrite(LEFT_B1, LOW);
 digitalWrite(RIGHT_A2, HIGH);
 digitalWrite(RIGHT_B2, LOW);
}
void sRight()//약 우회전 함수
{
 digitalWrite(LEFT_A1, HIGH);
 digitalWrite(LEFT_B1, LOW);
 digitalWrite(RIGHT_A2, LOW);
 digitalWrite(RIGHT_B2, LOW);
}

void stops() //정지 함수
{
 digitalWrite(LEFT_A1, LOW);
 digitalWrite(LEFT_B1, LOW);
 digitalWrite(RIGHT_A2, LOW);
 digitalWrite(RIGHT_B2, LOW);
}
void rotate_head()
{
  servo.write(rot_angle);
  if(state2 == 0)
  {
    rot_angle +=1;
  }
  else if(state2 == 1)
  {
    rot_angle -= 1;
  }

  if(rot_angle ==190)
  {
    state2 = 1;
  }
  else if(rot_angle == 0)
  {
    state2 = 0;
  }
}  


//void two_led()
//{
//  int cdscmd = analogRead(cds);
//
//  Serial.print("cds =  ");
//  Serial.println(cdscmd);
//  if (cdscmd > 220) 
//     {    
//     digitalWrite(led1, HIGH);
//     digitalWrite(led2, HIGH);     
//     } else {    
//     digitalWrite(led1, LOW);      
//     digitalWrite(led2, LOW);
//     }
//}



void setup() 
{
  //Serial.begin(9600); //시리얼모니터 
 // mySerial.begin(9600); //블루투스 시리얼 개방
  pinMode(LEFT_A1, OUTPUT);
  pinMode(RIGHT_A2, OUTPUT);
  pinMode(LEFT_B1, OUTPUT);
  pinMode(RIGHT_B2, OUTPUT);

//  pinMode(led1, OUTPUT);
//  pinMode(led2, OUTPUT);
  
  bluetooth.begin(9600); //블루투스 통신 속도
  servo.attach(9);     //맴버함수인 attach : 핀 설정
  servo.write(angle);

  pinMode(piezoPin, OUTPUT); //부저 인풋
 

  MsTimer2::set(30,rotate_head); // 서보모터 타이머 인터럽트
  MsTimer2::start();

//  MsTimer2::set(30,two_led);
//  MsTimer2::start();

   pinMode(4,INPUT); //적외선 센서 좌
   pinMode(3,INPUT); //적외선 센서 우
}

void loop()
 {
   if(bluetooth.available()) 
   {  
    cmd = bluetooth.read();
    if(cmd == 'y' || cmd == 'Y') //수동진입 
    {
      while(1)
      {
        cmd = bluetooth.read(); //

        if(cmd == 'd' || cmd == 'D') //우회전
        {
          sLeft();
        }
        else if(cmd == 'a' || cmd == 'A') //좌회전
        {
          sRight();
        }
        if(cmd == 'w' || cmd == 'W') //전진
        {
          forward();
        }
        else if(cmd == 's' || cmd =='S') //후진 
        {
          backward();
        }
        if(cmd == 'x' || cmd == 'X') //정지
          stops();
        }
        if(cmd == 'u' || cmd == 'U')  //수동모드 정지
        {
          stops();
          break;
        }
      }
    }
    else if(cmd == 'n' || cmd =='N') // 자동지입
    {
      while(1)
      {
        cmd = bluetooth.read();
        r=digitalRead(4); //적외선 값 
        l=digitalRead(3);


        if(r==LOW&&l==LOW)//if(r==HIGH&&l==HIGH)
        {forward();}//brake
 
        if(r==LOW&&l==HIGH)//if(r==HIGH&&l==LOW)
        {left();}
 
        if(r==HIGH&&l==LOW)//if(r==HIGH&&l==LOW)
        {right();}
 
        if(r==HIGH&&l==HIGH)//if(r==LOW&&l==LOW)
        {stops();}//forwar
   
        if(cmd == 'u' || cmd == 'U')  //자동모두 정지
        {
          stops();
          break;
        }
     }
    }
    
    else if (cmd=='e')  //경보음
    {      
      for (int i = 0; i<=300; i ++)
      {
        for(int freq = 150; freq <=1800; freq = freq + 2) 
        {
          tone(piezoPin, freq, 100);
        }
        for(int freq = 1800; freq <=150; freq = freq - 2) 
        {
          tone(piezoPin, freq, 100);      
        }
      }
     }

   }
}
