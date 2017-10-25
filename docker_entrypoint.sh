#!/usr/bin/env bash
flask db upgrade
if [ ! -f DATA_IMPORTED ]; then
        echo "Trying to connect to host ${DB_SERVICE} port ${DB_PORT}"
        nc -z -v -w${DB_CHECK_TIMEOUT} ${DB_SERVICE} ${DB_PORT};
    if [[ $? == 0 ]]; then
        flask import_data && touch DATA_IMPORTED;
    else
        echo "Attempt was unsuccessful. Give up..."
    fi;
else
    echo "Data already imported. Skip import."
fi;
flask run --host=${FLASK_HOST} --port=${FLASK_PORT}
