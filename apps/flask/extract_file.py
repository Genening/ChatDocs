import PyPDF2
import pytesseract
from PIL import Image
from bs4 import BeautifulSoup

# 设置tesseract.exe路径，注意要和安装的路径一致
pytesseract.pytesseract.tesseract_cmd = "C:\\Program Files\\Tesseract-OCR\\tesseract.exe"

# 解析pdf文件
def extract_pdf(filepath):
  text = ""
  # 打开PDF文件
  with open(filepath, 'rb') as file:
    # 创建PDF reader对象
    reader = PyPDF2.PdfReader(file)

    # 获取PDF文件页数
    num_pages = len(reader.pages)

    for i in range(num_pages):
      # 读取第i页
      page = reader.pages[i]

      # 提取文本
      text += f"\n\nPageNumber/页码: {i+1}" + page.extract_text()

  return text

# 解析图片文件
def extract_img(filepath):
  img = Image.open(filepath)
  img = img.convert('L')
  text = pytesseract.image_to_string(img, lang="eng+chi_sim")

  return text

# 解析html文件
def extract_html(filepath):
  with open(filepath, "r", encoding="utf-8") as f:
    soup = BeautifulSoup(f.read(), "html.parser")
    text = soup.get_text()

  return text

# 获取文件内容
def get_file_content(filepath):
  content = ""
  with open(filepath, "r", encoding="utf-8") as f:
    # 读取文本内容
    if filepath.endswith(".txt") or filepath.endswith(".md") or filepath.endswith(".docx") or filepath.endswith(".doc"):
      content += f.read()
    elif filepath.endswith(".pdf"):
      content += extract_pdf(filepath)
    elif filepath.endswith(".png") or filepath.endswith(".jpg") or filepath.endswith(".jpeg"):
      content += extract_img(filepath)
    elif filepath.endswith(".html"):
      content += extract_html(filepath)

  return content
