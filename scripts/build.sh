#!/bin/bash

# To copy the firebase production configuration
# To copy index.html with google tag

cp /Users/prashanth/projects/fyp-prod/.env.production /Users/prashanth/projects/FYP/frontend
cp /Users/prashanth/projects/FYP/frontend/index.html /Users/prashanth/projects/FYP/frontend/index.html.bkp
cp /Users/prashanth/projects/fyp-prod/index.html /Users/prashanth/projects/FYP/frontend

cd /Users/prashanth/projects/FYP && docker compose build

rm /Users/prashanth/projects/FYP/frontend/.env.production  
rm /Users/prashanth/projects/FYP/frontend/index.html
mv /Users/prashanth/projects/FYP/frontend/index.html.bkp /Users/prashanth/projects/FYP/frontend/index.html

# docker compose push frontend backend