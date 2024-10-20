#!/bin/bash

# CHANGE THE VERSION in .env file first like v2.0.0

# To build production
# To copy the firebase production configuration
# To copy index.html with google tag

if [ "$#" -ne 1 ]; then
    echo "Provide production credential path: /Users/prashanth/projects/selfdive/fyp-prod"
    exit 1  # Exit the script with a non-zero status code
fi

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
FRONTEND_DIR="$SCRIPT_DIR/../frontend"
CRED_DIR=$1

echo "Script Directory - $SCRIPT_DIR"
echo "Cred Directory - $CRED_DIR"
echo "Frontend Directory - $FRONTEND_DIR"

cd $FRONTEND_DIR && mv index.html index.html.bkp
cd $CRED_DIR && cp .env.production index.html $FRONTEND_DIR

# cd $SCRIPT_DIR/.. && docker compose build frontend backend

# cd $FRONTEND_DIR && rm .env.production index.html
# cd $FRONTEND_DIR && mv index.html.bkp index.html

# docker compose push frontend backend