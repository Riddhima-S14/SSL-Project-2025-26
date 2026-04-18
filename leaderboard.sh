echo "====================LEADERBOARD================="
echo "====================TIC-TAC-TOE================="
echo "|    PLAYER    |   WIN   |   LOSS   | WIN/LOSS |"
echo "================================================"
touch temp.txt players.txt win.txt loss.txt l1.txt l_tictactoe.txt
cut -d ',' -f 1 history.csv > temp.txt
cut -d ',' -f 2 history.csv >> temp.txt
sort temp.txt | uniq > players.txt
while read line; do
grep  'Tictactoe' history.csv | cut -d ',' -f 1 | grep -c "$line">>win.txt
grep  'Tictactoe' history.csv | cut -d ',' -f 2 | grep -c "$line">>loss.txt
done < players.txt
paste -d ' ' players.txt win.txt loss.txt > l1.txt
while read line; do
w=$(grep -E "$line" l1.txt | cut -d ' ' -f 2)
l=$(grep -E "$line" l1.txt | cut -d ' ' -f 3)
echo $l

if [[ $l -eq 0 ]] ; then
ratio="N.A."
else
ratio=$(echo "scale=2;$w / $l" | bc)
fi
echo $line ' ' $ratio >> l_tictactoe.txt
done < l1.txt
# cat l_tictactoe.txt
cat l1.txt
rm win.txt loss.txt temp.txt l1.txt l_tictactoe.txt players.txt
