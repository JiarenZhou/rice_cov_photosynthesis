import cv2
import heapq
import numpy as np
import open3d as o3d
from skimage import morphology, measure
import matplotlib.pyplot as plt


def get_point_cloud_range(file_path):
    point_cloud = o3d.io.read_point_cloud(file_path)
    points = np.asarray(point_cloud.points)

    min_x, min_y, min_z = np.min(points, axis=0)
    max_x, max_y, max_z = np.max(points, axis=0)

    return (min_x, max_x), (min_y, max_y), (min_z, max_z)


def point_cloud_projection(point_cloud, x_range, y_range, z_range, image_size=(70, 70)):
    projected_image = np.zeros(image_size, dtype=np.uint8)

    points = np.asarray(point_cloud.points)
    x = points[:, 0]
    y = points[:, 1]

    x_img = ((x - x_range[0]) / (x_range[1] - x_range[0]) * (image_size[0] - 1)).astype(int)
    y_img = ((y - y_range[0]) / (y_range[1] - y_range[0]) * (image_size[1] - 1)).astype(int)

    projected_image[y_img, x_img] = 255
    projected_image = np.flipud(projected_image)

    return projected_image


def skeletonize_image(image):
    # 找到最大连通域
    labeled_image, num_labels = morphology.label(image, return_num=True)
    region_props = measure.regionprops(labeled_image)
    largest_component_label = max(region_props, key=lambda x: x.area).label

    # 仅保留最大连通域的部分
    largest_connected_component = np.where(labeled_image == largest_component_label, 1, 0)

    # 使用 skeletonize 函数对输入图像进行骨架化
    skeletonized_image = morphology.skeletonize(largest_connected_component > 0, method='zhang')

    plt.imshow(skeletonized_image, cmap='gray')
    plt.title('skeletonized image')
    plt.show()

    return skeletonized_image


def calculate_point_distance(p1, p2):
    # 将坐标元组转换为NumPy数组
    p1 = np.array(p1)
    p2 = np.array(p2)
    return np.linalg.norm(p1 - p2)


def find_shortest_path(image, start_pixel, end_pixel, save_path_filename=None):
    print("起点坐标：" + str(start_pixel))
    print("终点坐标：" + str(end_pixel))
    directions = [(0, 1), (1, 0), (0, -1), (-1, 0), (1, 1), (-1, -1), (1, -1), (-1, 1)]

    def is_valid(x, y):
        return 0 <= x < image.shape[0] and 0 <= y < image.shape[1] and image[x, y] == 0

    labeled_image, num_labels = morphology.label(image, return_num=True)
    region_props = measure.regionprops(labeled_image)
    largest_component_label = max(region_props, key=lambda x: x.area).label
    minr, minc, maxr, maxc = region_props[largest_component_label - 1].bbox

    visited = np.zeros_like(image, dtype=bool)
    priority_queue = [(0, (minr, minc))]
    heapq.heapify(priority_queue)

    path = [(maxr, maxc)]
    path_length = 0

    while priority_queue:
        current_priority, (x, y) = heapq.heappop(priority_queue)

        if not visited[x, y]:
            visited[x, y] = True

            for dx, dy in directions:
                nx, ny = x + dx, y + dy

                if is_valid(nx, ny) and not visited[nx, ny]:
                    priority = calculate_point_distance(np.array((x, y)), np.array((nx, ny)))
                    heapq.heappush(priority_queue, (current_priority + priority, (nx, ny)))

                    # 更新路径
                    path_length = current_priority + priority

                    # 检查路径上是否已经有相同x或y值的点，如果有则不添加
                    if not any(point[0] == nx or point[1] == ny for point in path):
                        path.append((nx, ny))
                        print(f"Adding pixel ({nx}, {ny}) to the path with priority {path_length}")

                    # 如果到达终点，退出循环
                    if (nx, ny) == (minr, minc):
                        break

    path.reverse()
    print("Path updated. Current path length:", path_length)

    if save_path_filename:
        with open(save_path_filename, 'w') as file:
            for x, y in path:
                file.write(f"{x}\t{y}\n")

    return path, path_length


def PH2(image):
    # 找到最大连通域
    labeled_image, num_labels = morphology.label(image, return_num=True)

    # 使用measure.regionprops计算连通域的面积
    region_props = measure.regionprops(labeled_image)

    # 找到最大连通域的标签
    largest_component_label = max(region_props, key=lambda x: x.area).label

    # 找到最大连通域的边界框
    minr, minc, maxr, maxc = region_props[largest_component_label - 1].bbox

    # 仅保留最大连通域的部分
    largest_connected_component = np.where(labeled_image == largest_component_label, 1, 0)

    # 计算最短路径并获取最短路径的像素坐标
    start_pixel = (minr, minc)
    end_pixel = (maxr, maxc)
    shortest_path = find_shortest_path(image, start_pixel, end_pixel, 'data.txt')[1]
    return shortest_path


if __name__ == "__main__":
    point_cloud_file = r"J:\rice350_pointcloud\E1G1\C22_E1G1.ply"
    x_range, y_range, z_range = get_point_cloud_range(point_cloud_file)
    point_cloud = o3d.io.read_point_cloud(point_cloud_file)
    projected_image = point_cloud_projection(point_cloud, x_range, y_range, z_range)
    skeletonized_image = skeletonize_image(projected_image)
    ph2_values = PH2(skeletonized_image)
    print("PH2 Values:", ph2_values)

