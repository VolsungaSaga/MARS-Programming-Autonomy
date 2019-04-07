#include <string>
#include <iostream>
#include <cstdio>

#include <unistd.h>

//Base includes, we're using a serial library developed by
// William Woodall and John Harrison
#include "serial/serial.h"
#include "ros/ros.h"


using std::string;
using std::exception;
using std::cout;
using std::cerr;
using std::endl;
using std::vector;

int main(int argc, char** argv){

    ros::init(argc, argv, "vel_to_serial");
    
    ros::NodeHandle n;
    
    //First arg is port.
    string port(argv[1]);
    //Second is baud rate.
    unsigned int baud = 0;
    sscanf(argv[2], "%u", &baud);
    
    //Timeout
    serial::Timeout tout = serial::Timeout::simpleTimeout(1000);
    
    serial::Serial jetsonSerial(port, baud, tout);
    
    
    for(int i = 0; i < 10; i++){
        //Test if we can indeed write to the port.
        string test = "Testing";
        size_t bytes_pushed = jetsonSerial.write(test);
    
        string result = jetsonSerial.read(test.length());
    }
    


}
