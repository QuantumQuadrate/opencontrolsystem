//int data_stack[700];
int data_pointer  = 0;
//Test instruction stack
//byte instr_stack[4][7] = {{0x22, 100 ,0, 10,0, 3,0},
//                          {0x33, 150 ,0, 1,0, 2,0},
//                          {0x33, 180 ,0, 1,0, 1,0},
//                          {0x11, 220 ,0, 5,0, 2,0}};

byte instr_stack[4][7] = {{0x22, 100 ,0, 100, 0, 1,0}};

int instr_pointer = 0;
int instr_timeout = 20000;
int number_instructions = 1; //Each element is two bytes

boolean exp_done = false;
void setup()
{
  Serial.begin(115200);
}

void loop()
{
 if(!exp_done){
   exe_instr(instr_stack[instr_pointer], sizeof(instr_stack[instr_pointer]));
 }else{
   Serial.println(F("Experiment finished!"));
   delay(30000);
 }
}



//Maps experiment instructions to there functions, must pass in size
void exe_instr(byte block[31]){
  //break block into components as outlined in commons.py
  byte base_instruction = block[0]; //First byte is the exp instruction code
  unsigned int op_start_time    = bytes_to_int(block, 1); //Next two are the integer start time
  unsigned int op_reps          = bytes_to_int(block, 3); //Next two are the integer repetitions
  unsigned int op_delay         = bytes_to_int(block, 5); //Next two are the integer delay between reps
  
  inspect_instr(block);
  
  //Timing is based on addition of delay compared to absolute clock
  //TODO: check for missed instruction timing and flag error
  unsigned int next_instr_timing = op_start_time;
  for(int i = 0; i<op_reps;i++){
    //wait until next instruction time
    while((millis()<next_instr_timing) && (millis()<instr_timeout)){}
    //Execute instruction here
    op_map(block);
    //index instruction timing
    next_instr_timing = next_instr_timing + op_delay;
  }
  //check if this is the last instruction
  if(instr_pointer == (number_instructions-1)){
    //if it is, stop the experiment
    exp_done = true;
  }else{
    //otherwise, index instruction pointer
    instr_pointer++;
  }
}

void op_map(byte* block){
   //break block into components as outlined in commons.py
  byte base_instr = block[0]; //First byte is the exp instruction code
  //int op_start_time    = bytes_to_int(block, 1); //Next two are the integer start time
  //int op_reps          = bytes_to_int(block, 3); //Next two are the integer repetitions
  //int op_delay         = bytes_to_int(block, 5); //Next two are the integer delay between reps
  
  switch (base_instr) {
    case 34:
      //run function 1 
      func1();
      break;
    case 51:
      //run function 2
      func2();
      break;
    case 17:
      //run instruction 3
      func3();
      break;
    default: 
      bad_instr();
      // if nothing else matches, do the default
      // default is optional
  } 
}
void bad_instr(){
  Serial.println(F("Bad instruction"));
}

//Card specific instructions////////////////////////////////////////////////////////////////
//                                                                                        //
//                                                                                        //
void func1(){
  Serial.println(String(millis()));
}


void func2(){
  Serial.println("You called function 2 at time " + String(millis()));
}

void func3(){
  Serial.println("Free ram: " + String(free_ram()));
}

//                                                                                        //
//                                                                                        //
////////////////////////////////////////////////////////////////////////////////////////////




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

//Inspects experiment operation call
void inspect_exp_instr(byte* block){
  byte base_instr = block[0]; //First byte is the exp instruction code
  int op_start_time    = bytes_to_int(block, 1); //Next two are the integer start time
  int op_reps          = bytes_to_int(block, 3); //Next two are the integer repetitions
  int op_delay         = bytes_to_int(block, 5); //Next two are the integer delay between reps
  Serial.println("Executing instruction :" + String(base_instr) + ",starting on: " + String(op_start_time) + ", with " + String(op_reps) + " reps, of delay " + String(op_delay) + " ms");
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
  return (int) a[location+1] << 8 | a[location];
}

//Return amount of free ram
int free_ram() 
{
  extern int __heap_start, *__brkval; 
  int v; 
  return (int) &v - (__brkval == 0 ? (int) &__heap_start : (int) __brkval); 
}
