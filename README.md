# Document Intelligence Connected Container Layout  Sample

This repository is a minimal local setup for running the Azure AI Document Intelligence Layout v4.0 connected container with Docker Compose and calling it from Python.

The project has two moving parts:

- A Docker Compose service that starts `mcr.microsoft.com/azure-cognitive-services/form-recognizer/layout-4.0:latest` on `http://localhost:5000`.
- A Python sample that sends `sample-layout.pdf` to that local container and prints the detected layout content.

## What is in this repo

- `docker-compose.yml`: starts the Layout container and maps the shared and output folders.
- `run-compose.bat`: convenience wrapper around `docker compose`; it also creates `.env` from `.env.example` if needed.
- `sample_analyze_layout.py`: Python client that calls the local container endpoint.
- `sample-layout.pdf`: sample input document.
- `shared/`: host folder mounted into the container as `/share`.
- `output/`: host folder mounted into the container as `/logs` for generated runtime data.

## How this maps to the Microsoft container configuration doc

The official configuration page for Document Intelligence containers says these three settings are required together:

- `Key`
- `Billing`
- `Eula=accept`

This repo provides them through Docker Compose environment variables:

- `apikey: ${FORM_RECOGNIZER_KEY}`
- `billing: ${FORM_RECOGNIZER_ENDPOINT_URI}`
- `eula: accept`

The compose file also sets:

- `Logging:Console:LogLevel:Default: Information`
- `SharedRootFolder: /share`
- `Mounts:Shared: /share`
- `Mounts:Output: /logs`

Those settings align with the Microsoft guidance for connected containers that need billing information, accepted license terms, and writable host mounts.

## Prerequisites

You need the following before you start:

- Docker Desktop running locally.
- An Azure AI Document Intelligence resource.
- The resource endpoint and one API key from the Azure portal.
- Python and `pip`.

Notes:

- This is a connected container. It still runs locally, but it must be configured with a valid Azure endpoint and key for billing.
- On Windows, use absolute paths with forward slashes in `.env`, for example `D:/ProjectDocuments/doc-int-connected-containers/output`.
- If your Docker Desktop installation restricts drive sharing, allow access to the drive that contains this repo.

## 1. Configure the environment file

If `.env` does not exist yet, `run-compose.bat` creates it from `.env.example` and stops so you can fill in the values.

Create or update `.env` in the repo root:

```env
FORM_RECOGNIZER_KEY=<your-document-intelligence-key>
FORM_RECOGNIZER_ENDPOINT_URI=https://<your-resource-name>.cognitiveservices.azure.com/
SHARED_MOUNT_PATH=D:/ProjectDocuments/doc-int-connected-containers/shared
OUTPUT_MOUNT_PATH=D:/ProjectDocuments/doc-int-connected-containers/output
```

What each value does:

- `FORM_RECOGNIZER_KEY`: the Azure resource key used by the container for billing.
- `FORM_RECOGNIZER_ENDPOINT_URI`: the Azure resource endpoint used by the container for billing.
- `SHARED_MOUNT_PATH`: host folder mounted into the container at `/share`.
- `OUTPUT_MOUNT_PATH`: host folder mounted into the container at `/logs`.

## 2. Start the Layout container

From the repo root in PowerShell:

```powershell
.\run-compose.bat
```

By default the script runs:

```powershell
docker compose --file docker-compose.yml --env-file .env up -d
```

If `.env` is missing, the script creates it from `.env.example`, tells you to replace the placeholders, and exits.

Useful variants:

```powershell
.\run-compose.bat ps
.\run-compose.bat logs layout
.\run-compose.bat down
```

The service listens on:

```text
http://localhost:5000
```

## 3. Install the Python dependencies

If you already have a virtual environment, activate it. Otherwise, on Windows:

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install azure-ai-documentintelligence python-dotenv
```

## 4. Run the sample client

Run:

```powershell
python .\sample_analyze_layout.py
```

What the script does:

- Connects to `http://localhost:5000`.
- Reads `sample-layout.pdf`.
- Calls the `prebuilt-layout` model.
- Prints detected lines, selection marks, and table cells.

The sample intentionally uses a placeholder credential string when it creates the SDK client because it is targeting the local container endpoint. The actual Azure billing configuration is supplied when the container starts through Docker Compose.

## Expected result

When everything is configured correctly, you should see output similar to:

```text
Read <n> bytes from sample-layout.pdf
----Analyzing layout from page #1----
...Line #0 has text content '...'
...
----------------------------------------
```

The container also writes runtime artifacts under `output/`.

## Troubleshooting

### The batch script exits after creating `.env`

That is expected the first time. Open `.env`, replace the placeholder values, and run the script again.

### The container does not start

Check:

- Docker Desktop is running.
- The endpoint and key in `.env` are valid and belong to the same Azure resource.
- `SHARED_MOUNT_PATH` and `OUTPUT_MOUNT_PATH` exist and are accessible to Docker.
- Port `5000` is not already in use by another process.

Inspect container output with:

```powershell
.\run-compose.bat logs layout
```

### The Python script fails to connect

Usually this means the container is not running on `localhost:5000`. Verify it with:

```powershell
.\run-compose.bat ps
```

### You are behind an outbound proxy

The Microsoft configuration doc supports `HTTP_PROXY` and `HTTP_PROXY_CREDS` for container outbound calls. If your environment requires a proxy for Azure billing traffic, add the proxy settings to the container configuration before starting it.

### You want structured logs on disk

The Microsoft configuration doc supports disk logging with settings like:

- `Logging:Disk:Format=json`
- `Mounts:Output=<path>`

This repo currently uses console logging only.

## Reference

Official Microsoft documentation used for this setup:

- Configure Document Intelligence containers: https://learn.microsoft.com/en-us/azure/ai-services/document-intelligence/containers/configuration?view=doc-intel-4.0.0

## Quick start

```powershell
Copy-Item .env.example .env
# Edit .env with your Azure endpoint, key, and absolute host paths
.\run-compose.bat
.\venv\Scripts\Activate.ps1
pip install azure-ai-documentintelligence python-dotenv
python .\sample_analyze_layout.py
```