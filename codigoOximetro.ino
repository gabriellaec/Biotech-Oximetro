#include <Wire.h>
#include "SSD1306Ascii.h"
#include "SSD1306AsciiWire.h"
#include "MAX30100_PulseOximeter.h"

#define REPORTING_PERIOD_MS     1000

uint32_t tsLastReport = 0;

// 0X3C+SA0 - 0x3C or 0x3D
#define I2C_ADDRESS 0x3C

// Define proper RST_PIN if required.
#define RST_PIN -1

SSD1306AsciiWire oled;

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
    Wire.begin();
    Wire.setClock(400000L);
    
    Serial.begin(115200);

    Serial.print("Initializing pulse oximeter..");

    #if RST_PIN >= 0
    oled.begin(&Adafruit128x64, I2C_ADDRESS, RST_PIN);
    #else // RST_PIN >= 0
    oled.begin(&Adafruit128x64, I2C_ADDRESS);
    #endif // RST_PIN >= 0
  
    oled.setFont(System5x7);
    oled.clear();
    oled.print("Initializing pulse\noximeter..");

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
    // Make sure to call update as fast as possible
    pox.update();

    // Asynchronously dump heart rate and oxidation levels to the serial
    // For both, a value of 0 means "invalid"
    if (millis() - tsLastReport > REPORTING_PERIOD_MS) {
        Serial.print("Heart rate:");
        Serial.print(pox.getHeartRate());
        Serial.print("bpm / SpO2:");
        Serial.print(pox.getSpO2());
        Serial.println("%");
        oled.clear();
        oled.set2X();
        oled.print("BPM:");
        oled.print(pox.getHeartRate());
        oled.print("\nO2%:");
        oled.print(pox.getSpO2());
        tsLastReport = millis();
    }

}
