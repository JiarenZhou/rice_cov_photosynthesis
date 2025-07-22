import os
import open3d as o3d
import numpy as np
import pandas as pd


def calculate_cov(ply_path, voxel_size=0.005):
    # 读取PLY文件
    pcd = o3d.io.read_point_cloud(ply_path)

    # 获取点云的顶点
    vertices = np.asarray(pcd.points)

    # 计算COV
    occupied_voxels = set()

    # 计算每个点所在的体素坐标，并将其标记为被占用
    voxel_coords = np.floor(vertices / voxel_size).astype(int)
    for coord in voxel_coords:
        occupied_voxels.add(tuple(coord))

    # 计算COV的数量
    cov_count = len(occupied_voxels)

    return cov_count


def batch_calculate_cov(folder_path, output_csv_path, voxel_size=0.005):
    # 获取文件夹下所有PLY文件
    ply_files = [f for f in os.listdir(folder_path) if f.endswith('.ply')]

    # 存储计算结果的列表
    results = []

    # 遍历每个PLY文件并计算COV
    for ply_file in ply_files:
        ply_path = os.path.join(folder_path, ply_file)
        cov_count = calculate_cov(ply_path, voxel_size)
        results.append({'PLY_File': ply_file, 'COV_Count': cov_count})
        print(ply_file + " OK")

    # 将结果保存到CSV文件
    df = pd.DataFrame(results)
    df.to_csv(output_csv_path, index=False)
    print(f"COV计算完成，结果保存至 {output_csv_path}")


# 指定PLY文件所在的文件夹路径和输出CSV文件路径
folder_path = r'I:\rice66_dataset\rice66_new_meshed'
output_csv_path = r'C:\Users\86188\Desktop\COV.csv'

# 批量计算COV并保存结果
batch_calculate_cov(folder_path, output_csv_path)
