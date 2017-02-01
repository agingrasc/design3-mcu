echo "|******************************|"
echo "|*---------Unit tests---------*|"
echo "|******************************|"
echo ""
echo "----Tests for Game Board----"
python -m unittest python/test/gameboard/gameboardtest.py
echo "----Tests for Position----"
python -m unittest python/test/gameboard/positiontest.py
