// 좌측 모터 구동
int ENBPin_R = 8;
int IN1Pin_R = 9;
int IN2Pin_R = 10;

// 우측 모터 구동
int ENBPin_L = 11;
int IN1Pin_L = 12;
int IN2Pin_L = 13;


// 리프트 상하강 모터
int IN1Pin_UD = 4;
int IN2Pin_UD = 5;
int ENBPin_UD = 14;
int button_down = 6; // 리밋스위치 하
int button_up = 7;  // 리밋스위치 상

//  초음파 센서
int ECHO_F = 23;
int TRIG_F = 22;
int ECHO_R = 25;
int TRIG_R = 24;
int ECHO_J = 48;
int TRIG_J = 49;

// 리프트 횟수
int jim = 0;
int jam = 0;
int count = 0;
int state = 0;

//RGB센서
#define LL_s0 26       //Module pins wiring
#define LL_s1 28
#define LL_s2 30
#define LL_s3 32
#define LL_out 34

#define LR_s0 27      //Module pins wiring
#define LR_s1 29
#define LR_s2 31
#define LR_s3 35
#define LR_out 37

#define RL_s0 36      //Module pins wiring
#define RL_s1 38
#define RL_s2 42
#define RL_s3 44
#define RL_out 46

#define RR_s0 39     //Module pins wiring
#define RR_s1 41
#define RR_s2 43
#define RR_s3 45
#define RR_out 47  

//수신기 외부 인터럽트
//UNO, Nano, Mini and other 328 based are 2, 3 // Mega, Mega2560 and MegaADK are 2, 3, 18, 19, 20, 21
const byte interruptPin0 = 2; //interrupt
const byte interruptPin1 = 3; //interrupt
const byte interruptPin2 = 18; //interrupt
const byte interruptPin3 = 19; //interrupt

volatile unsigned long pwm_value[4] = {0, 0, 0, 0};
volatile unsigned long timer[4] = {0, 0, 0, 0};

void setup() {
  pinMode(IN1Pin_L, OUTPUT);
  pinMode(IN2Pin_L, OUTPUT);
  pinMode(IN1Pin_R, OUTPUT);
  pinMode(IN2Pin_R, OUTPUT);
  pinMode(TRIG_F, OUTPUT);
  pinMode(ECHO_F, INPUT);
  pinMode(TRIG_R, OUTPUT);
  pinMode(ECHO_R, INPUT);
  pinMode(TRIG_J, OUTPUT);
  pinMode(ECHO_J, INPUT);
  pinMode(IN1Pin_UD, OUTPUT);
  pinMode(IN2Pin_UD, OUTPUT);
  pinMode(button_down, INPUT_PULLUP);
  pinMode(button_up, INPUT_PULLUP);

  pinMode(LL_s0,OUTPUT);    //pin modes
  pinMode(LL_s1,OUTPUT);
  pinMode(LL_s2,OUTPUT);
  pinMode(LL_s3,OUTPUT);
  pinMode(LL_out,INPUT);

  pinMode(LR_s0,OUTPUT);    //pin modes
  pinMode(LR_s1,OUTPUT);
  pinMode(LR_s2,OUTPUT);
  pinMode(LR_s3,OUTPUT);
  pinMode(LR_out,INPUT);

  pinMode(RL_s0,OUTPUT);    //pin modes
  pinMode(RL_s1,OUTPUT);
  pinMode(RL_s2,OUTPUT);
  pinMode(RL_s3,OUTPUT);
  pinMode(RL_out,INPUT);

  pinMode(RR_s0,OUTPUT);    //pin modes
  pinMode(RR_s1,OUTPUT);
  pinMode(RR_s2,OUTPUT);
  pinMode(RR_s3,OUTPUT);
  pinMode(RR_out,INPUT);
  
  // when external interrupt pin 2, 3 go high, call the rising function
  attachInterrupt(digitalPinToInterrupt(interruptPin0), calcPWM1, CHANGE);
  attachInterrupt(digitalPinToInterrupt(interruptPin1), calcPWM2, CHANGE);
  attachInterrupt(digitalPinToInterrupt(interruptPin2), calcPWM3, CHANGE);
  attachInterrupt(digitalPinToInterrupt(interruptPin3), calcPWM4, CHANGE);
  
  Serial.begin(9600);
 }

void loop() {
  
  long duration, stopF;

  digitalWrite(TRIG_F, LOW);
  delayMicroseconds(2);
  digitalWrite(TRIG_F, HIGH);
  delayMicroseconds(10);
  digitalWrite(TRIG_F, LOW);
  
  long distance = pulseIn(ECHO_F, HIGH)*17/1000; 
  stopF = distance*2.2;
  
  Serial.print("\nDIstance : ");
  Serial.print(distance); //측정된 물체로부터 거리값(cm값)을 보여줍니다.
  Serial.println(" Cm");
  
  duration = Serial.println(String(pwm_value[0]) + "  " + String(pwm_value[1]) + "  " + String(pwm_value[2]) + "  " + String(pwm_value[3]));
  
  digitalWrite(TRIG_R, LOW);
  delayMicroseconds(2);
  digitalWrite(TRIG_R, HIGH);
  delayMicroseconds(10);
  digitalWrite(TRIG_R, LOW);
  
  long distanceR = pulseIn(ECHO_R, HIGH)*17/1000; 
  
  Serial.print("\nDIstanceR : ");
  Serial.print(distanceR); //측정된 물체로부터 거리값(cm값)을 보여줍니다.
  Serial.println(" Cm");

  digitalWrite(TRIG_J, LOW);
  delayMicroseconds(2);
  digitalWrite(TRIG_J, HIGH);
  delayMicroseconds(10);
  digitalWrite(TRIG_J, LOW);
  
  long distanceJ = pulseIn(ECHO_J, HIGH)*17/1000;

  Serial.print("\nDIstanceJ : ");
  Serial.print(distanceJ); //측정된 물체로부터 거리값(cm값)을 보여줍니다.
  Serial.println(" Cm");

  digitalWrite(LL_s0,HIGH); //Putting S0/S1 on HIGH/HIGH levels means the output frequency scalling is at 100% (recommended)
  digitalWrite(LL_s1,LOW); //LOW/LOW is off HIGH/LOW is 20% and LOW/HIGH is  2%
  digitalWrite(LR_s0,HIGH); //Putting S0/S1 on HIGH/HIGH levels means the output frequency scalling is at 100% (recommended)
  digitalWrite(LR_s1,LOW); //LOW/LOW is off HIGH/LOW is 20% and LOW/HIGH is  2%
  digitalWrite(RL_s0,HIGH); //Putting S0/S1 on HIGH/HIGH levels means the output frequency scalling is at 100% (recommended)
  digitalWrite(RL_s1,LOW); //LOW/LOW is off HIGH/LOW is 20% and LOW/HIGH is  2%
  digitalWrite(RR_s0,HIGH); //Putting S0/S1 on HIGH/HIGH levels means the output frequency scalling is at 100% (recommended)
  digitalWrite(RR_s1,LOW); //LOW/LOW is off HIGH/LOW is 20% and LOW/HIGH is  2%

  digitalWrite(LL_s2,LOW);        //S2/S3 levels define which set of photodiodes we are using LOW/LOW is for RED LOW/HIGH is for Blue and HIGH/HIGH is for green
  digitalWrite(LL_s3,LOW);

  //자동모드
  if(pwm_value[3] > 1500)
    {
      if(pwm_value[2] > 1500)
        {
          if(jim == 0)
            {
              jim = 1;
            }
        }

      if(pwm_value[2] < 1500)
        {
          if(jim == 1)
            {
              jam += 1;
              jim = 0;
            }
        }
    
      if(jam == 1)
        {
          while (digitalRead(button_up) != LOW)
            {
              digitalWrite(IN1Pin_UD, LOW);
              digitalWrite(IN2Pin_UD, HIGH); 
              analogWrite(ENBPin_UD, 180);

              if(pwm_value[3] < 1500)
                {
                  count = 0;
                  jam = 0;
            
                  digitalWrite(IN1Pin_UD, LOW);
                  digitalWrite(IN2Pin_UD, LOW);
                  analogWrite(ENBPin_UD, 0);
                  break;
                }
                delay(100);
            }
        }
        
      if(digitalRead(button_up) == LOW)
        {
          digitalWrite(IN1Pin_UD, LOW);
          digitalWrite(IN2Pin_UD, HIGH);
          analogWrite(ENBPin_UD, 0);
          delay(1000);
        }
               
      if(distanceJ < 25 || distanceR < 25)
        {
          if(state == 0)
             {
                state = 1; //sensorValue가 600초과시 '1'로 상태확인
                Serial.println("catch");
                delay(5);
             }
        }
                              
      if(distanceJ >= 25 || distanceR >= 25)
        {
          if(state == 1)
             {
                count += 1;
                state = 0; //sensorValue가 600미만시 '0'로 상태확인
             }
        }
                            
      if(count == 3)
        {
          count = 0;
          jam = 0;

          delay(5000);
          
          while (digitalRead(button_down) != LOW)
            {
              digitalWrite(IN1Pin_UD, HIGH);
              digitalWrite(IN2Pin_UD, LOW); 
              analogWrite(ENBPin_UD, 200);

              if(digitalRead(button_down) == LOW)
                {
                  digitalWrite(IN1Pin_UD, HIGH);
                  digitalWrite(IN2Pin_UD, LOW);
                  analogWrite(ENBPin_UD, 0);
                  break;
                }
            }  
          
          int red_color1  = pulseIn(LL_out, LOW);
          red_color1 = map(red_color1, 25,72,255,0);
          red_color1 = constrain(red_color1, 0, 255);
          Serial.print(" Red value1 = ");
          Serial.print(red_color1);
          delay(100);                //Executing GetData function to get the value
        
          digitalWrite(LL_s2,LOW);        
          digitalWrite(LL_s3,HIGH);
           
          int blue_color1 = pulseIn(LL_out, LOW);
          blue_color1 = map(blue_color1, 25,70,255,0);
          blue_color1 = constrain(blue_color1, 0, 255);
          Serial.print(" Blue value1 = ");
          Serial.print(blue_color1);
          delay(100);
           
          digitalWrite(LL_s2,HIGH);        
          digitalWrite(LL_s3,HIGH);
        
          int green_color1 = pulseIn(LL_out, LOW);
          green_color1 = map(green_color1, 30,90,255,0);
          green_color1 = constrain(green_color1, 0, 255);
          Serial.print(" Green value1 = ");
          Serial.print(green_color1);
          Serial.print(" ");
          delay(100);
           
          Serial.println();
        
          digitalWrite(LR_s2,LOW);        //S2/S3 levels define which set of photodiodes we are using LOW/LOW is for RED LOW/HIGH is for Blue and HIGH/HIGH is for green
          digitalWrite(LR_s3,LOW);
           
          int red_color2 = pulseIn(LR_out, LOW);
          red_color2 = map(red_color2, 25,72,255,0);
          red_color2 = constrain(red_color2, 0, 255);
          Serial.print(" Red value2 = ");
          Serial.print(red_color2); 
          delay(100);                //Executing GetData function to get the value
          
          digitalWrite(LR_s2,LOW);        
          digitalWrite(LR_s3,HIGH);
        
          int blue_color2 = pulseIn(LR_out, LOW);
          blue_color2 = map(blue_color2, 25,70,255,0);
          blue_color2 = constrain(blue_color2, 0, 255);
          Serial.print(" Blue value2 = ");
          Serial.print(blue_color2); 
          delay(100);
           
          digitalWrite(LR_s2,HIGH);        
          digitalWrite(LR_s3,HIGH);
          
          int green_color2 = pulseIn(LR_out, LOW);
          green_color2 = map(green_color2, 30,90,255,0);
          green_color2 = constrain(green_color2, 0, 255);
          Serial.print(" Green value2 = ");
          Serial.print(green_color2);
          Serial.print(" ");
          delay(100);
        
          Serial.println();
        
          digitalWrite(RL_s2,LOW);        //S2/S3 levels define which set of photodiodes we are using LOW/LOW is for RED LOW/HIGH is for Blue and HIGH/HIGH is for green
          digitalWrite(RL_s3,LOW);
           
          int red_color3 = pulseIn(RL_out, LOW);
          red_color3 = map(red_color3, 25,72,255,0);
          red_color3 = constrain(red_color3, 0, 255);
          Serial.print(" Red value3 = ");
          Serial.print(red_color3);
          delay(100);                //Executing GetData function to get the value
          
          digitalWrite(RL_s2,LOW);        
          digitalWrite(RL_s3,HIGH);
           
          int blue_color3 = pulseIn(RL_out, LOW);
          blue_color3 = map(blue_color3, 25,70,255,0);
          blue_color3 = constrain(blue_color3, 0, 255);
          Serial.print(" Blue value3 = ");
          Serial.print(blue_color3);
          delay(100);
        
          digitalWrite(RL_s2,HIGH);        
          digitalWrite(RL_s3,HIGH);
          
          int green_color3 = pulseIn(RL_out, LOW);
          green_color3 = map(green_color3, 30,90,255,0);
          green_color3 = constrain(green_color3, 0, 255);
          Serial.print(" Green value3 = ");
          Serial.print(green_color3);
          Serial.print(" ");
          delay(100);
        
          Serial.println();
        
          digitalWrite(RR_s2,LOW);        //S2/S3 levels define which set of photodiodes we are using LOW/LOW is for RED LOW/HIGH is for Blue and HIGH/HIGH is for green
          digitalWrite(RR_s3,LOW);
           
          int red_color4 = pulseIn(RR_out, LOW);
          red_color4 = map(red_color4, 25,72,255,0);
          red_color4 = constrain(red_color4, 0, 255);
          Serial.print(" Red value4 = ");
          Serial.print(red_color4);
          delay(100);                //Executing GetData function to get the value
        
          digitalWrite(RR_s2,LOW);        
          digitalWrite(RR_s3,HIGH);
           
          int blue_color4 = pulseIn(RR_out, LOW);
          blue_color4 = map(blue_color4, 25,70,255,0);
          blue_color4 = constrain(blue_color4, 0, 255);
          Serial.print(" Blue value4 = ");
          Serial.print(blue_color4);
          delay(100);
        
          digitalWrite(RR_s2,HIGH);        
          digitalWrite(RR_s3,HIGH);
          
          int green_color4 = pulseIn(RR_out, LOW);
          green_color4 = map(green_color4, 30,90,255,0);
          green_color4 = constrain(green_color4, 0, 255);
          Serial.print(" Green value4 = ");
          Serial.print(green_color4);
          Serial.print(" ");
          delay(100);
        
          Serial.println();
          
          // 자동 운전 센서 수신 22.09.17(확인 필요)
          if(distance >= 20)
            {
               digitalWrite(IN1Pin_L, HIGH);
               digitalWrite(IN2Pin_L, LOW);
               analogWrite(ENBPin_L, 200);
               delay(10);
               digitalWrite(IN1Pin_R, HIGH);
               digitalWrite(IN2Pin_R, LOW);
               analogWrite(ENBPin_R, 200);
               delay(10);
               
              if(red_color1 > blue_color1 || red_color3 > blue_color3 )
                {
                  digitalWrite(IN1Pin_L, LOW);
                  digitalWrite(IN2Pin_L, LOW);
                  analogWrite(ENBPin_L, 200);
                  delay(10);
                  digitalWrite(IN1Pin_R, HIGH);
                  digitalWrite(IN2Pin_R, LOW);
                  analogWrite(ENBPin_R, 200);
                  delay(10);
                }
                
              if(red_color2 > blue_color2 || red_color4 > blue_color4 )
                {
                  digitalWrite(IN1Pin_L, HIGH);
                  digitalWrite(IN2Pin_L, LOW);
                  analogWrite(ENBPin_L, 200);
                  delay(10);
                  digitalWrite(IN1Pin_R, LOW);
                  digitalWrite(IN2Pin_R, LOW);
                  analogWrite(ENBPin_R, 200);
                  delay(10);
                }
            }

          else if(distance >= 10 && distance < 20)
            {
              digitalWrite(IN1Pin_L, HIGH);
              digitalWrite(IN2Pin_L, LOW);
              analogWrite(ENBPin_L, stopF);
              delay(10);
              digitalWrite(IN1Pin_R, HIGH);
              digitalWrite(IN2Pin_R, LOW);
              analogWrite(ENBPin_R, stopF);
              delay(10); 
            }
                          
          else if(distance < 10 || distanceR < 10)
            {
              digitalWrite(IN1Pin_L, LOW);
              digitalWrite(IN2Pin_L, LOW);
              analogWrite(ENBPin_L, 0);
              delay(10);
              digitalWrite(IN1Pin_R, LOW);
              digitalWrite(IN2Pin_R, LOW);
              analogWrite(ENBPin_R, 0);
              delay(10);  
            }  
        }
    } 
  
  
  //수동모드(정차시, 초음파동작)
  else if(pwm_value[3] < 1500)
    {
      //리프트 상하강 모터
      if(pwm_value[2] >= 1300 && pwm_value[2] <= 1500)
        {
          digitalWrite(IN1Pin_UD, LOW);
          digitalWrite(IN2Pin_UD, LOW);
          analogWrite(ENBPin_UD, 0);
          delay(10);
        }
              
      else if(pwm_value[2] < 1300)
        {
          digitalWrite(IN1Pin_UD, HIGH);
          digitalWrite(IN2Pin_UD, LOW);
          analogWrite(ENBPin_UD, 200);
          delay(100);
          
          if(digitalRead(button_down) == LOW)
            {
              digitalWrite(IN1Pin_UD, HIGH);
              digitalWrite(IN2Pin_UD, LOW);
              analogWrite(ENBPin_UD, 0);
              delay(1000);
            }
        }
          
      else if(pwm_value[2] > 1500)
        {
          digitalWrite(IN1Pin_UD, LOW);
          digitalWrite(IN2Pin_UD, HIGH);
          analogWrite(ENBPin_UD, 200);
          delay(100);
          
          if(digitalRead(button_up) == LOW)
            {
              digitalWrite(IN1Pin_UD, LOW);
              digitalWrite(IN2Pin_UD, HIGH);
              analogWrite(ENBPin_UD, 0);
              delay(1000);
            }
        }   
      //정지
      if(pwm_value[0] >= 1400 && pwm_value[0] <= 1500)
        {
          digitalWrite(IN1Pin_L, LOW);
          digitalWrite(IN2Pin_L, LOW);
          analogWrite(ENBPin_L, 0);
          delay(10);
          digitalWrite(IN1Pin_R, LOW);
          digitalWrite(IN2Pin_R, LOW);
          analogWrite(ENBPin_R, 0);
          delay(10);
        }
          
      else if(distance < 20)
        {
          digitalWrite(IN1Pin_L, LOW);
          digitalWrite(IN2Pin_L, LOW);
          analogWrite(ENBPin_L, 0);
          delay(10);
          digitalWrite(IN1Pin_R, LOW);
          digitalWrite(IN2Pin_R, LOW);
          analogWrite(ENBPin_R, 0);
          delay(10);
        }
      
      //전진
      else if(pwm_value[0] > 1500 && pwm_value[0] <= 2000)
        {
          //좌회전
          if(pwm_value[1] >= 984 && pwm_value[1] < 1280)
            {
              int speed_Ri = (((pwm_value[1]-2000)*-1)-484.5)/2.1;
              digitalWrite(IN1Pin_R, HIGH);
              digitalWrite(IN2Pin_R, LOW);
              analogWrite(ENBPin_R, speed_Ri);
              delay(10);
              digitalWrite(IN1Pin_L, LOW);
              digitalWrite(IN2Pin_L, LOW);
              analogWrite(ENBPin_L, 0);
              delay(10);
            }
            
          //우회전
          else if(pwm_value[1] > 1500 && pwm_value[1] <= 1988)
            {
              int speed_L = (pwm_value[1]-1365.8)/2.44;
              digitalWrite(IN1Pin_L, HIGH);
              digitalWrite(IN2Pin_L, LOW);
              analogWrite(ENBPin_L, speed_L);
              delay(10);
              digitalWrite(IN1Pin_R, LOW);
              digitalWrite(IN2Pin_R, LOW);
              analogWrite(ENBPin_R, 0);
              delay(10);
            }
    
          else if(distance >= 40)
            {
              int speed_F = (pwm_value[0]-1362.5)/2.5;
              digitalWrite(IN1Pin_L, HIGH);
              digitalWrite(IN2Pin_L, LOW);
              analogWrite(ENBPin_L, speed_F);
              delay(10);
              digitalWrite(IN1Pin_R, HIGH);
              digitalWrite(IN2Pin_R, LOW);
              analogWrite(ENBPin_R, speed_F);
              delay(10);
            }  
              
          else if(20 <= distance < 40)
            {
              digitalWrite(IN1Pin_L, HIGH);
              digitalWrite(IN2Pin_L, LOW);
              analogWrite(ENBPin_L, stopF);
              delay(10);
              digitalWrite(IN1Pin_R, HIGH);
              digitalWrite(IN2Pin_R, LOW);
              analogWrite(ENBPin_R, stopF);
              delay(10);
            }
    
          //좌우조향_정지
          else if(pwm_value[1] >= 1280 && pwm_value[1] <= 1500)
            {
              digitalWrite(IN1Pin_L, LOW);
              digitalWrite(IN2Pin_L, LOW);
              analogWrite(ENBPin_L, 0);
              delay(10);
              digitalWrite(IN1Pin_R, LOW);
              digitalWrite(IN2Pin_R, LOW);
              analogWrite(ENBPin_R, 0);
              delay(10);
            }
        }
    
      //후진
      else if(pwm_value[0] >= 980 && pwm_value[0] < 1400)
        {
          if(distance >= 40)
            {
              int speed_R = (((pwm_value[0]-2000)*-1)-484.5)/2.1;
              digitalWrite(IN1Pin_L, LOW);
              digitalWrite(IN2Pin_L, HIGH);
              analogWrite(ENBPin_L, speed_R);
              delay(10);
              digitalWrite(IN1Pin_R, LOW);
              digitalWrite(IN2Pin_R, HIGH);
              analogWrite(ENBPin_R, speed_R);
              delay(10);
            }
            
          //좌회전
          if(pwm_value[1] >= 984 && pwm_value[1] < 1300)
            {
              int speed_Ri = (((pwm_value[1]-2000)*-1)-484.5)/2.1;
              digitalWrite(IN1Pin_R, LOW);
              digitalWrite(IN2Pin_R, HIGH);
              analogWrite(ENBPin_R, speed_Ri);
              delay(10);
              digitalWrite(IN1Pin_L, LOW);
              digitalWrite(IN2Pin_L, LOW);
              analogWrite(ENBPin_L, 0);
              delay(10);
            }
            
          //우회전
          else if(pwm_value[1] > 1500 && pwm_value[1] <= 1972)
            {
              int speed_L = (pwm_value[1]-1370.2)/2.36;
              digitalWrite(IN1Pin_L, LOW);
              digitalWrite(IN2Pin_L, HIGH);
              analogWrite(ENBPin_L, speed_L);
              delay(10);
              digitalWrite(IN1Pin_R, LOW);
              digitalWrite(IN2Pin_R, LOW);
              analogWrite(ENBPin_R, 0);
              delay(10);
            }

          else if(distance >= 40)
            {
              int speed_R = (((pwm_value[0]-2000)*-1)-484.5)/2.1;
              digitalWrite(IN1Pin_L, LOW);
              digitalWrite(IN2Pin_L, HIGH);
              analogWrite(ENBPin_L, speed_R);
              delay(10);
              digitalWrite(IN1Pin_R, LOW);
              digitalWrite(IN2Pin_R, HIGH);
              analogWrite(ENBPin_R, speed_R);
              delay(10);
            }

          //좌우조향_정지
          else if(pwm_value[1] >= 1300 && pwm_value[1] <= 1500)
            {
              digitalWrite(IN1Pin_L, LOW);
              digitalWrite(IN2Pin_L, LOW);
              analogWrite(ENBPin_L, 0);
              delay(10);
              digitalWrite(IN1Pin_R, LOW);
              digitalWrite(IN2Pin_R, LOW);
              analogWrite(ENBPin_R, 0);
              delay(10);
            }
        }
    }

  //리프트 상하강 모터
      if(pwm_value[2] >= 1300 && pwm_value[2] <= 1500)
        {
          digitalWrite(IN1Pin_UD, LOW);
          digitalWrite(IN2Pin_UD, LOW);
          analogWrite(ENBPin_UD, 0);
          delay(10);
        }
              
      else if(pwm_value[2] < 1300)
        {
          digitalWrite(IN1Pin_UD, HIGH);
          digitalWrite(IN2Pin_UD, LOW);
          analogWrite(ENBPin_UD, 200);
          delay(100);
          
          if(digitalRead(button_down) == LOW)
            {
              digitalWrite(IN1Pin_UD, HIGH);
              digitalWrite(IN2Pin_UD, LOW);
              analogWrite(ENBPin_UD, 0);
              delay(1000);
            }
        }
          
      else if(pwm_value[2] > 1500)
        {
          digitalWrite(IN1Pin_UD, LOW);
          digitalWrite(IN2Pin_UD, HIGH);
          analogWrite(ENBPin_UD, 200);
          delay(100);
          
          if(digitalRead(button_up) == LOW)
            {
              digitalWrite(IN1Pin_UD, LOW);
              digitalWrite(IN2Pin_UD, HIGH);
              analogWrite(ENBPin_UD, 0);
              delay(1000);
            }
        }   
 }

void calcPWM1() //전후진
{
  if(digitalRead(interruptPin0) == HIGH) { 
    timer[0] = micros(); 
    } 
  else {
    if(timer[0] != 0) {
      pwm_value[0] = micros() - timer[0];
      }
    } 
}

void calcPWM2() //좌우조향
{
  if(digitalRead(interruptPin1) == HIGH) { 
    timer[1] = micros();
    } 
  else {
    if(timer[1] != 0) {
      pwm_value[1] = micros() - timer[1];
      }
    } 
}

void calcPWM3() //리프트_상하
{
  if(digitalRead(interruptPin2) == HIGH) { 
    timer[2] = micros();
    } 
  else {
    if(timer[2] != 0) {
      pwm_value[2] = micros() - timer[2];
      }
    } 
}

void calcPWM4() //수동, 자동 변환
{
  if(digitalRead(interruptPin3) == HIGH) { 
    timer[3] = micros();
    } 
  else {
    if(timer[3] != 0) {
      pwm_value[3] = micros() - timer[3];
      }
    } 
} 
