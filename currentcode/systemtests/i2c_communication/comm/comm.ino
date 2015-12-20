#include <Wire.h>
String s = "";
String ws = "";
String out = "";
int chunk_size = 16;
volatile boolean write_finished   = true;
char charBuffer[16];
volatile boolean finished = false;
void setup(){
  Serial.begin(115200);
  init_setup_i2c(5);
}

void loop(){
  if(finished){
    write_stream(s);
    s = "";
    //Serial.println(s);
    //s = "";
    finished = false;
  }
  if(Serial.available()){
    Serial.read();
    //String rs = "hello my name is josh 12345678";
    write_stream(s);
    //s = "";
  }
}

void write_stream(String str){
  ws = str + '\n';
  write_finished = false;
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
  if(!write_finished){
    if(ws.length()>chunk_size){
      i2c_send_block(ws.substring(0, chunk_size), 0, chunk_size);
      ws = ws.substring(chunk_size);
    }else{
      i2c_send_block(ws, 0, ws.length());
      ws = "";
      write_finished = true;
    }
  }else{
    Wire.write('\n');
  }
  Serial.println("served request");
}


//i2c interupt receive handling function during setup procedure
void receive_handle(int howMany){
  char c = '_';
  //s = "";
  while(Wire.available()>0 && c != '\n'){
    c = Wire.read();
    if(c!='\n'){
      s += c;
    }else{
      finished = true;
    }
  }
}


void i2c_send_block(String str, int start, int last){
  size_t leng = last-start;
  byte new_array[leng];
  for(int i = 0;i<leng;i++){
    new_array[i] = str.charAt(start+i);
  }
  Wire.write(new_array, leng);
}
