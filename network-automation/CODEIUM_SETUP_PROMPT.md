# 🤖 Codeium/AI Assistant Setup Prompt

**Copy and paste this entire prompt into Codeium or your AI coding assistant to get step-by-step help setting up the N8N AI workflow generator.**

---

## **DETAILED SETUP PROMPT FOR AI ASSISTANT**

```
I need help setting up an AI-powered network automation workflow generator using N8N 
and Anthropic's Claude API. Here's what I need to accomplish:

GOAL: Get a fully functional N8N workflow that generates network automation workflows 
using AI agents, with the form accessible and tested end-to-end.

ENVIRONMENT:
- OS: [macOS/Windows/Linux]
- Docker: Installed and running
- Anthropic API Key: Available (from https://console.anthropic.com/)
- Repository: https://github.com/chasewoodard93/n8n-network-automation.git

TASKS (in order):

### TASK 1: Start N8N with Docker
I need to:
1. Create a directory for N8N data persistence
2. Start N8N container with proper volume mounting
3. Verify the container is running
4. Access N8N at http://localhost:5678

Please provide:
- Exact Docker command to run
- How to verify it's running (docker ps command)
- How to check logs if it fails (docker logs command)
- Expected output when successful
- Troubleshooting steps if port 5678 is already in use

### TASK 2: Initial N8N Setup
Once N8N is running, I need to:
1. Access the web interface at http://localhost:5678
2. Complete the initial setup wizard
3. Create an admin account
4. Verify the dashboard loads

Please provide:
- Step-by-step instructions for the setup wizard
- What credentials to use
- Screenshots description of what I should see
- How to verify setup is complete

### TASK 3: Import the Workflow File
I need to:
1. Download/locate the network_stack_generator.json file from the repository
2. Import it into N8N
3. Verify all nodes are present
4. Check for any import errors

Please provide:
- Exact steps to import (menu navigation)
- How to verify the import was successful
- What nodes should be present (list them)
- How to fix import errors if they occur

### TASK 4: Configure Anthropic API Credentials
I need to:
1. Locate the three AI Agent nodes in the workflow
2. Add my Anthropic API key to each node
3. Verify the credentials are saved
4. Test the API connection

Please provide:
- Which nodes need the API key (exact node names)
- How to add credentials in N8N (step-by-step)
- How to test the API connection
- Error messages and what they mean
- How to verify credentials are working

### TASK 5: Activate the Workflow
I need to:
1. Activate the workflow
2. Get the form URL
3. Verify the workflow is listening for submissions
4. Check the logs for any errors

Please provide:
- How to activate the workflow (button location)
- Where to find the form URL
- How to verify it's active (logs, status indicators)
- What the form URL should look like
- How to test the form is accessible

### TASK 6: Test End-to-End with Sample Data
I need to:
1. Access the form URL
2. Fill it with sample network device data
3. Submit the form
4. Monitor the workflow execution
5. Verify AI agents are generating content
6. Check for generated files/output

Please provide:
- Sample data to use in the form:
  * Project name
  * Company name
  * Network devices (5 Cisco switches)
  * Workflows to generate (Backup, Deploy)
  * Integrations (NetBox, Git)
  * Email address
- Step-by-step form filling instructions
- How to monitor workflow execution in N8N
- What to look for in the logs
- Expected output (workflows, tests, etc.)
- How long it should take
- Success indicators

### TASK 7: Verify AI Agents Are Working
I need to:
1. Check that AI Agent 1 generated a workflow YAML
2. Check that AI Agent 2 generated tests
3. Check that AI Agent 3 validated everything
4. Verify no errors occurred

Please provide:
- Where to find the generated files
- How to view the generated workflow YAML
- How to view the generated tests
- How to check the validation results
- What success looks like for each agent
- Common errors and how to fix them

### TASK 8: Troubleshooting Guide
Please provide solutions for:
1. N8N container won't start
2. Port 5678 already in use
3. Can't access http://localhost:5678
4. Import fails with error
5. Anthropic API key not working
6. Workflow won't activate
7. Form submission fails
8. AI agents not generating content
9. Generated files not appearing
10. Email notification not sending

For each issue, provide:
- Root cause
- Step-by-step fix
- How to verify it's fixed
- Prevention tips

### TASK 9: Success Verification Checklist
Please provide a checklist to verify everything is working:
- [ ] N8N running (docker ps shows container)
- [ ] Web interface accessible (http://localhost:5678)
- [ ] Workflow imported (all nodes visible)
- [ ] API credentials configured (test connection passes)
- [ ] Workflow activated (status shows "active")
- [ ] Form URL accessible (can open in browser)
- [ ] Form submission works (no errors)
- [ ] AI agents generating (files created)
- [ ] Output files present (workflows, tests)
- [ ] Email notification received

### TASK 10: Next Steps
After successful setup, please provide:
1. How to generate additional workflows
2. How to customize the generated workflows
3. How to run the generated workflows with NornFlow
4. How to schedule automated workflow generation
5. How to integrate with real network devices

IMPORTANT NOTES:
- I'm starting from scratch with N8N
- I have basic Docker knowledge
- I want detailed, step-by-step instructions
- Include exact commands and expected outputs
- Explain what each step does and why
- Provide troubleshooting for common issues
- Use clear, beginner-friendly language
- Include verification steps after each task
```

---

## **HOW TO USE THIS PROMPT**

### **Option 1: Codeium in VS Code**
1. Open VS Code
2. Press `Ctrl+Shift+A` (or `Cmd+Shift+A` on Mac)
3. Paste the prompt above
4. Press Enter
5. Codeium will provide step-by-step instructions

### **Option 2: ChatGPT/Claude Web Interface**
1. Go to https://chat.openai.com or https://claude.ai
2. Paste the prompt
3. Click Send
4. Follow the detailed instructions provided

### **Option 3: GitHub Copilot Chat**
1. Open VS Code
2. Click the Copilot Chat icon
3. Paste the prompt
4. Press Enter
5. Follow the instructions

### **Option 4: Codeium Chat (Standalone)**
1. Go to https://codeium.com/chat
2. Paste the prompt
3. Click Send
4. Follow the instructions

---

## **WHAT YOU'LL GET**

The AI assistant will provide:

✅ **Exact Docker commands** to run  
✅ **Step-by-step setup instructions** with screenshots descriptions  
✅ **Configuration details** for each component  
✅ **Verification commands** to check each step  
✅ **Troubleshooting guide** for common issues  
✅ **Sample data** to test with  
✅ **Success checklist** to verify everything works  
✅ **Next steps** for production use  

---

## **EXPECTED TIMELINE**

- **Task 1 (Start N8N):** 5 minutes
- **Task 2 (Initial Setup):** 5 minutes
- **Task 3 (Import Workflow):** 5 minutes
- **Task 4 (Configure API):** 10 minutes
- **Task 5 (Activate):** 5 minutes
- **Task 6 (Test):** 10 minutes
- **Task 7 (Verify):** 5 minutes
- **Total:** ~45 minutes

---

## **TIPS FOR BEST RESULTS**

1. **Copy the entire prompt** - Don't modify it
2. **Provide your OS** - Tell the AI your operating system
3. **Have API key ready** - Get it before starting
4. **Follow step-by-step** - Don't skip steps
5. **Ask for clarification** - If anything is unclear
6. **Save the output** - Copy the AI's response to a file
7. **Follow verification steps** - After each task
8. **Report errors** - If something fails, share the error message

---

## **ALTERNATIVE: QUICK SETUP PROMPT**

If you want a shorter, faster version:

```
Help me set up N8N with the network_stack_generator.json workflow in 15 minutes.

I have:
- Docker installed
- Anthropic API key
- The repository cloned

I need:
1. Docker command to start N8N
2. How to import the workflow file
3. How to add API credentials
4. How to activate and test

Provide exact commands and expected outputs only.
```

---

**Ready to get started? Use the prompt above with your AI assistant!** 🚀

