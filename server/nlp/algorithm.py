import os
import io
import re
import fitz
import pytesseract
import collections
import cv2
import docx
from PIL import Image
from deeppavlov import configs, build_model
from nltk.corpus import stopwords
from natasha import (
    Segmenter,
    MorphVocab,

    NewsEmbedding,
    NewsMorphTagger,
    NewsSyntaxParser,
    NewsNERTagger,

    NamesExtractor,

    Doc
)

segmenter = Segmenter()
morph_vocab = MorphVocab()
emb = NewsEmbedding()
morph_tagger = NewsMorphTagger(emb)
syntax_parser = NewsSyntaxParser(emb)
ner_tagger = NewsNERTagger(emb)
names_extractor = NamesExtractor(morph_vocab)

ner_model = build_model(configs.ner.ner_rus_bert, download=False)

russian_stopwords = stopwords.words("russian")
with open('stop_words.txt', 'r', encoding="utf-8") as file:
    for line in file:
        russian_stopwords.append(line.rstrip())


def main(doc, mode='default',file_name=None):
    data = process_document(doc=doc, mode=mode,file_name=file_name)
    return data


def process_document(doc, mode,file_name):
    if (file_name!=None):
        doc_type = file_name.split('.')[-1]
    else:
        doc_type = doc.name.split('.')[-1]
    if doc_type == 'docx':
        document = docx.Document(doc)
        text = ' '.join([paragraph.text for paragraph in document.paragraphs])
    elif doc_type == 'pdf':
        document = fitz.open(stream=doc.read(), filetype='pdf')
        text = ' '.join([page.getText("text") for page in document])

    original = text
    text = text.lower()
    if not text or not isscan(text):
        original = resolve_scan(document, doc_type=doc_type, text=original)
    data = process_text(original, mode)

    return data


def process_text(text, mode):
    original = text.replace('\n', ' ')
    text = original.lower()
    if (mode == 'default'):
        title_page = text[text.find('ульяновский'):text.find('введение')]
        dict = {
            'ФИО': find_full_name(text, original),
            'Факультет': find_faculty(title_page),
            'Кафедра': find_department(title_page),
            'Направление': find_direction(title_page),
            'Профиль': find_profile(title_page),
            'Тема ВКР': find_topic(title_page),
            'Частотный анализ слов': find_most_common_word(text)
        }
    else:
        dict = {'Частотный анализ слов': find_most_common_word(text)}

    return dict


def resolve_scan(document, doc_type, text):
    img_name = 'image1'
    if doc_type == 'docx':
        image2_info = []
        for r in document.part.rels.values():
            if isinstance(r._target, docx.parts.image.ImagePart) and ('{}.'.format(img_name) in r._target.partname):
                image2_info.append(r.rId)
                image2_info.append(os.path.basename(r._target.partname))
        image_part = document.part.related_parts[image2_info[0]]
        img = image_part.blob

        img = Image.open(io.BytesIO(img))
        img.save(image2_info[1])
        img = image2_info[1]
    elif doc_type == 'pdf':
        for img in document.getPageImageList(0):
            xref = img[0]
            pix = fitz.Pixmap(document, xref)
            pix1 = fitz.Pixmap(fitz.csRGB, pix)
            img = '{}.png'.format(img_name)
            pix1.writePNG(img)

    k1 = cv2.imread(img)
    gray = cv2.cvtColor(k1, cv2.COLOR_BGR2GRAY)

    text = pytesseract.image_to_string(gray, lang='rus') + ' ' + text

    return text


def isscan(text):
    if ('ульяновский' in text and
        'факультет' in text and
        'кафедра' in text) or (

            'ульян' in text and
            'факул' in text and
            'каф' in text):
        return True
    else:
        return False


def find_full_name(text, original):
    stud_name = original[text.find(
        'студент'):text.find('руководитель')].replace('_', '')
    if stud_name:
        result = ner_model([stud_name])
        if result:
            full_name = ' '.join(
                [result[0][0][i] for i, item in enumerate(result[1][0]) if item in ['I-PER', 'B-PER']])
            if full_name:
                return full_name
            else:
                return 'Error'
        else:
            return 'Error'
    else:
        return 'Error'


def find_faculty(text):
    faculties = re.findall(r"(?<=факультет ).*?(?=кафедра)", text)
    if faculties:
        return re.sub(r' {2,}', ' ', faculties[0])
    else:
        return 'Error'


def find_department(text):
    return find_smt(text=text, patterns=[], dict={1: ['кафедра', 'допус']})


def find_direction(text):
    return find_smt(text=text, patterns=[r"(?<=«).*?(?=»)"], dict={1: ['вление', 'проф'], 2: ['льность', 'студ']},
                    start='направление')


def find_profile(text):
    return find_smt(text=text, patterns=[r"(?<=«).*?(?=»)"], dict={1: ['филь', 'студ']}, start='профиль')


def find_topic(text):
    return find_smt(text=text,
                    patterns=[r"(?<=на тему «).*?(?=»)", r"(?<=на тему: «).*?(?=»)", r"(?<=на тему — «).*?(?=»)"],
                    dict={1: ['тема работы', 'студ']})


def find_smt(text, patterns, dict, start=None):
    if start:
        text = text[text.find(start):]
    for pattern in patterns:
        results = re.findall(pattern, text)
        if results:
            return results[0].strip()

    for value in dict.values():
        start_text = text.find(value[0])
        end_text = text.find(value[1])
        if (start_text != -1 and end_text != -1):
            result = text[start_text:end_text]
            return result.strip()

    return 'Error'


def find_most_common_word(text):
    if text:
        doc = Doc(text)
        doc.segment(segmenter)
        doc.tag_morph(morph_tagger)
        doc.parse_syntax(syntax_parser)
        doc.tag_ner(ner_tagger)

        for token in doc.tokens:
            token.lemmatize(morph_vocab)

        doc_words = []
        doc_words_normal = []
        for i in range(len(doc.tokens)):
            if (doc.tokens[i].pos in ['ADJ', 'NOUN']) and (len(doc.tokens[i].text) > 3) and (
                    doc.tokens[i].lemma.lower() not in russian_stopwords):
                doc_words.append(doc.tokens[i].lemma)
                doc_words_normal.append(doc.tokens[i].text)

        doc2_words = []
        normal_dict = {}

        for i in range(len(doc_words) - 1):
            doc2_words.append(doc_words[i] + ' ' + doc_words[i + 1])
            lemma = doc2_words[-1]
            normal = doc_words_normal[i] + ' ' + doc_words_normal[i + 1]
            normal_dict.update({lemma: normal})

        c2 = collections.Counter()

        for word in doc2_words:
            c2[word] += 1

        word_cloud = [normal_dict.get(word[0]) for word in c2.most_common(15)]
        print(word_cloud)

        return word_cloud
    else:
        return 'Error'
