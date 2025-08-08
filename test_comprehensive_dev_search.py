#!/usr/bin/env python3
"""
Test the comprehensive development search for PDW-9468
"""

import os
import sys
import json
from dotenv import load_dotenv
from jira_ticket_fetcher import JiraTicketFetcher

def main():
    # Load environment variables from .env file
    load_dotenv()
    
    # Get credentials from environment variables
    jira_url = "https://consumeraffairs.atlassian.net"
    email = os.getenv('JIRA_EMAIL')
    api_token = os.getenv('JIRA_API_TOKEN')
    
    # Validate credentials
    if not email or not api_token:
        print("❌ Error: JIRA_EMAIL and JIRA_API_TOKEN must be set in .env file")
        print("Please check your .env file contains:")
        print("JIRA_EMAIL=your-email@consumeraffairs.com")
        print("JIRA_API_TOKEN=your-jira-api-token")
        sys.exit(1)
    
    # Initialize fetcher
    fetcher = JiraTicketFetcher(jira_url, email, api_token)
    
    # Run comprehensive search on PDW-9468
    issue_key = "PDW-9468"
    print(f"🔍 Running comprehensive development search for {issue_key}")
    print("=" * 80)
    
    dev_info = fetcher.comprehensive_dev_search(issue_key)
    
    print("\n" + "=" * 80)
    print("🎯 SEARCH RESULTS:")
    print("=" * 80)
    
    if dev_info:
        print(f"✅ Found {len(dev_info)} sources of development information:")
        
        for source, data in dev_info.items():
            print(f"\n📋 Source: {source}")
            print("-" * 60)
            
            if isinstance(data, dict):
                print(f"   Type: Dictionary with {len(data)} keys")
                if len(str(data)) < 500:
                    print(f"   Content: {json.dumps(data, indent=2)}")
                else:
                    print(f"   Content (first 500 chars): {str(data)[:500]}...")
            elif isinstance(data, list):
                print(f"   Type: List with {len(data)} items")
                print(f"   Content: {json.dumps(data, indent=2)}")
            else:
                print(f"   Type: {type(data).__name__}")
                print(f"   Content: {str(data)}")
        
        # Save results for inspection
        with open('comprehensive_dev_search_results.json', 'w') as f:
            json.dump(dev_info, f, indent=2, default=str)
        print(f"\n💾 Full results saved to comprehensive_dev_search_results.json")
        
    else:
        print("❌ No development information found through any approach")
    
    print("\n" + "=" * 80)
    print("🏁 Search completed")

if __name__ == "__main__":
    main()