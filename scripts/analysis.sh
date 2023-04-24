#!/bin/bash

## Decode using fine-tuneind phone recognizer
python3 local/transcribe.py

## Force-Align reference (g2P) & phonetic transcriptions
python3 local/alignProcess.py
bash local/align.sh

## generate confusionmatrix & analysis
python3 local/cmProcess.py
python3 local/confusionMatrix.py
