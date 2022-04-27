String readdata;
int pin1 = 2;
int pin2 = 3;
int pin3 = 4;
int pin4 = 5;
int pin5 = 8;
int pin6 = 9;
int pin7 = 10;
int pin8 = 11;

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  pinMode(pin1, OUTPUT);
  pinMode(pin2, OUTPUT);
  pinMode(pin3, OUTPUT);
  pinMode(pin4, OUTPUT);
  pinMode(pin5, OUTPUT);
  pinMode(pin6, OUTPUT);
  pinMode(pin7, OUTPUT);
  pinMode(pin8, OUTPUT);
  
  digitalWrite(pin1, LOW);
  digitalWrite(pin2, LOW);
  digitalWrite(pin3, LOW);
  digitalWrite(pin4, LOW);
  digitalWrite(pin5, LOW);
  digitalWrite(pin6, LOW);
  digitalWrite(pin7, LOW);
  digitalWrite(pin8, LOW);
}

void loop() {

  if(Serial.available()>0)
  {
    char data = Serial.read();
    readdata.concat(data);
    }
    else
    {
      if(readdata.substring(0) == "Hello")
      {
        Serial.println("ardok");
        readdata = "";
      }
      else if(readdata.substring(0) =="1H")
      {
        digitalWrite(pin1, HIGH);
        Serial.println(readdata.substring(0));
        readdata = "";
      }
      else if(readdata.substring(0) =="1L")
      {
        digitalWrite(pin1, LOW);
        Serial.println(readdata.substring(0));
        readdata = "";
      }
      else if(readdata.substring(0) =="2H")
      {
        digitalWrite(pin2, HIGH);
        Serial.println(readdata.substring(0));
        readdata = "";
      }
      else if(readdata.substring(0) =="2L")
      {
        digitalWrite(pin2, LOW);
        Serial.println(readdata.substring(0));
        readdata = "";
      }
      else if(readdata.substring(0) =="3H")
      {
        digitalWrite(pin3, HIGH);
        Serial.println(readdata.substring(0));
        readdata = "";
      }
      else if(readdata.substring(0) =="3L")
      {
        digitalWrite(pin3, LOW);
        Serial.println(readdata.substring(0));
        readdata = "";
      }
      else if(readdata.substring(0) =="4H")
      {
        digitalWrite(pin4, HIGH);
        Serial.println(readdata.substring(0));
        readdata = "";
      }
      else if(readdata.substring(0) =="4L")
      {
        digitalWrite(pin4, LOW);
        Serial.println(readdata.substring(0));
        readdata = "";
      }
      else if(readdata.substring(0) =="5H")
      {
        digitalWrite(pin5, HIGH);
        Serial.println(readdata.substring(0));
        readdata = "";
      }
      else if(readdata.substring(0) =="5L")
      {
        digitalWrite(pin5, LOW);
        Serial.println(readdata.substring(0));
        readdata = "";
      }
      else if(readdata.substring(0) =="6H")
      {
        digitalWrite(pin6, HIGH);
        Serial.println(readdata.substring(0));
        readdata = "";
      }
      else if(readdata.substring(0) =="6L")
      {
        digitalWrite(pin6, LOW);
        Serial.println(readdata.substring(0));
        readdata = "";
      }
      else if(readdata.substring(0) =="7H")
      {
        digitalWrite(pin7, HIGH);
        Serial.println(readdata.substring(0));
        readdata = "";
      }
      else if(readdata.substring(0) =="7L")
      {
        digitalWrite(pin7, LOW);
        Serial.println(readdata.substring(0));
        readdata = "";
      }
      else if(readdata.substring(0) =="8H")
      {
        digitalWrite(pin8, HIGH);
        Serial.println(readdata.substring(0));
        readdata = "";
      }
      else if(readdata.substring(0) =="8L")
      {
        digitalWrite(pin8, LOW);
        Serial.println(readdata.substring(0));
        readdata = "";
      }
    }
}
