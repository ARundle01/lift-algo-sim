# lift-algo-sim
Simulation of two different Lift Algorithms.

## What is this project?
This repository contains the code for one of my University projects. This project was for the Data Structures and Algorithms module and concerned the simulation of lifts (elevators). 

### The Naïve Lift
The original specification required a basic (sometimes referred to as Naïve) lift system wherein the lift has a set capacity of six people and could only move up or down. This lift could only change directions when it had reached the top or bottom floor; this is an attempt to model original mechanical lifts.

### The Improved Lift
The specification also required an algorithm written by the student that was, in some form or another, more efficient than the Naïve lift. My improved code is based on the SCAN disk scheduling algorithm (sometimes referred to as [The Elevator algorithm](https://en.wikipedia.org/wiki/Elevator_algorithm)) wherein the Lift can now change direction anywhere, on any floor. However, it is always checking for:
- people in the floors ahead of the lift (if it is going up, it checks for people further up the building.)
- people in the lift that need to be delivered ahead of the lift
If either of these conditions are met, it continues in its current direction. If neither are met, then it will change directions and continue the other way.

## Can I use this code?
I mean, if you really want to. This code was made to fit the specification under a time pressure so isn't the nicest to look at or work with. 

## Details
This code was written in Python 3.8.0 and uses Pygame 1.9.6
