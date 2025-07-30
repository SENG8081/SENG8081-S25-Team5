@echo off
setlocal
:: Set log file name with timestamp
set LOGFILE=etl_log_%DATE:~10,4%-%DATE:~4,2%-%DATE:~7,2%_%TIME:~0,2%-%TIME:~3,2%.log
set LOGFILE=%LOGFILE: =0%
set LOGPATH=%~dp0logs\%LOGFILE%

:: Create logs directory if not exists
if not exist "%~dp0logs" mkdir "%~dp0logs"

echo ============================ >> "%LOGPATH%"
echo ETL Job started at %DATE% %TIME% >> "%LOGPATH%"

:: Step 1: Run cleaning script
echo [STEP 1] Cleaning and normalizing Kaggle data... >> "%LOGPATH%"
python "normalize_and_clean_kaggle_data.py" >> "%LOGPATH%" 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo ERROR in cleaning script. Job FAILED. >> "%LOGPATH%"
    echo Job FAILED during cleaning phase. See log: %LOGPATH%
    exit /b 1
)

:: Step 2: Load cleaned data into SQL Server
echo [STEP 2] Loading cleaned data into SQL Server... >> "%LOGPATH%"
python "load_csv_to_sqlserver.py" >> "%LOGPATH%" 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo ERROR in loading script. Job FAILED. >> "%LOGPATH%"
    echo Job FAILED during loading phase. See log: %LOGPATH%
    exit /b 1
)

echo ETL Job completed successfully at %DATE% %TIME% >> "%LOGPATH%"
echo Job SUCCESSFUL. Log saved at %LOGPATH%
exit /b 0
