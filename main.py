from docx import Document


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
    document = Document('./Валитов-ВКР.docx'
                        '')
    for para in document.paragraphs:
        if para.text:
            a = para.text
            a = a.replace("+", "")
            a = a.replace("=", "")
            a = a.replace('.', "")
            a = a.replace(",", "")
            a = a.replace("}", "")
            a = a.replace("{", "")
            a = a.replace(";", "")
            a = a.replace("(", "")
            a = a.replace(")", "")
            for i in a.split(' '):
                if i:
                    yield i


dict = dict()
for i in list():
    try:
        dict[i] += 1
    except:
        dict[i] = 1

print({k: v for k, v in reversed(sorted(dict.items(), key=lambda item: item[1]))})
