#!/bin/sh
set -e

echo "🟡 Starting Ollama server..."
/bin/ollama serve &
pid=$!

echo "⏳ Waiting for Ollama to initialize..."
sleep 5

MODEL="qwen2.5"

# Check if model exists
if ollama list | grep -q "^${MODEL}\b"; then
  echo "✅ $MODEL already present, skipping pull"
else
  echo "🔴 Pulling $MODEL..."
  ollama pull $MODEL
  echo "🟢 $MODEL downloaded successfully!"
fi

echo "✅ Ollama is ready and serving"
wait $pid
