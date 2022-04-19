#include <Wire.h>
#include <LiquidCrystal_I2C.h>
#include "MAX30100_PulseOximeter.h"

LiquidCrystal_I2C lcd(0x27,16,2);  // Configurando o endereco do LCD 16x2 para 0x27

#define TEMPO_LEITURA_MS     1000

PulseOximeter pox;

long int tempo = 0;

// Callback (registered below) fired when a pulse is detected
void onBeatDetected()
{
    Serial.println("Beat!");
}

void setup()
{
    Serial.begin(115200);

    Serial.print("Initializing pulse oximeter..");

    //Inicializa o Sensor MAX30100
    if (!pox.begin()) {
        Serial.println("Falha na Inicializacao do Sensor");
        for(;;);
    } else {
        Serial.println("Comunicacao Realizada com Sucesso!");
    }

    //O padrao de corrente para o LED e de 50mA, mas poderá ser alterado
    //Descomente a linha abaixo e ajuste o valor de corrente desejado para a aplicacao
    //pox.setIRLedCurrent(MAX30100_LED_CURR_30_6MA);

    //Registrar um retorno de chamada para a detecção de batimentos
    pox.setOnBeatDetectedCallback(onBeatDetected);
}

void loop()
{
    //Atualizacao dos dados do Sensor MAX30100
    pox.update();

    if (millis() - tempo < TEMPO_LEITURA_MS) 
    {
        Serial.print("Frequencia Cardiaca:");
        Serial.print(pox.getHeartRate());
        Serial.print("SpO2:");
        Serial.print(pox.getSpO2());
        Serial.println("%");

        tempo = millis();

        lcd.clear();
        lcd.setCursor(0,0);
        lcd.print("BPM:");
        lcd.setCursor(6,0);
        lcd.print(pox.getHeartRate());

        lcd.clear();
        lcd.setCursor(0,1);
        lcd.print("SpO2:");
        lcd.setCursor(7,0);
        lcd.print(pox.getSpO2());
    }
}
