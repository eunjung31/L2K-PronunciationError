#!/bin/bash

## Decode using fine-tuneind phone recognizer
python3 transcribe.py

## Force-Align reference (g2P) & phonetic transcriptions
python3 alignProcess.py
bash align.sh

## generate confusionmatrix & analysis
python3 cmProcess.py
python3 confusionMatrix.py
