#include <stdio.h>
#include <cstdint>
#include <iostream>
#include <fstream>
#include <sstream>
#include <string>
#include <vector>
using namespace std;

int main(){
    double time[30250];
    double TPSval[30250];
    std::ifstream TPS("TPS2.csv");

    if (!TPS.is_open()){
        cout<<"file error\n";
        return 1;
    }

}