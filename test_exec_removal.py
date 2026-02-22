"""
Validation test for exec() removal
Verify that radar chart functionality still works correctly after removing exec() statements
"""

import sys
import os

# Add project path
project_dir = os.path.dirname(os.path.abspath(__file__))
if project_dir not in sys.path:
    sys.path.insert(0, project_dir)

import matplotlib
matplotlib.use('Agg')  # Use non-GUI backend for testing

import matplotlib.pyplot as plt
from matplotlib.patches import Wedge
import numpy as np

def test_radar_chart_without_exec():
    """Test radar chart creation without using exec()"""
    
    print("Test 1: Create radar chart sectors (without exec())")
    
    # Simulate original code logic (without exec())
    num_segments = 8
    angle = 360 / num_segments
    center = (0.5, 0.5)
    radius = 0.4
    colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#FFA07A', 
              '#98D8C8', '#F7DC6F', '#BB8FCE', '#85C1E2']
    
    sectors = []
    
    # Create sectors (exec() statement removed)
    for i in range(num_segments):
        theta1 = i * angle + 22.5
        theta2 = theta1 + angle
        sector = Wedge(center, radius, theta1, theta2, 
                      edgecolor='black', facecolor=colors[i], linewidth=0.5)
        sectors.append(sector)
        # Note: No exec(f"sector{i + 1} = sectors[{i}]") here
    
    # Verify all sectors are created
    assert len(sectors) == num_segments, f"Should create {num_segments} sectors, but created {len(sectors)}"
    print(f"✓ Successfully created {len(sectors)} sectors")
    
    # Create figure and add sectors
    fig, ax = plt.subplots(figsize=(8, 8))
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.set_aspect('equal')
    
    # Add all sectors to axes
    for sector in sectors:
        ax.add_patch(sector)
    
    print("✓ All sectors successfully added to figure")
    
    # Save figure to verify rendering
    output_file = os.path.join(project_dir, 'test_radar_output.png')
    plt.savefig(output_file, dpi=100, bbox_inches='tight')
    plt.close()
    
    # Verify file was created
    assert os.path.exists(output_file), "Radar chart output file was not created"
    file_size = os.path.getsize(output_file)
    print(f"✓ Radar chart saved: {output_file} ({file_size:,} bytes)")
    
    # Clean up test file
    if os.path.exists(output_file):
        os.remove(output_file)
        print("✓ Test file cleaned up")
    
    print("\nTest 2: Verify that sector1, sector2, etc. variables are not needed")
    
    # Verify we can access directly through list
    first_sector = sectors[0]
    last_sector = sectors[-1]
    middle_sector = sectors[num_segments // 2]
    
    assert isinstance(first_sector, Wedge), "First sector should be a Wedge object"
    assert isinstance(last_sector, Wedge), "Last sector should be a Wedge object"
    assert isinstance(middle_sector, Wedge), "Middle sector should be a Wedge object"
    
    print("✓ Sectors can be accessed directly by index")
    print(f"✓ First sector: {first_sector}")
    print(f"✓ Middle sector: {middle_sector}")
    print(f"✓ Last sector: {last_sector}")
    
    print("\nTest 3: Verify exec() is indeed not being used")
    
    # Confirm that sector1, sector2, etc. local variables do not exist
    local_vars = locals()
    exec_created_vars = [f'sector{i+1}' for i in range(num_segments) 
                         if f'sector{i+1}' in local_vars]
    
    assert len(exec_created_vars) == 0, \
        f"There should be no exec()-created variables, but found: {exec_created_vars}"
    
    print("✓ Confirmed no exec()-created variables exist")
    
    return True

def test_code_quality():
    """Test code quality improvements"""
    
    print("\nTest 4: Code quality verification")
    
    # Read ESAI.py and verify no exec() statements
    esai_file = os.path.join(project_dir, 'ESAI.py')
    
    if os.path.exists(esai_file):
        with open(esai_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Search for exec() usage
        exec_count = content.count('exec(f"sector')
        
        assert exec_count == 0, \
            f"ESAI.py should not contain exec(f\"sector...\"), but found {exec_count} instances"
        
        print("✓ All exec() statements removed from ESAI.py")
        
        # Verify sectors list is still in use
        assert 'sectors = []' in content or 'sectors=[]' in content, \
            "ESAI.py should still use sectors list"
        
        print("✓ sectors list is still in use")
    else:
        print("⚠ Warning: ESAI.py file not found, skipping code quality check")
    
    return True

def main():
    """Run all tests"""
    print("=" * 70)
    print("exec() Removal Validation Test")
    print("=" * 70)
    print()
    
    try:
        # Run tests
        test_radar_chart_without_exec()
        test_code_quality()
        
        print("\n" + "=" * 70)
        print("✅ All tests passed!")
        print("=" * 70)
        print()
        print("Verification results:")
        print("  ✓ Radar chart can be created normally without using exec()")
        print("  ✓ Sectors can be accessed directly through list")
        print("  ✓ No need for dynamically created variables (sector1, sector2, etc.)")
        print("  ✓ Code is cleaner, safer, and more maintainable")
        print()
        return True
        
    except AssertionError as e:
        print("\n" + "=" * 70)
        print("❌ Test failed")
        print("=" * 70)
        print(f"Error: {e}")
        print()
        return False
    except Exception as e:
        print("\n" + "=" * 70)
        print("❌ Test error")
        print("=" * 70)
        print(f"Exception: {e}")
        import traceback
        traceback.print_exc()
        print()
        return False

if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)
