#!/usr/bin/env bash
DB_CONNECTOR="-database_connector=messaging.DatabasePostgresql"
CONNECTION_STRING="-connection_string=dbname=$DB_NAME user=$DB_USER password=$DB_PASSWORD host=127.0.0.1"
HOST="-host=127.0.0.1"
PORT="-port=8000"
"$PYTHON" -m messaging.server "$DB_CONNECTOR" "$CONNECTION_STRING" "$HOST" "$PORT" &

SERVER_PID="$!"

sleep 3

"$PYTHON" test.py "$HOST" "$PORT"
EXIT_CODE="$?"

kill "$SERVER_PID"

if [ "$EXIT_CODE" == "0" ]; then
    echo "All tests passed"
else
    echo "Failed tests"
fi

exit $EXIT_CODE