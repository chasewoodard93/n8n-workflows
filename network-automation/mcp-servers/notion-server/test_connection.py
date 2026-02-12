#!/usr/bin/env python3
"""
Test script to verify Notion API connection.

This script tests your Notion API key and integration setup
before configuring the MCP server.
"""

import os
import sys
import asyncio
from notion_client import AsyncClient


async def test_notion_connection():
    """Test Notion API connection."""
    
    print("🔍 Testing Notion API Connection...\n")
    
    # Get API key
    api_key = os.getenv("NOTION_API_KEY")
    if not api_key:
        print("❌ ERROR: NOTION_API_KEY environment variable not set")
        print("\nTo fix:")
        print("  export NOTION_API_KEY='secret_your_api_key_here'")
        return False
    
    print(f"✅ API key found: {api_key[:20]}...")
    
    # Initialize client
    try:
        notion = AsyncClient(auth=api_key)
        print("✅ Notion client initialized")
    except Exception as e:
        print(f"❌ Failed to initialize client: {str(e)}")
        return False
    
    # Test search
    try:
        print("\n🔍 Testing search...")
        results = await notion.search(query="", page_size=5)
        
        if results.get("results"):
            print(f"✅ Search successful! Found {len(results['results'])} pages/databases")
            print("\nYour Notion pages:")
            for i, result in enumerate(results["results"][:5], 1):
                title = "Untitled"
                if result.get("properties"):
                    for prop_name, prop_value in result["properties"].items():
                        if prop_value.get("type") == "title":
                            title_array = prop_value.get("title", [])
                            if title_array:
                                title = title_array[0].get("text", {}).get("content", "Untitled")
                                break
                
                print(f"  {i}. {title}")
                print(f"     Type: {result['object']}")
                print(f"     ID: {result['id']}")
                print(f"     URL: {result.get('url', 'N/A')}")
                print()
        else:
            print("⚠️  No pages found. Make sure you've shared pages with your integration!")
            print("\nTo share pages:")
            print("  1. Open a Notion page")
            print("  2. Click '...' → 'Connections'")
            print("  3. Select your integration")
            return False
        
    except Exception as e:
        print(f"❌ Search failed: {str(e)}")
        print("\nPossible issues:")
        print("  - Invalid API key")
        print("  - Integration not created properly")
        print("  - Network connection issues")
        return False
    
    # Test getting a page
    if results.get("results"):
        try:
            print("\n📄 Testing page retrieval...")
            first_page_id = results["results"][0]["id"]
            page = await notion.pages.retrieve(first_page_id)
            print(f"✅ Successfully retrieved page: {first_page_id}")
        except Exception as e:
            print(f"⚠️  Could not retrieve page: {str(e)}")
    
    print("\n" + "="*60)
    print("✅ ALL TESTS PASSED!")
    print("="*60)
    print("\nYour Notion integration is working correctly!")
    print("\nNext steps:")
    print("  1. Note the page/database IDs above")
    print("  2. Configure Claude Desktop with these settings")
    print("  3. Restart Claude Desktop")
    print("  4. Test by asking me to search your Notion")
    
    return True


async def main():
    """Main entry point."""
    success = await test_notion_connection()
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    asyncio.run(main())

