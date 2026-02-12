# 🔗 Notion Integration Guide - Complete Setup

This guide shows you how to connect me (Claude) to your Notion workspace for project tracking and context management.

---

## 🎯 **What You'll Get**

Once connected, I can:

✅ **Read** your project tracking pages and databases  
✅ **Search** for specific projects, tasks, or documentation  
✅ **Update** task statuses and progress  
✅ **Create** new pages and tasks  
✅ **Track** project progress automatically  
✅ **Provide context** from your Notion workspace in our conversations  

---

## 🚀 **Quick Start (Choose Your Path)**

### **Path 1: Super Simple (2 minutes)** ⭐ Start Here

**Best for:** Quick testing, immediate access, read-only

1. Open your Notion project page
2. Click "Share" → "Share to web"
3. Copy the link
4. Paste it in our conversation

**Example:**
```
Here's my project: https://notion.so/AI-Network-Automation-abc123
Can you review the current status?
```

**Pros:** Instant, no setup  
**Cons:** Read-only, manual sharing

---

### **Path 2: Full Integration (15 minutes)** ⭐⭐⭐ Recommended

**Best for:** Long-term use, automatic access, read/write

Follow the detailed setup below.

---

## 📋 **Full Integration Setup**

### **Step 1: Create Notion Integration (5 minutes)**

1. **Go to Notion Integrations:**
   - Visit: https://www.notion.so/my-integrations
   - Click "New integration"

2. **Configure Integration:**
   - **Name:** `AI Assistant MCP`
   - **Associated workspace:** Select your workspace
   - **Type:** Internal integration
   - **Capabilities:** 
     - ✅ Read content
     - ✅ Update content
     - ✅ Insert content
   - Click "Submit"

3. **Copy API Key:**
   - You'll see: `Internal Integration Token`
   - Click "Show" and copy the token
   - It starts with `secret_`
   - **Save this securely!**

---

### **Step 2: Share Pages with Integration (2 minutes)**

For each page/database you want me to access:

1. Open the page in Notion
2. Click "..." (top right corner)
3. Scroll down to "Connections"
4. Click "Add connections"
5. Search for "AI Assistant MCP"
6. Click to connect

**Tip:** Share your main project tracking page - I'll automatically have access to all sub-pages!

---

### **Step 3: Install MCP Server (5 minutes)**

```bash
# Navigate to the MCP server directory
cd /Users/admin/Documents/NetScripts/n8n/mcp-servers/notion-server

# Install dependencies
pip install -r requirements.txt

# Test the connection
export NOTION_API_KEY="secret_your_api_key_here"
python test_connection.py
```

**Expected output:**
```
🔍 Testing Notion API Connection...
✅ API key found: secret_abc123...
✅ Notion client initialized
✅ Search successful! Found 5 pages/databases
✅ ALL TESTS PASSED!
```

If you see errors, check:
- API key is correct
- Pages are shared with integration
- Internet connection is working

---

### **Step 4: Configure Claude Desktop (3 minutes)**

1. **Find your Claude Desktop config file:**
   - **macOS:** `~/Library/Application Support/Claude/claude_desktop_config.json`
   - **Windows:** `%APPDATA%\Claude\claude_desktop_config.json`
   - **Linux:** `~/.config/Claude/claude_desktop_config.json`

2. **Edit the config file:**

```json
{
  "mcpServers": {
    "notion": {
      "command": "python",
      "args": [
        "/Users/admin/Documents/NetScripts/n8n/mcp-servers/notion-server/server.py"
      ],
      "env": {
        "NOTION_API_KEY": "secret_your_actual_api_key_here"
      }
    }
  }
}
```

**Important:** 
- Replace the path with your actual path
- Replace the API key with your actual key
- Use forward slashes (/) even on Windows

3. **Save the file**

---

### **Step 5: Restart Claude Desktop**

1. Completely quit Claude Desktop (Cmd+Q on Mac, Alt+F4 on Windows)
2. Reopen Claude Desktop
3. The MCP server will start automatically

---

### **Step 6: Test the Integration**

In our conversation, try these commands:

```
Can you search my Notion for "AI Network Automation"?
```

```
What's the current status of my projects in Notion?
```

```
Show me all tasks marked as "In Progress" in my Notion database
```

If it works, you'll see me accessing your Notion data! 🎉

---

## 📊 **Recommended Notion Setup for Project Tracking**

### **Create a Project Database**

Create a database in Notion with these properties:

| Property | Type | Options |
|----------|------|---------|
| **Name** | Title | - |
| **Status** | Select | Not Started, In Progress, Complete, Blocked |
| **Priority** | Select | Low, Medium, High, Critical |
| **Type** | Select | Feature, Bug, Task, Documentation |
| **Assignee** | Person | - |
| **Due Date** | Date | - |
| **Notes** | Text | - |

### **Example Database Structure**

| Name | Status | Priority | Type | Notes |
|------|--------|----------|------|-------|
| LabFlow Integration | ✅ Complete | High | Feature | Fixed method calls |
| N8N Workflow Import | 🔄 In Progress | High | Task | Ready to test |
| Production Deployment | ⏸️ Not Started | Medium | Task | Waiting on testing |
| Documentation | 🔄 In Progress | Low | Documentation | Adding examples |

### **Get Database ID**

1. Open your database in Notion
2. Look at the URL: `https://notion.so/workspace/DATABASE_ID?v=...`
3. Copy the `DATABASE_ID` part
4. Remove any hyphens: `abc123def456` → `abc123def456`

---

## 🎯 **Usage Examples**

Once connected, you can ask me:

### **Project Status**
```
What's the current status of all my projects?
```

### **Task Updates**
```
Mark the "LabFlow Integration" task as complete
```

### **Create New Tasks**
```
Create a new task in my project tracker:
- Name: "Test Production Deployment"
- Status: Not Started
- Priority: High
```

### **Search**
```
Find all tasks related to "deployment" in my Notion
```

### **Context**
```
Based on my Notion project tracker, what should I work on next?
```

### **Updates**
```
Add these notes to my "AI Network Automation" project page:
[your notes here]
```

---

## 🔧 **Troubleshooting**

### **"NOTION_API_KEY not set"**

**Problem:** Environment variable not configured  
**Solution:** 
1. Check Claude Desktop config has correct API key
2. Restart Claude Desktop
3. Verify API key is valid in Notion

---

### **"No pages found"**

**Problem:** Pages not shared with integration  
**Solution:**
1. Open Notion page
2. Click "..." → "Connections"
3. Add your integration
4. Try again

---

### **"Integration not working"**

**Problem:** MCP server not starting  
**Solution:**
1. Check Python is installed: `python --version`
2. Check dependencies: `pip list | grep notion`
3. Test manually: `python test_connection.py`
4. Check Claude Desktop logs

---

### **"Permission denied"**

**Problem:** Integration doesn't have access  
**Solution:**
1. Verify integration has correct capabilities
2. Re-share pages with integration
3. Check API key is correct

---

## 🔐 **Security Best Practices**

✅ **Do:**
- Store API key in Claude Desktop config (not in code)
- Only share necessary pages with integration
- Rotate API keys periodically
- Use internal integrations (not public)

❌ **Don't:**
- Share API key in conversations
- Commit API key to Git
- Use public integrations for sensitive data
- Share more pages than needed

---

## 📝 **What Gets Shared**

When you connect me to Notion, I can access:

✅ **Pages** you explicitly share with the integration  
✅ **Sub-pages** of shared pages  
✅ **Databases** you share  
✅ **Database entries** in shared databases  

❌ **I CANNOT access:**
- Pages you haven't shared
- Other workspaces
- Private pages (unless shared)
- Deleted content

---

## 🎉 **You're All Set!**

Once configured, I'll automatically have context from your Notion workspace in every conversation!

**Try it now:**
```
Can you check my Notion and tell me what I should work on next for the AI Network Automation project?
```

---

## 🆘 **Need Help?**

If you run into issues:

1. **Test the connection:**
   ```bash
   cd mcp-servers/notion-server
   export NOTION_API_KEY="your_key"
   python test_connection.py
   ```

2. **Check the logs:**
   - Claude Desktop logs are in the app's console
   - Look for MCP server startup messages

3. **Verify setup:**
   - API key is correct
   - Pages are shared
   - Config file is valid JSON
   - Python dependencies installed

4. **Ask me for help:**
   ```
   I'm having trouble setting up the Notion integration.
   Here's the error I'm seeing: [paste error]
   ```

---

## 🚀 **Next Steps**

After setup:

1. ✅ Share your main project tracking page
2. ✅ Test with a simple search
3. ✅ Try updating a task
4. ✅ Use it in our conversations for context

**The integration will make our collaboration much more effective!** 🎯

