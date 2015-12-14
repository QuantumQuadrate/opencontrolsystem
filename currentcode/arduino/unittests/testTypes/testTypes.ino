int num = -500;
uint8_t test[] = {0, 128, 0};

void setup(){
  Serial.begin(115200);
}


void loop(){
 //place_int(num,1,test);
 print_array(test, sizeof(test));
 Serial.println("Amount of free ram:" + String(free_ram()));
 Serial.println(String(bytes_to_int(test, 1)));
  delay(200); 
}

//Prints an array of bytes
void print_array(uint8_t* array, int size){
   if(size>=1){
     Serial.print("block :[");
     for(int i = 0;i<size-1;i++){
       Serial.print(array[i], HEX);
       Serial.print("|");
     }
     Serial.print(array[size-1], HEX);
     Serial.print("]");
     Serial.println();
   }
}

//Converts an int to 2 bytes and places it at the location specified
void place_int(int x,int location, byte* array){
  uint8_t xlow = x & 0xff;
  uint8_t xhigh = (x >> 8);
  array[location] = xlow;
  array[location+1] = xhigh;
}

//converts 4 bytes from an array location to a single long (little endian)
long bytes_to_long(byte* a, int location){
  long retval  = (unsigned long) a[location+3] << 24 | (unsigned long) a[location+2] << 16;
  retval |= (unsigned long) a[location+1] << 8 | a[location];
  return retval;
}

//converts 2 bytes from an array location to a single int (little endian)
int  bytes_to_int(byte* a, int location){
  int retval = (int) a[location+1] << 8 | a[location];
  return retval;
}

//Return amount of free ram
int free_ram() 
{
  extern int __heap_start, *__brkval; 
  int v; 
  return (int) &v - (__brkval == 0 ? (int) &__heap_start : (int) __brkval); 
}
