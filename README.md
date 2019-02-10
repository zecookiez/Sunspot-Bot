## Inspiration
How many times have you ever killed a plant? While watering a plant is simple enough, it is far more difficult to ensure your house plant is exposed to the correct amount of sunlight. With increasingly busy schedules, and less time spent at home, plants are stuck in their pots, unable to get the sunlight they need. We had the opportunity to use a RedBot chassis and board (from the MLH hardware lab), photoresistors, as well as a Leap Motion sensor device, tying everything together by incorporating Solace PubSub+ messaging. The Sunspot Bot integrates all these components, to ultimately to optimize the living conditions of our plants.

## What it does
This plant-carrying robot uses photoresistors and motors to detect and navigate towards or away from light, giving your plant the chance to survive another day. Leap Motion hand tracking sensors are used for gesture-control of the plant, making remote plant care as easy as a flick of the wrist.

## How we built it
We used a RedBot chassis allows the plant to move, and photoresistors to detect the intensity of light. We used Leap Motion to incorporate gesture recognition for more intuitive remote control of the bot. In order to facilitate communication between all devices, we used Solace PubSub+ messaging, with a Kilo configuration using an AWS server:
- a combination of point-to-point messaging between the Leap Motion microservice, to the RedBot board
- a request-reply configuration for the initial connectivity check
- a publish-subscribe connection between webcam frames to the web app (in construction)

## Challenges we ran into
Working to calibrate and further improve the accuracy of the hand-gesture tracking and commands with Leap Motion. Integrating PubSub+ to our multi-lingual system. Sending segmented video stream packets to be displayed to a web app (still a challenge). Finding a live plant (also still a challenge).

## Accomplishments that we're proud of
Successfully communicating gesture commands from the Leap Motion to the robot, across multiple platforms, using multiple configurations of PubSub+

## What we learned
Integrating many different microservices into a single functional product is truly a challenge, but was made easier through the innovative application of Solace PubSub+ messaging.

## What's next for Sunspot-Bot
Completing the web application to allow for live streaming from the plant and switching between manual and autonomous navigation.
