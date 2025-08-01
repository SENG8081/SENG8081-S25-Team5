@echo off
SET SCRIPT_DIR=C:\Users\jyoro\Documents\RetailETL\Scripts
SET LOGFILE=%SCRIPT_DIR%\etl_log.txt
SET PYTHON_EXE=C:\Users\jyoro\AppData\Local\Programs\Python\Python310\python.exe

echo ============================= >> "%LOGFILE%"
echo %DATE% %TIME% - Starting ETL Run >> "%LOGFILE%"
echo Using Python: "%PYTHON_EXE%" >> "%LOGFILE%"

:: Change directory before execution
cd /d "%SCRIPT_DIR%"

:: Run Cleaning Script
echo Running normalize_and_clean_kaggle_data.py >> "%LOGFILE%"
"%PYTHON_EXE%" normalize_and_clean_kaggle_data.py >> "%LOGFILE%" 2>&1
IF %ERRORLEVEL% NEQ 0 (
    echo ERROR: Cleaning script failed! >> "%LOGFILE%"
) ELSE (
    echo SUCCESS: Cleaning script ran successfully. >> "%LOGFILE%"
)

:: Run Load Script
echo Running load_csv_to_sqlserver.py >> "%LOGFILE%"
"%PYTHON_EXE%" load_csv_to_sqlserver.py >> "%LOGFILE%" 2>&1
IF %ERRORLEVEL% NEQ 0 (
    echo ERROR: Loading script failed! >> "%LOGFILE%"
) ELSE (
    echo SUCCESS: Loading script ran successfully. >> "%LOGFILE%"
)

echo %DATE% %TIME% - ETL Run Finished. >> "%LOGFILE%"
echo ============================= >> "%LOGFILE%"
