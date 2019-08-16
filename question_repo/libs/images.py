from PIL import Image

# ����pathͼ�������ͼ
def make_thumb(path, size):
    pixbuf = Image.open(path)
    width, height = pixbuf.size
    # �����ȴ���size
    if width > size:
        delta = width / size
        height = int(height / delta)
        pixbuf.thumbnail((size, height), Image.ANTIALIAS)
        return pixbuf