
// include queue library header.
#include <QueueArray.h>

// declare a string message.
String msg[] = {"Hello", "Goodbye", "Goodday"};

// create a queue of characters.
QueueArray <String> queue;

// startup point entry (runs once).
void
setup () {
  // start serial communication.
  Serial.begin (9600);

  // set the printer of the queue.
  //queue.setPrinter (Serial);

  // enqueue all the message's characters to the queue.
  for (int i = 0; i < 3; i++){
    delay(100);
    Serial.println("Free ram: " + String(free_ram()));
    queue.enqueue (msg[i]);
  }
  // dequeue all the message's characters from the queue.
  while (!queue.isEmpty ()){
    delay(100);
    Serial.print (String(queue.dequeue ()));
  }
  // print end of line character.
  Serial.println ();
}

// loop the main sketch.
void loop () {
  
}

//Return amount of free ram
int free_ram() 
{
  extern int __heap_start, *__brkval; 
  int v; 
  return (int) &v - (__brkval == 0 ? (int) &__heap_start : (int) __brkval); 
}



