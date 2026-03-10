#!/bin/bash
# Helper script to run the IDS detection engine

echo "=========================================="
echo "Network Intrusion Detection System (IDS)"
echo "=========================================="
echo ""

# Check if running as root
if [ "$EUID" -ne 0 ]; then 
    echo "❌ Error: This script must be run with sudo"
    echo ""
    echo "Usage:"
    echo "  sudo ./run_ids.sh"
    echo ""
    exit 1
fi

# Show available network interfaces
echo "📡 Available network interfaces:"
ip -br addr show | grep -v "lo" | awk '{print "   - " $1 " (" $3 ")"}'
echo ""

# Get the configured interface from config
CONFIGURED_INTERFACE=$(grep -A 2 "network:" config.yaml | grep "interface:" | awk '{print $2}' | tr -d '"')
echo "⚙️  Configured interface: $CONFIGURED_INTERFACE"
echo ""

# Ask if user wants to continue
read -p "Press Enter to start IDS on $CONFIGURED_INTERFACE (or Ctrl+C to cancel)... "

echo ""
echo "🚀 Starting IDS Detection Engine..."
echo "   Dashboard: http://localhost:5000"
echo "   Press Ctrl+C to stop"
echo ""
echo "=========================================="
echo ""

# Run the IDS
./venv/bin/python Integration.py
