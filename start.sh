#!/bin/bash
cd src
python preprocess.py
streamlit run main.py --server.port $PORT --server.enableCORS false
