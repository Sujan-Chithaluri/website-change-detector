try:
    from PIL import Image
except ImportError:
    import Image
import pytesseract

def ocr_core(filename):
    pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
    custom_config = r'--oem 3 --psm 6'
    img=Image.open(filename)
    # img.show()
    text = pytesseract.image_to_string(img)  # We'll use Pillow's Image class to open the image and pytesseract to detect the string in the image
    return text


# path1=r'C:\Users\DELL\VII Sem\Major Project\static\original-old\\'
# path1=path1+'google.png'
# print(ocr_core(path1))