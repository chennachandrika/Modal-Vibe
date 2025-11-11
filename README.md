# Modal Vibe: A scalable AI coding platform

<center>
<video controls playsinline class="w-full aspect-[16/9]" poster="https://modal-cdn.com/blog/videos/modal-vibe-scaleup-poster.png">
<source src="https://modal-cdn.com/blog/videos/modal-vibe-scaleup.mp4" type="video/mp4">
<track kind="captions" />
</video>
</center>

The [Modal Vibe repo](https://github.com/modal-labs/modal-vibe) demonstrates how you can build
a scalable AI coding platform on Modal.

Users of the application can prompt an LLM to create sandboxed applications that service React through a UI.

Each application lives on a [Modal Sandbox](https://modal.com/docs/guide/sandbox)
and contains a webserver accessible through
[Modal Tunnels](https://modal.com/docs/guide/tunnels).

For a high-level overview of Modal Vibe, including performance numbers and why they matter, see
[the accompanying blog post](https://modal.com/blog/modal-vibe).
For details on the implementation, read on.

## How it's structured

![Architecture diagram for Modal Vibe](https://modal-cdn.com/modal-vibe/architecture.png)

- `main.py` is the entrypoint that runs the FastAPI controller that serves the web app and manages the sandbox apps.
- `core` contains the logic for `SandboxApp` model and LLM logic.
- `sandbox` contains a small HTTP server that gets put inside every Sandbox that's created, as well as some sandbox lifecycle management code.
- `web` contains the Modal Vibe website that users see and interact with, as well as the api server that manages Sandboxes.

## How to run

First, set up the local environment:

```bash
python3 -m venv venv && source venv/bin/activate && pip install -r requirements.dev.txt
```

### Deploy

To deploy to Modal:

1. Copy `.env.example` to a file called `.env` and fill in your Azure OpenAI credentials:
   - `AZURE_OPENAI_API_KEY`: Your Azure OpenAI API key
   - `AZURE_OPENAI_API_BASE`: Your Azure OpenAI base URL (e.g., `https://your-resource-name.openai.azure.com`)
   - `AZURE_OPENAI_API_VERSION`: API version (default: `2025-01-01-preview`)
   - `AZURE_OPENAI_DEPLOYMENT`: Deployment name (default: `gpt-4o`)

2. Create a [Modal Secret](https://modal.com/docs/guide/secrets) called `anthropic-secret` with all the Azure OpenAI environment variables:
   ```bash
   modal secret create anthropic-secret \
     AZURE_OPENAI_API_KEY="your-key" \
     AZURE_OPENAI_API_BASE="https://your-resource.openai.azure.com" \
     AZURE_OPENAI_API_VERSION="2025-01-01-preview" \
     AZURE_OPENAI_DEPLOYMENT="gpt-4o"
   ```

Then, deploy the application with Modal:

```bash
python3 -m modal deploy -m main
```

### Local Development

**Run the app locally:**

```bash
python3 -m modal serve -m main
```

or

```bash
python3 -m modal serve main.py
```

This will start the FastAPI app locally and provide a URL to access it. Make sure you have:
1. Created the `.env` file with your Azure OpenAI credentials
2. Created the Modal secret `anthropic-secret` with your Azure OpenAI credentials

**Other development commands:**

Run a load test:

```bash
python3 -m modal run main.py::create_app_loadtest_function --num-apps 10
```

Delete a sandbox:

```bash
python3 -m modal run main.py::delete_sandbox_admin_function --app-id <APP_ID>
```

Run an example sandbox HTTP server:

```bash
python -m sandbox.server
```
