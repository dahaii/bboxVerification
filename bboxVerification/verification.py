import cv2
import os
from tqdm import tqdm

# YOLO formatındaki bbox'ları çizme fonksiyonu
def draw_bboxes(img_path, txt_path, output_path):
    img = cv2.imread(img_path)
    height, width, _ = img.shape

    with open(txt_path, 'r') as file:
        lines = file.readlines()

    for line in lines:
        class_id, x_center, y_center, bbox_width, bbox_height = map(float, line.strip().split())

        # YOLO formatından piksel formatına dönüştürme
        x_center = int(x_center * width)
        y_center = int(y_center * height)
        bbox_width = int(bbox_width * width)
        bbox_height = int(bbox_height * height)

        # Rectangle koordinatlarını hesaplama
        x1 = int(x_center - bbox_width / 2)
        y1 = int(y_center - bbox_height / 2)
        x2 = int(x_center + bbox_width / 2)
        y2 = int(y_center + bbox_height / 2)

        # Rectangle çizimi
        cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)

    cv2.imwrite(output_path, img)

# Test örneği
source_folder = "C:/test/train"  # JPG ve TXT dosyalarının bulunduğu klasör
output_folder = os.path.join(source_folder, 'verification/')  # 'verification' klasörünü oluşturma

if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# Tüm TXT dosyalarını bulmak için listeleme
txt_files = [f for f in os.listdir(source_folder) if f.endswith('.txt')]

# İlerleme çubuğuyla işlemleri gerçekleştirme
for filename in tqdm(txt_files, desc="Processing images", unit="file"):
    img_filename = filename.replace('.txt', '.jpg')
    img_path = os.path.join(source_folder, img_filename)
    txt_path = os.path.join(source_folder, filename)
    output_path = os.path.join(output_folder, img_filename)

    draw_bboxes(img_path, txt_path, output_path)

print("İşlem tamamlandı! Tüm görseller 'verification' klasörüne kaydedildi.")
