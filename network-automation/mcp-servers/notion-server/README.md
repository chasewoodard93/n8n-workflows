# 🔗 Notion MCP Server

Lightweight MCP server for AI assistant to interact with your Notion workspace for project tracking and context management.

## 🎯 Features

- ✅ **Search** Notion pages and databases
- ✅ **Read** page content and database entries
- ✅ **Create** new pages and database entries
- ✅ **Update** existing pages and tasks
- ✅ **Track** project status and progress
- ✅ **Append** content to existing pages

## 🚀 Quick Setup

### 1. Get Notion API Key

1. Go to: https://www.notion.so/my-integrations
2. Click "New integration"
3. Name: "AI Assistant MCP"
4. Select your workspace
5. Click "Submit"
6. **Copy the Internal Integration Token**

### 2. Share Pages with Integration

1. Open your Notion project page
2. Click "..." (top right) → "Connections"
3. Search for "AI Assistant MCP"
4. Click to connect

### 3. Install Dependencies

```bash
cd mcp-servers/notion-server
pip install -r requirements.txt
```

### 4. Configure Environment

```bash
export NOTION_API_KEY="secret_your_notion_api_key_here"
```

### 5. Add to Claude Desktop Config

Edit your Claude Desktop config file:

**macOS:** `~/Library/Application Support/Claude/claude_desktop_config.json`
**Windows:** `%APPDATA%\Claude\claude_desktop_config.json`

Add this configuration:

```json
{
  "mcpServers": {
    "notion": {
      "command": "python",
      "args": [
        "/Users/admin/Documents/NetScripts/n8n/mcp-servers/notion-server/server.py"
      ],
      "env": {
        "NOTION_API_KEY": "secret_your_notion_api_key_here"
      }
    }
  }
}
```

### 6. Restart Claude Desktop

Close and reopen Claude Desktop. The Notion MCP server will be available.

## 📖 Usage Examples

### Search for Pages

```
Can you search my Notion for "AI Network Automation" project?
```

### Get Project Status

```
What's the current status of all my projects in Notion?
```

### Update Task Status

```
Mark the "LabFlow Integration" task as complete in Notion
```

### Create New Page

```
Create a new page in my Notion project tracker for "Production Deployment"
```

### Append Content

```
Add these deployment notes to my Notion project page
```

## 🔧 Available Tools

1. **notion_search** - Search workspace
2. **notion_get_page** - Get page content
3. **notion_get_database** - Query database
4. **notion_create_page** - Create new page
5. **notion_update_page** - Update page
6. **notion_append_blocks** - Append content
7. **notion_get_project_status** - Get all project statuses
8. **notion_update_task** - Update task status

## 📊 Project Tracking Setup

### Recommended Notion Database Structure

Create a database in Notion with these properties:

- **Name** (Title) - Project/Task name
- **Status** (Select) - Not Started, In Progress, Complete, Blocked
- **Priority** (Select) - Low, Medium, High, Critical
- **Type** (Select) - Feature, Bug, Task, Documentation
- **Assignee** (Person) - Who's working on it
- **Due Date** (Date) - When it's due
- **Notes** (Text) - Additional context

### Example Database

| Name | Status | Priority | Type | Notes |
|------|--------|----------|------|-------|
| LabFlow Integration | Complete | High | Feature | Fixed method calls |
| N8N Workflow Import | In Progress | High | Task | Ready to test |
| Production Deployment | Not Started | Medium | Task | Waiting on testing |

## 🔐 Security

- API key stored in environment variable
- Only accesses pages you explicitly share with the integration
- No data stored locally
- All communication over HTTPS

## 🆘 Troubleshooting

### "NOTION_API_KEY not set"
- Make sure you've set the environment variable in Claude Desktop config
- Restart Claude Desktop after changing config

### "Page not found"
- Ensure you've shared the page with your integration
- Check the page ID is correct (remove hyphens)

### "Integration not working"
- Verify integration is created in Notion
- Check API key is valid
- Ensure pages are shared with integration

## 📝 Notes

- Page IDs can be found in the URL: `notion.so/Page-Name-{PAGE_ID}`
- Database IDs are similar: `notion.so/{DATABASE_ID}?v=...`
- Remove hyphens from IDs when using in API calls

