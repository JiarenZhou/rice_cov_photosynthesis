import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.neighbors import KNeighborsRegressor
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import PolynomialFeatures
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score

# 加载CSV数据
data = pd.read_csv('C://Users//86188//Desktop//水稻小论文//干重.csv', sep=',')

# 数据探索与准备
print(data.head())  # 查看前几行数据
print(data.info())  # 查看数据类型和缺失值情况
print(data.describe())  # 描述性统计信息

# 数据分割
X = data[['point_cov']]  # 只选择point_cov作为特征
y = data['dry_weight']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

degree = 5

# 创建多项式特征
poly = PolynomialFeatures(degree=degree)
X_train_poly = poly.fit_transform(X_train)
X_test_poly = poly.transform(X_test)

# 训练多项式回归模型
poly_model = LinearRegression()
poly_model.fit(X_train_poly, y_train)

# 预测
y_pred_poly = poly_model.predict(X_test_poly)

# 评估多项式回归模型
rmse = np.sqrt(mean_squared_error(y_test, y_pred_poly))
mae = mean_absolute_error(y_test, y_pred_poly)
r2 = r2_score(y_test, y_pred_poly)

# 定义K近邻回归模型
knn = KNeighborsRegressor(n_neighbors=6)  # 设置n_neighbors=6

# 随机森林回归作为集成方法
rf_model = RandomForestRegressor(n_estimators=100, random_state=42)  # 可以调整n_estimators

# 训练K近邻回归模型
knn.fit(X_train, y_train)

# 训练随机森林回归模型
rf_model.fit(X_train, y_train)

# 集成预测
knn_pred = knn.predict(X_test)
rf_pred = rf_model.predict(X_test)

# 取平均作为最终预测结果
ensemble_pred = (knn_pred + rf_pred) / 2

print(f'Degree {degree} Polynomial Regression Results:')
print(f'RMSE: {rmse:.2f}')
print(f'MAE: {mae:.2f}')
print(f'R^2 Score: {r2:.2f}')

# 绘制预测线
X_range = np.linspace(min(X_test['point_cov']), max(X_test['point_cov']), 100).reshape(-1, 1)
X_range_poly = poly.transform(X_range)

# 多项式回归预测线
y_pred_poly_line = poly_model.predict(X_range_poly)

# K近邻回归和随机森林回归的预测线
y_pred_knn_line = knn.predict(X_range)
y_pred_rf_line = rf_model.predict(X_range)

# 集成预测线
ensemble_pred_line = (y_pred_knn_line + y_pred_rf_line) / 2

# 计算每个数据点的误差
errors_poly = np.abs(y_test - y_pred_poly)
errors_ensemble = np.abs(y_test - ensemble_pred)

# 设置全局字体为"Times New Roman"
plt.rcParams['font.family'] = 'Times New Roman'
plt.rcParams['font.size'] = 18  # 设置字体大小

# 创建两个子图，水平排布
fig, axes = plt.subplots(nrows=1, ncols=2, figsize=(16, 6))

# 子图1：多项式回归
scatter1 = axes[0].scatter(X_test['point_cov'], y_test, color='black', label='True value', marker='s', s=10)
scatter2 = axes[0].scatter(X_test['point_cov'], y_pred_poly, color='red', label='Predicted value (Polynomial)', s=10)
errorbar = axes[0].errorbar(X_test['point_cov'].to_numpy(), y_pred_poly, yerr=errors_poly, fmt='none', ecolor='gray', elinewidth=0.5, capsize=2, linestyle='--')
axes[0].plot(X_range, y_pred_poly_line, color='red', linestyle='--', linewidth=1)

# 添加误差线区域的填充
axes[0].fill_between(X_range.flatten(), y_pred_poly_line - errors_poly.max(), y_pred_poly_line + errors_poly.max(), color='lightcoral', alpha=0.2, label='Poly Error Area')
axes[0].set_title('(a) Polynomial Regression (Degree 5)')
axes[0].set_xlabel('COV')
axes[0].set_ylabel('Biomass')
axes[0].legend()

# 子图2：集成方法回归
scatter3 = axes[1].scatter(X_test['point_cov'], y_test, color='black', label='True value', marker='s', s=10)
scatter4 = axes[1].scatter(X_test['point_cov'], ensemble_pred, color='orange', label='Predicted value (Ensemble)', s=10)
errorbar2 = axes[1].errorbar(X_test['point_cov'].to_numpy(), ensemble_pred, yerr=errors_ensemble, fmt='none', ecolor='gray', elinewidth=0.5, capsize=2, linestyle='--')
axes[1].plot(X_range, ensemble_pred_line, color='orange', linestyle='--', linewidth=1)

# 添加误差线区域的填充
axes[1].fill_between(X_range.flatten(), ensemble_pred_line - errors_ensemble.max(), ensemble_pred_line + errors_ensemble.max(), color='lightsalmon', alpha=0.2, label='Ensemble Error Area')
axes[1].set_title('(b) Ensemble Regression (KNN + RF)')
axes[1].set_xlabel('COV')
axes[1].set_ylabel('Biomass')
axes[1].legend()

plt.tight_layout()  # 调整子图布局，防止重叠
plt.show()