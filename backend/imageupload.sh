#!/bin/bash

curl http://localhost:9000/graphql \
  -H "Content-Type: multipart/form-data" \
  -F operations='{"query": "mutation ($file: Upload) { createPost (file: $file, category: 1, competition: 1, user: 1) { post { category { name }, competition { name } } } }", "variables": { "file": null }}' \
  -F map='{ "0": ["variables.file"]}' \
  -F 0=@requirements.txt


# curl -X POST -H "Content-Type: multipart/form-data" -F operations='{"query": "mutation ($file: Upload) { createPost (file: $file, category: 1, competition: 1, description: 'hello Testing', user: 1) { post { category { name }, competition { name } } } }", "variables": { "file": null } }' -F "map=123" -F "file=requirements.txt" http://localhost:9000/graphql


