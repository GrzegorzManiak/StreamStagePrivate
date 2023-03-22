@echo off

echo:
echo Deleting existing migrations...
echo:

for /r %%i in (migrations) do (
    if exist "%%i" (
        echo Deleting "%%i"
        rd /s /q "%%i"
    )
)

echo:
echo Deleting complete.
echo:

echo WOULD YOU LIKE TO DELETE YOUR DATABASE?
echo:
CHOICE /C YNS /M "Type Y for YES, N for NO, or S to skip migration altogether. "
echo:

if "%ERRORLEVEL%" == "1" (
    echo Deleting Database...
    if exist "App\db.sqlite3" (
        del App\db.sqlite3
    ) else (
        echo Database file does not exist.
    )
    echo:
)

if ERRORLEVEL 3 goto :fin

:migrate
echo Making migrations...
echo:

set apps= accounts applications events orders store search StreamStage

for %%i in (%apps%) do (
    py App/manage.py makemigrations %%i
    echo:
)

echo Migrating...
echo:

py App/manage.py migrate

echo:

:fin
PAUSE