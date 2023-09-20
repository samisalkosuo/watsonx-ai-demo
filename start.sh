#!/bin/bash

python print_info.py

exec python -m streamlit run app/main.py --server.port=8080
