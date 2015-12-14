
uint8_t instructions[64][12];
uint8_t data[128][5];

void setup() {
  Serial.begin(115200);
  instructions[0][0] = 0xff;
  data[0][0]         = 0xff;
}

void loop() {
  Serial.println(free_ram());
  delay(1000);
}



//Return amount of free ram
int free_ram() 
{
  extern int __heap_start, *__brkval; 
  int v; 
  return (int) &v - (__brkval == 0 ? (int) &__heap_start : (int) __brkval); 
}
