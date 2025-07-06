#!/usr/bin/env python3
"""
Test script to verify that GitHub Secrets are properly loaded
"""
import os
import sys

def test_secrets():
    """Test if all required secrets are available"""
    print("🔍 Testing GitHub Secrets...")
    
    # Check each secret
    secrets = {
        'ANTHROPIC_API_KEY': os.getenv('ANTHROPIC_API_KEY'),
        'FAL_KEY': os.getenv('FAL_KEY'),
        'GOOGLE_APPLICATION_CREDENTIALS': os.getenv('GOOGLE_APPLICATION_CREDENTIALS'),
        'GOOGLE_APPLICATION_CREDENTIALS_JSON': os.getenv('GOOGLE_APPLICATION_CREDENTIALS_JSON')
    }
    
    print("\n📋 Secret Status:")
    missing_secrets = []
    
    for name, value in secrets.items():
        if value:
            # Show first 10 characters only for security
            masked_value = value[:10] + "..." if len(value) > 10 else value
            print(f"  ✅ {name}: {masked_value}")
        else:
            print(f"  ❌ {name}: NOT SET")
            missing_secrets.append(name)
    
    if missing_secrets:
        print(f"\n❌ Missing secrets: {', '.join(missing_secrets)}")
        return False
    else:
        print("\n✅ All secrets are properly configured!")
        return True

def test_google_credentials():
    """Test Google Cloud credentials setup"""
    print("\n🔍 Testing Google Cloud credentials...")
    
    creds_file = os.getenv('GOOGLE_APPLICATION_CREDENTIALS')
    creds_json = os.getenv('GOOGLE_APPLICATION_CREDENTIALS_JSON')
    
    if creds_file:
        if os.path.exists(creds_file):
            print(f"  ✅ Credentials file exists: {creds_file}")
            # Try to read the file
            try:
                with open(creds_file, 'r') as f:
                    content = f.read()
                    if content and 'type' in content:
                        print("  ✅ Credentials file contains valid JSON")
                        return True
                    else:
                        print("  ❌ Credentials file appears to be empty or invalid")
                        return False
            except Exception as e:
                print(f"  ❌ Error reading credentials file: {e}")
                return False
        else:
            print(f"  ❌ Credentials file does not exist: {creds_file}")
            return False
    elif creds_json:
        print("  ✅ JSON credentials provided via environment variable")
        return True
    else:
        print("  ❌ No Google Cloud credentials found")
        return False

def main():
    print("🚀 GitHub Secrets Test Script")
    print("=" * 50)
    
    # Test basic secrets
    secrets_ok = test_secrets()
    
    # Test Google credentials
    google_ok = test_google_credentials()
    
    # Overall result
    print("\n" + "=" * 50)
    if secrets_ok and google_ok:
        print("🎉 ALL TESTS PASSED! Ready for media generation.")
        sys.exit(0)
    else:
        print("❌ TESTS FAILED! Check your GitHub Secrets configuration.")
        sys.exit(1)

if __name__ == "__main__":
    main()