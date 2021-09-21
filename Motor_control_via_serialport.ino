#define ARRAY_SIZE 8
const int quarter = 5;
const int half = 4;
const int en = 3;
const int sec_stepPin = 9; 
const int sec_dirPin = 8; 
const int stepPin = 7; 
const int dirPin = 6; 
const int limitswitch = 10;
const int limitswitch2 = 12;
String incomingByte; 
char *strings[16]; // an array of pointers to the pieces of the above array after strtok()
char *floats[16];
char *ptr = NULL;
int pos[16];
float measure[16];
 
void setup() {
  pinMode(sec_stepPin,OUTPUT); 
  pinMode(sec_dirPin,OUTPUT);
  pinMode(stepPin,OUTPUT); 
  pinMode(dirPin,OUTPUT);
  pinMode(quarter,OUTPUT);
  pinMode(half,OUTPUT);
  pinMode(en,OUTPUT);
  pinMode(limitswitch, INPUT);
  pinMode(limitswitch2, INPUT);
  digitalWrite(quarter,HIGH);
  digitalWrite(half,HIGH);
  digitalWrite(en,HIGH);
  //digitalWrite(stepPin,LOW); 
  Serial.begin(9600);
  
}
void loop() {
  default_pos();
  if (Serial.available() > 0) {
  incomingByte = Serial.readStringUntil('\n');
    if (incomingByte != "off") {
     //digitalWrite(stable,LOW);
     char str_array[incomingByte.length()+1];
     incomingByte.toCharArray(str_array, incomingByte.length()+1);
     char* token = strtok(str_array, " ");
     byte index = 0;
     int half_length = (countOccurences(incomingByte, ',')+1)/2;
     ptr = strtok(token, ",");  // delimiter
     int counter = 0;
     while (ptr != NULL)
     {  
        if (counter >= half_length){
          if (counter == half_length){
            index = 0; 
          }
          floats[index] = ptr;  
        }
        else {
          strings[index] = ptr;
        }
        index++;
        counter++;
        ptr = strtok(NULL, ",");
     }
     for (int n = 0; n < half_length; n++)
     {
        Serial.print(n);
        Serial.print("  ");
        Serial.println(strings[n]);
        Serial.print(n);
        Serial.print("  ");
        Serial.println(floats[n]);
     }

     for (int n = 0; n <= half_length; n++) {
       pos[n] = atoi(strings[n]);
       measure[n] = atof(floats[n]);
     }
      top_module(pos, measure, half_length);
      Serial.print("Done");
 
    }
    else{
     Serial.write("invald input");
    }
  }
}


void top_module(int pos[], float measure[], int arsize) {

  int all_pos[] = {1500,2840,4180,5600,6850,8100,9500,10800};
  int current_steps = 0;
  for (int n = 0; n < arsize; n++) {
    if (current_steps < all_pos[pos[n]]) {
      clockwise(all_pos[pos[n]]-current_steps);
      delay(1000);
      digitalWrite(en,LOW);
      y_axis(measure[n]);
      digitalWrite(en,HIGH);
      //Serial.print(all_pos[pos[n]]-current_steps);
      current_steps = all_pos[pos[n]];
    }
    else {
      counter_clockwise(current_steps-all_pos[pos[n]]);
      delay(1000);
      digitalWrite(en,LOW);
      y_axis(measure[n]);
      digitalWrite(en,HIGH);
      //Serial.print(current_steps-all_pos[pos[n]]);
      current_steps = all_pos[pos[n]];
    }
  }
  delay(100);
  counter_clockwise_return(current_steps);

}


void clockwise(int step_count){
  digitalWrite(dirPin,HIGH); 
  float delay_time = 500;
  for(int x = 0; x < step_count; x++) {
    delay_time = acc(delay_time, x, step_count);
    digitalWrite(stepPin,HIGH); 
    delayMicroseconds(delay_time); 
    digitalWrite(stepPin,LOW); 
    delayMicroseconds(delay_time); 
  }
  delay(100); // One second delay
}

void counter_clockwise(int step_count){
  digitalWrite(dirPin,LOW); 
  float delay_time = 500;
  for(int x = 0; x < step_count; x++) {
    delay_time = acc(delay_time, x, step_count);
    digitalWrite(stepPin,HIGH);
    delayMicroseconds(delay_time);
    digitalWrite(stepPin,LOW);
    delayMicroseconds(delay_time);
  }
  delay(100);
}

void counter_clockwise_return(int step_count){
  digitalWrite(dirPin,LOW); 
  float delay_time = 500;
  int x=0;
  while (digitalRead(limitswitch) == LOW) {
    delay_time = acc(delay_time, x, step_count);
    digitalWrite(stepPin,HIGH);
    delayMicroseconds(delay_time);
    digitalWrite(stepPin,LOW);
    delayMicroseconds(delay_time);
    x+=1;
  }
  delay(100);
}

void limit_vertical(){
  digitalWrite(sec_dirPin,LOW); 
  while (digitalRead(limitswitch2) == LOW) {
    digitalWrite(sec_stepPin,HIGH);
    delayMicroseconds(200);
    digitalWrite(sec_stepPin,LOW);
    delayMicroseconds(200);
  }
  delay(100);
  Serial.print("l2 funker");
}

void default_pos(){
  digitalWrite(dirPin,LOW); 
  float delay_time = 1400;
  while (digitalRead(limitswitch) == LOW) {
    digitalWrite(stepPin,HIGH);
    delayMicroseconds(delay_time);
    digitalWrite(stepPin,LOW);
    delayMicroseconds(delay_time);
  }
  delay(100);
}

void y_axis(float times){
  float time_delay = 0;
  Serial.print(times);
  while (times >= 0.25) {
    if (times-1 >= 0) {
      time_delay = 4;
      times = times-1;
    }
    else if (times == 0.75) {
      time_delay = 1.6;
      times = times-1;
    }
    else if (times == 0.50) {
      time_delay = 1.3;
      times = times-1;
    }
    else if (times == 0.25) {
      time_delay = 1;
      times = times-1;
    }
    sec_clockwise(1250);
    delay(2*1000);
    limit_vertical();
    if (times >= 0.25) {
      delay(2500);
    }
  }

}

void sec_clockwise(int step_count){
  digitalWrite(sec_dirPin,HIGH); 
  for(int x = 0; x < step_count; x++) {
    digitalWrite(sec_stepPin,HIGH); 
    delayMicroseconds(300); 
    digitalWrite(sec_stepPin,LOW); 
    delayMicroseconds(300); 
  }
}

void sec_counter_clockwise(int step_count){
  digitalWrite(sec_dirPin,LOW); 
  for(int x = 0; x < step_count; x++) {
    digitalWrite(sec_stepPin,HIGH);
    delayMicroseconds(200);
    digitalWrite(sec_stepPin,LOW);
    delayMicroseconds(200);
  }
}

int countOccurences(String word, char character){
  int count = 0;
  for(int i = 0; i < word.length(); i++){
    if(word.charAt(i) == character){      
      count++; } 
                 }
      return count;
}

float acc(float delay_time, int steps, int step_count) {
  
    if (steps > step_count-900){
      delay_time = delay_time + delay_time*0.0024;
      if (delay_time > 1400){
       delay_time = 1400;
      } 
    }
    else{
      delay_time = delay_time - delay_time*0.0007;
      if (delay_time < 130){
        delay_time = 130;
      } 
    }
    return delay_time;
}
