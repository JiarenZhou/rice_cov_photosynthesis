import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsRegressor
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score

# 加载CSV数据
data = pd.read_csv('C://Users//86188//Desktop//水稻小论文//干重.csv', sep=',')

# 数据探索与准备
# ...

# 数据分割
X = data[['point_cov']]  # 只选择point_cov作为特征
y = data['dry_weight']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

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

# 评估模型性能
rmse = np.sqrt(mean_squared_error(y_test, ensemble_pred))
mae = mean_absolute_error(y_test, ensemble_pred)
r2 = r2_score(y_test, ensemble_pred)

print('Ensemble (K-Nearest Neighbors + Random Forest) Regression Results:')
print(f'RMSE: {rmse:.2f}')
print(f'MAE: {mae:.2f}')
print(f'R^2 Score: {r2:.2f}')

plt.figure(figsize=(8, 6))
plt.scatter(X_test, y_test, color='blue', label='Actual')
plt.scatter(X_test, ensemble_pred, color='red', label='Predicted')
plt.title(f'K-Nearest Neighbors Regression for COV and Biomass')
plt.xlabel('cov')
plt.ylabel('biomass')
plt.legend()
plt.show()
