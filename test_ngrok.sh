#!/bin/bash

echo "Testing ngrok connection..."
echo ""

echo "1. Testing local Flask app:"
curl http://localhost:5002/health
echo ""
echo ""

echo "2. Testing via ngrok:"
curl https://unchokable-unresented-maxwell.ngrok-free.dev/health
echo ""
echo ""

echo "3. Testing webhook endpoint:"
curl https://unchokable-unresented-maxwell.ngrok-free.dev/webhook
echo ""
