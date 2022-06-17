#include <AFMotor.h>

//Dip Switch
int SwB1 = 33, SwB2 = 35;
bool VB1,VB2;

//Motor
AF_DCMotor motor1(1);
AF_DCMotor motor2(2);
AF_DCMotor motor3(3);
AF_DCMotor motor4(4);

//Ultrasonico
int Trig = 39;
int Echo = 41;
const int pBuzzer = 43;
int TIEMPO;
int DISTANCIA;

//Potenciomotro
const int velocidad = A13;

void setup(){
  //Comunicacion
  Serial.begin(9600);
  //Dip switch
  pinMode(SwB1,INPUT);
  pinMode(SwB2,INPUT);
  //Ultrasonico
  pinMode(Trig, OUTPUT);
  pinMode(Echo, INPUT);
  pinMode(pBuzzer,OUTPUT);
  //Potenciometro
  pinMode(velocidad, OUTPUT);
  
  }

void loop(){
   int brillo = analogRead(velocidad);
   int i = brillo * .2490234375;

   Serial.println(i);

  //Motor
  motor1.setSpeed(i);
  motor2.setSpeed(i);
  motor3.setSpeed(i);
  motor4.setSpeed(i);
  
  VB1 = digitalRead(SwB1);
  VB2 = digitalRead(SwB2);

  Serial.print(VB1);
  Serial.print(VB2);
  
  if (VB1 == 0){   
  digitalWrite(Trig,HIGH);
  delay(1);
  digitalWrite(Trig,LOW);
  TIEMPO = pulseIn(Echo,HIGH);
  DISTANCIA = TIEMPO / 58.2; //Obtencion de distancia en centrimentros
  delay(100);
  Serial.println(String(DISTANCIA));
  if (DISTANCIA <= 30 && DISTANCIA >= 2){ //Si la distanciia es menor a 30
    digitalWrite(pBuzzer,HIGH);
    delay(DISTANCIA*10);
    digitalWrite(pBuzzer,LOW);
    }
  if(DISTANCIA <= 8){
    motor1.run(RELEASE);
    motor2.run(RELEASE);
    motor3.run(RELEASE);
    motor4.run(RELEASE); 
    }
   else{
    motor1.run(BACKWARD);
    motor2.run(BACKWARD);
    motor3.run(BACKWARD);
    motor4.run(BACKWARD); 
    }
  }

  else if (VB2 == 0){
  motor1.run(FORWARD);
  motor2.run(FORWARD);
  motor3.run(FORWARD);
  motor4.run(FORWARD); 
  }

  else {
  motor1.run(RELEASE);
  motor2.run(RELEASE);
  motor3.run(RELEASE);
  motor4.run(RELEASE);  
    }
  }
