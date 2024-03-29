@echo off
mode con: cols=120 lines=43
title=Game Releases Tracker

: ======================================================================================
: Installing virtual environment
: ======================================================================================
echo Activating virtual environment. Please stand by...
set venv_name=venv
py -m venv %venv_name%
call %venv_name%\Scripts\activate
pip install -r requirements.txt 1>nul 2>nul

: ======================================================================================
: Starting the application
: ======================================================================================
py main.py

: ======================================================================================
: So that we can read logs if needed
: ======================================================================================
timeout -1