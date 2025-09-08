#!/bin/bash

set -e

echo "🚀 Starting application..."

apply_migrations() {
    echo "🔄 Applying database migrations..."

    if alembic upgrade head; then
        echo "✅ Migrations applied successfully!"
    else
        echo "❌ Failed to apply migrations!"
        exit 1
    fi
}

start_app() {
    echo "🌟 Starting 'Soil Laboratory Application'..."

    # Using the .env variables
    HOST="${APP_HOST:-0.0.0.0}"
    PORT="${APP_PORT:-8000}"

    exec uvicorn src.main:app \
        --host "$HOST" \
        --port "$PORT" \
        --reload \
        --log-level="${LOG_LEVEL:-info}"
}

main() {
    apply_migrations
    start_app
}

main "$@"
