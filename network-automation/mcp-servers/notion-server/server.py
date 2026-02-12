#!/usr/bin/env python3
"""
Notion MCP Server - Lightweight server for AI assistant to interact with Notion.

This server provides read/write access to Notion pages, databases, and blocks
for project tracking and context management.
"""

import os
import json
import asyncio
from typing import Any, Dict, List, Optional
from datetime import datetime

from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import (
    Tool,
    TextContent,
    ImageContent,
    EmbeddedResource,
)

# Notion API client
try:
    from notion_client import AsyncClient
except ImportError:
    print("ERROR: notion-client not installed. Run: pip install notion-client")
    exit(1)


class NotionMCPServer:
    """MCP Server for Notion integration."""
    
    def __init__(self):
        """Initialize Notion MCP server."""
        self.notion_token = os.getenv("NOTION_API_KEY")
        if not self.notion_token:
            raise ValueError("NOTION_API_KEY environment variable not set")
        
        self.notion = AsyncClient(auth=self.notion_token)
        self.server = Server("notion-mcp-server")
        
        # Register tools
        self._register_tools()
    
    def _register_tools(self):
        """Register available tools."""
        
        @self.server.list_tools()
        async def list_tools() -> List[Tool]:
            """List available Notion tools."""
            return [
                Tool(
                    name="notion_search",
                    description="Search for pages and databases in Notion workspace",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "query": {
                                "type": "string",
                                "description": "Search query"
                            },
                            "filter": {
                                "type": "string",
                                "enum": ["page", "database"],
                                "description": "Filter by type (optional)"
                            }
                        },
                        "required": ["query"]
                    }
                ),
                Tool(
                    name="notion_get_page",
                    description="Get content of a Notion page by ID",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "page_id": {
                                "type": "string",
                                "description": "Notion page ID"
                            }
                        },
                        "required": ["page_id"]
                    }
                ),
                Tool(
                    name="notion_get_database",
                    description="Query a Notion database and get entries",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "database_id": {
                                "type": "string",
                                "description": "Notion database ID"
                            },
                            "filter": {
                                "type": "object",
                                "description": "Filter criteria (optional)"
                            },
                            "sorts": {
                                "type": "array",
                                "description": "Sort criteria (optional)"
                            }
                        },
                        "required": ["database_id"]
                    }
                ),
                Tool(
                    name="notion_create_page",
                    description="Create a new page in Notion",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "parent_id": {
                                "type": "string",
                                "description": "Parent page or database ID"
                            },
                            "title": {
                                "type": "string",
                                "description": "Page title"
                            },
                            "content": {
                                "type": "string",
                                "description": "Page content in markdown"
                            },
                            "properties": {
                                "type": "object",
                                "description": "Database properties (if parent is database)"
                            }
                        },
                        "required": ["parent_id", "title"]
                    }
                ),
                Tool(
                    name="notion_update_page",
                    description="Update an existing Notion page",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "page_id": {
                                "type": "string",
                                "description": "Page ID to update"
                            },
                            "title": {
                                "type": "string",
                                "description": "New title (optional)"
                            },
                            "content": {
                                "type": "string",
                                "description": "Content to append in markdown (optional)"
                            },
                            "properties": {
                                "type": "object",
                                "description": "Properties to update (optional)"
                            }
                        },
                        "required": ["page_id"]
                    }
                ),
                Tool(
                    name="notion_append_blocks",
                    description="Append content blocks to a Notion page",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "page_id": {
                                "type": "string",
                                "description": "Page ID to append to"
                            },
                            "content": {
                                "type": "string",
                                "description": "Content in markdown format"
                            }
                        },
                        "required": ["page_id", "content"]
                    }
                ),
                Tool(
                    name="notion_get_project_status",
                    description="Get current status of all projects from project tracking database",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "database_id": {
                                "type": "string",
                                "description": "Project tracking database ID"
                            }
                        },
                        "required": ["database_id"]
                    }
                ),
                Tool(
                    name="notion_update_task",
                    description="Update a task status in project tracking",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "page_id": {
                                "type": "string",
                                "description": "Task page ID"
                            },
                            "status": {
                                "type": "string",
                                "description": "New status (e.g., 'In Progress', 'Complete', 'Blocked')"
                            },
                            "notes": {
                                "type": "string",
                                "description": "Additional notes (optional)"
                            }
                        },
                        "required": ["page_id", "status"]
                    }
                )
            ]
        
        @self.server.call_tool()
        async def call_tool(name: str, arguments: Any) -> List[TextContent]:
            """Execute a tool."""
            
            if name == "notion_search":
                return await self._search(arguments)
            elif name == "notion_get_page":
                return await self._get_page(arguments)
            elif name == "notion_get_database":
                return await self._get_database(arguments)
            elif name == "notion_create_page":
                return await self._create_page(arguments)
            elif name == "notion_update_page":
                return await self._update_page(arguments)
            elif name == "notion_append_blocks":
                return await self._append_blocks(arguments)
            elif name == "notion_get_project_status":
                return await self._get_project_status(arguments)
            elif name == "notion_update_task":
                return await self._update_task(arguments)
            else:
                return [TextContent(type="text", text=f"Unknown tool: {name}")]
    
    async def _search(self, args: Dict[str, Any]) -> List[TextContent]:
        """Search Notion workspace."""
        try:
            query = args["query"]
            filter_type = args.get("filter")
            
            search_params = {"query": query}
            if filter_type:
                search_params["filter"] = {"property": "object", "value": filter_type}
            
            results = await self.notion.search(**search_params)
            
            formatted_results = []
            for result in results.get("results", []):
                formatted_results.append({
                    "id": result["id"],
                    "type": result["object"],
                    "title": self._extract_title(result),
                    "url": result.get("url", "")
                })
            
            return [TextContent(
                type="text",
                text=json.dumps(formatted_results, indent=2)
            )]
        
        except Exception as e:
            return [TextContent(type="text", text=f"Error searching Notion: {str(e)}")]
    
    async def _get_page(self, args: Dict[str, Any]) -> List[TextContent]:
        """Get page content."""
        try:
            page_id = args["page_id"].replace("-", "")
            
            # Get page metadata
            page = await self.notion.pages.retrieve(page_id)
            
            # Get page blocks (content)
            blocks = await self.notion.blocks.children.list(page_id)
            
            content = {
                "id": page["id"],
                "title": self._extract_title(page),
                "url": page.get("url", ""),
                "created_time": page.get("created_time", ""),
                "last_edited_time": page.get("last_edited_time", ""),
                "properties": page.get("properties", {}),
                "content": self._blocks_to_markdown(blocks.get("results", []))
            }
            
            return [TextContent(
                type="text",
                text=json.dumps(content, indent=2)
            )]
        
        except Exception as e:
            return [TextContent(type="text", text=f"Error getting page: {str(e)}")]
    
    async def _get_database(self, args: Dict[str, Any]) -> List[TextContent]:
        """Query database."""
        try:
            database_id = args["database_id"].replace("-", "")
            filter_criteria = args.get("filter")
            sorts = args.get("sorts")
            
            query_params = {}
            if filter_criteria:
                query_params["filter"] = filter_criteria
            if sorts:
                query_params["sorts"] = sorts
            
            results = await self.notion.databases.query(database_id, **query_params)
            
            entries = []
            for page in results.get("results", []):
                entries.append({
                    "id": page["id"],
                    "properties": self._format_properties(page.get("properties", {})),
                    "url": page.get("url", ""),
                    "created_time": page.get("created_time", ""),
                    "last_edited_time": page.get("last_edited_time", "")
                })
            
            return [TextContent(
                type="text",
                text=json.dumps(entries, indent=2)
            )]
        
        except Exception as e:
            return [TextContent(type="text", text=f"Error querying database: {str(e)}")]
    
    async def _create_page(self, args: Dict[str, Any]) -> List[TextContent]:
        """Create a new page."""
        try:
            parent_id = args["parent_id"].replace("-", "")
            title = args["title"]
            content = args.get("content", "")
            properties = args.get("properties", {})

            # Create page
            new_page = await self.notion.pages.create(
                parent={"page_id": parent_id} if not properties else {"database_id": parent_id},
                properties={"title": {"title": [{"text": {"content": title}}]}, **properties}
            )

            # Add content if provided
            if content:
                blocks = self._markdown_to_blocks(content)
                await self.notion.blocks.children.append(new_page["id"], children=blocks)

            return [TextContent(
                type="text",
                text=f"Page created successfully!\nID: {new_page['id']}\nURL: {new_page.get('url', '')}"
            )]

        except Exception as e:
            return [TextContent(type="text", text=f"Error creating page: {str(e)}")]

    async def _update_page(self, args: Dict[str, Any]) -> List[TextContent]:
        """Update an existing page."""
        try:
            page_id = args["page_id"].replace("-", "")
            properties = args.get("properties", {})

            if properties:
                await self.notion.pages.update(page_id, properties=properties)

            content = args.get("content")
            if content:
                blocks = self._markdown_to_blocks(content)
                await self.notion.blocks.children.append(page_id, children=blocks)

            return [TextContent(type="text", text="Page updated successfully!")]

        except Exception as e:
            return [TextContent(type="text", text=f"Error updating page: {str(e)}")]

    async def _append_blocks(self, args: Dict[str, Any]) -> List[TextContent]:
        """Append content blocks to a page."""
        try:
            page_id = args["page_id"].replace("-", "")
            content = args["content"]

            blocks = self._markdown_to_blocks(content)
            await self.notion.blocks.children.append(page_id, children=blocks)

            return [TextContent(type="text", text="Content appended successfully!")]

        except Exception as e:
            return [TextContent(type="text", text=f"Error appending content: {str(e)}")]

    async def _get_project_status(self, args: Dict[str, Any]) -> List[TextContent]:
        """Get project status from database."""
        try:
            database_id = args["database_id"].replace("-", "")

            results = await self.notion.databases.query(database_id)

            projects = []
            for page in results.get("results", []):
                props = page.get("properties", {})
                projects.append({
                    "name": self._extract_title(page),
                    "status": self._extract_select(props.get("Status")),
                    "priority": self._extract_select(props.get("Priority")),
                    "assignee": self._extract_people(props.get("Assignee")),
                    "id": page["id"]
                })

            return [TextContent(
                type="text",
                text=json.dumps(projects, indent=2)
            )]

        except Exception as e:
            return [TextContent(type="text", text=f"Error getting project status: {str(e)}")]

    async def _update_task(self, args: Dict[str, Any]) -> List[TextContent]:
        """Update task status."""
        try:
            page_id = args["page_id"].replace("-", "")
            status = args["status"]
            notes = args.get("notes")

            properties = {
                "Status": {"select": {"name": status}}
            }

            await self.notion.pages.update(page_id, properties=properties)

            if notes:
                blocks = self._markdown_to_blocks(f"\n**Update ({datetime.now().strftime('%Y-%m-%d %H:%M')})**\n{notes}")
                await self.notion.blocks.children.append(page_id, children=blocks)

            return [TextContent(type="text", text=f"Task status updated to: {status}")]

        except Exception as e:
            return [TextContent(type="text", text=f"Error updating task: {str(e)}")]

    def _extract_title(self, page: Dict) -> str:
        """Extract title from page object."""
        try:
            properties = page.get("properties", {})
            for prop_name, prop_value in properties.items():
                if prop_value.get("type") == "title":
                    title_array = prop_value.get("title", [])
                    if title_array:
                        return title_array[0].get("text", {}).get("content", "Untitled")
            return "Untitled"
        except:
            return "Untitled"

    def _extract_select(self, prop: Optional[Dict]) -> str:
        """Extract select property value."""
        if not prop:
            return ""
        select = prop.get("select")
        return select.get("name", "") if select else ""

    def _extract_people(self, prop: Optional[Dict]) -> List[str]:
        """Extract people property value."""
        if not prop:
            return []
        people = prop.get("people", [])
        return [person.get("name", "") for person in people]

    def _blocks_to_markdown(self, blocks: List[Dict]) -> str:
        """Convert Notion blocks to markdown."""
        markdown = []
        for block in blocks:
            block_type = block.get("type")
            if block_type == "paragraph":
                text = self._extract_rich_text(block.get("paragraph", {}).get("rich_text", []))
                markdown.append(text)
            elif block_type == "heading_1":
                text = self._extract_rich_text(block.get("heading_1", {}).get("rich_text", []))
                markdown.append(f"# {text}")
            elif block_type == "heading_2":
                text = self._extract_rich_text(block.get("heading_2", {}).get("rich_text", []))
                markdown.append(f"## {text}")
            elif block_type == "heading_3":
                text = self._extract_rich_text(block.get("heading_3", {}).get("rich_text", []))
                markdown.append(f"### {text}")
            elif block_type == "bulleted_list_item":
                text = self._extract_rich_text(block.get("bulleted_list_item", {}).get("rich_text", []))
                markdown.append(f"- {text}")
            elif block_type == "numbered_list_item":
                text = self._extract_rich_text(block.get("numbered_list_item", {}).get("rich_text", []))
                markdown.append(f"1. {text}")
            elif block_type == "code":
                code_block = block.get("code", {})
                text = self._extract_rich_text(code_block.get("rich_text", []))
                language = code_block.get("language", "")
                markdown.append(f"```{language}\n{text}\n```")

        return "\n\n".join(markdown)

    def _extract_rich_text(self, rich_text: List[Dict]) -> str:
        """Extract plain text from rich text array."""
        return "".join([rt.get("text", {}).get("content", "") for rt in rich_text])

    def _markdown_to_blocks(self, markdown: str) -> List[Dict]:
        """Convert markdown to Notion blocks (simplified)."""
        blocks = []
        lines = markdown.split("\n")

        for line in lines:
            line = line.strip()
            if not line:
                continue

            if line.startswith("# "):
                blocks.append({
                    "object": "block",
                    "type": "heading_1",
                    "heading_1": {"rich_text": [{"type": "text", "text": {"content": line[2:]}}]}
                })
            elif line.startswith("## "):
                blocks.append({
                    "object": "block",
                    "type": "heading_2",
                    "heading_2": {"rich_text": [{"type": "text", "text": {"content": line[3:]}}]}
                })
            elif line.startswith("### "):
                blocks.append({
                    "object": "block",
                    "type": "heading_3",
                    "heading_3": {"rich_text": [{"type": "text", "text": {"content": line[4:]}}]}
                })
            elif line.startswith("- ") or line.startswith("* "):
                blocks.append({
                    "object": "block",
                    "type": "bulleted_list_item",
                    "bulleted_list_item": {"rich_text": [{"type": "text", "text": {"content": line[2:]}}]}
                })
            else:
                blocks.append({
                    "object": "block",
                    "type": "paragraph",
                    "paragraph": {"rich_text": [{"type": "text", "text": {"content": line}}]}
                })

        return blocks

    def _format_properties(self, properties: Dict) -> Dict:
        """Format database properties for display."""
        formatted = {}
        for prop_name, prop_value in properties.items():
            prop_type = prop_value.get("type")

            if prop_type == "title":
                formatted[prop_name] = self._extract_rich_text(prop_value.get("title", []))
            elif prop_type == "rich_text":
                formatted[prop_name] = self._extract_rich_text(prop_value.get("rich_text", []))
            elif prop_type == "select":
                formatted[prop_name] = self._extract_select(prop_value)
            elif prop_type == "multi_select":
                multi = prop_value.get("multi_select", [])
                formatted[prop_name] = [item.get("name", "") for item in multi]
            elif prop_type == "date":
                date = prop_value.get("date")
                formatted[prop_name] = date.get("start", "") if date else ""
            elif prop_type == "people":
                formatted[prop_name] = self._extract_people(prop_value)
            elif prop_type == "checkbox":
                formatted[prop_name] = prop_value.get("checkbox", False)
            elif prop_type == "number":
                formatted[prop_name] = prop_value.get("number")
            elif prop_type == "url":
                formatted[prop_name] = prop_value.get("url", "")
            else:
                formatted[prop_name] = str(prop_value)

        return formatted

    async def run(self):
        """Run the MCP server."""
        async with stdio_server() as (read_stream, write_stream):
            await self.server.run(
                read_stream,
                write_stream,
                self.server.create_initialization_options()
            )


async def main():
    """Main entry point."""
    server = NotionMCPServer()
    await server.run()


if __name__ == "__main__":
    asyncio.run(main())

