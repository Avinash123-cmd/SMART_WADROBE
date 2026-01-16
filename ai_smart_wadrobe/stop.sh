#!/bin/bash

echo "🛑 Stopping AI Smart Wardrobe services..."

docker-compose down

echo "✅ Services stopped"
echo ""
echo "🚀 To restart:"
echo "   ./setup.sh"