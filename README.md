# AIEmbedded Email MCP

A custom Mail Control Panel (MCP) server for ChatGPT that connects to your IONOS email account (`info@aiembedded.tech`). It exposes a simple HTTP API that allows ChatGPT or other clients to fetch recent emails and save draft replies. This repository contains the FastAPI application, Dockerfile, Fly.io configuration, and supporting files so you can deploy the service quickly.

## Features

- **Fetch recent emails** – Lists the most recent messages from your IONOS inbox (default 5) using IMAP. Returns sender, recipient, subject, and a snippet of the body.
- **Save draft replies** – Takes a destination address, subject and body, and stores the message in your IONOS "Drafts" folder using IMAP. Drafts are available when you open your mailbox.
- **Environment based credentials** – Email address and password are provided via environment variables (`EMAIL` and `PASSWORD`) and are not hard‑coded in the repository.
- **Ready for Fly.io** – Includes a `Dockerfile` and `fly.toml` for deployment to Fly.io.

## Requirements

- Python 3.11
- IONOS email account credentials
- IMAP and SMTP access enabled on your IONOS account

## Setup (Local)

1. Clone the repository and navigate into it.

   ```bash
   git clone https://github.com/Abhinav330/aiembedded-email-mcp.git
   cd aiembedded-email-mcp
   ```

2. Install dependencies.

   ```bash
   pip install -r requirements.txt
   ```

3. Set the required environment variables in your shell.

   ```bash
   export EMAIL=info@aiembedded.tech
   export PASSWORD=your_email_password
   ```

4. Start the server with Uvicorn.

   ```bash
   uvicorn app.main:app --host 0.0.0.0 --port 8080
   ```

## Docker

You can run the service inside a container using the provided `Dockerfile`.

```bash
# Build the image
docker build -t aiembedded-email-mcp .

# Run the container
docker run -e EMAIL=info@aiembedded.tech -e PASSWORD=your_email_password -p 8080:8080 aiembedded-email-mcp
```

## Deployment on Fly.io

1. Install the Fly.io CLI and log in.

   ```bash
   curl -L https://fly.io/install.sh | sh
   fly auth login
   ```

2. Create and configure the app (once).

   ```bash
   fly launch --name aiembedded-email-mcp --no-deploy
   ```

3. Set secrets for your email credentials.

   ```bash
   fly secrets set EMAIL=info@aiembedded.tech PASSWORD=your_email_password
   ```

4. Deploy the application.

   ```bash
   fly deploy
   ```

Once deployed, your API will be available at `https://<your-app-name>.fly.dev`.

## API Endpoints

### `GET /emails`

Fetches the most recent emails from your IONOS inbox.

**Query Parameters:**

- `limit` (optional, default: 5) – The number of messages to return.

**Example:**

```
GET https://<your-app-name>.fly.dev/emails?limit=5
```

### `POST /drafts`

Saves a draft reply in your IONOS account.

**Request body (JSON):**

```json
{
  "to": "recipient@example.com",
  "subject": "Hello",
  "body": "This is a draft reply"
}
```

**Example:**

```
POST https://<your-app-name>.fly.dev/drafts
```

## Contributing

Feel free to open issues or pull requests if you find bugs or have suggestions for improvements.
