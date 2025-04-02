#!/usr/bin/env sh

# Run static site generater script
python3 "./src/main.py"

# Run webserver to display the generated html files
if [ $? -eq 0 ];
then
    cd public && python3 -m http.server 8888
else
    echo "Page generation failed"
fi