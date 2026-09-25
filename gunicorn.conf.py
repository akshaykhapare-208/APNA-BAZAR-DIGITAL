import os

# Render automatically sets PORT. Default to 5000 if running locally or not set.
port = os.environ.get("PORT", "5000")
bind = f"0.0.0.0:{port}"

# Worker configuration (recommended for Render Free/Starter instance: 2-4 workers)
workers = int(os.environ.get("WEB_CONCURRENCY", "2"))
threads = 4
worker_class = "gthread"
timeout = 120
keepalive = 5

# Logging
accesslog = "-"
errorlog = "-"
loglevel = "info"
