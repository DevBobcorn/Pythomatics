@echo off
color 02
title Minecraft News Checker - By Bobcorn
python.exe "%~dp0\LogoPrint.py"
python.exe "%~dp0\NewsGet.py"
pause