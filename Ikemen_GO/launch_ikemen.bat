@echo off
REM Ikemen GO launch script

REM Character def paths
SET CHAR_DEF=..\kfm_env\kfm_env.def

REM Launch Ikemen GO
Ikemen_GO.exe ^
-p1 %CHAR_DEF% ^
-p1.color 1 ^
-p2 %CHAR_DEF% ^
-p2.ai 1 ^
-p2.color 3 ^
-s stages/training.def ^
-rounds 1 ^
--nosound ^
--windowed ^
--width 320 ^
--height 240

REM Exit with Ikemen's error code
exit /b %errorlevel%