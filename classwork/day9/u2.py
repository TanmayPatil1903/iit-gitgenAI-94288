from langchain_text_splitters import CharacterTextSplitter
from langchain_text_splitters import RecursiveCharacterTextSplitter
text_splitter = CharacterTextSplitter(chunk_size = 200,chunk_overlap = 20,separator = " ")
text_splitter = RecursiveCharacterTextSplitter(chunk_size = 200,chunk_overlap = 20,separators=[" ","\n","\n\n"])
text = [
    """A computer is a machine that can be programmed to automatically carry out sequences of arithmatic or logical operations(computation).modern digital electronic """
]
docs = text_splitter.create_documents(text)
print("type of docs:",type(docs))
print("num of docs:",len(docs))
doc = docs[0]
print("type of doc:",type(doc))
print("doc coontent:",doc.page_content)

