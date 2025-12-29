import chromadb
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.document_loaders import DirectoryLoader, PyPDFLoader
from langchain.chat_models import init_chat_model
import streamlit as st  
st.title("resume analysis using RAG...")
#embedding model
embed_model = HuggingFaceEmbeddings(model_name="sentence-transformers/paraphrase-MiniLM-L3-v2")
client = chromadb.Client(settings=chromadb.Settings(persist_directory="./chroma_db"))
collection = client.get_or_create_collection(name = "demo")
#load docs
loader = DirectoryLoader(
    path=r"D:\task2\iit-gitgenAI-94288\fake-resumes",
    glob="*.pdf",    
    loader_cls=PyPDFLoader
)
documents = loader.load()
#metadata
for doc in documents:
        doc.metadata["pdf_name"] = doc.metadata["source"].split("/")[-1]
        doc.metadata["page_number"] = doc.metadata["page"] + 1
#chunking
splitter = RecursiveCharacterTextSplitter(
        chunk_size = 800,
        chunk_overlap = 50,
        separators=[" ","\n","\n\n"]
)
chunks = splitter.split_documents(documents=documents)
# metadata for chunking
texts = []
metadata = []
ids = []
for idx, chunk in enumerate(chunks):
    texts.append(chunk.page_content)
    chunk.metadata["chunk_id"] = str(idx)
    chunk.metadata["chunk_size"] = len(chunk.page_content)
    metadata.append(chunk.metadata)
    ids.append(str(idx))
embeddings = embed_model.embed_documents(texts)
#Add to Chroma DB
collection.add(ids=ids,documents=texts,embeddings=embeddings,metadatas=metadata)
print("Document successfully added in chroma db")
#Read 
query = st.text_input("Enter your query regarding resumes :")
query_embedding = embed_model.embed_query(query)
results = collection.query(query_embeddings=[query_embedding],n_results=3)
#results
for doc,meta in zip(results["documents"][0],results["metadatas"][0]):
    print("\n Metadata:", meta)
    print("Content:", doc[:300], "...")

llm = init_chat_model(
    model = "phi-3-mini-4k-instruct",
    model_provider="openai",
    base_url = "http://127.0.0.1:1234/v1",
    api_key = "not-needed"
)
llm_prompt = f"""
    User Query:
    {query}

Resume Context:
    {results}

Instruction:
From the resume context above, extract the names of candidates whose profiles
best match the user query.

Return the result as:
- process and give result for an input for the query
- No explanations
- No extra text
- Give result as only original content of data
- Give me a result in one sentence
"""
result = llm.invoke(llm_prompt)
st.write(result.content)