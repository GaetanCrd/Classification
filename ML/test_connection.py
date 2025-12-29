#!/usr/bin/env python3
"""
Quick helper to test the batch prediction setup
"""

import requests

print("🔍 Testing Label Studio Connection")
print("=" * 60)

# Test Label Studio
try:
    response = requests.get("http://localhost:8080/api/projects", timeout=5)
    if response.status_code == 401:
        print("✅ Label Studio is running")
        print("⚠️  But you need an API token to access it")
        print()
        print("📝 How to get your API token:")
        print("   1. Go to: http://localhost:8080")
        print("   2. Click on your account icon (top right)")
        print("   3. Click 'Account & Settings'")
        print("   4. Copy the 'Access Token'")
        print()
        print("Then run:")
        print("   export LABEL_STUDIO_TOKEN='paste-your-token-here'")
        print("   python3 generate_predictions_batch.py")
    elif response.status_code == 200:
        print("✅ Label Studio is running and accessible!")
    else:
        print(f"⚠️  Label Studio returned status: {response.status_code}")
except Exception as e:
    print(f"❌ Cannot connect to Label Studio: {e}")
    print("   Make sure it's running: ./start_label_studio.sh")

print()

# Test ML Backend
try:
    response = requests.get("http://localhost:9090/health", timeout=5)
    if response.status_code == 200:
        data = response.json()
        print("✅ ML Backend is running and healthy")
        print(f"   Status: {data.get('status')}")
        print(f"   Model dir: {data.get('model_dir')}")
    else:
        print(f"⚠️  ML Backend returned status: {response.status_code}")
except Exception as e:
    print(f"❌ Cannot connect to ML Backend: {e}")
    print("   Make sure it's running:")
    print("   cd custom_ml_backend && ../.venv/bin/python _wsgi.py &")

print()
print("=" * 60)
