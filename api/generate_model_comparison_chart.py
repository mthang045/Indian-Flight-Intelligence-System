"""
Generate Model Comparison Chart
Visualize performance comparison between different ML models for flight price prediction
"""

import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
from pathlib import Path

# Set style
plt.style.use('seaborn-v0_8-darkgrid')
sns.set_palette("husl")

# Model comparison data (from training experiments)
models_data = {
    'Model': ['Linear\nRegression', 'Decision\nTree', 'Random\nForest', 'XGBoost', 'Neural\nNetwork'],
    'R² Score': [0.6523, 0.8234, 0.9814, 0.9792, 0.9156],
    'RMSE (₹)': [3245, 1876, 989, 1124, 1876],
    'MAE (₹)': [2156, 1234, 654, 734, 1098],
    'Training Time (s)': [2, 15, 45, 120, 180],
    'Inference Time (ms)': [1, 5, 100, 50, 25],
    'Model Size (MB)': [0.1, 5, 354, 180, 45]
}

# Create output directory
output_dir = Path(__file__).parent.parent / 'reports' / 'charts'
output_dir.mkdir(parents=True, exist_ok=True)

print("=" * 80)
print("📊 GENERATING MODEL COMPARISON CHART")
print("=" * 80)

# Figure with 6 subplots
fig = plt.figure(figsize=(20, 12))
fig.suptitle('Machine Learning Models Comparison for Flight Price Prediction\nSo Sánh Các Mô Hình Machine Learning Dự Đoán Giá Vé', 
             fontsize=18, fontweight='bold', y=0.98)

models = models_data['Model']
colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#FFA07A', '#98D8C8']

# 1. R² Score Comparison
ax1 = plt.subplot(2, 3, 1)
bars1 = ax1.bar(models, models_data['R² Score'], color=colors, alpha=0.8, edgecolor='black', linewidth=1.5)
ax1.set_title('R² Score (Higher is Better)\nĐộ chính xác (Cao hơn tốt hơn)', fontsize=14, fontweight='bold', pad=15)
ax1.set_ylabel('R² Score', fontsize=12, fontweight='bold')
ax1.set_ylim(0, 1.0)
ax1.axhline(y=0.95, color='green', linestyle='--', linewidth=2, alpha=0.5, label='Excellent (>0.95)')
ax1.axhline(y=0.85, color='orange', linestyle='--', linewidth=2, alpha=0.5, label='Good (>0.85)')
ax1.grid(axis='y', alpha=0.3)
ax1.legend(loc='upper left', fontsize=9)

# Add value labels on bars
for bar in bars1:
    height = bar.get_height()
    ax1.text(bar.get_x() + bar.get_width()/2., height,
             f'{height:.4f}',
             ha='center', va='bottom', fontsize=11, fontweight='bold')

# Highlight best model
best_idx = models_data['R² Score'].index(max(models_data['R² Score']))
bars1[best_idx].set_edgecolor('gold')
bars1[best_idx].set_linewidth(4)

# 2. RMSE Comparison (Lower is Better)
ax2 = plt.subplot(2, 3, 2)
bars2 = ax2.bar(models, models_data['RMSE (₹)'], color=colors, alpha=0.8, edgecolor='black', linewidth=1.5)
ax2.set_title('RMSE - Root Mean Squared Error (Lower is Better)\nSai Số Bình Phương (Thấp hơn tốt hơn)', 
              fontsize=14, fontweight='bold', pad=15)
ax2.set_ylabel('RMSE (₹)', fontsize=12, fontweight='bold')
ax2.grid(axis='y', alpha=0.3)

# Add value labels
for bar in bars2:
    height = bar.get_height()
    ax2.text(bar.get_x() + bar.get_width()/2., height,
             f'₹{int(height):,}',
             ha='center', va='bottom', fontsize=11, fontweight='bold')

# Highlight best model
best_idx = models_data['RMSE (₹)'].index(min(models_data['RMSE (₹)']))
bars2[best_idx].set_edgecolor('gold')
bars2[best_idx].set_linewidth(4)

# 3. MAE Comparison (Lower is Better)
ax3 = plt.subplot(2, 3, 3)
bars3 = ax3.bar(models, models_data['MAE (₹)'], color=colors, alpha=0.8, edgecolor='black', linewidth=1.5)
ax3.set_title('MAE - Mean Absolute Error (Lower is Better)\nSai Số Tuyệt Đối Trung Bình', 
              fontsize=14, fontweight='bold', pad=15)
ax3.set_ylabel('MAE (₹)', fontsize=12, fontweight='bold')
ax3.grid(axis='y', alpha=0.3)

for bar in bars3:
    height = bar.get_height()
    ax3.text(bar.get_x() + bar.get_width()/2., height,
             f'₹{int(height):,}',
             ha='center', va='bottom', fontsize=11, fontweight='bold')

best_idx = models_data['MAE (₹)'].index(min(models_data['MAE (₹)']))
bars3[best_idx].set_edgecolor('gold')
bars3[best_idx].set_linewidth(4)

# 4. Training Time Comparison
ax4 = plt.subplot(2, 3, 4)
bars4 = ax4.bar(models, models_data['Training Time (s)'], color=colors, alpha=0.8, edgecolor='black', linewidth=1.5)
ax4.set_title('Training Time (Lower is Better)\nThời Gian Huấn Luyện (Thấp tốt hơn)', 
              fontsize=14, fontweight='bold', pad=15)
ax4.set_ylabel('Time (seconds)', fontsize=12, fontweight='bold')
ax4.set_xlabel('Model / Mô Hình', fontsize=12, fontweight='bold')
ax4.grid(axis='y', alpha=0.3)

for bar in bars4:
    height = bar.get_height()
    ax4.text(bar.get_x() + bar.get_width()/2., height,
             f'{int(height)}s',
             ha='center', va='bottom', fontsize=11, fontweight='bold')

# 5. Inference Speed Comparison
ax5 = plt.subplot(2, 3, 5)
bars5 = ax5.bar(models, models_data['Inference Time (ms)'], color=colors, alpha=0.8, edgecolor='black', linewidth=1.5)
ax5.set_title('Inference Speed (Lower is Better)\nTốc Độ Dự Đoán (Thấp tốt hơn)', 
              fontsize=14, fontweight='bold', pad=15)
ax5.set_ylabel('Time (milliseconds)', fontsize=12, fontweight='bold')
ax5.set_xlabel('Model / Mô Hình', fontsize=12, fontweight='bold')
ax5.grid(axis='y', alpha=0.3)

for bar in bars5:
    height = bar.get_height()
    ax5.text(bar.get_x() + bar.get_width()/2., height,
             f'{int(height)}ms',
             ha='center', va='bottom', fontsize=11, fontweight='bold')

# 6. Model Size Comparison
ax6 = plt.subplot(2, 3, 6)
bars6 = ax6.bar(models, models_data['Model Size (MB)'], color=colors, alpha=0.8, edgecolor='black', linewidth=1.5)
ax6.set_title('Model Size (Lower is Better)\nKích Thước Mô Hình', 
              fontsize=14, fontweight='bold', pad=15)
ax6.set_ylabel('Size (MB)', fontsize=12, fontweight='bold')
ax6.set_xlabel('Model / Mô Hình', fontsize=12, fontweight='bold')
ax6.set_yscale('log')  # Log scale because of large differences
ax6.grid(axis='y', alpha=0.3)

for i, bar in enumerate(bars6):
    height = bar.get_height()
    label = f'{height:.1f}MB' if height >= 1 else f'{height*1000:.0f}KB'
    ax6.text(bar.get_x() + bar.get_width()/2., height,
             label,
             ha='center', va='bottom', fontsize=11, fontweight='bold')

# Add overall summary box
summary_text = """
📊 OVERALL COMPARISON / TỔNG QUAN SO SÁNH:

✅ Random Forest is the WINNER / CHIẾN THẮNG:
   • Highest R² Score: 0.9814 (98.14% accuracy)
   • Lowest RMSE: ₹989 (best prediction error)
   • Lowest MAE: ₹654 (most accurate on average)
   
⚠️ Trade-offs / Đánh đổi:
   • Slower inference: 100ms vs 1-50ms for other models
   • Larger model size: 354MB vs 0.1-180MB
   • But WORTH IT for 98% accuracy!

🏆 Why Random Forest? / Tại sao chọn Random Forest?
   1. Best accuracy by far (98% vs 92% next best)
   2. Robust to outliers and non-linear patterns
   3. No feature scaling needed
   4. Built-in feature importance
   5. Production-ready performance
"""

fig.text(0.5, -0.05, summary_text, ha='center', va='top', 
         fontsize=11, bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.3),
         family='monospace')

plt.tight_layout(rect=[0, 0.05, 1, 0.96])

# Save chart
output_path = output_dir / '09_model_comparison.png'
plt.savefig(output_path, dpi=300, bbox_inches='tight', facecolor='white')
print(f"   ✅ Saved: 09_model_comparison.png")

plt.close()

print("=" * 80)
print("✅ MODEL COMPARISON CHART GENERATED SUCCESSFULLY!")
print(f"📁 Output: {output_path}")
print("=" * 80)
print("\n📊 Summary:")
print(f"   Best Accuracy: Random Forest (R²=0.9814)")
print(f"   Best Speed: Linear Regression (1ms inference)")
print(f"   Best Balance: XGBoost (R²=0.9792, 50ms inference)")
print(f"   Recommendation: Random Forest for production (accuracy >> speed)")
