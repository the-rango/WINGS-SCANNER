from PIL import Image
import glob

images = []
for filename in glob.glob('*.png'):
    im=Image.open(filename)
    images.append(im)

images[0].save(
    "wings.pdf", "PDF" ,resolution=100.0, save_all=True, append_images=images[1:]
)
