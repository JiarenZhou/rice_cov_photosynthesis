import os
import open3d as o3d
import numpy as np
from sklearn.cluster import DBSCAN
from sklearn.preprocessing import StandardScaler


# 读取点云文件
def read_point_cloud(file_path):
    return o3d.io.read_point_cloud(file_path)


# 写入点云文件
def write_point_cloud(point_cloud, file_path):
    o3d.io.write_point_cloud(file_path, point_cloud)


# 预处理第一步：点云下采样
def downsample_point_cloud(point_cloud, voxel_size):
    return point_cloud.voxel_down_sample(voxel_size)


# 预处理第二步：超绿分割
def exg_segmentation(point_cloud, threshold=0.0):
    colors = np.asarray(point_cloud.colors)
    exg = 2 * colors[:, 1] - colors[:, 0] - colors[:, 2]
    mask = exg > threshold
    return point_cloud.select_by_index(np.where(mask)[0])


# 预处理第三步：统计滤波
def statistical_outlier_removal(point_cloud, mean_k=50, std_dev_mul=1.0):
    filtered_point_cloud, _ = point_cloud.remove_statistical_outlier(nb_neighbors=mean_k, std_ratio=std_dev_mul)
    return filtered_point_cloud


# 预处理第四步：DBSCAN聚类
def dbscan_clustering(point_cloud, eps, min_samples):
    points = np.asarray(point_cloud.points)
    scaler = StandardScaler()
    scaled_points = scaler.fit_transform(points)
    dbscan = DBSCAN(eps=eps, min_samples=min_samples)
    labels = dbscan.fit_predict(scaled_points)
    unique_labels, counts = np.unique(labels, return_counts=True)
    if len(counts) == 0:
        print("No clusters found after DBSCAN.")
        return None
    max_size_label = unique_labels[np.argmax(counts)]
    selected_points = points[labels == max_size_label]
    selected_colors = np.asarray(point_cloud.colors)[labels == max_size_label]
    selected_point_cloud = o3d.geometry.PointCloud()
    selected_point_cloud.points = o3d.utility.Vector3dVector(selected_points)
    if selected_colors.size > 0:
        selected_point_cloud.colors = o3d.utility.Vector3dVector(selected_colors)
    return selected_point_cloud


# 预处理第五步：特定颜色剔除
def filter_colors(point_cloud, white_range=([200, 200, 160], [255, 255, 255]),
                  soil_range=([0, 0, 0], [100, 100, 100]), label_range=([130, 130, 130], [200, 200, 200])):
    points = np.asarray(point_cloud.points)
    colors = np.asarray(point_cloud.colors) * 255
    white_mask = np.all((colors >= white_range[0]) & (colors <= white_range[1]), axis=1)
    soil_mask = np.all((colors >= soil_range[0]) & (colors <= soil_range[1]), axis=1)
    camera_mask = np.all((colors >= label_range[0]) & (colors <= label_range[1]), axis=1)
    valid_indices = np.logical_not(white_mask | soil_mask | camera_mask)
    filtered_points = points[valid_indices]
    filtered_colors = colors[valid_indices] / 255
    filtered_point_cloud = o3d.geometry.PointCloud()
    filtered_point_cloud.points = o3d.utility.Vector3dVector(filtered_points)
    filtered_point_cloud.colors = o3d.utility.Vector3dVector(filtered_colors)
    return filtered_point_cloud


# 预处理第六步：Y轴截取
def filter_y_axis(point_cloud, min_y=-5, max_y=5):
    points = np.asarray(point_cloud.points)
    valid_indices = np.logical_and(points[:, 0] >= min_y, points[:, 0] <= max_y)
    if np.any(valid_indices):
        filtered_points = points[valid_indices]
        filtered_colors = np.asarray(point_cloud.colors)[valid_indices]
        filtered_point_cloud = o3d.geometry.PointCloud()
        filtered_point_cloud.points = o3d.utility.Vector3dVector(filtered_points)
        filtered_point_cloud.colors = o3d.utility.Vector3dVector(filtered_colors)
        return filtered_point_cloud
    else:
        print("No points left after filtering.")
        return None


def filter_x_axis(point_cloud, min_x=-5, max_x=5):
    points = np.asarray(point_cloud.points)
    valid_indices = np.logical_and(points[:, 0] >= min_x, points[:, 0] <= max_x)

    if np.any(valid_indices):
        filtered_points = points[valid_indices]
        filtered_colors = np.asarray(point_cloud.colors)[valid_indices]
        filtered_point_cloud = o3d.geometry.PointCloud()
        filtered_point_cloud.points = o3d.utility.Vector3dVector(filtered_points)
        filtered_point_cloud.colors = o3d.utility.Vector3dVector(filtered_colors)
        return filtered_point_cloud
    else:
        print("No points left after filtering.")
        return None


def filter_z_axis(point_cloud, min_z=-15, max_z=15):
    points = np.asarray(point_cloud.points)
    valid_indices = np.logical_and(points[:, 2] >= min_z, points[:, 2] <= max_z)

    if np.any(valid_indices):
        filtered_points = points[valid_indices]
        filtered_colors = np.asarray(point_cloud.colors)[valid_indices]
        filtered_point_cloud = o3d.geometry.PointCloud()
        filtered_point_cloud.points = o3d.utility.Vector3dVector(filtered_points)
        filtered_point_cloud.colors = o3d.utility.Vector3dVector(filtered_colors)
        return filtered_point_cloud
    else:
        print("No points left after filtering.")
        return None


# 水稻点云批量预处理
def process_point_cloud(input_folder, output_folder, voxel_size=0.002, exg_threshold=0.2):
    # 获取输入文件夹中所有点云文件
    point_cloud_files = [f for f in os.listdir(input_folder) if f.endswith('.ply')]

    for input_file_name in point_cloud_files:
        # 构建输入文件路径和输出文件路径
        input_file_path = os.path.join(input_folder, input_file_name)
        output_file_name = os.path.splitext(input_file_name)[0] + ".ply"
        output_file_path = os.path.join(output_folder, output_file_name)

        # 读取原始点云
        original_point_cloud = read_point_cloud(input_file_path)
        print("正在处理" + input_file_path)

        # 第一步：点云下采样
        downsampled_point_cloud = downsample_point_cloud(original_point_cloud, voxel_size)
        # 第二步：超绿分割
        green_segmented_point_cloud = exg_segmentation(downsampled_point_cloud, exg_threshold)
        # 第三步：统计滤波
        final_cloud = statistical_outlier_removal(green_segmented_point_cloud)

        final_cloud = filter_x_axis(final_cloud)
        final_cloud = filter_y_axis(final_cloud)
        final_cloud = filter_z_axis(final_cloud)

        # 保存处理后的点云
        if final_cloud is not None:
            write_point_cloud(final_cloud, output_file_path)
            print(input_file_path + "处理完成，保存至" + output_file_path)


if __name__ == "__main__":
    input_folder_path = r"I:\rice2024_minicore40\Point Cloud\3D PointClouds (original)"    # 原点云文件存放路径
    output_folder_path = r"I:\rice2024_minicore40\Point Cloud\3D PointClouds (simplified)"  # 处理后点云文件存放路径
    process_point_cloud(input_folder_path, output_folder_path)
    print("已全部处理完成！")