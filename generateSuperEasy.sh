#!/bin/bash

rm -rf Worlds
mkdir Worlds

python WorldGenerator.py 1000 super_easy_world_ 5 5 1

echo Finished generating worlds!
