#!/bin/bash

# Default values
DEFAULT_LEVEL_MSG="iterative"
DEFAULT_COMMIT_MSG="update"

# Check if the first argument is provided
if [ -z "$1" ]; then
  echo "Usage: $0 <commit_message> [<branch_name>]"
  exit 1
fi

# Set the commit message
DEFAULT_LEVEL=${2:-$DEFAULT_LEVEL_MSG}
COMMIT_MSG=${3:-$DEFAULT_COMMIT_MSG}

# Add all changes
git add .

# Commit changes
git commit -m "$DEFAULT_LEVEL/$COMMIT_MSG"

# Push changes
git push 