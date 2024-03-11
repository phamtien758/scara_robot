#include <Servo.h>

#define MICROSTEP 16
#define R1_DIR    A1
#define R1_STEP   A0
#define R1_EN     38
#define R3_DIR    A7
#define R3_STEP   A6
#define R3_EN     A2
#define R4_DIR    28
#define R4_STEP   26
#define R4_EN     24
#define P2_DIR    48
#define P2_STEP   46
#define P2_EN     A8

#define R1_MIN  3
#define R3_MIN  14
#define R4_MIN  15
#define P2_MIN  2

#define GEAR_RATIO_R1 10.619   // (40/20)*(100/20)
#define GEAR_RATIO_R3 9.199
#define GEAR_RATIO_R4 3
#define GEAR_RATIO_P2 2
#define VITME_PITCH 8     // Bước ren vitme

float steps_per_angle = MICROSTEP / 1.8;      //Số steps để quay được 1 độ

float last_R1 = 0;
float last_R3 = 0;
float last_R4 = 0;
float last_P2 = 0;

Servo gripper;


void setup() {
  Serial.begin(9600);

  gripper.attach(11);
  pinMode(R1_DIR, OUTPUT);
  pinMode(R1_STEP, OUTPUT);
  pinMode(R1_EN, OUTPUT);
  
  pinMode(R3_DIR, OUTPUT);
  pinMode(R3_STEP, OUTPUT);
  pinMode(R3_EN, OUTPUT);

  pinMode(R4_DIR, OUTPUT);
  pinMode(R4_STEP, OUTPUT);
  pinMode(R4_EN, OUTPUT);

  pinMode(P2_DIR, OUTPUT);
  pinMode(P2_STEP, OUTPUT);
  pinMode(P2_EN, OUTPUT);

  pinMode(R1_MIN, INPUT_PULLUP);
  pinMode(R3_MIN, INPUT_PULLUP);
  pinMode(R4_MIN, INPUT_PULLUP);
  pinMode(P2_MIN, INPUT_PULLUP);

  digitalWrite(R1_EN, LOW);
  digitalWrite(R3_EN, LOW);
  digitalWrite(R4_EN, LOW);
  digitalWrite(P2_EN, LOW);

  delay(500);
  
}

void loop(){
  
  String dulieu = "";
  while(Serial.available()>0)
  {
    char c = Serial.read();
    dulieu = dulieu + c;
    delay(5);
  }
  
  if(dulieu[0]=='a')
  {
    String r1_raw = "";
    String p2_raw = "";
    String r3_raw = "";
    String r4_raw = "";

    float angle_r1 = 0;
    float distance_p2 = 0;
    float angle_r3 = 0;
    float angle_r4 = 0;
    int i=1;
    
    while(dulieu[i]!='b')
    {
      r1_raw += dulieu[i];
      ++i;
    }
    ++i;
    while(dulieu[i]!='c')
    {
      p2_raw += dulieu[i];
      ++i;
    }
    ++i;
    while(dulieu[i]!='d')
    {
      r3_raw += dulieu[i];
      ++i;
    }
    ++i;
    while(i<dulieu.length())
    {
      r4_raw += dulieu[i];
      ++i;
    }
    if(r1_raw=="") {angle_r1=last_R1;}  else {angle_r1 = r1_raw.toFloat();}
    if(r3_raw=="") {angle_r3=last_R3;}  else {angle_r3 = r3_raw.toFloat();}
    if(r4_raw=="") {angle_r4=last_R4;}  else {angle_r4 = r4_raw.toFloat();}
    if(p2_raw=="") {distance_p2=last_P2;}  else {distance_p2 = p2_raw.toFloat();}
    
    motor_run(angle_r1, distance_p2, angle_r3, angle_r4,2);
//    Serial.println(r1_raw);
//    Serial.println(p2_raw);
//    Serial.println(r3_raw);
//    Serial.println(r4_raw);
//Serial.println(angle_r1);
//Serial.println(angle_r3);
//Serial.println(angle_r4);
//Serial.println(distance_p2);
  }
  
  if(dulieu == "home")
  {
    go_home();
    last_R1 = 0;
    last_P2 = 0;
    last_R3 = 0;
    last_R4 = 0;
    motor_run(98,80,127.5,190,2);
    last_R1 = 0;
    last_P2 = 0;
    last_R3 = 0;
    last_R4 = 0;
    gripper.write(150);
    delay(500);
  }

  if(dulieu == "on")
  {
    gripper_on();
  }
  if(dulieu == "off")
  {
    gripper_off();
  }

}

void motor_run(float angle_R1, float distance_P2, float angle_R3, float angle_R4, int safe) //kiểm tra CTHT: bật -> safe=0, tắt -> safe=x (x!=1 và x!=0)
{
  //Góc cần xoay
  float delta_R1 = angle_R1 - last_R1;
  float delta_R3 = angle_R3 - last_R3;
  float delta_R4 = angle_R4 - last_R4;
  float delta_P2 = distance_P2 - last_P2;
  
  //Số steps cần
  float total_steps_R1 = abs(delta_R1) * steps_per_angle * GEAR_RATIO_R1;
  float total_steps_R3 = abs(delta_R3) * steps_per_angle * GEAR_RATIO_R3;
  float total_steps_R4 = abs(delta_R4) * steps_per_angle * GEAR_RATIO_R4;
  float total_steps_P2 = ((360 * abs(delta_P2))/ VITME_PITCH) * steps_per_angle * GEAR_RATIO_P2;   // Với bước ren =8, xoay một vòng thì đi được 8mm
  //Serial.println(total_steps_R1);
  //Điều chỉnh hướng
  if(delta_R1 > 0)
    digitalWrite(R1_DIR, LOW);
  else
    digitalWrite(R1_DIR, HIGH);

  if(delta_R3 > 0)
    digitalWrite(R3_DIR, HIGH);
  else
    digitalWrite(R3_DIR, LOW);

  if(delta_R4 > 0)
    digitalWrite(R4_DIR, HIGH);
  else
    digitalWrite(R4_DIR, LOW);

  if(delta_P2 > 0)
    digitalWrite(P2_DIR, LOW);
  else
    digitalWrite(P2_DIR, HIGH);

  //Chạy motor
  while(digitalRead(R4_MIN) != safe && total_steps_R4 > 0)
  {
    digitalWrite(R4_STEP, HIGH);
    digitalWrite(R4_STEP, LOW);
    delayMicroseconds(500);
    --total_steps_R4;
  }
  while(digitalRead(R3_MIN) != safe && total_steps_R3 > 0)
  {
    digitalWrite(R3_STEP, HIGH);
    digitalWrite(R3_STEP, LOW);
    delayMicroseconds(500);
    --total_steps_R3;
  }
  while(digitalRead(R1_MIN) != safe && total_steps_R1 > 0)
  {
    digitalWrite(R1_STEP, HIGH);
    digitalWrite(R1_STEP, LOW);
    delayMicroseconds(500);
    --total_steps_R1;
    //Serial.println(total_steps_R1);
  }
  while(digitalRead(P2_MIN) != safe && total_steps_P2 > 0)
  {
    digitalWrite(P2_STEP, HIGH);
    digitalWrite(P2_STEP, LOW);
    delayMicroseconds(200);
    --total_steps_P2;
  }
  Serial.print("ok");
  Serial.flush();
  last_R1 = angle_R1;
  last_R3 = angle_R3;
  last_R4 = angle_R4;
  last_P2 = distance_P2;
}

void go_home()
{
  gripper.write(150);
  delay(1000);
  digitalWrite(P2_DIR, HIGH);
  while(digitalRead(P2_MIN) != 0)
  {
    digitalWrite(P2_STEP, HIGH);
    digitalWrite(P2_STEP, LOW);
    delayMicroseconds(200);
  }
  digitalWrite(R4_DIR, LOW);
  while(digitalRead(R4_MIN) != 0)
  {
    digitalWrite(R4_STEP, HIGH);
    digitalWrite(R4_STEP, LOW);
    delayMicroseconds(500);
  }
  digitalWrite(R3_DIR, LOW);
  while(digitalRead(R3_MIN) != 0)
  {
    digitalWrite(R3_STEP, HIGH);
    digitalWrite(R3_STEP, LOW);
    delayMicroseconds(500);
  }
  digitalWrite(R1_DIR, HIGH);
  while(digitalRead(R1_MIN) != 0)
  {
    digitalWrite(R1_STEP, HIGH);
    digitalWrite(R1_STEP, LOW);
    delayMicroseconds(500);
  }
}
void gripper_on()
{
  gripper.write(46);
  delay(200);
  Serial.print("ok");
  Serial.flush();
}
void gripper_off()
{
  gripper.write(100);
  delay(200);
  Serial.print("ok");
  Serial.flush();
}
