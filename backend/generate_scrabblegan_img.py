import base64
from io import BytesIO

from matplotlib import pyplot as plt
from ScrabbleGAN.config import Config
import pickle as pkl
from ScrabbleGAN.generate_images import ImgGenerator


config = Config
config.dataset = "IAM"
config.lexicon_file = 'ScrabbleGAN/words.txt'
config.num_chars = 74 

with open(f'ScrabbleGAN/IAM_char_map.pkl', 'rb') as f:
   char_map = pkl.load(f)

generator = ImgGenerator(checkpt_path=f'ScrabbleGAN/IAM_best_checkpoint.tar',
                         config=config, char_map=char_map)


def generate_image():
    generated_imgs, _, word_labels = generator.generate(random_num_imgs=1)
    image_data = image_to_base64(generated_imgs[0])
    result = {"label": word_labels[0], "image": image_data}
    print(result)
    return result

def image_to_base64(image_array):
    image_buffer = BytesIO()
    plt.imsave(image_buffer, image_array, format='png')
    base64_image = base64.b64encode(image_buffer.getvalue()).decode('utf-8')
    return base64_image
# def generate_image():
#     generated_imgs, _, word_labels = generator.generate(random_num_imgs=1)
#     result = {"label": word_labels[0], "image": generated_imgs[0].tolist()}
#     print(result)
#     return result

