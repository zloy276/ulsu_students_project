import docx
from natasha import (
    Segmenter,

    NewsEmbedding,
    NewsMorphTagger,
    NewsSyntaxParser,

    Doc, MorphVocab
)


#
# def getText(filename):
#     doc = Document(filename)
#     fullText = []
#     for para in doc.paragraphs:
#         if fullText:
#             fullText[-1] += para.text
#         else:
#             fullText.append('')
#     return '\n'.join(fullText)
#
# a = getText("./Валитов-ВКР.docx")
# for i in a:
#     print(i)
#


def list():
    emb = NewsEmbedding()
    document = docx.Document('Валитов-ВКР.docx')
    text = '\n'.join([para.text for para in document.paragraphs])

    segmenter = Segmenter()
    doc = Doc(text)
    doc.segment(segmenter)

    morph_tagger = NewsMorphTagger(emb)
    doc.tag_morph(morph_tagger)

    morph_vocab = MorphVocab()
    for token in doc.tokens:
        token.lemmatize(morph_vocab)
    for token in doc.tokens:
        yield token.lemma


dict = dict()
for i in list():
    try:
        dict[i] += 1
    except:
        dict[i] = 1

print({k: v for k, v in reversed(sorted(dict.items(), key=lambda item: item[1]))})
