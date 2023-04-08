#!/bin/bash

# Create
curl http://localhost:8000/graphql \
  -H "Content-Type: multipart/form-data" \
  -F operations='{"query": "mutation ($file: Upload) { createPost (file: $file, category: 1, competition: 1, user: 6) { post { category { name }, competition { name } } } }", "variables": { "file": null }}' \
  -F map='{ "0": ["variables.file"]}' \
  -F 0=@Screenshot1.png

# Update
# curl http://localhost:8000/graphql \
#   -H "Content-Type: multipart/form-data" \
#   -F operations='{"query": "mutation ($file: Upload) { updatePost (id: 1, file: $file) { post { category { name }, competition { name } } } }", "variables": { "file": null }}' \
#   -F map='{ "0": ["variables.file"]}' \
#   -F 0=@work.md


# curl -X POST -H "Content-Type: multipart/form-data" -F operations='{"query": "mutation ($file: Upload) { createPost (file: $file, category: 1, competition: 1, description: 'hello Testing', user: 1) { post { category { name }, competition { name } } } }", "variables": { "file": null } }' -F "map=123" -F "file=requirements.txt" http://localhost:9000/graphql


