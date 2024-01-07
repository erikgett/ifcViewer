from translate import Translator


def translate_word(word):
    translator = Translator(from_lang='ru', to_lang='en')
    perevod = translator.translate(word)
    return perevod


def translate_prompt(prompt):
    words_list = prompt.split(',')
    out_promt = ''
    for w in words_list:
        out_promt += translate_word(w) + ", "
    return out_promt[:-2]


def add_lora(prompt):
    defaul_prompt = "<lora:XSarchitectural-38InteriorForBedroom_safetensors (1):1>"
    return defaul_prompt + prompt


# Добавляет в промт слова, которые улучшат итоговый результат
def correct_neg_prompt(neg_prompt):
    return neg_prompt


# Добавляем в промт слова, которые мы не хотим видеть на изображении
def correct_prompt(prompt):
    return prompt


if __name__ == "__main__":
    print(translate_prompt("Speak English, а по русски"))
