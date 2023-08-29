#include <Servo.h>
Servo myServo;
const int wait_face_pin = 3;
const int open_door_pin = 4;
int indoor_way1 = 0;
int indoor_way2 = 0;
int face_recognition = 0;
int indoor_step = 0;
String send_data = "";
int indoor_way1_th = 15;
int indoor_way2_th = 15;
int car_state = 0;
void setup() {
  Serial.begin(9600);
  pinMode(wait_face_pin, OUTPUT);
  pinMode(open_door_pin, OUTPUT);
  digitalWrite(wait_face_pin, HIGH);
  digitalWrite(open_door_pin, HIGH);
  digitalWrite(wait_face_pin, LOW);
  digitalWrite(open_door_pin, LOW); 
  myServo.attach(9);
  delay(1000);
  myServo.write(90);
  delay(1000);
  myServo.write(180);
  delay(1000);
  myServo.write(270);
  delay(1000);
  myServo.write(360);
  delay(1000);
  myServo.write(90);
}
void loop() {
  indoor_way1 = map(analogRead(A2), 0, 1023, 0, 100); //on 3 off
  indoor_way2 = map(analogRead(A3), 0, 1023, 0, 100); //on 5 off
  //Serial.println(indoor_way1);
  
  // 人不在房間
  if (indoor_step == 0 && indoor_way1 < indoor_way1_th) {
    //進門光敏1偵測，亮黃燈與等待人臉辨識成功
    Serial.println("人在房門前");
    indoor_step = 100;
    while(Serial.available() == false){
      digitalWrite(wait_face_pin, HIGH);
      delay(100);
      digitalWrite(wait_face_pin, LOW);
      delay(100);
    }
    send_data = Serial.readString();
    //Serial.println("send_data:"+send_data);
    if (send_data.indexOf("car_false") != -1){
      indoor_step = 0;
    }
    delay(1000);
  }
  if (indoor_step == 100 && indoor_way1 < indoor_way1_th) {
    //進門光敏1偵測，亮黃燈與等待人臉辨識成功
    Serial.println("人在房門前，車也在");
    indoor_step = 1;
    digitalWrite(wait_face_pin, HIGH);
    //送出辨識
    Serial.println("face_recognition");
    //等待辨識
    while(Serial.available() == false){
      digitalWrite(wait_face_pin, HIGH);
      delay(100);
      digitalWrite(wait_face_pin, LOW);
      delay(100);
    }
    send_data = Serial.readString();
    while(send_data.indexOf("recognition_true") == -1){
      Serial.println("人臉辨識失敗");
    }
    digitalWrite(wait_face_pin, LOW);
    face_recognition = 1;
  } else if (indoor_step == 1 && face_recognition == 1) {
    Serial.println("人臉辨識成功，開門");
    myServo.write(180);
    indoor_step = 2;
    face_recognition = 0;
    digitalWrite(open_door_pin, HIGH);
  } else if (indoor_step == 2 && indoor_way2 < indoor_way2_th) {
    indoor_step = 3;
    Serial.println("進入房門，送人在房間到server");
    myServo.write(90);
    digitalWrite(wait_face_pin, LOW);
    digitalWrite(open_door_pin, LOW);
    delay(2000);
  }
  
  // 人在房間
  if (indoor_step == 3 && map(analogRead(A3), 0, 1023, 0, 100) < indoor_way2_th) {
    Serial.println("人在房間，要出去");
    digitalWrite(open_door_pin, HIGH); // 開門
    myServo.write(180);
    delay(500);
    indoor_step = 4;
  }
  if (indoor_step == 4 && map(analogRead(A2), 0, 1023, 0, 100) < indoor_way1_th) {
    Serial.println("人剛出房間，送人不在房間到server");
    digitalWrite(open_door_pin, LOW); // 關門
    myServo.write(90);
    delay(2000);
    indoor_step = 0;
  }
  //Serial.println(map(analogRead(A2), 0, 1023, 0, 100));

  
  delay(100); 
  
}

void serialEvent() {
  /*
  while (Serial.available()) {
    send_data = Serial.readString();
    Serial.println("send_data:"+send_data);
    if (send_data.indexOf("car_false") != -1){
      indoor_step = -1;
    }else if(send_data.indexOf("car_true") !=-1 && indoor_step==-1){
      indoor_step = 0;
    }
  }
  */
}
