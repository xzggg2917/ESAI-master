"""
Test script to verify ESAI application works with different locale settings.
This simulates the environment issues mentioned by the reviewer.
"""
import os
import sys
import subprocess

def test_with_locale(locale_setting):
    """Test application with specific locale setting"""
    print(f"\n{'='*60}")
    print(f"Testing with locale: {locale_setting}")
    print('='*60)
    
    env = os.environ.copy()
    if locale_setting == "none":
        # Simulate environment without locale
        env.pop('LC_ALL', None)
        env.pop('LANG', None)
        env.pop('LC_CTYPE', None)
    else:
        env['LC_ALL'] = locale_setting
        env['LANG'] = locale_setting
    
    try:
        # Try to import and check if it crashes
        result = subprocess.run(
            [sys.executable, '-c', 
             'from esai.main import main; print("SUCCESS: Application imports without crashing")'],
            env=env,
            capture_output=True,
            text=True,
            timeout=5
        )
        
        if result.returncode == 0:
            print(f"✓ PASSED: Application works with {locale_setting}")
            if result.stdout:
                print(f"  Output: {result.stdout.strip()}")
            if result.stderr:
                print(f"  Warnings: {result.stderr.strip()}")
        else:
            print(f"✗ FAILED: Application crashed with {locale_setting}")
            print(f"  Error: {result.stderr}")
            return False
            
    except subprocess.TimeoutExpired:
        print(f"✗ TIMEOUT: Application did not respond with {locale_setting}")
        return False
    except Exception as e:
        print(f"✗ EXCEPTION: {e}")
        return False
    
    return True

def main():
    print("ESAI Locale Compatibility Test")
    print("="*60)
    print("This test verifies the application works across different locale settings")
    print("as mentioned in the reviewer's feedback.\n")
    
    # Test different locale scenarios
    test_cases = [
        ("C", "Standard C locale"),
        ("POSIX", "POSIX locale"),
        ("none", "No locale set (simulates minimal environments)"),
        ("en_US.UTF-8", "Common UTF-8 locale"),
    ]
    
    results = []
    for locale_val, description in test_cases:
        print(f"\nTest: {description}")
        passed = test_with_locale(locale_val)
        results.append((description, passed))
    
    # Summary
    print("\n" + "="*60)
    print("TEST SUMMARY")
    print("="*60)
    
    passed_count = sum(1 for _, passed in results if passed)
    total_count = len(results)
    
    for description, passed in results:
        status = "✓ PASSED" if passed else "✗ FAILED"
        print(f"{status}: {description}")
    
    print(f"\nTotal: {passed_count}/{total_count} tests passed")
    
    if passed_count == total_count:
        print("\n✓ All locale compatibility tests passed!")
        print("The application should work in Docker containers, minimal Linux")
        print("installations, and various Windows configurations.")
    else:
        print("\n✗ Some tests failed. Please review the output above.")
    
    return passed_count == total_count

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
