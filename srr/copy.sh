#!/bin/bash

# All this script dose is copys the .so files to 
# ../App/StreamStage

# -- This is the path to the .so files
so_path=./target/release/libsrr.so
app_path=../App/srr/srr.so

# -- Check if both paths exist
if [ ! -f $so_path ]; then
    echo "Error: $so_path does not exist"
    exit 1
fi

# -- Copy the .so files to the app
cp $so_path $app_path
echo "Copied .so files to $app_path"