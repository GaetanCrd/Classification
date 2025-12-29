#!/usr/bin/env python3
"""
Get a valid API access token from Label Studio using the refresh token.
"""

import requests
import json

LABEL_STUDIO_URL = "http://localhost:8080"

# Your refresh token from the Account page
REFRESH_TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6ODA2OTY3NTM5NSwiaWF0IjoxNzYyNDc1Mzk1LCJqdGkiOiJmMjQ2MzBjZjVmYzU0NDQwYmIyM2QzNTk5ZTM3Njk1OSIsInVzZXJfaWQiOiIxIn0.hJU3JFGnMokP_hfd9_bffQBInPrn5lrOw7_93x1y3Mw"

print("🔑 Getting API Access Token from Label Studio...")
print()

# Try to get an access token using the refresh token
try:
    response = requests.post(
        f"{LABEL_STUDIO_URL}/api/token/refresh/",
        json={"refresh": REFRESH_TOKEN},
        headers={"Content-Type": "application/json"}
    )
    
    if response.status_code == 200:
        data = response.json()
        access_token = data.get("access")
        
        if access_token:
            print("✅ Success! Your API Access Token is:")
            print()
            print(access_token)
            print()
            print("📝 This token will work for API calls.")
            print("   It expires after some time, so you may need to run this script again.")
            print()
            
            # Save to environment variable suggestion
            print("💡 To use it automatically, run:")
            print(f"   export LABEL_STUDIO_TOKEN='{access_token}'")
            print("   ./start_batch_predictions.sh")
            
            # Save to file
            with open(".label_studio_token", "w") as f:
                f.write(access_token)
            print()
            print("✅ Token saved to .label_studio_token")
            
        else:
            print("❌ No access token in response")
            print(response.text)
    else:
        print(f"❌ Failed to get access token: {response.status_code}")
        print(response.text)
        print()
        print("🔍 Trying alternative: using refresh token directly...")
        print()
        
        # Some Label Studio versions accept the refresh token directly
        test_response = requests.get(
            f"{LABEL_STUDIO_URL}/api/projects/",
            headers={"Authorization": f"Token {REFRESH_TOKEN}"}
        )
        
        if test_response.status_code == 200:
            print("✅ Good news! Your refresh token works as an access token!")
            print(f"   Use: {REFRESH_TOKEN}")
            
            with open(".label_studio_token", "w") as f:
                f.write(REFRESH_TOKEN)
            print()
            print("✅ Token saved to .label_studio_token")
        else:
            print(f"❌ Refresh token also doesn't work: {test_response.status_code}")
            print(test_response.text)

except Exception as e:
    print(f"❌ Error: {e}")
    print()
    print("💡 Manual alternative:")
    print("   1. Open Label Studio in browser: http://localhost:8080")
    print("   2. Open Developer Tools (F12)")
    print("   3. Go to Application → Local Storage → http://localhost:8080")
    print("   4. Look for 'access_token' key")
    print("   5. Copy that value")
