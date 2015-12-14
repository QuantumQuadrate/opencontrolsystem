#include <Wire.h>

/////////////////////////Constants to be stored in flash memory/////////////////////////////
//                                                                                        //
//                                                                                        //

const int hardwareID      PROGMEM = 55;   //Hardware id
const uint8_t uuid[8]     PROGMEM = {0x00, 0x01, 0x00, 0x00, 0x00, 0x00, 0x00, 0x03}; //card's uuid
const int IACKin          PROGMEM = 5;   //Acknowledge pin in
const int IACKout         PROGMEM = 4;   //Acknowledge pin out
const int i2c_SDA         PROGMEM = A4;   //i2c SDA pin
const int i2c_SCL         PROGMEM = A5;   //i2c SCL pin
const int default_address PROGMEM = 5;    //define default routing address on bus

const boolean verbose_functions PROGMEM   = false;       //Print instruction calls for debugging
const boolean instr_timeout PROGMEM       = 30000;      //Max instruction execution duration in ms

const unsigned int max_instructions PROGMEM = 16;
const unsigned int max_data         PROGMEM = 128;
//                                                                                        //
//                                                                                        //
///////////////////////////////////End constants////////////////////////////////////////////



/////////////////////////Dynamic variables//////////////////////////////////////////////////
//                                                                                        //
//                                                                                        //

//Variables for initialization
volatile int init_state = 0;                   //define initialization state 
volatile int assigned_address    = 0;  
volatile boolean initialized = false;          //define boolean for initialization complete
volatile boolean got_IACK_signal_high = false; //track if iack is high
volatile boolean update_address = false;
volatile boolean wait_for_IACK_signal_low  = false;

//Runtime variables
byte             current_command[31]; //Stores the last command to run it outside of i2c interupt

volatile boolean flag_got_instruction;//flags that an instruction has been received

volatile boolean flag_interupt_0_fired = false; //flag for interupt 0 being fired
volatile boolean flag_interupt_1_fired = false; //flag for interupt 1 being fired


uint8_t exp_instructions[max_instructions][16];      //stores experiment operations
unsigned int number_instr = 0;                      //counts number of loaded instructions
volatile boolean exp_done = true;                   //Is experiment done?
unsigned int exp_instr_pointer = 0;                 //Points to the current instruction being executed
unsigned long exp_start_time   = 0;


uint8_t exp_data[max_data][8];
volatile unsigned int exp_data_pointer = 0;
volatile unsigned int exp_get_pointer = 0;

//                                                                                        //
//                                                                                        //
///////////////////////////////////End dynamics/////////////////////////////////////////////




void setup()
{
  //intilize data matrix to zero
  for(int i = 0;i<max_data;i++){
    for(int j = 0;j<8;j++){
      exp_data[i][j] = 0x00;
    }
  }
  Serial.begin(115200);
  //initialize I2C to high impedence to reduce interference / slew rate on bus
  pinMode(i2c_SDA, INPUT);
  pinMode(i2c_SCL, INPUT);
  //initialize IACK lines
  pinMode(IACKin, INPUT);
  pinMode(IACKout, OUTPUT);
  digitalWrite(IACKout, LOW);
  //work around to avoid using interupts for initialization
  while(!initialized){
     setup_poll_iack();
  }
}


//Mainly event handled except checking if IACK is high
void loop()
{
 runtime_poll();
}



/////////////////////////////////////////START SETUP PROCEDURE//////////////////////////////
//                                                                                        //
//                                                                                        //


//Poll the IACK lines for setup purposes
void setup_poll_iack(){
  if(!got_IACK_signal_high){
    if(digitalRead(IACKin) == HIGH){
      init_setup_i2c(default_address);
      got_IACK_signal_high = true;
      //pln("Initializing...");
    }
  }
  
  if(wait_for_IACK_signal_low){
    //wait for iack in to be low
    if(digitalRead(IACKin) == LOW){
    //pln("Carrying low signal to next slave");
    digitalWrite(IACKout, LOW);
    //pln("Initialization complete!");
    wait_for_IACK_signal_low = false;
    initialized = true;
    runtime_setup_i2c(assigned_address);
    //pln("Slave initialized with address " + String(address));
    }
  }
  
  if(update_address){
    //Serial.println("Changing address");
    //Setup I2C with new address
    init_setup_i2c(assigned_address);
    wait_for_IACK_signal_low = true;
    update_address = false;
  }
}

//setup I2C communication with specific address
void init_setup_i2c(int addr){
  //pln("Setting up IACK with address " + String(addr))
  Wire.begin(addr);    // join i2c bus with default address
  Wire.onReceive(setup_receive_handle); // define function to hook on
  Wire.onRequest(setup_request_handle); // define function to hook on
}

//setup I2C communication with specific address for runtime operations
void runtime_setup_i2c(int addr){
  //pln("Setting up IACK with address " + String(addr))
  Wire.begin(addr);    // join i2c bus with default address
  Wire.onReceive(runtime_receive_handle); // define function to hook on
  Wire.onRequest(runtime_request_handle); // define function to hook on
}

//i2c interupt request handling function during setup procedure
void setup_request_handle(){
  if(init_state == 0) {
    //Write out this card's id on request
    Wire.write(char(hardwareID));
    //update state variable
    init_state = 1;
  }
}

//i2c interupt receive handling function during setup procedure
void setup_receive_handle(int howMany){
  //pln("Receive handler fired");
  if(init_state == 1){
    assigned_address = i2c_read_byte(); // receive byte as a character
    digitalWrite(IACKout, HIGH);        //carry on high signal to next slave
    init_state = 2;                     //update state
    update_address = true;              //update state (Might cause error to update interupt handler within the interupt itself)
  }
}

//                                                                                        //
//                                                                                        //
///////////////////////////////////END SETUP PROCEDURES/////////////////////////////////////



///////////////////////////////////BEGIN RUNTIME AREA///////////////////////////////////////
//                                                                                        //
//                                                                                        //

void runtime_poll(){ 
  if(flag_got_instruction){
    flag_got_instruction = false;
    operation_router(current_command);
  }
}

void interupt_0(){
  flag_interupt_0_fired = true;
}

void interupt_1(){
  flag_interupt_1_fired = true;
}

//i2c interupt request handling function during runtime operation
void runtime_request_handle(){
  
  //Detect if command wants immediate response data or not.
  //This is done because the main command switch is out
  //of the i2c interupt and would require a second 
  //request for the data from the controller.
  //Command block was first set in the recieve handler
  //before request handler is called
  switch(current_command[0]){
    //return the card's uuid
    case 0x01:
      util_get_uuid();
      break;
    case 0x02:
       util_free_ram();
    case 0x17:
       exp_get();
      break;
    default:
      flag_got_instruction  = true;
  }
  
}

//i2c interupt receive handling function during runtime operation
void runtime_receive_handle(int number_of_bytes){
  //Wire.write("Hello world!");
  byte* temp = i2c_read_block();
  //copy over bytes from variable size array to constant size current_command
  for(int i = 0;i<number_of_bytes;i++){
    current_command[i] = temp[i];
  }
  flag_got_instruction  = true;
  if(verbose_functions){
      print_bytes(current_command, sizeof(current_command));
  }
}

//                                                                                        //
//                                                                                        //
///////////////////////////////////////END RUNTIME AREA/////////////////////////////////////


////////////////////////////////////BEGIN COMMAND ROUTER SECTION////////////////////////////
//                                                                                        //
//                                                                                        //
void operation_router(byte block[31]){
   //break block into components as outlined in commons.py
  byte base_instr = block[0]; //Base insstruction of block
  //int op_start_time    = bytes_to_int(block, 1); //Next two are the integer start time
  //int op_reps          = bytes_to_int(block, 3); //Next two are the integer repetitions
  //int op_delay         = bytes_to_int(block, 5); //Next two are the integer delay between reps
  //Serial.println(Instruction);
  switch (base_instr) {
    ////START UTILITY SWITCH SECTION////
    //                                //
    case 0x00:
      util_blink_led(block);
      break;
    case 0x01:
      //util_get_uuid();
      break;
    case 0x02:        //Handled inside interupt
      //util_free_ram(); 
      break;
    case 0x03:
      //util_bench_com();
      break;
    case 0x04:
      util_check_pulses(block);
      break;
    //                                //
    ////END UTILITY SWITCH SECTION//////
    
    ////START EXP OP SWITCH SECTION////
    //                               //
    case 0x10:
      exp_run();
      break;
    case 0x11:
      //exp_run_slow();
      break;
    case 0x12:
      exp_load_op(block);
      break;
    case 0x13:
      //exp_run_op();
      break;
    case 0x14:
      //exp_bench_op();
      break;
    case 0x15:
      //exp_check();
      break;
    case 0x16:
      //exp_clear();
      break;
    case 0x17:
      //exp_get();
      break;
    //                                //
    /////END EXP OP SWITCH SECTION//////
    default: 
      Serial.println("Bad instruction");
      //bad_instr();
  } 
}

//                                                                                        //
//                                                                                        //
///////////////////////////////////////END COMMAND ROUTER SECTION///////////////////////////


////////////////////////////////////START UTILITY METHODS///////////////////////////////////
//                                                                                        //
//                                                                                        //

//utility command to blink led as outlined in commons.py
void util_blink_led(byte block[31]){
  //Parse instruction based on commons.py
  unsigned int number_of_blinks  = bytes_to_int(block,1);
  unsigned int duration_of_blink = bytes_to_int(block,3);
  if(verbose_functions){
    Serial.println("called blink led, number of blinks=" + String(number_of_blinks) + ", duration of each blink = " + String(duration_of_blink));
  }
  //divide duration by 2
  unsigned int half_duration = duration_of_blink/2;
  pinMode(13, OUTPUT);
  for(unsigned int i = 0; i < number_of_blinks; i++){
    digitalWrite(13, HIGH);
    delay(half_duration);
    digitalWrite(13, LOW);
    delay(half_duration);
  }
}

//Utility command to return the card's uuid to the master
void util_get_uuid(){
  size_t s = 8;
  Wire.write(uuid,s);
}

void util_free_ram(){
  unsigned int temp_x = free_ram();
  uint8_t temp_arr[] = {0x00, 0x00};
  temp_arr[0] = (temp_x & 0xff);
  temp_arr[1] = (temp_x >> 8);
  Wire.write(temp_arr, 2);
}
//Utility command to send timed pulses as outlined in commons.py
void util_check_pulses(byte block[31]){
  //Parse instruction based on commons.py
  unsigned int pin_number         = bytes_to_int(block,1);
  unsigned int number_of_pulses   = bytes_to_int(block,3);
  unsigned long duration_of_pulse  = bytes_to_int(block,5)*1000;

  if(verbose_functions){
    Serial.println("Called test pulses on pin number "+ String(pin_number)+", with " + String(number_of_pulses) + " pulses of duration " + String(duration_of_pulse) + " us per cycle");
  }
  //calculate half duration for 50 duty cycle
  unsigned long half_duration      = duration_of_pulse/2; 
  
  //Prevent messing up communication pins
  switch(pin_number){
    case(IACKin):
      return;
      break;
    case(IACKout):
      return;
      break;
    case(i2c_SDA):
      return;
      break;
    case(i2c_SCL):
      return;
      break;
  }
  
  
  //Pre initialize variables, reserve stack space before operation is fired
  int i =0;
  unsigned long next_instr_timing = 0;
  pinMode(pin_number, OUTPUT);
  digitalWrite(pin_number, LOW);

  //Attach interupt and wait for it to be fired
  attachInterrupt(0, interupt_0, RISING);
  while(!flag_interupt_0_fired){}
  flag_interupt_0_fired = false;
  detachInterrupt(0);

  //unsigned long now = micros();
  //while((micros()-now)<10000L){}
  
  next_instr_timing  = micros();
  for(i = 0; i<number_of_pulses;i++){
    //wait until next instruction time
    while(micros() < next_instr_timing){}
    digitalWrite(pin_number, HIGH);
    delayMicroseconds(half_duration);
    digitalWrite(pin_number, LOW);
    //index instruction timing
    next_instr_timing = next_instr_timing + duration_of_pulse;
  }
}


//                                                                                        //
//                                                                                        //
/////////////////////////////////////END UTILITY METHODS////////////////////////////////////

///////////////////////////////BEGIN EXPERIMENT UTILITY METHODS/////////////////////////////
//                                                                                        //
//                                                                                        //
void exp_load_op(byte block[31]){
  if(number_instr<max_instructions){
    int w = 0;
    for(int i = 0;i<16;i++){
      exp_instructions[number_instr][i] = block[i+1];
    }
    Serial.println(number_instr);
    number_instr++;
  }
}

void exp_get(){
  //unsigned int exp_data_pointer = 0;
  //unsigned int exp_get_pointer = 0;
  if(exp_get_pointer<exp_data_pointer && exp_get_pointer<max_data){
    byte send_array[9];
    send_array[0] = 0x01; // indicate data left in array
    for(int g = 0; g<8;g++){
      send_array[g+1] = exp_data[exp_get_pointer][g];
    }
    Wire.write(send_array, 9);
    //print_bytes(send_array, 9);
    exp_get_pointer++;
  }else{
    byte send_array[9];
    send_array[0] = 0x00; //indicate data empty
    Wire.write(send_array, 9);
    exp_data_pointer = 0;
    exp_get_pointer = 0;
  }
}

//Run the experiment
void exp_run(){
   Serial.println("Running experiment");
  //Set instruction pointer to zero
  exp_get_pointer   = 0;
  exp_instr_pointer = 0;
  
  //Wait for interupt before starting experiment
  attachInterrupt(0, interupt_0, RISING);
  while(!flag_interupt_0_fired){}
  //Set experiment start time to now
  detachInterrupt(0);
  flag_interupt_0_fired = false;
  exp_done = false;
  exp_start_time = micros();
  
  while(!exp_done && exp_instr_pointer<number_instr){
    exp_exe_instr();
  }
}

//Execute single instruction from the experiment instruction array
void exp_exe_instr(){
  byte block[16];
  for(int w = 0; w<16;w++){
    block[w] = exp_instructions[exp_instr_pointer][w];
  }
  exp_instr_pointer++;
  if(block[0]==0xff){
    //Print data array
    //for(int i = 0;i<max_data;i++){
      //for(int j = 0;j<8;j++){
        //Serial.print(String(exp_data[i][j]) + ",");
      //}
      //Serial.println();
    //}
    
    exp_done = true;
    return;
  }
  //break block into components as outlined in commons.py
  //If speed becomes an issue, preallocate memory for these variables
  //byte base_instruction = block[0]; //First byte is the exp instruction code
  unsigned long op_start_time    = ((long)bytes_to_int(block, 1))*1000L; //Next two are the integer start time us relative to exp_start time
  unsigned int  op_reps          = bytes_to_int(block, 3);      //Next two are the integer repetitions
  unsigned long op_delay         = ((long)(bytes_to_int(block, 5)))*1000L; //Next two are the integer delay between reps us
  
  Serial.print("Instr:" + String(block[0]));
  Serial.print(",Start time:" + String(op_start_time));
  Serial.print(",op reps:" + String(op_reps));
  Serial.println(",op delay:" + String(op_delay));
  
  //Calculate first instruction timing based on the experiment's start time
  unsigned long next_instr_timing = exp_start_time + op_start_time;
  
  for(int i = 0; i<op_reps;i++){
    //wait until next instruction time
    while(micros() < next_instr_timing){}
    //Map operation to appropriate operation and pass in arguments (if any)
    exp_instr_router(block);
    //index instruction timing
    next_instr_timing = next_instr_timing + op_delay;
  }
}
//                                                                                        //
//                                                                                        //
/////////////////////////////////////END EXPERIMENT UTILITY METHODS/////////////////////////


///////////////////////////////BEGIN CARD SPECIFIC METHODS//////////////////////////////////
//                                                                                        //
//                                                                                        //
void exp_instr_router(byte block[16]){
  byte base_instruction = block[0]; //First byte is the exp instruction code

  switch(base_instruction){
    case 0x00:
      read_analog(block);
      break;
    default:
      Serial.println();
      break;
  }
}


void read_analog(byte block[16]){
  unsigned int analog_pin = bytes_to_int(block, 7);
  unsigned int local_pin;
  switch(analog_pin){
    case 0:
      local_pin = A0;
      break;
    case 1:
      local_pin = A1;
      break;
    case 2:
      local_pin = A2;
      break;
    case 3:
      local_pin = A3;
      break; 
    default:
       return;
      break;
  }
  int voltage = analogRead(local_pin);
  uint8_t data[] = {0,0,0,0,0,0,0,0};
  data[0] = block[0]; //record which instruction this data came from
  place_int(data, (int)((micros()-exp_start_time)/1000L), 1); //(int)((micros()-exp_start_time)/1000)
  place_int(data, voltage, 3);
  if(exp_data_pointer<max_data){
    for(int h = 0;h<8;h++){
      exp_data[exp_data_pointer][h] = data[h];
    }
    print_bytes(data, 8);
    exp_data_pointer++;
  }else{
    Serial.println(F("Data array full!"));
  }
}
//                                                                                        //
//                                                                                        //
/////////////////////////////////////END CARD SPECIFIC METHODS//////////////////////////////


////////////////////////////////////START USEFUL METHODS SECTION////////////////////////////
//                                                                                        //
//                                                                                        //

//Shorthand print statement
void pln(String s){
  Serial.println(s);
}

char* string_to_chars(String s){
  char charBuf[s.length()];
  s.toCharArray(charBuf, s.length());
  return charBuf;
}

//Return amount of free ram
int free_ram() 
{
  extern unsigned int __heap_start, *__brkval; 
  unsigned int v; 
  return (unsigned int) &v - (__brkval == 0 ? (unsigned int) &__heap_start : (unsigned int) __brkval); 
}

//Read single byte of i2c buffer
char i2c_read_byte(){
  char chr;
  while(Wire.available()>0){
        chr = Wire.read(); // receive byte as a character
  }
  return chr;
}


//Read block of data from I2C
byte* i2c_read_block(){
  //initialize array of max length
  char chars1[31];
  unsigned int index = 0;
  //fill array
  while((Wire.available()>0)&&(index<31)){
      chars1[index] = Wire.read();
      index++;
  }
  unsigned int num = index+1;
  byte chars2[num];
  for(int i = 0;i<num;i++){
    chars2[i] = chars1[i];
  }
  return chars2;
}


void i2c_write_block(uint8_t* array, unsigned int len){
  uint8_t new_array[len];
  for(int i = 0;i<len;i++){
    new_array[i] = array[i];
  }
  Wire.write(new_array, len);
}

//Converts an int to 2 bytes and places it at the location specified
void place_int(uint8_t* array, unsigned int x, int location){
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
  return (unsigned int) a[location+1] << 8 | a[location];
}

void print_bytes(byte* bytes, int s){
  Serial.print("[");
  for(int i = 0;i<s;i++){
    Serial.print(String(bytes[i]) + ",");
  }
  Serial.print("]");
  Serial.println();
}

//                                                                                        //
//                                                                                        //
/////////////////////////////////////END USEFUL METHODS SECTION/////////////////////////////

