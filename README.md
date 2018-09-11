# CMPUT399Lab1
Lab 1 working with differential drive motor robotics using the EV3 lego kit.

## Step 4
* Straight line (20cm)
* Rectangle
* Circle
* Figure-eight

## Step 5
Add a pen or pencil to your robot in such a way that you can draw the above shapes (line, rectangle, circle, figure-eight) when placing the robot over a sheet of paper. Draw each shape at least 3 times. What can be concluded and why? State your answer in the report.

## Step 6
Write a program that receives as input a 3x3 array. The first two columns are the left and right motor power respectively, the last column is the time during which the power is apply to the motors. Your program has to read each row in sequence and for each row the robot has to apply power to the motors according to columns 1 and 2 and maintain this value for duration stated in column 3. Example:
```
int[][] command = {
      { 80, 60, 2},
      { 60, 60, 1},
      {-50, 80, 2}
    };
 ```
row1: During the first two seconds motor one and two are powered with 80% and 60% of their max capacity 
row2: During the third second motor one and two are powered with 60% and 60% of their max capacity 
row3: During second 4 and 5 two motor one and two are powered with -50% and 60% of their max capacity (the minus means change in rotation direction) 

After finishing the three rows execution the robot has to transmit its location and orientation to the PC and/or show it in the display. Make sure you add some lego blocks structure to be able to align your robot with the (0,0) coordinate reference frame. Describe your implementation in detail.

## Step 7
How does error accumulate in rotation and linear movements of your robot, as function of the power applied to the robot motors?

Your robot is "probably" not perfect. There are small errors in moves. For the straight line movement, the easiest way to see this could be to measure the actual distance travelled by the robot and compare it to the computed distance.

Design two ways of measuring the error when your robot is moving in straight line. At least one of them must use input from some sensors. Compare the two methods. What do you find?
Design two ways of measuring the error when the robot is rotating. At least one of them must use input from some sensors. Compare the two methods. What do you find? Add your answers to the report.

## Step 8
Convert your differential drive vehicle into a Braitenberg vehicle:
Using light detecting sensors, implement in your robot the following behaviours against a light source: Coward, Aggresive, Love and Explore. 

## What to hand in:
A ZIP file and a report file (.pdf) electronically on the course homepage. The ZIP file has to contain your implementations and any data you either measured or generated. The implementation have to be well documented. In the ZIP file use a proper directory arrangement and write a readme.txt file about its structure.
