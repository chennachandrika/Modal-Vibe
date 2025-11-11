# Setup Guide

After cloning this repository, follow these steps to configure your environment:

## 1. Local Development Setup

### Create `.env` file

1. Copy the example file:
   ```bash
   cp .env.example .env
   ```

2. Edit `.env` and replace the placeholders with your actual Azure OpenAI credentials:
   ```bash
   AZURE_OPENAI_API_KEY=your-actual-azure-openai-api-key
   AZURE_OPENAI_API_BASE=https://your-resource-name.openai.azure.com
   AZURE_OPENAI_API_VERSION=2025-01-01-preview
   AZURE_OPENAI_DEPLOYMENT=gpt-4o
   ```

   **Where to get these values:**
   - `AZURE_OPENAI_API_KEY`: Get from Azure Portal → Your OpenAI Resource → Keys and Endpoint
   - `AZURE_OPENAI_API_BASE`: Your Azure OpenAI endpoint URL (e.g., `https://nw-tech-je.openai.azure.com`)
   - `AZURE_OPENAI_API_VERSION`: Usually `2025-01-01-preview` (check Azure documentation)
   - `AZURE_OPENAI_DEPLOYMENT`: The name of your deployment (e.g., `gpt-4o`)

3. **Important:** The `.env` file is in `.gitignore` and will NOT be committed to git.

## 2. Modal Deployment Setup

For deploying to Modal, you need to create a Modal secret:

### Create Modal Secret

Run this command (replace with your actual values):

```bash
modal secret create anthropic-secret \
  AZURE_OPENAI_API_KEY="your-actual-azure-openai-api-key" \
  AZURE_OPENAI_API_BASE="https://your-resource-name.openai.azure.com" \
  AZURE_OPENAI_API_VERSION="2025-01-01-preview" \
  AZURE_OPENAI_DEPLOYMENT="gpt-4o"
```

**Or use the editor method (more secure):**

```bash
modal secret create anthropic-secret \
  AZURE_OPENAI_API_KEY=- \
  AZURE_OPENAI_API_BASE="https://your-resource-name.openai.azure.com" \
  AZURE_OPENAI_API_VERSION="2025-01-01-preview" \
  AZURE_OPENAI_DEPLOYMENT="gpt-4o"
```

The `-` will open your editor to paste the API key securely.

### Verify Secret

Check that your secret was created:

```bash
modal secret list
```

You should see `anthropic-secret` in the list.

## 3. Deploy

After setting up the Modal secret, deploy the app:

```bash
modal deploy -m main
```

## Summary

- **Local development**: Use `.env` file (not committed to git)
- **Modal deployment**: Use Modal secrets (created via `modal secret create`)
- **Never commit**: `.env` files or API keys to git

