#include <DHT.h>;
#define DHTPIN A5     // what pin we're connected to
#define DHTTYPE DHT22   // DHT 22  (AM2302)
DHT dht(DHTPIN, DHTTYPE);

byte pinWater = A7;
byte pinLight = A6;
byte pinWaterRelay = 6;
byte pinLightRelay = 7;

int chk;
float hum;  //Stores humidity value
float temp; //Stores temperature value

void setup() {
  pinMode(pinWater, INPUT);
  pinMode(pinLight, INPUT);
  pinMode(pinWaterRelay, OUTPUT);
  pinMode(pinLightRelay, OUTPUT);  
  dht.begin();
  
  Serial.begin(9600);
  Serial1.begin(9600);
}

void loop() { 
  int valueWater = analogRead(pinWater);
  int valueLight = analogRead(pinLight);
  hum = dht.readHumidity();
  temp= dht.readTemperature();

  Serial.print("[T:" + String(temp) + ",");
  Serial.print("H:"+String(hum)+",");
  Serial.print("L:"+String(valueLight)+",");
  Serial.println("W:"+String(valueWater)+"]");
  
  Serial1.print("[T:" + String(temp) + ",");
  Serial1.print("H:"+String(hum)+",");
  Serial1.print("L:"+String(valueLight)+",");
  Serial1.print("W:"+String(valueWater)+"]");
  //Serial1.print(",H:"); Serial1.print(hum);
  //Serial1.print(",L:"); Serial1.print(valueLight);
  //Serial1.print(",W:"); Serial1.print(valueWater);
  
  //if(valueLight<500) {
  //  digitalWrite(pinLightRelay, HIGH);
  //}else{
  //  digitalWrite(pinLightRelay, LOW);
  //}

  
  
  //if(valueWater<1000) {
  //  digitalWrite(pinWaterRelay, HIGH);
  //}else{
  //  digitalWrite(pinWaterRelay, LOW);
  //}  
  delay(1000);
}
