import os
import torch
import pandas as pd
from PIL import Image

# 定义模型路径和主目录路径
MODEL_PATH = 'I:/李万万PC/LeafCounter/exp6/weights/best.pt'  # 替换为您的模型路径
ROOT_DIR = 'J:/第三次0927/3D/2021.9.27 第三次拍摄p'  # 替换为大写字母开头文件夹的主目录路径
OUTPUT_CSV = 'C:/Users/86188/Desktop/E3.csv'  # 输出汇总表格的路径

# 加载模型
model = torch.hub.load('ultralytics/yolov5', 'custom', path=MODEL_PATH)


# 检查大写字母开头的文件夹
def is_uppercase_folder(folder_name):
    return folder_name[0].isupper()


# 存储检测结果
results_summary = []

# 遍历大写字母开头的文件夹
for folder in os.listdir(ROOT_DIR):
    folder_path = os.path.join(ROOT_DIR, folder)

    if os.path.isdir(folder_path) and is_uppercase_folder(folder):
        photos_path = os.path.join(folder_path, 'Photos', '1')

        if os.path.exists(photos_path):
            max_count = 0

            # 遍历图片
            for image_file in os.listdir(photos_path):
                image_path = os.path.join(photos_path, image_file)

                if image_file.lower().endswith(('.jpg', '.jpeg', '.png')):
                    try:
                        # 确保图片能够打开
                        img = Image.open(image_path)
                        img.verify()  # 验证图片的完整性

                        # 对单张图片进行检测
                        results = model(image_path)
                        detections = results.xyxy[0]  # 获取检测结果
                        max_count = max(max_count, len(detections))

                    except (OSError, ValueError) as e:
                        print(f"无法读取图像: {image_path}, 错误: {e}")
                        continue  # 跳过无法读取的图像

            # 添加结果到列表
            results_summary.append({'Folder': folder + "_E3", 'DetectionCount': max_count})
            print(folder + "OK")

# 转换为DataFrame并保存为CSV
results_df = pd.DataFrame(results_summary)
results_df.to_csv(OUTPUT_CSV, index=False)

print(f"检测完成，结果已保存到 {OUTPUT_CSV}")



# 定义模型路径和主目录路径
MODEL_PATH = 'I:/李万万PC/LeafCounter/exp6/weights/best.pt'  # 替换为您的模型路径
ROOT_DIR = 'J:/第四次1011/3D/2021.10.11第四次拍摄第一次重复p'  # 替换为大写字母开头文件夹的主目录路径
OUTPUT_CSV = 'C:/Users/86188/Desktop/E4G1.csv'  # 输出汇总表格的路径

# 加载模型
model = torch.hub.load('ultralytics/yolov5', 'custom', path=MODEL_PATH)


# 检查大写字母开头的文件夹
def is_uppercase_folder(folder_name):
    return folder_name[0].isupper()


# 存储检测结果
results_summary = []

# 遍历大写字母开头的文件夹
for folder in os.listdir(ROOT_DIR):
    folder_path = os.path.join(ROOT_DIR, folder)

    if os.path.isdir(folder_path) and is_uppercase_folder(folder):
        photos_path = os.path.join(folder_path, 'Photos', '1')

        if os.path.exists(photos_path):
            max_count = 0

            # 遍历图片
            for image_file in os.listdir(photos_path):
                image_path = os.path.join(photos_path, image_file)

                if image_file.lower().endswith(('.jpg', '.jpeg', '.png')):
                    try:
                        # 确保图片能够打开
                        img = Image.open(image_path)
                        img.verify()  # 验证图片的完整性

                        # 对单张图片进行检测
                        results = model(image_path)
                        detections = results.xyxy[0]  # 获取检测结果
                        max_count = max(max_count, len(detections))

                    except (OSError, ValueError) as e:
                        print(f"无法读取图像: {image_path}, 错误: {e}")
                        continue  # 跳过无法读取的图像

            # 添加结果到列表
            results_summary.append({'Folder': folder + "_E4G1", 'DetectionCount': max_count})
            print(folder + "OK")

# 转换为DataFrame并保存为CSV
results_df = pd.DataFrame(results_summary)
results_df.to_csv(OUTPUT_CSV, index=False)

print(f"检测完成，结果已保存到 {OUTPUT_CSV}")



# 定义模型路径和主目录路径
MODEL_PATH = 'I:/李万万PC/LeafCounter/exp6/weights/best.pt'  # 替换为您的模型路径
ROOT_DIR = 'J:/第四次1011/3D/2021.10.12第四次拍摄第二次重复p'  # 替换为大写字母开头文件夹的主目录路径
OUTPUT_CSV = 'C:/Users/86188/Desktop/E4G2.csv'  # 输出汇总表格的路径

# 加载模型
model = torch.hub.load('ultralytics/yolov5', 'custom', path=MODEL_PATH)


# 检查大写字母开头的文件夹
def is_uppercase_folder(folder_name):
    return folder_name[0].isupper()


# 存储检测结果
results_summary = []

# 遍历大写字母开头的文件夹
for folder in os.listdir(ROOT_DIR):
    folder_path = os.path.join(ROOT_DIR, folder)

    if os.path.isdir(folder_path) and is_uppercase_folder(folder):
        photos_path = os.path.join(folder_path, 'Photos', '1')

        if os.path.exists(photos_path):
            max_count = 0

            # 遍历图片
            for image_file in os.listdir(photos_path):
                image_path = os.path.join(photos_path, image_file)

                if image_file.lower().endswith(('.jpg', '.jpeg', '.png')):
                    try:
                        # 确保图片能够打开
                        img = Image.open(image_path)
                        img.verify()  # 验证图片的完整性

                        # 对单张图片进行检测
                        results = model(image_path)
                        detections = results.xyxy[0]  # 获取检测结果
                        max_count = max(max_count, len(detections))

                    except (OSError, ValueError) as e:
                        print(f"无法读取图像: {image_path}, 错误: {e}")
                        continue  # 跳过无法读取的图像

            # 添加结果到列表
            results_summary.append({'Folder': folder + "_E4G2", 'DetectionCount': max_count})
            print(folder + "OK")

# 转换为DataFrame并保存为CSV
results_df = pd.DataFrame(results_summary)
results_df.to_csv(OUTPUT_CSV, index=False)

print(f"检测完成，结果已保存到 {OUTPUT_CSV}")



# 定义模型路径和主目录路径
MODEL_PATH = 'I:/李万万PC/LeafCounter/exp6/weights/best.pt'  # 替换为您的模型路径
ROOT_DIR = 'J:/第四次1011/3D/2021.10.13第四次拍摄第三次重复p'  # 替换为大写字母开头文件夹的主目录路径
OUTPUT_CSV = 'C:/Users/86188/Desktop/E4G3.csv'  # 输出汇总表格的路径

# 加载模型
model = torch.hub.load('ultralytics/yolov5', 'custom', path=MODEL_PATH)


# 检查大写字母开头的文件夹
def is_uppercase_folder(folder_name):
    return folder_name[0].isupper()


# 存储检测结果
results_summary = []

# 遍历大写字母开头的文件夹
for folder in os.listdir(ROOT_DIR):
    folder_path = os.path.join(ROOT_DIR, folder)

    if os.path.isdir(folder_path) and is_uppercase_folder(folder):
        photos_path = os.path.join(folder_path, 'Photos', '1')

        if os.path.exists(photos_path):
            max_count = 0

            # 遍历图片
            for image_file in os.listdir(photos_path):
                image_path = os.path.join(photos_path, image_file)

                if image_file.lower().endswith(('.jpg', '.jpeg', '.png')):
                    try:
                        # 确保图片能够打开
                        img = Image.open(image_path)
                        img.verify()  # 验证图片的完整性

                        # 对单张图片进行检测
                        results = model(image_path)
                        detections = results.xyxy[0]  # 获取检测结果
                        max_count = max(max_count, len(detections))

                    except (OSError, ValueError) as e:
                        print(f"无法读取图像: {image_path}, 错误: {e}")
                        continue  # 跳过无法读取的图像

            # 添加结果到列表
            results_summary.append({'Folder': folder + "_E4G3", 'DetectionCount': max_count})
            print(folder + "OK")

# 转换为DataFrame并保存为CSV
results_df = pd.DataFrame(results_summary)
results_df.to_csv(OUTPUT_CSV, index=False)

print(f"检测完成，结果已保存到 {OUTPUT_CSV}")



# 定义模型路径和主目录路径
MODEL_PATH = 'I:/李万万PC/LeafCounter/exp6/weights/best.pt'  # 替换为您的模型路径
ROOT_DIR = 'J:/第四次1011/3D/2021.10.14第四次拍摄第四次重复p'  # 替换为大写字母开头文件夹的主目录路径
OUTPUT_CSV = 'C:/Users/86188/Desktop/E4G4.csv'  # 输出汇总表格的路径

# 加载模型
model = torch.hub.load('ultralytics/yolov5', 'custom', path=MODEL_PATH)


# 检查大写字母开头的文件夹
def is_uppercase_folder(folder_name):
    return folder_name[0].isupper()


# 存储检测结果
results_summary = []

# 遍历大写字母开头的文件夹
for folder in os.listdir(ROOT_DIR):
    folder_path = os.path.join(ROOT_DIR, folder)

    if os.path.isdir(folder_path) and is_uppercase_folder(folder):
        photos_path = os.path.join(folder_path, 'Photos', '1')

        if os.path.exists(photos_path):
            max_count = 0

            # 遍历图片
            for image_file in os.listdir(photos_path):
                image_path = os.path.join(photos_path, image_file)

                if image_file.lower().endswith(('.jpg', '.jpeg', '.png')):
                    try:
                        # 确保图片能够打开
                        img = Image.open(image_path)
                        img.verify()  # 验证图片的完整性

                        # 对单张图片进行检测
                        results = model(image_path)
                        detections = results.xyxy[0]  # 获取检测结果
                        max_count = max(max_count, len(detections))

                    except (OSError, ValueError) as e:
                        print(f"无法读取图像: {image_path}, 错误: {e}")
                        continue  # 跳过无法读取的图像

            # 添加结果到列表
            results_summary.append({'Folder': folder + "_E4G4", 'DetectionCount': max_count})
            print(folder + "OK")

# 转换为DataFrame并保存为CSV
results_df = pd.DataFrame(results_summary)
results_df.to_csv(OUTPUT_CSV, index=False)

print(f"检测完成，结果已保存到 {OUTPUT_CSV}")