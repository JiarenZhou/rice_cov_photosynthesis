import os
import open3d as o3d
import numpy as np


def mesh_point_cloud(file_path, output_folder):
    # 读取PLY点云文件
    point_cloud = o3d.io.read_point_cloud(file_path)

    if point_cloud.is_empty():
        print(f"点云文件 {file_path} 为空或无法读取。")
        return

    # 计算法线
    point_cloud.estimate_normals(search_param=o3d.geometry.KDTreeSearchParamHybrid(radius=0.1, max_nn=30))
    point_cloud.normalize_normals()

    # 计算点云的平均距离
    distances = np.asarray(point_cloud.compute_nearest_neighbor_distance())
    mean_distance = np.mean(distances)

    # 进行Crust面片化
    mesh = o3d.geometry.TriangleMesh.create_from_point_cloud_ball_pivoting(
        point_cloud,
        o3d.utility.DoubleVector([mean_distance * 2.0, mean_distance * 0.5])
    )

    # 空洞填补
    mesh.remove_degenerate_triangles()  # 移除退化三角形
    mesh.remove_duplicated_triangles()  # 移除重复的三角形
    mesh.remove_duplicated_vertices()  # 移除重复的顶点
    mesh.remove_non_manifold_edges()  # 移除非流形边

    # 构造新的文件名
    base_name = os.path.splitext(os.path.basename(file_path))[0]
    output_file_path = os.path.join(output_folder, f"{base_name}_meshed.ply")

    # 保存Crust面片化后的点云PLY文件到新文件夹
    o3d.io.write_triangle_mesh(output_file_path, mesh)
    print("已完成 " + file_path + " 的面片化")


# 文件夹路径
input_folder = r"I:\rice66_dataset\rice66_new"
output_folder = r"I:\rice66_dataset\rice66_new_meshed"

# 创建输出文件夹
os.makedirs(output_folder, exist_ok=True)

# 遍历文件夹中的所有PLY文件并进行网格化
for file_name in os.listdir(input_folder):
    if file_name.endswith(".ply"):
        file_path = os.path.join(input_folder, file_name)
        mesh_point_cloud(file_path, output_folder)
