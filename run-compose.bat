@echo off
setlocal

set "SCRIPT_DIR=%~dp0"
pushd "%SCRIPT_DIR%" >nul

where docker >nul 2>&1
if errorlevel 1 (
    echo Docker was not found in PATH.
    popd >nul
    exit /b 1
)

if not exist ".env" (
    copy /Y ".env.example" ".env" >nul
    echo Created .env from .env.example.
    echo Update the placeholder values in .env and run this script again.
    popd >nul
    exit /b 1
)

if "%~1"=="" (
    set "COMPOSE_ARGS=up -d"
) else (
    set "COMPOSE_ARGS=%*"
)

docker compose --file "docker-compose.yml" --env-file ".env" %COMPOSE_ARGS%
set "EXIT_CODE=%ERRORLEVEL%"

popd >nul
exit /b %EXIT_CODE%