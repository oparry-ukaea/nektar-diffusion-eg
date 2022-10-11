#! /bin/env bash

EXE="Lorenz.exe"
g++ Lorenz_integrator.cpp -o "$EXE"
"./$EXE"