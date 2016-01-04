#include <Wire.h>

byte new_array[10];

char w = 'a';

volatile boolean finished = false;

void setup(){
  Serial.begin(115200);
  init_setup_i2c(5);
}

void loop(){
  
}
//setup I2C communication with specific address
void init_setup_i2c(int addr){
  //pln("Setting up IACK with address " + String(addr))
  Wire.begin(addr);    // join i2c bus with default address
  Wire.onReceive(receive_handle); // define function to hook on
  Wire.onRequest(request_handle); // define function to hook on
}

//i2c interupt request handling function during setup procedure
void request_handle(){
  while(Wire.available()>0){
    Wire.read();
  }
  Wire.write("Hello world\n");
}


//i2c interupt receive handling function during setup procedure
void receive_handle(int howMany){
  //delay(1000);
  while(Wire.available()>0){
    w = Wire.read();
  }
  //delay(1000);
}


void i2c_send_block(String str, int start, int last){
  size_t leng = last-start;
  byte new_array[leng];
  for(int i = 0;i<leng;i++){
    new_array[i] = str.charAt(start+i);
  }
  Wire.write(new_array, leng);
}
