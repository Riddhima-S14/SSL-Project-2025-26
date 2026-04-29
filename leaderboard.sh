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

games=$(cut -d ',' -f 3 history.csv | sort | uniq)


ordered_games="$game_input $(echo "$games" | grep -vx "$game_input")"

for game in $ordered_games; do

    # 2. Centered Game Header
    total_width=66
    len=${#game}
    padding=$(( (total_width - len) / 2 ))
    left_side=$(printf '%.0s=' $(seq 1 $padding))
    right_side=$(printf '%.0s=' $(seq 1 $((total_width - len - padding))))
    echo "${left_side}${game}${right_side}"

    # 3. Table Header
    printf "| %-22s | %-8s | %-8s | %-14s |\n" "PLAYER" "WIN" "LOSS" "WIN/LOSS"
    echo "------------------------------------------------------------------"

    # 4. Data Processing
    touch temp.txt players.txt final_data.txt
    grep "$game" history.csv | cut -d ',' -f 1 > temp.txt
    grep "$game" history.csv | cut -d ',' -f 2 >> temp.txt
    sort temp.txt | uniq > players.txt

    > final_data.txt

    while read -r p; do
        [ -z "$p" ] && continue
        w=$(grep "$game" history.csv | cut -d ',' -f 1 | grep -xc "$p")
        l=$(grep "$game" history.csv | cut -d ',' -f 2 | grep -xc "$p")

        if [[ $l -eq 0 ]]; then
            ratio_num="999.00"
            ratio_disp="UNDEFEATED"
        else
            ratio_num=$(echo "scale=2; $w / $l" | bc)
            ratio_disp=$ratio_num
        fi

        echo "$p $w $l $ratio_num $ratio_disp" >> final_data.txt
    done < players.txt

    # 5. Sorting Logic
    if [[ "$sort_option" == "1" ]]; then
        sorted_data=$(sort -k2,2nr -k1,1 final_data.txt)
    elif [[ "$sort_option" == "2" ]]; then
        sorted_data=$(sort -k3,3nr -k1,1 final_data.txt)
    elif [[ "$sort_option" == "3" ]]; then
        sorted_data=$(sort -k4,4nr -k1,1 final_data.txt)
    else
        sorted_data=$(cat final_data.txt)
    fi

    # 6. Final Print
    while read -r p w l r_num r_disp; do
        printf "| %-22s | %-8s | %-8s | %-14s |\n" "$p" "$w" "$l" "$r_disp"
    done <<< "$sorted_data"

    echo "=================================================================="
    echo

    # Cleanup
    rm temp.txt players.txt final_data.txt 2>/dev/null

done