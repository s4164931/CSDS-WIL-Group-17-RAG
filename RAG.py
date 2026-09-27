# importing the models and packages

from langchain_core.documents import Document
from langchain_ollama import OllamaEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_ollama import OllamaEmbeddings, ChatOllama
from langchain_core.prompts import ChatPromptTemplate
from langchain_classic.chains.combine_documents import create_stuff_documents_chain


# importing data
from data.eval_questions_revised import eval_questions_dict, out_of_scope_dict
from data.categories_dict import categories_dict
import json


def parse_through_json_file(json_file_path):
    """
    Reads through a json file

    Input:
    file path: str

    Output:
    data: dict
    """
    with open(f"{json_file_path}", "r") as f:
        return json.load(f)


def load_into_document_class(data_dict):
    """
    loads the dictionary and converts the seperate values for each key into a document in preparation for the embedding model

    Input:
    data_dict: dict
    categories_dict: dict

    Output:
    documents: List[Document]
    """
    documents = [
        Document(page_content=values, metadata={"id":key})
        for key, values in data_dict.items()
    ]
    
    return documents 



def load_data_to_embed_model(data, embedding_model=OllamaEmbeddings(model="nomic-embed-text", base_url="http://localhost:11434")):
    """
    returns the vector conversion of the documents

    Input: 
    documents : List[Document]

    Output:
    List of the vectors: list
    """
    vector_db = FAISS.from_documents(data, embedding_model)
    return vector_db



if __name__ == "__main__":

    # can hyper parameter tune the temperature value
    llm = ChatOllama(model="llama3", temperature=0)

    data_dict = parse_through_json_file("data/data_dict.json")

    documents = load_into_document_class(data_dict)

    # consider saving this locally (writing up to a diff file)
    vector_db = load_data_to_embed_model(documents)

    retriever = vector_db.as_retriever(
    search_type="similarity",

    # hyper-parameter k tuning 
    search_kwargs={"k": 3}
    )

    query = "What isolation steps are required before starting installation?"
    print(f"Querying vector database: '{query}'\n")
    retrieved_chunks = retriever.invoke(query)

    print(f"Total chunks retrieved: {len(retrieved_chunks)}")
    for idx, doc in enumerate(retrieved_chunks, start=1):
        print(f"--- Top Match #{idx} ---")
        print(f"Content: {doc.page_content}")
        print(f"Metadata: {doc.metadata}\n")

    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are a helpful assistant. Answer the user's question using ONLY the provided context. If you do not know the answer based on the context, say 'I cannot find that in the documents.'\n\nContext:\n{context}"),
        ("human", "{input}"),
    ])

    qa_chain = create_stuff_documents_chain(llm, prompt)

    print("\n--- Llama 3 Generating Answer ---")
    response = qa_chain.invoke({
        "input": query,
        "context": retrieved_chunks
    })

    print(response)


    



