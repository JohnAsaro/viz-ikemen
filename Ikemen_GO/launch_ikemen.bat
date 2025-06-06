@echo off
REM Ikemen GO launch script

REM Character def paths
SET CHAR_DEF=..\sf_alpha_ryu\ryu.def

REM Launch Ikemen GO
Ikemen_GO.exe ^
-p1 %CHAR_DEF% ^
-p1.color 1 ^
-p2 %CHAR_DEF% ^
-p2.ai 4 ^
-p2.color 2 ^
-s stages/training.def ^
-rounds 1 ^
-setport 7500 ^
--nosound ^
--windowed ^
--width 320 ^
--height 240

REM Exit with Ikemen's error code
exit /b %errorlevel%