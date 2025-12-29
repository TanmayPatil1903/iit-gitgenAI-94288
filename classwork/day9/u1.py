from langchain.embeddings import init_embeddings
embed_model = init_embeddings(
    model = "second-state/All-MiniLM-L6-v2-Embedding-GGUF",
    provider = "openai",
    base_url= "http://127.0.0.1:1234/v1",
    api_key = "not-needed",
    check_embedding_ctx_length = False
)
sentences = [
    "I like Artificial Intelligece",
    "Generative AI is magnificant",
    "world is amazing"
]
embeddings = embed_model.embed_documents(sentences)
for embedding in embeddings:
    print(f"Len = {len(embedding)} --> {embedding[:4]}")
    