#include "SoftwareI2C.h"
#include "MAX30100_PulseOximeter.h"

SoftwareI2C wire;

PulseOximeter pox;

void setup() {
  // put your setup code here, to run once:
    Serial.begin(115200);
    Serial.println("Initializing Software I2C");
    pox.initSoftwareI2C(&wire,4, 3);       // sda, scl

    Serial.println("Initializing pulse oximeter..");
    //Inicializa o Sensor MAX30100
    if (!pox.begin()) {
        Serial.println("Falha na Inicializacao do Sensor");
        for(;;);
    } else {
        Serial.println("Comunicacao Realizada com Sucesso!");
    }


}

void loop() {
  // put your main code here, to run repeatedly:

}
