import os
from win32com import client

def create_Excel(word_path,Excel_path):
    """
    :param word_path:word路经
    :param Excel_path: excel路径
    :return:
    """

    word=client.Dispatch("word.Application")
    doc=word.Documents.Open(word_path)
    doc.SaveAs(Excel_path)
    word.Quit()

base_path=os.path.dirname(os.path.abspath(__file__))
# create_Excel(os.path.join(base_path,"xxx.excel"),os.path.join(base_path))
word_file=[]
for f in os.listdir("."):
    if f.endswith((".docx")):
        word_file.append(f)

for i in word_file:
    word_path=os.path.abspath(i)
    print(word_path)
    index=word_path.rindex(".")
    excel_path=word_path[:index]+".docx"
    print(excel_path)
    create_Excel(word_path,excel_path)


