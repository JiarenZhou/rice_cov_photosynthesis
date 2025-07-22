import os
import open3d as o3d
import csv

def get_point_cloud_count(file_path):
    """
    获取点云文件中的点数。

    参数：
    - file_path: 点云文件路径

    返回：
    - 点数
    """
    point_cloud = o3d.io.read_point_cloud(file_path)
    if point_cloud.is_empty():
        return 0
    return len(point_cloud.points)

def save_point_cloud_counts(input_folder, output_csv):
    """
    提取输入文件夹中所有点云文件的点数，并保存至 CSV 文件。

    参数：
    - input_folder: 存放点云文件的文件夹路径
    - output_csv: 输出 CSV 文件路径
    """
    # 打开 CSV 文件进行写入
    with open(output_csv, mode='w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['File Name', 'Point Count']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()

        # 遍历文件夹中的所有点云文件
        for file_name in os.listdir(input_folder):
            if file_name.endswith(".ply"):
                file_path = os.path.join(input_folder, file_name)
                point_count = get_point_cloud_count(file_path)
                writer.writerow({'File Name': file_name, 'Point Count': point_count})
                print(f"{file_name}: {point_count} points")

# 输入文件夹路径
input_folder = r"I:\rice350_pointcloud_simplified\E4G4"
# 输出 CSV 文件路径
output_csv = r"C:\Users\86188\Desktop\point_cloud_counts.csv"

# 保存点云文件点数至 CSV
save_point_cloud_counts(input_folder, output_csv)
