#!/bin/bash

# Load environment variables from .env file
if [ -f .env ]; then
    export $(grep -v '^#' .env | xargs)
fi

# Jira credentials are loaded from .env file

# Custom field mappings
export DESCRIPTION_FIELD="customfield_12881"
export ACCEPTANCE_CRITERIA_FIELD="customfield_12819"
export TEST_CASES_FIELD="customfield_11600"

# All configuration values are loaded from .env file

echo "🎯 Jira Test Case Generator"
echo "=========================="
echo ""

# Prompt for JQL query
echo "Enter your JQL query to fetch tickets:"
echo "Examples:"
echo "  - project = \"Product Development Work\" and status = \"Ready for QA\""
echo "  - assignee = currentUser() and status in (\"In Progress\", \"Ready for QA\")"
echo "  - key in (PDW-9468, PDW-9469, PDW-9470)"
echo ""
read -p "JQL Query: " JQL_QUERY

if [ -z "$JQL_QUERY" ]; then
    echo "❌ No JQL query provided. Exiting."
    exit 1
fi

echo ""
echo "🔍 Searching for tickets with JQL: $JQL_QUERY"
echo ""

# Export the JQL query for the Python script
export JQL_QUERY="$JQL_QUERY"

# Run the Python script in preview mode first
export PREVIEW_MODE="true"
python3 jira_ticket_fetcher.py

# Check if the Python script found any tickets
if [ $? -ne 0 ]; then
    echo "❌ Error occurred while fetching tickets. Exiting."
    exit 1
fi

echo ""
read -p "📋 Do you want to proceed with test case generation for these tickets? (y/n): " PROCEED

if [[ $PROCEED =~ ^[Yy]$ ]]; then
    echo ""
    echo "🚀 Starting test case generation..."
    echo ""
    
    # Run the Python script in full mode
    export PREVIEW_MODE="false"
    python3 jira_ticket_fetcher.py
    
    echo ""
    echo "✅ Test case generation completed!"
else
    echo ""
    echo "❌ Test case generation cancelled."
fi