@echo off
echo Generating 3x3 Grid Network...
netgenerate --grid --grid.number=3 --grid.length=200 --output-file sumo_sim/grid.net.xml --no-turnarounds --default.type traffic_light
if %ERRORLEVEL% NEQ 0 (
    echo Error generating network.
    exit /b %ERRORLEVEL%
)

echo Generating Random Trips...
python "%SUMO_HOME%/tools/randomTrips.py" -n sumo_sim/grid.net.xml -r sumo_sim/grid.rou.xml -e 500 -p 0.5
if %ERRORLEVEL% NEQ 0 (
    echo Error generating trips. Make sure SUMO_HOME is set correctly.
    echo Trying fallback assuming python tools are in path...
    randomTrips.py -n sumo_sim/grid.net.xml -r sumo_sim/grid.rou.xml -e 500 -p 0.5
)

echo Map generation complete.
