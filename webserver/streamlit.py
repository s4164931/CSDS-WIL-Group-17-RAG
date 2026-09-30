import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import RAG

import streamlit as st
from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama import ChatOllama, OllamaEmbeddings


st.set_page_config(page_title="Solar Pro Assistant", page_icon="☀️")
st.title("☀️ Solar Pro Assistant")
st.caption(
    "Ask a question about STC eligibility, accreditation, or installation "
    "compliance. Answers come only from our knowledge base of CER / SAA / "
    "CEC sources"
)


PROMPT = ChatPromptTemplate.from_messages([
    ("system",
     "You are a helpful assistant. Answer the user's question using ONLY "
     "the provided context. If you do not know the answer based on the "
     "context, say 'Unfortunately my database does not cover this data'"
     "\n\nContext:\n{context}"),
    ("human", "{input}"),
])

@st.cache_resource(show_spinner="Loading knowledge base...")
def load_pipeline():
    embedding_model = OllamaEmbeddings(model="nomic-embed-text", base_url="http://localhost:11434")
    data = RAG.parse_through_json_file("data/data_dict.json")
    documents = RAG.load_into_document_class(data)
    vector_store = RAG.vectoriser(documents, embedding_model)
    llm = ChatOllama(model="llama3", temperature=0.5)

    # FIXME Hyperparameters need to still be chosen here!!!
    retriever = vector_store.as_retriever(search_type="similarity", search_kwargs={"k": 5})
    return retriever, llm

retriever, llm = load_pipeline()


question = st.chat_input("Enter your query here")

if question:
    st.chat_message("user").write(question)

    with st.spinner("Loading..."):
        retrieved_docs = RAG.retrieve_chunks(question, retriever)
        answer = RAG.generate_answer(question, retrieved_docs, PROMPT, llm)

    with st.chat_message("assistant"):
        st.write(answer)
