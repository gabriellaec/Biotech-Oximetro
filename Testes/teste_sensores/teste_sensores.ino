#include <Wire.h>
#include <LiquidCrystal_I2C.h>
#include "MAX30100_PulseOximeter.h"

LiquidCrystal_I2C lcd(0x27,16,2);  // Configurando o endereco do LCD 16x2 para 0x27

#define TEMPO_LEITURA_MS     1000

PulseOximeter pox;

long int tempo = 0;
float x, prev_x;

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

float movingAverage(float value) {
  const byte nvalues = 100;             // Moving average window size

  static byte current = 0;            // Index for current value
  static byte cvalues = 0;            // Count of values read (<= nvalues)
  static float sum = 0;               // Rolling sum
  static float values[nvalues];

  sum += value;

  // If the window is full, adjust the sum by deleting the oldest value
  if (cvalues == nvalues)
    sum -= values[current];

  values[current] = value;          // Replace the oldest with the latest

  if (++current >= nvalues)
    current = 0;

  if (cvalues < nvalues)
    cvalues += 1;

  return sum/cvalues;
}

void loop()
{
    //Atualizacao dos dados do Sensor MAX30100
    pox.update();

    if (millis() - tempo < TEMPO_LEITURA_MS) 
    {   
        x = movingAverage(pox.getSpO2());
        //Serial.println(abs(prev_x - x));
        if(abs(prev_x - x) > 1){
          Serial.print("Frequencia Cardiaca:");
          Serial.print(pox.getHeartRate());
          Serial.print("SpO2:");
          Serial.print(x);
          Serial.print(abs(prev_x - x));
          Serial.println("%");
          prev_x = x;
        }
        
        tempo = millis();

//        lcd.clear();
//        lcd.setCursor(0,0);
//        lcd.print("BPM:");
//        lcd.setCursor(6,0);
//        lcd.print(pox.getHeartRate());
//
//        lcd.clear();
//        lcd.setCursor(0,1);
//        lcd.print("SpO2:");
//        lcd.setCursor(7,0);
//        lcd.print(pox.getSpO2());
    }
}
