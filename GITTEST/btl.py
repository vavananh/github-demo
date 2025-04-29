import cv2
import pytesseract
import argparse
import os
from PIL import Image
from docx import Document

# Tạo đối tượng tài liệu mới
document = Document()

# Thiết lập bộ phân tích đối số dòng lệnh
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required=True, help="Đường dẫn tới ảnh đầu vào")
ap.add_argument("-p", "--preprocess", type=str, default="thresh",
                help="Loại tiền xử lý ảnh: 'thresh' hoặc 'blur'")
args = vars(ap.parse_args())

# Đọc file ảnh và chuyển về ảnh xám
image = cv2.imread(args["image"])
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# Tiền xử lý ảnh
if args["preprocess"] == "thresh":
    gray = cv2.threshold(gray, 0, 255,
                         cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
elif args["preprocess"] == "blur":
    gray = cv2.medianBlur(gray, 3)

# Ghi tạm ảnh xuống ổ cứng để sau đó apply OCR
filename = "{}.png".format(os.getpid())
cv2.imwrite(filename, gray)

# Load ảnh và apply nhận dạng bằng Tesseract OCR
text = pytesseract.image_to_string(Image.open(filename), lang='vie')

# Xóa ảnh tạm sau khi nhận dạng
os.remove(filename)

# In dòng chữ nhận dạng được
print(text)
document.add_paragraph(text)
document.save('demo.docx')

# Hiển thị các ảnh chúng ta đã xử lý (nếu cần)
# cv2.imshow("Image", image)
# cv2.imshow("Output", gray)

# Đợi chúng ta gõ phím bất kỳ
cv2.waitKey(0)
