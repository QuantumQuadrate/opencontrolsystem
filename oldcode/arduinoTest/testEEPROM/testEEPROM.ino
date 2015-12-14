#include <EEPROM.h>


unsigned int number = 0;
unsigned int test   = 0;
unsigned long cycles = 0;
void setup() {
  Serial.begin(115200);
}

void loop() {
  // put your main code here, to run repeatedly:
  for(int i = 0;i<1024;i++){
    number = random(255);
    EEPROM.write(i, number);
    test = EEPROM.read(i);
    cycles++;
    if(test != number){
      Serial.println("Failure at location " + String(i) + " after " + String(cycles) + " cycles");
    }
    if((cycles%1000L) == 0L){
      Serial.println("Passed " + String(cycles) + " cycles");
    }
  }
}
