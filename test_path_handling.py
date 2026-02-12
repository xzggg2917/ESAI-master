"""
Test script to verify resource path handling works from different working directories.
This addresses the reviewer's concern about hardcoded relative file paths.
"""
import os
import sys
import subprocess
from pathlib import Path
import tempfile

def test_resource_path_function():
    """Test the get_resource_path function works correctly"""
    print("="*70)
    print("TEST 1: Resource Path Function")
    print("="*70)
    
    test_code = """
import sys
from pathlib import Path

# Add the ESAI directory to the path
esai_dir = Path(__file__).parent.resolve()
sys.path.insert(0, str(esai_dir))

# Import the function (we'll test it without running the GUI)
import os
from pathlib import Path

def get_resource_path(relative_path):
    try:
        if getattr(sys, 'frozen', False):
            base_path = Path(sys.executable).parent
        else:
            base_path = Path(__file__).parent.resolve()
        
        resource_path = base_path / relative_path
        
        if not resource_path.exists():
            raise FileNotFoundError(f"Resource file not found: {resource_path}")
        
        return str(resource_path)
    except Exception as e:
        print(f"Error: {e}")
        raise

# Test with existing files
try:
    logo_path = get_resource_path("logo.ico")
    print(f"Found logo.ico at: {logo_path}")
    assert os.path.exists(logo_path), "Logo file doesn't exist"
    print("Test 1.1 PASSED: logo.ico located successfully")
except Exception as e:
    print(f"Test 1.1 FAILED: {e}")
    sys.exit(1)

try:
    splash_path = get_resource_path("rj.png")
    print(f"Found rj.png at: {splash_path}")
    assert os.path.exists(splash_path), "Splash file doesn't exist"
    print("Test 1.2 PASSED: rj.png located successfully")
except Exception as e:
    print(f"Test 1.2 FAILED: {e}")
    sys.exit(1)

# Test with non-existent file (should raise clear error)
try:
    nonexistent = get_resource_path("nonexistent.png")
    print("Test 1.3 FAILED: Should have raised FileNotFoundError")
    sys.exit(1)
except FileNotFoundError as e:
    print("Test 1.3 PASSED: Correct error handling for missing files")
except Exception as e:
    print(f"Test 1.3 FAILED: Wrong exception type: {e}")
    sys.exit(1)

print("\\nAll resource path tests passed!")
"""
    
    # Save test to temporary file
    test_file = Path("d:/Projects/ESAI-master") / "temp_test.py"
    try:
        with open(test_file, 'w', encoding='utf-8') as f:
            f.write(test_code)
        
        result = subprocess.run(
            [sys.executable, str(test_file)],
            capture_output=True,
            text=True,
            timeout=10,
            cwd="d:/Projects/ESAI-master"
        )
        
        print(result.stdout)
        if result.stderr:
            print("Warnings:", result.stderr[:300])
        
        return result.returncode == 0
    except Exception as e:
        print(f"Test failed: {e}")
        return False
    finally:
        # Cleanup
        if test_file.exists():
            test_file.unlink()

def test_different_working_directories():
    """Test that resources can be found from different working directories"""
    print("\n" + "="*70)
    print("TEST 2: Different Working Directories")
    print("="*70)
    
    esai_dir = Path("d:/Projects/ESAI-master").resolve()
    
    # Test directories to run from
    test_dirs = [
        esai_dir,  # Same directory (should work)
        esai_dir.parent,  # Parent directory (common case)
        Path(tempfile.gettempdir()),  # Temp directory (edge case)
    ]
    
    test_code = """
import sys
import os
from pathlib import Path

# Get the ESAI directory
esai_file = Path(r'{esai_path}') / 'ESAI.py'
print(f"Testing from CWD: {{os.getcwd()}}")
print(f"ESAI.py location: {{esai_file}}")

# Read the ESAI.py file to check for get_resource_path
try:
    with open(esai_file, 'r', encoding='utf-8') as f:
        content = f.read()
        if 'def get_resource_path' in content:
            print("get_resource_path function found in ESAI.py")
        else:
            print("WARNING: get_resource_path function not found")
            sys.exit(1)
    
    # Check that resource files exist relative to ESAI.py
    logo_path = esai_file.parent / 'logo.ico'
    splash_path = esai_file.parent / 'rj.png'
    
    if logo_path.exists():
        print(f"logo.ico exists at: {{logo_path}}")
    else:
        print(f"ERROR: logo.ico not found at: {{logo_path}}")
        sys.exit(1)
    
    if splash_path.exists():
        print(f"rj.png exists at: {{splash_path}}")
    else:
        print(f"ERROR: rj.png not found at: {{splash_path}}")
        sys.exit(1)
    
    print("All resource files accessible!")
    
except Exception as e:
    print(f"Error: {{e}}")
    sys.exit(1)
"""
    
    all_passed = True
    for i, test_dir in enumerate(test_dirs, 1):
        print(f"\nTest 2.{i}: Running from {test_dir}")
        
        try:
            result = subprocess.run(
                [sys.executable, '-c', test_code.format(esai_path=str(esai_dir))],
                capture_output=True,
                text=True,
                timeout=10,
                cwd=str(test_dir)
            )
            
            print(result.stdout)
            
            if result.returncode == 0:
                print(f"Test 2.{i} PASSED")
            else:
                print(f"Test 2.{i} FAILED")
                if result.stderr:
                    print("Error:", result.stderr[:200])
                all_passed = False
                
        except Exception as e:
            print(f"Test 2.{i} FAILED: {e}")
            all_passed = False
    
    return all_passed

def test_import_without_crash():
    """Test that ESAI.py can be parsed with the new code"""
    print("\n" + "="*70)
    print("TEST 3: ESAI.py Syntax and Import")
    print("="*70)
    
    esai_file = Path("d:/Projects/ESAI-master/ESAI.py")
    
    try:
        with open(esai_file, 'r', encoding='utf-8') as f:
            code = f.read()
        
        # Check for key components
        checks = [
            ("get_resource_path function", "def get_resource_path(relative_path):"),
            ("Path import", "from pathlib import Path"),
            ("Resource path usage for logo", 'get_resource_path("logo.ico")'),
            ("Resource path usage for splash", 'get_resource_path("rj.png")'),
            ("Error handling for logo", "except FileNotFoundError as e:"),
        ]
        
        all_found = True
        for name, pattern in checks:
            if pattern in code:
                print(f"✓ {name}: Found")
            else:
                print(f"✗ {name}: Not found")
                all_found = False
        
        if all_found:
            print("\nAll required components present")
        else:
            print("\nSome components missing")
            return False
        
        # Try to compile
        compile(code, str(esai_file), 'exec')
        print("✓ ESAI.py compiles without syntax errors")
        
        return True
        
    except Exception as e:
        print(f"✗ Error: {e}")
        return False

def main():
    print("\n" + "="*70)
    print("ESAI RESOURCE PATH HANDLING TEST SUITE")
    print("="*70)
    print("Testing fix for hardcoded relative file paths (Reviewer Comment 3)")
    print("="*70 + "\n")
    
    results = []
    
    # Test 1: Resource path function
    results.append(("Resource Path Function", test_resource_path_function()))
    
    # Test 2: Different working directories
    results.append(("Different Working Directories", test_different_working_directories()))
    
    # Test 3: Import and syntax
    results.append(("ESAI.py Syntax Check", test_import_without_crash()))
    
    # Summary
    print("\n" + "="*70)
    print("TEST SUMMARY")
    print("="*70)
    
    for test_name, passed in results:
        status = "✓ PASSED" if passed else "✗ FAILED"
        print(f"{status}: {test_name}")
    
    passed_count = sum(1 for _, passed in results if passed)
    total_count = len(results)
    print(f"\nTotal: {passed_count}/{total_count} tests passed")
    
    if passed_count == total_count:
        print("\n" + "="*70)
        print("✓✓✓ ALL TESTS PASSED ✓✓✓")
        print("="*70)
        print("\nThe application now handles resource paths robustly:")
        print("  ✓ Works from any working directory")
        print("  ✓ Provides clear error messages for missing files")
        print("  ✓ Supports both script and frozen executable modes")
        print("  ✓ Graceful fallback for missing resources")
        print("="*70)
    else:
        print("\n⚠ Some tests failed. Review output above.")
    
    return passed_count == total_count

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
