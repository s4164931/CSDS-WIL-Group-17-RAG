import streamlit as st
import sys
sys.path.append("/users/lukegeorge/CSDS-WIL-Group-17-RAG")
import RAG

from langchain_ollama import OllamaEmbeddings, ChatOllama
from langchain_core.prompts import ChatPromptTemplate
# FIXME Hyperparameters need to still be chosen here!!!
llm = ChatOllama(model="llama3", temperature=0.5)
embedding_model = OllamaEmbeddings(model="nomic-embed-text", base_url="http://localhost:11434")

prompt = ChatPromptTemplate.from_messages([
        ("system", "You are a helpful assistant. Answer the user's question using ONLY the provided context. If you do not know the answer based on the context, say 'Unfortunately my database does not cover this data'\n\nContext:\n{context}"),
        ("human", "{input}"),
])

Parsed_data = RAG.parse_through_json_file("data/data_dict.json")
documents = RAG.load_into_document_class(Parsed_data)
vectorised_data = RAG.vectoriser(documents, embedding_model)
# FIXME Hyperparameters need to still be chosen here!!!
retriever = vectorised_data.as_retriever(search_type="similarity", search_kwargs={"k": 5})

user_query = st.text_input("Enter your query here")

results = RAG.run_a_singular_query(user_query, retriever, prompt, llm)

for i in results:
    st.write(i)

# ./.venv/bin/python -m streamlit run /Users/lukegeorge/CSDS-WIL-Group-17-RAG/webserver/streamlit_run.py