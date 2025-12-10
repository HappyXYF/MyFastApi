#!/bin/bash

# Activate virtual environment
source favenv/bin/activate

# Install requirements
pip install -r requirements.txt

# Check if ODBC Driver is installed
if ! python -c "import pyodbc; print([d for d in pyodbc.drivers() if 'SQL Server' in d])" 2>/dev/null | grep -q "SQL Server"; then
    echo "SQL Server ODBC driver not found. Installing..."
    ./install_odbc_driver.sh
fi

# Run the application
python app.py
