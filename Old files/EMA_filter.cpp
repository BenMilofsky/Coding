#include <stdio.h>
#include <cstdint>
#include <iostream>
#include <fstream>
#include <sstream>
#include <string>
#include <vector>


class EmaFilter
{
public:
    EmaFilter(double alpha) :
        m_alpha(alpha), m_lastOutput(0.0) {}

    double Run(double input)
    {
        m_lastOutput = m_alpha * input + (1 - m_alpha) * m_lastOutput;
        return m_lastOutput;
    }
private:
    double m_alpha;
    double m_lastOutput;
};

int main() {

    std::ifstream file("TPS2.csv");
    std::string line;
    const int N= 30250;


    

    float time[N];
    float throttle[N];
    EmaFilter emaFilter(0.5);

    for(uint32_t i = 0; i < 20; i++)
    {
        double input = 1.0;
        double output = emaFilter.Run(input);
        printf("%f\n", output);
    }
}




    // std::getline(file,line);
    // int N =0;