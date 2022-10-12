// Lorenz_integrator.cpp : This file contains the 'main' function. Program execution begins and ends there.
//

#include <iostream>

#pragma warning(disable:4996)  //needed in VS2022 to stop security check error

#define NUMSTAGES 5

//parameters
//initial conditions
double gX0 = 0.0;
double gY0 = 1.0;
double gZ0 = 0.0;

//timestep
double gDt = 0.001;

//all the following model parameters are >0
//see https://www2.physics.ox.ac.uk/sites/default/files/profiles/read/lect6-43147.pdf
double gSigma = 10.0;  //is basically Prandtl number
double gRho   = 28.0;  //is basically Rayleigh number
double gBeta  = 8.0/3.0;


void EvaluateLorenz(double t, double& x, double& y, double& z);
void EvaluateLorenzDerivs(double x, double y, double z, double& xDot, double& yDot, double& zDot);

int main()
{
    std::cout << "Lorenz model time series generator.\n";

    //quick test of Lorenz, generate time series
#if 1
    FILE* outFile = fopen("orig/lorenz.csv", "w");

    fprintf(outFile, "x,y,z\n");

    double x = gX0;
    double y = gY0;
    double z = gZ0;

    for (int it = 0; it < 100000; it++)  //time loop
    {
        EvaluateLorenz(0.0, x, y, z);
        fprintf(outFile, "%.6e,%.6e,%.6e\n", x, y, z);  
    }
    fclose(outFile);
    return 1;
#endif

    return 0;

}

void EvaluateLorenz(double t, double& x, double& y, double& z)
{
    double xS, yS, zS;  //temp storage for LSRK
    xS = yS = zS = 0.0;

    double xDot, yDot, zDot;
    double dt = gDt;

    double A[NUMSTAGES];
    double B[NUMSTAGES];

    //scheme 2 Carpenter - Kennedy (NUMSTAGES must be 5)
    A[0] = 0.0;
    A[1] = -0.4801594388478;
    A[2] = -1.4042471952;
    A[3] = -2.016477077503;
    A[4] = -1.056444269767;

    B[0] = 0.1028639988105;
    B[1] = 0.7408540575767;
    B[2] = 0.7426530946684;
    B[3] = 0.4694937902358;
    B[4] = 0.1881733382888;

    for (int iStage = 0; iStage < NUMSTAGES; iStage++)
    {
        EvaluateLorenzDerivs(x, y, z, xDot, yDot, zDot);

        xS = A[iStage] * xS + dt * xDot;
        yS = A[iStage] * yS + dt * yDot;
        zS = A[iStage] * zS + dt * zDot;
        x += B[iStage] * xS;
        y += B[iStage] * yS;
        z += B[iStage] * zS;
    }
}



void EvaluateLorenzDerivs(double x, double y, double z, double& xDot, double& yDot, double& zDot)
{
    double sigma = gSigma;
    double rho   = gRho;
    double beta  = gBeta;
    xDot = sigma * (y - x);
    yDot = x * (rho - z) - y;
    zDot = x * y - beta * z;
}
