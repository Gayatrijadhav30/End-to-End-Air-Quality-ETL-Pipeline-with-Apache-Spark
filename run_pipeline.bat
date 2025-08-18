@echo off
cd /d "C:\Diproject\Project"
echo [⚙️] Starting EPA Air Pipeline Automation...

:: Step 1: Create virtual environment (if not exists)
if not exist dataenv (
    echo [📦] Creating virtual environment 'dataenv'...
    python -m venv dataenv_test
)

:: Step 2: Activate the virtual environment
call dataenv_test\Scripts\activate

:: Step 3: Install required Python packages
echo [📥] Installing required Python libraries...
pip install --upgrade pip
pip install pyspark pandas psycopg2-binary

:: Step 4: Run the main pipeline script
echo [🚀] Running main_test.py...
python main_test.py

echo.
pause
