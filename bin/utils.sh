#!/bin/bash

ask() # $1 - message , if $2='exit' - exit from script on N/n
{
    if [ -n "${ALL_QUESTION_YES}" ]; then
        return 0
    fi
    PROMPT="$1 (Y/n/a/q)"
    while true
    do 
        echo ""
        read -p "${PROMPT}" answer
        echo ""
        case ${answer} in
            "N") RESULT=1; break;;
            "n") RESULT=1; break;; 
            "Y") RESULT=0; break;;
            "y") RESULT=0; break;;
            "A") RESULT=0; export ALL_QUESTION_YES=1; break;;
            "a") RESULT=0; export ALL_QUESTION_YES=1; break;;
             "") RESULT=0; break;;
            "Q") echo "Canceled"; exit 1; break;;
            "q") echo "Canceled"; exit 1; break;;
            *) echo ""; echo "Only Y/y or N/n or Q/q allowed!"; echo "";;
        esac
    done
    if [ "$2" = "exit" -a "${RESULT}" = "1" ]; then
        echo "Canceled"; 
        exit 1
    fi
    return ${RESULT}
}

exit_if_fail() # call it as 'exit_if_fail $?'
{
    if [ "$1" = "1" ]; then
        echo ""
        echo "Error detected! Exit now."
        exit 1
    fi
}

message()
{
    echo ""
    echo "$1"
    echo ""
}

