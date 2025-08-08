#!/usr/bin/env python3
"""
Simple test script to verify Jira API update is working
"""

import os
import requests
import json
from base64 import b64encode
from dotenv import load_dotenv

def test_jira_update():
    # Load environment variables from .env file
    load_dotenv()
    
    # Set up authentication
    jira_url = "https://consumeraffairs.atlassian.net"
    email = os.getenv('JIRA_EMAIL')
    api_token = os.getenv('JIRA_API_TOKEN')
    
    if not email or not api_token:
        print("❌ Error: JIRA_EMAIL and JIRA_API_TOKEN must be set in .env file")
        print("Please check your .env file contains:")
        print("JIRA_EMAIL=your-email@consumeraffairs.com")
        print("JIRA_API_TOKEN=your-jira-api-token")
        return
    
    credentials = f"{email}:{api_token}"
    encoded_credentials = b64encode(credentials.encode()).decode()
    auth_header = f"Basic {encoded_credentials}"
    
    issue_key = "PDW-9468"
    test_cases_field = "customfield_11600"
    
    # First, let's read the current field value
    print(f"🔍 Reading current value of {test_cases_field} for {issue_key}...")
    
    read_url = f"{jira_url}/rest/api/3/issue/{issue_key}"
    headers = {
        "Authorization": auth_header,
        "Accept": "application/json"
    }
    
    params = {"fields": test_cases_field}
    response = requests.get(read_url, headers=headers, params=params)
    
    if response.status_code == 200:
        issue_data = response.json()
        current_value = issue_data.get('fields', {}).get(test_cases_field)
        print(f"✅ Current field value exists: {current_value is not None}")
        if current_value:
            print(f"📝 Current content length: {len(str(current_value))} characters")
    else:
        print(f"❌ Error reading field: {response.status_code} - {response.text}")
        return
    
    # Now let's try a simple update with a test message
    print(f"\n🔄 Testing update to {test_cases_field}...")
    
    from datetime import datetime
    test_content = f"TEST UPDATE - {datetime.now()}\n\nThis is a test update to verify the API is working."
    
    # Create ADF content for the update
    adf_content = {
        "type": "doc",
        "version": 1,
        "content": [
            {
                "type": "codeBlock",
                "attrs": {
                    "language": "text"
                },
                "content": [
                    {
                        "type": "text",
                        "text": test_content
                    }
                ]
            }
        ]
    }
    
    update_url = f"{jira_url}/rest/api/3/issue/{issue_key}"
    headers = {
        "Authorization": auth_header,
        "Accept": "application/json",
        "Content-Type": "application/json"
    }
    
    payload = {
        "fields": {
            test_cases_field: adf_content
        }
    }
    
    response = requests.put(update_url, headers=headers, json=payload)
    
    if response.status_code == 204:
        print(f"✅ Update successful! Status code: {response.status_code}")
        print(f"📋 Please check Jira ticket {issue_key} to verify the update appeared")
    else:
        print(f"❌ Update failed! Status code: {response.status_code}")
        print(f"📄 Response: {response.text}")
        
        # Let's also check what fields are actually available for this issue
        print(f"\n🔍 Checking available fields for {issue_key}...")
        all_fields_response = requests.get(f"{jira_url}/rest/api/3/issue/{issue_key}", headers={"Authorization": auth_header})
        if all_fields_response.status_code == 200:
            issue_data = all_fields_response.json()
            available_fields = list(issue_data.get('fields', {}).keys())
            custom_fields = [f for f in available_fields if f.startswith('customfield_')]
            print(f"📋 Available custom fields: {len(custom_fields)}")
            for field in custom_fields[:10]:
                print(f"  - {field}")
            if test_cases_field in available_fields:
                print(f"✅ Target field {test_cases_field} exists in this issue")
            else:
                print(f"❌ Target field {test_cases_field} NOT found in this issue")

if __name__ == "__main__":
    test_jira_update()