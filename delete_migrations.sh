#!/bin/bash

# find all directories named "migrations"
find . -type d -name "migrations" | while read dir; do
  echo "Deleting $dir"
  rm -rf "$dir"

# delete sb.sqlite3
echo "Deleting sb.sqlite3"
rm App/sb.sqlite3

done
