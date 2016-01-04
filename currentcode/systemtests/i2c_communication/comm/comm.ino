#include <Wire.h>

char message_array[128];
int  message_location = -1;
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
  Wire.write("Hello raspberry pi!\n");
  while(Wire.available()>0){
    Wire.read();
  }
}


//i2c interupt receive handling function during setup procedure
void receive_handle(int howMany){\
  //cut off first byte, it's the command byte
  if(Wire.available() && message_location==-1){
    Wire.read();
    message_location = 0;
  }
  while(Wire.available()>0){
    w = Wire.read();
    if(w == '\n'){
      Serial.println(message_array);
      message_location = -1;
      for(int i = 0;i<128;i++){
          message_array[i] = 0;
      }
    }else{
      message_array[message_location] = w;
      if(message_location<128){
        message_location++;
      }else{
        flag_error("buffer overflow");
      }
    }
  }
}

//Handle errors
void flag_error(String str){
  Serial.println("{error_flag: " + str + "}");
}

void i2c_send_block(String str, int start, int last){
  size_t leng = last-start;
  byte new_array[leng];
  for(int i = 0;i<leng;i++){
    new_array[i] = str.charAt(start+i);
  }
  Wire.write(new_array, leng);
}
