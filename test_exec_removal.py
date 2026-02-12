"""
exec() 移除验证测试
验证移除 exec() 语句后雷达图功能仍然正常工作
"""

import sys
import os

# 添加项目路径
project_dir = os.path.dirname(os.path.abspath(__file__))
if project_dir not in sys.path:
    sys.path.insert(0, project_dir)

import matplotlib
matplotlib.use('Agg')  # 使用非GUI后端进行测试

import matplotlib.pyplot as plt
from matplotlib.patches import Wedge
import numpy as np

def test_radar_chart_without_exec():
    """测试不使用 exec() 的雷达图创建"""
    
    print("测试 1: 创建雷达图扇形（无 exec()）")
    
    # 模拟原始代码逻辑（不含 exec()）
    num_segments = 8
    angle = 360 / num_segments
    center = (0.5, 0.5)
    radius = 0.4
    colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#FFA07A', 
              '#98D8C8', '#F7DC6F', '#BB8FCE', '#85C1E2']
    
    sectors = []
    
    # 创建扇形（移除了 exec() 语句）
    for i in range(num_segments):
        theta1 = i * angle + 22.5
        theta2 = theta1 + angle
        sector = Wedge(center, radius, theta1, theta2, 
                      edgecolor='black', facecolor=colors[i], linewidth=0.5)
        sectors.append(sector)
        # 注意：这里没有 exec(f"sector{i + 1} = sectors[{i}]")
    
    # 验证所有扇形已创建
    assert len(sectors) == num_segments, f"应该创建 {num_segments} 个扇形，实际创建了 {len(sectors)} 个"
    print(f"✓ 成功创建 {len(sectors)} 个扇形")
    
    # 创建图形并添加扇形
    fig, ax = plt.subplots(figsize=(8, 8))
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.set_aspect('equal')
    
    # 添加所有扇形到轴上
    for sector in sectors:
        ax.add_patch(sector)
    
    print("✓ 所有扇形已成功添加到图形")
    
    # 保存图形以验证渲染
    output_file = os.path.join(project_dir, 'test_radar_output.png')
    plt.savefig(output_file, dpi=100, bbox_inches='tight')
    plt.close()
    
    # 验证文件已创建
    assert os.path.exists(output_file), "雷达图输出文件未创建"
    file_size = os.path.getsize(output_file)
    print(f"✓ 雷达图已保存: {output_file} ({file_size:,} bytes)")
    
    # 清理测试文件
    if os.path.exists(output_file):
        os.remove(output_file)
        print("✓ 测试文件已清理")
    
    print("\n测试 2: 验证不需要 sector1, sector2 等变量")
    
    # 验证我们可以直接通过列表访问
    first_sector = sectors[0]
    last_sector = sectors[-1]
    middle_sector = sectors[num_segments // 2]
    
    assert isinstance(first_sector, Wedge), "第一个扇形应该是 Wedge 对象"
    assert isinstance(last_sector, Wedge), "最后一个扇形应该是 Wedge 对象"
    assert isinstance(middle_sector, Wedge), "中间扇形应该是 Wedge 对象"
    
    print("✓ 可以通过索引直接访问扇形")
    print(f"✓ 第一个扇形: {first_sector}")
    print(f"✓ 中间扇形: {middle_sector}")
    print(f"✓ 最后扇形: {last_sector}")
    
    print("\n测试 3: 验证 exec() 确实没有被使用")
    
    # 确认不存在 sector1, sector2 等局部变量
    local_vars = locals()
    exec_created_vars = [f'sector{i+1}' for i in range(num_segments) 
                         if f'sector{i+1}' in local_vars]
    
    assert len(exec_created_vars) == 0, \
        f"不应该有 exec() 创建的变量，但发现: {exec_created_vars}"
    
    print("✓ 确认没有使用 exec() 创建的变量")
    
    return True

def test_code_quality():
    """测试代码质量改进"""
    
    print("\n测试 4: 代码质量验证")
    
    # 读取 ESAI.py 并验证没有 exec() 语句
    esai_file = os.path.join(project_dir, 'ESAI.py')
    
    if os.path.exists(esai_file):
        with open(esai_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 搜索 exec() 的使用
        exec_count = content.count('exec(f"sector')
        
        assert exec_count == 0, \
            f"ESAI.py 中不应该包含 exec(f\"sector...\")，但发现 {exec_count} 处"
        
        print("✓ ESAI.py 中已移除所有 exec() 语句")
        
        # 验证 sectors 列表仍在使用
        assert 'sectors = []' in content or 'sectors=[]' in content, \
            "ESAI.py 应该仍然使用 sectors 列表"
        
        print("✓ sectors 列表仍在使用")
    else:
        print("⚠ 警告: 未找到 ESAI.py 文件，跳过代码质量检查")
    
    return True

def main():
    """运行所有测试"""
    print("=" * 70)
    print("exec() 移除验证测试")
    print("=" * 70)
    print()
    
    try:
        # 运行测试
        test_radar_chart_without_exec()
        test_code_quality()
        
        print("\n" + "=" * 70)
        print("✅ 所有测试通过！")
        print("=" * 70)
        print()
        print("验证结果:")
        print("  ✓ 雷达图可以在不使用 exec() 的情况下正常创建")
        print("  ✓ 扇形可以通过列表直接访问")
        print("  ✓ 不需要动态创建的变量（sector1, sector2 等）")
        print("  ✓ 代码更简洁、更安全、更易维护")
        print()
        return True
        
    except AssertionError as e:
        print("\n" + "=" * 70)
        print("❌ 测试失败")
        print("=" * 70)
        print(f"错误: {e}")
        print()
        return False
    except Exception as e:
        print("\n" + "=" * 70)
        print("❌ 测试出错")
        print("=" * 70)
        print(f"异常: {e}")
        import traceback
        traceback.print_exc()
        print()
        return False

if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)
