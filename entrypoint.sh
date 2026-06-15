#!/bin/sh

set -e

export FLASK_APP="${FLASK_APP:-main:app}"

wait_for_database() {
    echo "Aguardando o banco de dados..."

    elapsed=0
    max_wait="${MAX_DB_WAIT_SECONDS:-60}"

    until python - <<'PY'
import os
import sys

import psycopg2

try:
    psycopg2.connect(
        dbname=os.environ["DB_NAME"],
        user=os.environ["DB_USER"],
        password=os.environ["DB_PASSWORD"],
        host=os.environ["DB_HOST"],
        port=os.environ.get("DB_PORT", "5432"),
        connect_timeout=3,
    ).close()
except Exception as exc:
    print(exc, file=sys.stderr)
    sys.exit(1)
PY
    do
        elapsed=$((elapsed + 3))

        if [ "$elapsed" -ge "$max_wait" ]; then
            echo "Banco de dados indisponivel apos ${max_wait}s."
            exit 1
        fi

        sleep 3
    done
}

if [ "${RUN_MIGRATIONS:-true}" = "true" ]; then
    if [ ! -f "migrations/env.py" ]; then
        echo "Pasta migrations invalida ou ausente. Migrations devem estar versionadas no projeto."
        exit 1
    fi

    wait_for_database

    echo "Aplicando migrations..."
    SCHEDULER_ENABLED=false flask db upgrade
fi

if [ "$1" = "flask" ]; then
    export SCHEDULER_ENABLED=false
fi

echo "Inicializando aplicacao..."
exec "$@"
