import streamlit as st

from langchain_ollama import OllamaEmbeddings, ChatOllama
from langchain_core.prompts import ChatPromptTemplate

from RAG import (
    parse_through_json_file,
    load_into_document_class,
    vectoriser,
    retrieve_chunks,
    generate_answer
)


# Page Configuration

st.set_page_config(
    page_title="Solar Installer RAG Assistant",
    page_icon="☀️",
    layout="wide"
)


# Header Section
st.title("☀️ Solar Installer RAG Assistant")

st.write(
    "Ask questions about solar installation, renewable energy "
    "requirements, standards, and regulations."
)

st.divider()


# Setup RAG
@st.cache_resource
def setup_rag():

    # Embedding model
    embedding_model = OllamaEmbeddings(
        model="nomic-embed-text",
        base_url="http://localhost:11434"
    )

    # LLM
    llm = ChatOllama(
        model="llama3",
        temperature=0
    )

    # Prompt
    prompt = ChatPromptTemplate.from_messages([
        (
            "system",
            "You are a helpful assistant. Answer the user's question "
            "using ONLY the provided context. If you do not know the "
            "answer based on the context, say "
            "'Unfortunately my database does not cover this data'\n\n"
            "Context:\n{context}"
        ),
        ("human", "{input}"),
    ])

    # Load knowledge base
    data_dict = parse_through_json_file(
        "data/data_dict.json"
    )

    documents = load_into_document_class(data_dict)

    # Create vector store
    vectorised_data = vectoriser(
        documents,
        embedding_model
    )

    # Create retriever
    retriever = vectorised_data.as_retriever(
        search_type="similarity",
        search_kwargs={"k": 5}
    )

    return retriever, prompt, llm


#Load RAG
retriever, prompt, llm = setup_rag()


# Question Input
question = st.text_area(
    "Enter your question:",
    placeholder="e.g. Who should be accredited for STCs?",
    height=120
)


# Ask Button
if st.button("Ask Question", type="primary"):

    if not question.strip():

        st.warning("Please enter a question.")

    else:

        with st.spinner("Searching the knowledge base..."):

            # Retrieve documents
            retrieved_chunks = retrieve_chunks(
                question,
                retriever
            )

            # Generate answer
            answer = generate_answer(
                question,
                retrieved_chunks,
                prompt,
                llm
            )


        # Answer Section
        st.subheader("Answer")

        st.write(answer)


        # Retrieved Sources Section
        st.subheader("Retrieved Sources")

        for index, document in enumerate(
            retrieved_chunks,
            start=1
        ):

            source_id = document.metadata.get(
                "id",
                "Unknown"
            )

            with st.expander(
                f"Source {index} — {source_id}"
            ):

                st.write(document.page_content)