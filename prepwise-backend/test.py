import os
import json
import requests
from dotenv import load_dotenv
import time

# Load environment variables
load_dotenv()

# OpenRouter API configuration
API_KEY = os.getenv("GEMINI_API_KEY") or os.getenv("GEMINI_API_KEY") or "GEMINI_API_KEY"
BASE_URL = "https://openrouter.ai/api/v1/chat/completions"
MODEL = "google/gemini-2.0-flash-exp:free"

headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json",
    "HTTP-Referer": "https://prepwise.com",
    "X-Title": "PrepWise Test"
}

def test_simple_text():
    """Test simple text generation"""
    print("\n" + "="*60)
    print("TEST: Simple Text Generation")
    print("="*60)
    
    payload = {
        "model": MODEL,
        "messages": [
            {
                "role": "user",
                "content": "Say hello from Gemini and tell me what you can do in one sentence."
            }
        ]
    }
    
    try:
        print("Sending request to OpenRouter...")
        response = requests.post(BASE_URL, headers=headers, json=payload, timeout=30)
        response.raise_for_status()
        
        data = response.json()
        if data.get("choices") and len(data["choices"]) > 0:
            content = data["choices"][0]["message"]["content"]
            print(f"\n[SUCCESS] Response received:\n")
            print("-" * 60)
            print(content)
            print("-" * 60)
            print(f"\nModel used: {data.get('model', 'N/A')}")
            print(f"Usage: {data.get('usage', {})}")
            return True
        else:
            print("[ERROR] No response content found")
            print(f"Response data: {json.dumps(data, indent=2)}")
            return False
    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 429:
            print(f"[ERROR] Rate limit exceeded (429). Please wait before trying again.")
            print(f"Response: {e.response.text}")
        else:
            print(f"[ERROR] HTTP Error {e.response.status_code}: {e}")
            try:
                error_data = e.response.json()
                print(f"Error details: {json.dumps(error_data, indent=2)}")
            except:
                print(f"Response: {e.response.text}")
        return False
    except requests.exceptions.RequestException as e:
        print(f"[ERROR] Request failed: {e}")
        return False
    except Exception as e:
        print(f"[ERROR] Unexpected error: {e}")
        return False

def main():
    """Run test"""
    print("\n" + "="*60)
    print("OpenRouter API Test")
    print("="*60)
    print(f"Model: {MODEL}")
    print(f"API Key: {API_KEY[:20]}..." if API_KEY else "[ERROR] No API Key found!")
    print("="*60)
    
    if not API_KEY:
        print("\n[ERROR] No API key found!")
        print("Please set GEMINI_API_KEY or OPENROUTER_API_KEY environment variable")
        return
    
    # Run test
    success = test_simple_text()
    
    # Summary
    print("\n" + "="*60)
    if success:
        print("[SUCCESS] Test completed successfully!")
    else:
        print("[FAILED] Test did not complete successfully.")
    print("="*60 + "\n")

if __name__ == "__main__":
    main()
