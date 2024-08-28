import cv2
import os
from tqdm import tqdm

# Her label için farklı renkler
label_colors = {
    0: (0, 255, 0),  # Yeşil
    1: (255, 0, 0),  # Mavi
    2: (0, 0, 255)  # Kırmızı
}


# YOLO formatındaki bbox'ları çizme fonksiyonu
def draw_bboxes(img_path, txt_path, output_path):
    img = cv2.imread(img_path)

    if img is None:
        print(f"Error: Unable to read image {img_path}. Skipping...")
        return

    height, width, _ = img.shape

    if not os.path.exists(txt_path):
        print(f"Error: {txt_path} does not exist. Skipping...")
        return

    with open(txt_path, 'r') as file:
        lines = file.readlines()

    if not lines:
        print(f"Warning: {txt_path} is empty. Skipping...")
        return

    for line in lines:
        try:
            class_id, x_center, y_center, bbox_width, bbox_height = map(float, line.strip().split())
        except ValueError:
            print(f"Error: Invalid bbox format in {txt_path}. Skipping...")
            return

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

        # Doğru rengi seçmek
        color = label_colors.get(int(class_id), (255, 255, 255))  # Label yoksa beyaz renk kullan

        # Rectangle çizimi
        cv2.rectangle(img, (x1, y1), (x2, y2), color, 2)

    cv2.imwrite(output_path, img)


# Test örneği
source_folder = "C:/deneme/test/mix/train"  # JPG ve TXT dosyalarının bulunduğu klasör
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
