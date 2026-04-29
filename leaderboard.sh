#!/bin/bash

game_input=$1
sort_option=$2 
#1=Wins, 2=Losses, 3=Ratio

cat << "EOF"
  _                _           _                         _ 
 | |              | |         | |                       | |
 | | ___  __ _  __| | ___ _ __| |__   ___   __ _ _ __ __| |
 | |/ _ \/ _` |/ _` |/ _ \ '__| '_ \ / _ \ / _` | '__/ _` |
 | |  __/ (_| | (_| |  __/ |  | |_) | (_) | (_| | | | (_| |
 |_|\___|\__,_|\__,_|\___|_|  |_.__/ \___/ \__,_|_|  \__,_|
EOF

#check what games have histories
games=$(cut -d ',' -f 3 history.csv | tr -d '\r' | sort -u)

#order them with the last played game first
ordered_games="$game_input $(echo "$games" | grep -vxF "$game_input")"
for game in $ordered_games; do

    #centered game header
    total_width=66
    len=${#game}
    padding=$(( (total_width - len) / 2 ))
    left_side=$(printf '%.0s=' $(seq 1 $padding))
    right_side=$(printf '%.0s=' $(seq 1 $((total_width - len - padding))))
    echo "${left_side}${game}${right_side}"

    #table header
    printf "| %-22s | %-8s | %-8s | %-14s |\n" "PLAYER" "WIN" "LOSS" "WIN/LOSS"
    echo "------------------------------------------------------------------"

    #extract all players (both winners and losers) for the current game
    #use awk to filter rows where game name matches ($3 == g)
    #remove any hidden carriage returns (\r) from the game field
    #print winners (column 1) and losers (column 2) into a temp file
    #sort and remove duplicates to get a unique list
    touch temp.txt players.txt final_data.txt
    awk -F',' -v g="$game" '{sub(/\r$/, "", $3)} $3 == g {print $1}' history.csv > temp.txt
    awk -F',' -v g="$game" '{sub(/\r$/, "", $3)} $3 == g {print $2}' history.csv >> temp.txt
    sort temp.txt | uniq > players.txt

    > final_data.txt

    
    while read -r p; do
        #skip empty lines (just in case)
        [ -z "$p" ] && continue
        #count wins
        w=$(awk -F',' -v g="$game" -v p="$p" '{sub(/\r$/, "", $3)} $3==g && $1==p' history.csv | wc -l)
        #count losses
        l=$(awk -F',' -v g="$game" -v p="$p" '{sub(/\r$/, "", $3)} $3==g && $2==p' history.csv | wc -l)

        if [[ $l -eq 0 ]]; then
            #undefeated should be the highest
            ratio_num="9999.00"
            ratio_disp="UNDEFEATED"
        else
            ratio_num=$(awk "BEGIN { printf \"%.2f\", $w / $l }")
            ratio_disp=$ratio_num
        fi

        #store player stats: name, wins, losses, numeric ratio, display ratio
        echo "$p $w $l $ratio_num $ratio_disp" >> final_data.txt
    done < players.txt

    #sorting logic
    if [[ "$sort_option" == "1" ]]; then
        sorted_data=$(sort -k2,2nr -k1,1 final_data.txt)
    elif [[ "$sort_option" == "2" ]]; then
        sorted_data=$(sort -k3,3nr -k1,1 final_data.txt)
    elif [[ "$sort_option" == "3" ]]; then
        sorted_data=$(sort -k4,4nr -k1,1 final_data.txt)
    else
        sorted_data=$(cat final_data.txt)
    fi

    #final print
    while read -r p w l r_num r_disp; do
        printf "| %-22s | %-8s | %-8s | %-14s |\n" "$p" "$w" "$l" "$r_disp"
    done <<< "$sorted_data"

    echo "=================================================================="
    echo

    #cleanup
    rm temp.txt players.txt final_data.txt 2>/dev/null

done
