import os
import open3d as o3d
import numpy as np
import pandas as pd


def process_ply_file(file_path):
    # 读取PLY点云文件
    point_cloud = o3d.io.read_point_cloud(file_path)

    # 将点云转换为NumPy数组
    points = np.asarray(point_cloud.points)

    # 计算x方向上的极差
    x_range = np.ptp(points[:, 0])

    # 计算y方向上的极差
    y_range = np.ptp(points[:, 1])

    # 计算z方向上的极差
    z_range = np.ptp(points[:, 2])

    # 取较大者作为冠幅
    canopy_width = np.round(max(x_range, y_range), 4)

    # 计算垂直方向上距离之差的最大值（直线株高）
    plant_height = np.round(z_range, 4)

    return plant_height, canopy_width


def batch_process_ply_files(folder_path):
    results = []

    # 遍历文件夹中的所有PLY文件
    for file_name in os.listdir(folder_path):
        if file_name.endswith(".ply"):
            file_path = os.path.join(folder_path, file_name)
            plant_height, canopy_width = process_ply_file(file_path)
            results.append({"File": file_name, "PH": plant_height, "CW": canopy_width})
            print("已完成 " + file_name + " 的直线株高和冠幅的提取")

    return results


def save_to_csv(results, output_csv):
    df = pd.DataFrame(results)
    df.to_csv(output_csv, index=False)


# 文件夹路径
input_folder = r"I:\rice350_pointcloud_simplified\E1G1"

# 批量处理PLY文件
results = batch_process_ply_files(input_folder)

# 保存结果到CSV文件
output_csv = r"C:\Users\86188\Desktop\株高和冠幅.csv"
save_to_csv(results, output_csv)
