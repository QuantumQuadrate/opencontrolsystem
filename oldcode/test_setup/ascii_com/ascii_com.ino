String input = "";
const char *manifest = "{cardtype:DAC,[]}\n";

void setup() {
  // Open serial communications and wait for port to open:
  Serial.begin(57600);
  while (!Serial) {
    ; // wait for serial port to connect. Needed for native USB port only
  }
}

void loop() { // run over and over
  Serial.print(manifest);
  if (Serial.available()) {
    char inChar = Serial.read();
    if(inChar=='\n'){
      parse();
      input = "";
    }else{
      input += inChar;
    }
  }
}

void parse(){
  String inner     = input.substring(input.indexOf('{')+1,input.indexOf('}'));

      boolean onetogo = false;
      boolean finish  = false;
      while(!finish){
        String pair      = inner.substring(0, inner.indexOf(','));
        inner            = inner.substring(inner.indexOf(',')+1);
        if(onetogo){
          finish = true;
        }
        if(inner.indexOf(',') == -1){
          onetogo = true;
        }
        String key       = pair.substring(0, pair.indexOf(':'));
        String val       = pair.substring(pair.indexOf(':')+1);

        Serial.println("key:" + key);
        if(val.indexOf('"') != -1){
          Serial.println("found string with value :" + val);
        }else if(val.indexOf('.') != -1){
           Serial.println("found floating point with value :" + String(val.toFloat()));
        }else{
          Serial.println("found int with value :" + String(val.toInt()));
        }
      }
      input = "";
}


