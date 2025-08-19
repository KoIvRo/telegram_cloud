import json
from collections import Counter
import numpy as np
import matplotlib.pyplot as plt
from wordcloud import WordCloud

colours = {"Красная": 'inferno', "Фиолетовая": 'magma', "Радужная": 'jet'}

count_words_in_heart = int(input("Количество слов в сердце (100+): "))
color = input(f"Цветовая гамма слов {colours.keys()}: ")
while color not in colours:
    color = input(f"Цветовая гамма слов {colours.keys()}: ")
color = colours[color]
count_words_to_print = int(input("Какое количество слов надо вывести: "))

with open("result.json", "r", encoding = "utf-8") as file:
    data = json.load(file)

words_counter = Counter()
system_word = {"stickersstickerwebp", "resappendchrlet",\
               "iostreamninclude", "matrixheight", "fstreamnusing",\
                "ifileinputtxtn", "selfcellsize", "eventtype",\
                "namespace", "customemoji", "documentid",\
                "return", "videofilessticker", "language",\
                "stickersanimatedsticker", "stickerssticker",\
                "textlink"}
alphabet = "абвгдеёжзийклмнопрстуфхцчшщъыьэюя"

for message in data["messages"]:
    if "text" in message and message["text"]:
        cleaned_text = ''.join(char for char in str(message["text"]).lower() if (char.isalpha() and char in alphabet ) or char == " ").lower().split()
        important_word = []

        for word in cleaned_text:
            if len(word) > 4 and word not in system_word:
                important_word.append(word)


        words_counter.update(important_word)

for word, count in words_counter.most_common(count_words_to_print):
    print(f"{word}: {count}")

x = np.linspace(-1.5, 1.5, 800)
y = np.linspace(-1.5, 1.5, 800)
X, Y = np.meshgrid(x, y)
mask = ((X**2 + Y**2 - 1)**3 - X**2 * (Y**3)) <= 0  
mask = np.where(mask, 0, 255).astype(np.uint8)
mask = np.flipud(mask)

wc = WordCloud(
    background_color = "white",
    max_words = count_words_in_heart,
    mask= mask,
    prefer_horizontal = 0.7,
    colormap = color
)

wc.generate_from_frequencies(words_counter)

plt.figure(figsize = (8, 8))
plt.imshow(wc, interpolation = "bilinear")
plt.axis("off")
plt.show()

wc.to_file("heart_words.png")