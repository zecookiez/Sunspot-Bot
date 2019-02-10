#include <RedBot.h>
//#include "PID_Drive.h"
#define NONE -1
#define STOP 0
#define FORWARDS 1
#define BACKWARDS 2
#define SPIN_LEFT 3
#define SPIN_RIGHT 4
#define TURN_LEFT 5
#define TURN_RIGHT 6
#define BACK_LEFT 7
#define BACK_RIGHT 8

RedBotMotors motors;
RedBotEncoder encoders = RedBotEncoder(A2, 10);
RedBotBumper bumperL = RedBotBumper(3);
RedBotBumper bumperR = RedBotBumper(11);
RedBotSensor light = RedBotSensor(A0);


int leftPower;  // variable for setting the drive power
int rightPower;
String data;  // variable for holding incoming data from PC to Arduino
int moveType; //variable for setting type of movement
int xVel;
int yVel;
float turnFactor = 0.2;
int lEnc = 0;
int rEnc = 0;
int offset = 1;
bool lBump = false;
bool rBump = false;
bool collision = false;
bool takeover = false;
int lightLevel = 0;

void setup(void)
{
  Serial.begin(9600);
  //Serial.setTimeout(50);
  /*Serial.print("Enter in left and right motor power values and click [Send]."); 
  Serial.print("Separate values with a space or non-numeric character.");
  Serial.println();
  Serial.print("Positive values spin the motor CW, and negative values spin the motor CCW.");*/
}

void loop(void)
{
  //Keep straight and correct if needed
  if(moveType == FORWARDS or moveType == BACKWARDS)
  {
    lEnc = -1 * encoders.getTicks(LEFT);
    rEnc = encoders.getTicks(RIGHT);
    //Serial.println(lEnc);
    //Serial.println(rEnc);
    if(abs(lEnc - rEnc) > 2 and abs(lEnc - rEnc) < 200 ) {
      if(lEnc > rEnc) {
        leftPower = constrain(leftPower - offset, -255, 255);
        rightPower = constrain(rightPower + offset, -255, 255);
      } else if(lEnc < rEnc) {
        leftPower = constrain(leftPower + offset, -255, 255);
        rightPower = constrain(rightPower - offset, -255, 255);
      }
    }
  }

  if(moveType == SPIN_LEFT or moveType == SPIN_RIGHT or moveType == TURN_LEFT or moveType == TURN_RIGHT or moveType == BACK_LEFT or moveType == BACK_RIGHT or moveType == STOP)
  {
    encoders.clearEnc(BOTH);
  }
  //Update movement
  //Serial.print("Movetype: ");
  //Serial.println(moveType);
  //Serial.print("LPower: ");
  //Serial.println(leftPower);
  //Serial.print("RPower: ");
  //Serial.println(rightPower);
  motors.leftMotor(leftPower);
  motors.rightMotor(rightPower);
  
  //Check serial for new instructions
  if(Serial.available())
  {
    //Serial.println("Event!");
    data = Serial.readStringUntil(' ');
    data.trim();
    //Serial.println(data);
    if(data == "N")
    {
      moveType = FORWARDS;
    }
    else if(data == "S")
    {
      moveType = BACKWARDS;
    }
    else if(data == "W")
    {
      moveType = SPIN_LEFT;
    }
    else if(data == "E")
    {
      moveType = SPIN_RIGHT;
    }
    else if(data == "NW")
    {
      moveType = TURN_LEFT;
    }
    else if(data == "NE")
    {
      moveType = TURN_RIGHT;
    }
    else if(data == "SW")
    {
      moveType = BACK_LEFT;
    }
    else if(data == "SE")
    {
      moveType = BACK_RIGHT;
    } 
    else if(data == "STOP")
    {
      moveType = STOP;
      motors.brake();
      Serial.read();
      Serial.read();
    } 
    else if(data == "TAKEOVER")
    {
      takeover = true;
      Serial.read();
      Serial.read();
    } 
    else
    {
      moveType = NONE;
      motors.brake();
      Serial.read();
      Serial.read();
    }
    //Set initial values for motor power, positive is forwards and negative is backwards
    if(moveType != NONE and moveType != STOP)
    {
      //Serial.println("getting vel!");
      xVel = Serial.parseInt();
      yVel = Serial.parseInt();
      Serial.read(); 
      Serial.read(); 
      Serial.read(); 
      Serial.read(); 
      //Serial.flush();
      //Serial.println(moveType);
      //Serial.println(xVel);
      //Serial.println(yVel);
    }
    if(moveType == FORWARDS)
    {
      leftPower = yVel;
      rightPower = yVel;
    } else if(moveType == BACKWARDS)
    {
      leftPower = -yVel;
      rightPower = -yVel;
    } else if(moveType == SPIN_LEFT)
    {
      leftPower = -xVel;
      rightPower = xVel;
    } else if(moveType == SPIN_RIGHT)
    {
      leftPower = xVel;
      rightPower = -xVel;
    } else if(moveType == TURN_LEFT)
    {
      leftPower = yVel - int(xVel * turnFactor) - 10;
      rightPower = yVel;
    } else if(moveType == TURN_RIGHT)
    {
      leftPower = yVel;
      rightPower = yVel - int(xVel * turnFactor);
    } else if(moveType == BACK_LEFT)
    {
      leftPower = -1 * (yVel - int(xVel * turnFactor) - 10);
      rightPower = -1 * yVel;
    } else if(moveType == BACK_RIGHT)
    {
      leftPower = -1 * yVel;
      rightPower = -1 * (yVel - int(xVel * turnFactor));
    } else if(moveType == STOP) {
      leftPower = 0;
      rightPower = 0;
    } else {
      leftPower = 0;
      rightPower = 0;
    }
    if(collision and !takeover)
    {
      //Serial.println("Frozen");
      moveType = STOP;
      leftPower = 0;
      rightPower = 0;
    }
  }

  //Check for whiskers
  lBump = !bumperL.read();
  rBump = !bumperR.read();
  //Serial.println(lBump);
  //Serial.println(rBump);
  if ((lBump or rBump) and !takeover)
  {
    //Serial.println("boop");
    collision = true;
    moveType = 0;
    leftPower = rightPower = 0;
    motors.brake();
    //Send an error to the serial port
    if(!collision)
    {
      Serial.println("COLLISION");
    }
  } else if (!lBump and !rBump and collision)
  {
    collision = false;
    takeover = false;
    Serial.println("RESUME");
  }
  //Read and send light data
  lightLevel = light.read();
  Serial.println(lightLevel);
}

void serialEvent() {
  
 
}
