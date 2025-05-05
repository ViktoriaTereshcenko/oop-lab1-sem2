#!/bin/bash

DB_NAME="shop"
DB_USER="vikilinater"
INIT_SQL="init.sql"

DB_EXISTS=$(psql -U $DB_USER -tAc "SELECT 1 FROM pg_database WHERE datname = '$DB_NAME'")

if [ "$DB_EXISTS" = "1" ]; then
  echo "База даних '$DB_NAME' вже існує. Створення пропущено."
else
  echo "Створення бази даних '$DB_NAME'..."
  createdb -U $DB_USER $DB_NAME

  echo "Імпортування структури з '$INIT_SQL'..."
  psql -U $DB_USER -d $DB_NAME -f $INIT_SQL

  echo "База даних '$DB_NAME' успішно створена та ініціалізована."
fi
