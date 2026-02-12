#!/usr/bin/env python3
"""
GitHub Integration for AI Learning Loop.

Handles automatic commits of successful automation workflows.
"""

import asyncio
import base64
import json
from typing import Dict, List, Any, Optional
from datetime import datetime
import logging

import httpx

logger = logging.getLogger(__name__)


class GitHubManager:
    """
    Manages GitHub repository operations for automated commits.
    """
    
    def __init__(self, token: str, username: str, repo: str, base_url: str = "https://api.github.com"):
        """Initialize GitHub manager."""
        self.token = token
        self.username = username
        self.repo = repo
        self.base_url = base_url
        self.client = httpx.AsyncClient(timeout=30.0)
        
        self.headers = {
            "Authorization": f"token {token}",
            "Accept": "application/vnd.github.v3+json",
            "User-Agent": "AI-Learning-Loop/1.0"
        }
        
        logger.info(f"GitHub manager initialized for {username}/{repo}")
    
    async def commit_files(
        self,
        files: Dict[str, str],
        commit_message: str,
        branch: str = "main",
        create_branch: bool = True
    ) -> Dict[str, Any]:
        """
        Commit multiple files to GitHub repository.
        
        Args:
            files: Dictionary of file_path: content
            commit_message: Commit message
            branch: Target branch name
            create_branch: Whether to create branch if it doesn't exist
            
        Returns:
            Commit result information
        """
        try:
            logger.info(f"Committing {len(files)} files to {self.username}/{self.repo}:{branch}")
            
            # Get repository information
            repo_info = await self._get_repository_info()
            if not repo_info["success"]:
                return repo_info
            
            # Get or create branch
            branch_info = await self._get_or_create_branch(branch, create_branch)
            if not branch_info["success"]:
                return branch_info
            
            # Get current tree SHA
            current_sha = branch_info["sha"]
            
            # Create blobs for all files
            blob_results = await self._create_blobs(files)
            if not blob_results["success"]:
                return blob_results
            
            # Create new tree
            tree_result = await self._create_tree(blob_results["blobs"], current_sha)
            if not tree_result["success"]:
                return tree_result
            
            # Create commit
            commit_result = await self._create_commit(
                tree_sha=tree_result["sha"],
                parent_sha=current_sha,
                message=commit_message
            )
            
            if not commit_result["success"]:
                return commit_result
            
            # Update branch reference
            update_result = await self._update_branch_reference(branch, commit_result["sha"])
            if not update_result["success"]:
                return update_result
            
            logger.info(f"Successfully committed files to {branch}")
            
            return {
                "success": True,
                "commit_sha": commit_result["sha"],
                "commit_url": commit_result["url"],
                "branch": branch,
                "files_committed": len(files),
                "repository_url": f"https://github.com/{self.username}/{self.repo}"
            }
        
        except Exception as e:
            logger.error(f"Failed to commit files: {str(e)}")
            return {
                "success": False,
                "error": str(e)
            }
    
    async def _get_repository_info(self) -> Dict[str, Any]:
        """Get repository information."""
        try:
            url = f"{self.base_url}/repos/{self.username}/{self.repo}"
            response = await self.client.get(url, headers=self.headers)
            
            if response.status_code == 200:
                repo_data = response.json()
                return {
                    "success": True,
                    "name": repo_data["name"],
                    "full_name": repo_data["full_name"],
                    "default_branch": repo_data["default_branch"]
                }
            else:
                return {
                    "success": False,
                    "error": f"Repository not found or access denied: {response.status_code}"
                }
        
        except Exception as e:
            return {
                "success": False,
                "error": f"Failed to get repository info: {str(e)}"
            }
    
    async def _get_or_create_branch(self, branch: str, create_if_missing: bool = True) -> Dict[str, Any]:
        """Get branch information or create if it doesn't exist."""
        try:
            # Try to get existing branch
            url = f"{self.base_url}/repos/{self.username}/{self.repo}/git/refs/heads/{branch}"
            response = await self.client.get(url, headers=self.headers)
            
            if response.status_code == 200:
                ref_data = response.json()
                return {
                    "success": True,
                    "sha": ref_data["object"]["sha"],
                    "ref": ref_data["ref"]
                }
            
            elif response.status_code == 404 and create_if_missing:
                # Branch doesn't exist, create it from main/master
                return await self._create_branch_from_main(branch)
            
            else:
                return {
                    "success": False,
                    "error": f"Branch {branch} not found and creation not requested"
                }
        
        except Exception as e:
            return {
                "success": False,
                "error": f"Failed to get/create branch: {str(e)}"
            }
    
    async def _create_branch_from_main(self, branch: str) -> Dict[str, Any]:
        """Create new branch from main/master."""
        try:
            # Get main branch SHA
            for main_branch in ["main", "master"]:
                url = f"{self.base_url}/repos/{self.username}/{self.repo}/git/refs/heads/{main_branch}"
                response = await self.client.get(url, headers=self.headers)
                
                if response.status_code == 200:
                    main_data = response.json()
                    main_sha = main_data["object"]["sha"]
                    
                    # Create new branch
                    create_url = f"{self.base_url}/repos/{self.username}/{self.repo}/git/refs"
                    create_data = {
                        "ref": f"refs/heads/{branch}",
                        "sha": main_sha
                    }
                    
                    create_response = await self.client.post(
                        create_url,
                        headers=self.headers,
                        json=create_data
                    )
                    
                    if create_response.status_code == 201:
                        logger.info(f"Created branch {branch} from {main_branch}")
                        return {
                            "success": True,
                            "sha": main_sha,
                            "ref": f"refs/heads/{branch}"
                        }
            
            return {
                "success": False,
                "error": "Could not find main or master branch to create from"
            }
        
        except Exception as e:
            return {
                "success": False,
                "error": f"Failed to create branch: {str(e)}"
            }
    
    async def _create_blobs(self, files: Dict[str, str]) -> Dict[str, Any]:
        """Create blobs for all files."""
        try:
            blobs = {}
            
            for file_path, content in files.items():
                # Encode content as base64
                content_bytes = content.encode('utf-8')
                content_b64 = base64.b64encode(content_bytes).decode('utf-8')
                
                # Create blob
                url = f"{self.base_url}/repos/{self.username}/{self.repo}/git/blobs"
                blob_data = {
                    "content": content_b64,
                    "encoding": "base64"
                }
                
                response = await self.client.post(url, headers=self.headers, json=blob_data)
                
                if response.status_code == 201:
                    blob_info = response.json()
                    blobs[file_path] = {
                        "sha": blob_info["sha"],
                        "content": content
                    }
                else:
                    return {
                        "success": False,
                        "error": f"Failed to create blob for {file_path}: {response.status_code}"
                    }
            
            return {
                "success": True,
                "blobs": blobs
            }
        
        except Exception as e:
            return {
                "success": False,
                "error": f"Failed to create blobs: {str(e)}"
            }
    
    async def _create_tree(self, blobs: Dict[str, Dict[str, str]], base_tree_sha: str) -> Dict[str, Any]:
        """Create new tree with all files."""
        try:
            tree_items = []
            
            for file_path, blob_info in blobs.items():
                tree_items.append({
                    "path": file_path,
                    "mode": "100644",  # Regular file
                    "type": "blob",
                    "sha": blob_info["sha"]
                })
            
            url = f"{self.base_url}/repos/{self.username}/{self.repo}/git/trees"
            tree_data = {
                "base_tree": base_tree_sha,
                "tree": tree_items
            }
            
            response = await self.client.post(url, headers=self.headers, json=tree_data)
            
            if response.status_code == 201:
                tree_info = response.json()
                return {
                    "success": True,
                    "sha": tree_info["sha"]
                }
            else:
                return {
                    "success": False,
                    "error": f"Failed to create tree: {response.status_code}"
                }
        
        except Exception as e:
            return {
                "success": False,
                "error": f"Failed to create tree: {str(e)}"
            }
    
    async def _create_commit(self, tree_sha: str, parent_sha: str, message: str) -> Dict[str, Any]:
        """Create new commit."""
        try:
            url = f"{self.base_url}/repos/{self.username}/{self.repo}/git/commits"
            commit_data = {
                "message": message,
                "tree": tree_sha,
                "parents": [parent_sha],
                "author": {
                    "name": "AI Learning Loop",
                    "email": "ai-learning-loop@automation.local",
                    "date": datetime.utcnow().isoformat() + "Z"
                },
                "committer": {
                    "name": "AI Learning Loop",
                    "email": "ai-learning-loop@automation.local", 
                    "date": datetime.utcnow().isoformat() + "Z"
                }
            }
            
            response = await self.client.post(url, headers=self.headers, json=commit_data)
            
            if response.status_code == 201:
                commit_info = response.json()
                return {
                    "success": True,
                    "sha": commit_info["sha"],
                    "url": commit_info["html_url"]
                }
            else:
                return {
                    "success": False,
                    "error": f"Failed to create commit: {response.status_code}"
                }
        
        except Exception as e:
            return {
                "success": False,
                "error": f"Failed to create commit: {str(e)}"
            }
    
    async def _update_branch_reference(self, branch: str, commit_sha: str) -> Dict[str, Any]:
        """Update branch reference to point to new commit."""
        try:
            url = f"{self.base_url}/repos/{self.username}/{self.repo}/git/refs/heads/{branch}"
            update_data = {
                "sha": commit_sha,
                "force": False
            }
            
            response = await self.client.patch(url, headers=self.headers, json=update_data)
            
            if response.status_code == 200:
                return {"success": True}
            else:
                return {
                    "success": False,
                    "error": f"Failed to update branch reference: {response.status_code}"
                }
        
        except Exception as e:
            return {
                "success": False,
                "error": f"Failed to update branch reference: {str(e)}"
            }
    
    async def close(self):
        """Close the HTTP client."""
        await self.client.aclose()
