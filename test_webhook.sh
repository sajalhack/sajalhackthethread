#!/bin/bash

echo "Testing webhook endpoints..."
echo ""

echo "1. Testing /health endpoint:"
curl -v https://unchokable-unresented-maxwell.ngrok-free.dev/health
echo ""
echo ""

echo "2. Testing /webhook endpoint (GET):"
curl -v https://unchokable-unresented-maxwell.ngrok-free.dev/webhook
echo ""
echo ""

echo "3. Testing /webhook endpoint (POST):"
curl -v -X POST https://unchokable-unresented-maxwell.ngrok-free.dev/webhook \
  -d "From=whatsapp:+1234567890" \
  -d "Body=test"
echo ""
echo ""

echo "4. Testing local Flask app:"
curl -v http://localhost:5002/health
echo ""
