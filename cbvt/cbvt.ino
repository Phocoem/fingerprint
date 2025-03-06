#include <Adafruit_Fingerprint.h>
#include <LiquidCrystal.h>
#include <ModbusRtu.h>

#define mySerial Serial1
#define ID1   1 

#if (defined(__AVR__) || defined(ESP8266)) && !defined(__AVR_ATmega2560__)
// For UNO and others without hardware serial, we must use software serial...
// pin #2 is IN from sensor (GREEN wire)
// pin #3 is OUT from arduino  (WHITE wire)
// Set up the serial port to use softwareserial..
// SoftwareSerial mySerial(2, 3);
#define mySerial Serial2
#else
// On Leonardo/M0/etc, others with hardware serial, use hardware serial!
// #0 is green wire, #1 is white
#define mySerial Serial2

#endif

Modbus slave(ID1, 0, 4);
uint16_t au16data[6];
// void loop() {
// slave.poll(au16data,10);
// au16data[0] = id;
                                          



LiquidCrystal lcd(13, 12, 11, 10, 9, 8);
Adafruit_Fingerprint finger = Adafruit_Fingerprint(&mySerial);

uint8_t id;
uint8_t mode;
void setup()
{
  Serial.begin(9600);
  slave.start();
  lcd.begin(16, 2);
  delay(100);

  // set the data rate for the sensor serial port
  finger.begin(57600);
  delay(1000);
  if (finger.verifyPassword()) {
    lcd.print("Found fingerprint sensor!");
  } else {
    lcd.print("Did not find fingerprint sensor :(");
    while (1);
  }
  pinMode(7,INPUT);
  digitalWrite(7,HIGH);
}

void loop()                     // run over and over again
{
  slave.poll(au16data,6);
  //tim van tay

  mode = au16data[2];
  if(mode==2){
    id = au16data[3];
    if (id == 0) {// ID #0 not allowed, try again!
      return;
    }
    while (! getFingerprintEnroll() );
    if(au16data[0]==101){
      au16data[2]=1;
    }
  }
  else if(mode==3){
    uint8_t id = au16data[3];
    if (id == 0) {// ID #0 not allowed, try again!
      return;
    }
    deleteFingerprint(id);
    delay(2000);
    au16data[2]=1;
  }
  else{
    id = au16data[3];
    getFingerprintID();
    if(au16data[0]==100){
      lcd.clear();
      lcd.print("Hoan thanh dd");
      //lcd.print(di);

      delay(2000);
      au16data[0]=0;
    }
  }
  mode=0;
  // if(mode==1){
  //   id = au16data[3];
  //   getFingerprintID();
  // }

  // //them van tay
  // else if(mode==2){
  //   id = au16data[3];
  //   if (id == 0) {// ID #0 not allowed, try again!
  //     return;
  //   }
  //   while (! getFingerprintEnroll() );
  //   mode=1;
  // }
  // // xoa van tay
  // else if(mode==3){
  //   uint8_t id = au16data[3];
  //   if (id == 0) {// ID #0 not allowed, try again!
  //     return;
  //   }
  //   deleteFingerprint(id);
  //   mode=1;
  // }
  
}


//them van tay
//
//

uint8_t getFingerprintEnroll() {

  int p = -1;
  lcd.clear();
  lcd.setCursor(0,0); 
  lcd.print("wait id:");
  lcd.print(id);
  while (p != FINGERPRINT_OK) {
    slave.poll(au16data,6);
    p = finger.getImage();
    switch (p) {
    case FINGERPRINT_OK:
      // Serial.println("Image taken");
      break;
    case FINGERPRINT_NOFINGER:
      // Serial.print(".");
      au16data[0] = 2;
      au16data[1] = 10;
      break;
    case FINGERPRINT_PACKETRECIEVEERR:
      // Serial.println("Communication error");
      break;
    case FINGERPRINT_IMAGEFAIL:
      // Serial.println("Imaging error");
      break;
    default:
      // Serial.println("Unknown error");
      break;
    }
  }

  // OK success!

  p = finger.image2Tz(1);
  switch (p) {
    case FINGERPRINT_OK:
      // Serial.println("Image converted");
      break;
    case FINGERPRINT_IMAGEMESS:
      // Serial.println("Image too messy");
      return p;
    case FINGERPRINT_PACKETRECIEVEERR:
      // Serial.println("Communication error");
      return p;
    case FINGERPRINT_FEATUREFAIL:
      // Serial.println("Could not find fingerprint features");
      return p;
    case FINGERPRINT_INVALIDIMAGE:
      // Serial.println("Could not find fingerprint features");
      return p;
    default:
      // Serial.println("Unknown error");
      return p;
  }

  // Serial.println("Remove finger");
  // delay(2000);
  // p = 0;
  // while (p != FINGERPRINT_NOFINGER) {
  //   p = finger.getImage();
  //   slave.poll(au16data,4);
  //   au16data[0] = 1;
  //   au16data[1] = 0;
  // }
  // Serial.print("ID "); Serial.println(id);
  p = -1;
  // lcd.clear();
  // lcd.setCursor(0,0);
  // lcd.print("nhap lai van tay");
  while (p != FINGERPRINT_OK) {
    slave.poll(au16data,6);
    p = finger.getImage();
    switch (p) {
    case FINGERPRINT_OK:
      // Serial.println("Image taken");
      break;
    case FINGERPRINT_NOFINGER:
      // Serial.print(".");
      au16data[0] = 2;
      au16data[1] = 11;
      break;
    case FINGERPRINT_PACKETRECIEVEERR:
      // Serial.println("Communication error");
      break;
    case FINGERPRINT_IMAGEFAIL:
      // Serial.println("Imaging error");
      break;
    default:
      // Serial.println("Unknown error");
      break;
    }
  }

  // OK success!

  p = finger.image2Tz(2);
  switch (p) {
    case FINGERPRINT_OK:
      //Serial.println("Image converted");
      break;
    case FINGERPRINT_IMAGEMESS:
      //Serial.println("Image too messy");
      return p;
    case FINGERPRINT_PACKETRECIEVEERR:
      //Serial.println("Communication error");
      return p;
    case FINGERPRINT_FEATUREFAIL:
      //Serial.println("Could not find fingerprint features");
      return p;
    case FINGERPRINT_INVALIDIMAGE:
      //Serial.println("Could not find fingerprint features");
      return p;
    default:
      //Serial.println("Unknown error");
      return p;
  }

  // OK converted!
  //Serial.print("Creating model for #");  Serial.println(id);

  p = finger.createModel();
  if (p == FINGERPRINT_OK) {
    //Serial.print("Prints matched!");
  } else if (p == FINGERPRINT_PACKETRECIEVEERR) {
    //Serial.println("Communication error");
    return p;
  } else if (p == FINGERPRINT_ENROLLMISMATCH) {
    lcd.clear();
    lcd.setCursor(0,0);
    lcd.println("khong khop");
    au16data[0] = 2;
    au16data[0] = 0;
    return p;
  } else {
    //Serial.println("Unknown error");
    return p;
  }
  lcd.clear();
  lcd.setCursor(0,0);
  lcd.print("ID "); 
  lcd.print(id);
  p = finger.storeModel(id);
  if (p == FINGERPRINT_OK) {
    lcd.clear();
    lcd.setCursor(0,1);
    lcd.print("Stored!");
    au16data[0] = 2;
    au16data[1] = id;
    au16data[2]=1;
  } else if (p == FINGERPRINT_PACKETRECIEVEERR) {
    //Serial.println("Communication error");
    return p;
  } else if (p == FINGERPRINT_BADLOCATION) {
    //Serial.println("Could not store in that location");
    return p;
  } else if (p == FINGERPRINT_FLASHERR) {
    //Serial.println("Error writing to flash");
    return p;
  } else {
    //Serial.println("Unknown error");
    return p;
  }

  return true;
}



//fringer delete




uint8_t deleteFingerprint(uint8_t id) {
  uint8_t p = -1;

  p = finger.deleteModel(id);

  if (p == FINGERPRINT_OK) {
    lcd.clear();
    lcd.setCursor(0,0);
    lcd.print("Deleted: ");
    lcd.print(id);
    au16data[0] = 3;
    au16data[1] = id;
    au16data[2] = 1;
    delay(500);
  } else if (p == FINGERPRINT_PACKETRECIEVEERR) {
    //Serial.println("Communication error");
  } else if (p == FINGERPRINT_BADLOCATION) {
    //Serial.println("Could not delete in that location");
  } else if (p == FINGERPRINT_FLASHERR) {
    //Serial.println("Error writing to flash");
  } else {
    //Serial.print("Unknown error: 0x"); Serial.println(p, HEX);
  }

  return true;
}




//fingerprint



uint8_t getFingerprintID() {
  uint8_t p = finger.getImage();
  switch (p) {
    case FINGERPRINT_OK:
      //Serial.println("Image taken");
      break;
    case FINGERPRINT_NOFINGER:
      //Serial.println("No finger detected");
      lcd.clear();
      lcd.setCursor(0,0);
      lcd.print("Diem danh lo");
  

      // lcd.print(id);
      au16data[4] = 1;
      au16data[5] = 0;
      return p;
    case FINGERPRINT_PACKETRECIEVEERR:
      //Serial.println("Communication error");
      return p;
    case FINGERPRINT_IMAGEFAIL:
      //Serial.println("Imaging error");
      return p;
    default:
      //println("Unknown error");
      return p;
  }

  // OK success!

  p = finger.image2Tz();
  switch (p) {
    case FINGERPRINT_OK:
      //Serial.println("Image converted");
      lcd.clear();
      lcd.setCursor(0,0);
      lcd.print("Khong tim thay...");
      //lcd.print(id);
      au16data[4] = 1;
      au16data[5] = 0;
      break;
    case FINGERPRINT_IMAGEMESS:
      //Serial.println("Image too messy");
      return p;
    case FINGERPRINT_PACKETRECIEVEERR:
      //Serial.println("Communication error");
      return p;
    case FINGERPRINT_FEATUREFAIL:
      //Serial.println("Could not find fingerprint features");
      return p;
    case FINGERPRINT_INVALIDIMAGE:
     // Serial.println("Could not find fingerprint features");
      return p;
    default:
      //Serial.println("Unknown error");
      return p;
  }

  // OK converted!
  p = finger.fingerSearch();
  if (p == FINGERPRINT_OK) {
    //Serial.println("Found a print match!");
  } else if (p == FINGERPRINT_PACKETRECIEVEERR) {
    //Serial.println("Communication error");
    return p;
  } else if (p == FINGERPRINT_NOTFOUND) {
    //Serial.println("Did not find a match");
    lcd.clear();
    lcd.setCursor(0,0);
    lcd.print("khong tim thay...");
    lcd.print(id);
    au16data[4] = 1;
    au16data[5] = 0;
    return p;
  } else {
    //Serial.println("Unknown error");
    return p;
  }

  // found a match!
  lcd.clear();
  lcd.setCursor(0,0);
  lcd.print("wait...."); 
  au16data[4] = 1;
  au16data[5] = finger.fingerID;
  return finger.fingerID;
}

// returns -1 if failed, otherwise returns ID #
// int getFingerprintIDez() {
//   uint8_t p = finger.getImage();
//   if (p != FINGERPRINT_OK)  return -1;

//   p = finger.image2Tz();
//   if (p != FINGERPRINT_OK)  return -1;

//   p = finger.fingerFastSearch();
//   if (p != FINGERPRINT_OK)  return -1;

//   // found a match!
//   Serial.print("Found ID #"); Serial.print(finger.fingerID);
//   Serial.print(" with confidence of "); Serial.println(finger.confidence);
//   return finger.fingerID;
// }
