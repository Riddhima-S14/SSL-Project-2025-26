#!/bin/bash

users="users.tsv"
touch "$users"

#function to hash a password
hash_password(){
    echo "$1" | shasum -a 256 | awk '{print $1}'
}

#function to authenticate a user
authenticate_user(){
    local player_number=$1
    local authenticated=false

    while [[ "$authenticated" == "false" ]]; do
        echo "--- Player $player_number Authentication ---" >&2
        read -p "Username: " username
        
        stored_credentials=$(grep "^$username" "$users")
        
        #if registered
        if [[ -n $stored_credentials ]]; then
            read -sp "Password: " password
            echo "" >&2
            hashed_password=$(hash_password "$password")
            stored_hash=$(echo "$stored_credentials" | cut -f2)

            if [[ $hashed_password == $stored_hash ]]; then
                echo "Welcome $username!" >&2
                authenticated=true
                echo "$username"
            else
                echo "Incorrect password. Please try again." >&2
            fi

        #if not registered
        else
            read -p "User "$username" not found. Would you like to register? (y/n): " answer
            if [[ $answer =~ ^[Yy]$ ]]; then
                read -sp "Password: " password
                echo -e "">&2
                hashed_password=$(hash_password "$password")
                echo -e "$username\t$hashed_password" >> "$users"
                echo "Registration successful!" >&2
                echo "Welcome $username!" >&2
                authenticated=true
                echo "$username"
            else 
                echo "Please try a different username." >&2
            fi 
        
        fi
    done
}

echo "==============================="
echo "     WELCOME TO THE ARCADE     "
echo "==============================="

#player 1
user1=$(authenticate_user 1)

#player 2
while true; do
    user2=$(authenticate_user 2)
    if [[ $user1 == $user2 ]]; then
        echo "Player 2 must be a different user than Player 1. Please try again."
        continue
    fi
    break
done

#entering the game
echo "May the best player win..."
python3 game.py "$user1" "$user2"
