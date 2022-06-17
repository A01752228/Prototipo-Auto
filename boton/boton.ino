#include <SPI.h>      //  Libreria SPI
#include <MFRC522.h>      // Libreria  MFRC522
#include <Servo.h>     // Libreria  SERVO

#define RST_PIN  9      // Pin de reset
#define SS_PIN  10      // Pin de slave select

MFRC522 mfrc522(SS_PIN, RST_PIN); // Objeto mfrc522 enviando pines de slave select y reset

byte LecturaUID[4];         // Array para almacenar el UID leido
byte Usuario1[4]= {0xB6, 0xE0, 0x61, 0x33} ;    // NUMERO DEL USUARIO 1 (ponga el de su tarjeta)
byte Usuario2[4]= {0xE6, 0x73, 0x61, 0x30} ;    // NUMERO DEL USUARIO 2 (ponga el de su tarjeta)
int analogo5=0;                                 // Variable de lectura del Analogo5 para sensor de obstaculos
Servo servoPT,servoMotor;     

//RASP
int x = 0;

void setup() {
  //RASP
  pinMode(2, INPUT);
  
  //Boton e intermitentess
  pinMode(6,OUTPUT);
  pinMode(7, OUTPUT);
  //Puerta
  Serial.begin(115200);     // inicializa comunicacion por monitor serie a 9600 bps
  
  servoPT.attach(4);      // Sevo asociado al pin 4 y lleva a 170 grados
  servoPT.write(90);
  servoMotor.attach(5);      // Sevo asociado al pin 5 y lleva a 170 grados
  servoPT.write(90);
  
  SPI.begin();        // inicializa bus SPI
  mfrc522.PCD_Init();     // inicializa modulo lector
  //Serial.println("Sistema Activado");    // Muestra texto Listo
}
void loop() {
  // Si el pin2 envia 0 es que el pulsador no esta presionando.
  if(digitalRead(2)== x){
     Serial.println("");   
  }
  else if(digitalRead(2)==0 && x == 1){
     x = not(x);
     Serial.println("Presionado");    
  }
  else{
    x = not(x);
  }



   //
   loopBoton();
   loopIntermitentes();
   loopPuerta();
}
void loopBoton(){
  digitalWrite(6, HIGH);
}

void loopIntermitentes(){
  digitalWrite(7, HIGH);
  delay(250);
  digitalWrite(7, LOW);
  delay(250); 
}

void loopPuerta() {
  if ( ! mfrc522.PICC_IsNewCardPresent())   // si no hay una tarjeta presente
    return;           // retorna al loop esperando por una tarjeta
  
  if ( ! mfrc522.PICC_ReadCardSerial())     // si no puede obtener datos de la tarjeta
    return;           // retorna al loop esperando por otra tarjeta
    
    //Serial.print("UID:");       // muestra texto UID:
    for (byte i = 0; i < 4; i++) { // bucle recorre de a un byte por vez el UID
      if (mfrc522.uid.uidByte[i] < 0x10){   // si el byte leido es menor a 0x10
        //Serial.print(" 0");       // imprime espacio en blanco y numero cero
        }
        else{           // sino
          //Serial.print(" ");        // imprime un espacio en blanco
          }
          //Serial.print(mfrc522.uid.uidByte[i], HEX);    // imprime el byte del UID leido en hexadecimal
          LecturaUID[i]=mfrc522.uid.uidByte[i];     // almacena en array el byte del UID leido      
          }
          
          //Serial.print("\t");         // imprime un espacio de tabulacion             
                   
          if(comparaUID(LecturaUID, Usuario1)){    // llama a funcion comparaUID con Usuario1
            //Serial.println("Bienvenido Saul"); // si retorna verdadero muestra texto bienvenida
            abrirPuerta();                      // funcion para abrir la puerta
          }
          else if(comparaUID(LecturaUID, Usuario2)){ // llama a funcion comparaUID con Usuario2
            //Serial.println("Bienvenido Alan"); // si retorna verdadero muestra texto bienvenida
             abrirPuerta();                      // funcion para abrir la puerta
          }
           else {          // si retorna falso
            //Serial.println("No Registrado");    // muestra texto equivalente a acceso denegado          
             Mal_Registro();                    // funcion sonido de targeta no identificada
           }  
                  mfrc522.PICC_HaltA();     // detiene comunicacion con tarjeta    
}

void abrirPuerta() {
  servoPT.write(160);
  servoMotor.write(45);// Abrir la puerta 
  delay(4000);             // Tiempo de la puerta abierta
  servoPT.write(90); 
  servoMotor.write(90); // Cierra puerta 
}


void Mal_Registro() {      // Activa el Buzzer 2 veces por tarjeta no autorizada
  /*digitalWrite(7, HIGH);
  delay(200);
  digitalWrite(7, LOW);
  delay(100);
  digitalWrite(7, HIGH);
  delay(200);
  digitalWrite(7, LOW);*/
}

boolean comparaUID(byte lectura[],byte usuario[]) // funcion comparaUID
{
  for (byte i=0; i < 4; i++){    // bucle recorre de a un byte por vez el UID
  if(lectura[i] != usuario[i])        // si byte de UID leido es distinto a usuario
    return(false);          // retorna falso
  }
  return(true);           // si los 4 bytes coinciden retorna verdadero
}
