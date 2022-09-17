
void setup()
{
  Serial.begin(9600);
  // Aguarda 1 seg antes de acessar as informações do sensor
  delay(1000);
  pinMode(A0, INPUT);
}
 
void loop()
{
  int h = analogRead(A0);
 
  // Mostra os valores lidos, na serial
  Serial.print("Sensor real = ");
  Serial.print(h);
 
  // Nao diminuir muito o valor abaixo
  // O ideal e a leitura a cada 2 segundos
  delay(2000);
}
