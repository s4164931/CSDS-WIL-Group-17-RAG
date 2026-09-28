# importing the models and packages

from langchain_core.documents import Document
from langchain_ollama import OllamaEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_ollama import OllamaEmbeddings, ChatOllama
from langchain_core.prompts import ChatPromptTemplate
from langchain_classic.chains.combine_documents import create_stuff_documents_chain


# importing data + functions from other python files
from data.eval_questions_revised import eval_questions_dict, out_of_scope_dict
from data.categories_dict import categories_dict
import json


def parse_through_json_file(json_file_path):
    """
    Reads through the JSON file and outputs it in a readable and editable format

    Input:
    File Path: (str)

    Output:
    Data: (dict)
    """
    with open(f"{json_file_path}", "r") as f:
        return json.load(f)


def load_into_document_class(data_dict):
    """
    Loads the dictionary and converts the seperate values for each key into a document in preparation for the embedding model

    Input:
    Data Dictionary: dict

    Output:
    Documents: List[Document] (in Ollama formatting)
    """
    documents = [
        Document(page_content=values, metadata={"id":key})
        for key, values in data_dict.items()
    ]
    
    return documents 



def vectoriser(data, embedding_model=OllamaEmbeddings(model="nomic-embed-text", base_url="http://localhost:11434")):
    """
    Returns the vectorised version of any data

    Input: 
    data : List[Document]
    embedding_model : an embeddings object (default: model="nomic-embed-text" powered by Ollama)

    Output:
    FAISS : vector store containing the embedded documents
    """
    vectorised_data = FAISS.from_documents(data, embedding_model)
    return vectorised_data

def run_a_singular_query(query, retriever, prompt, llm):
    """
    Returns a SINGLE query response. Made to get a basic input --> output from the baseline RAG Model

    Input:
    Query: (str)
    Retriever: LangChain retriver (contains the top_k function)
    Prompt: ChatPromptTemplate (contains the main prompt given to the LLM)
    LLM: LangChain chat model 

    Output:
    Print statements of the following:
        Query
        Retrieved Chunks
        Generated Response
    """
    print(f"Query: {query}")

    # run the top_k algorithim on the query and generate the most similar chunks of data
    retrieved_chunks = retriever.invoke(query)

    print(f"Total chunks retrieved: {len(retrieved_chunks)}")

    for idx, doc in enumerate(retrieved_chunks):
        print(f"========= Top Match #{idx} =========")
        print(f"Content: {doc.page_content}")
        print(f"Metadata: {doc.metadata}\n")
        print(f"====================================")

    qa_chain = create_stuff_documents_chain(llm, prompt)

    response = qa_chain.invoke({
            "input": query,
            "context": retrieved_chunks
        })

    print(f"========== Generated Anwser ==========")
    print(response)
    print(f"======================================")


def main():
    # main variables that can be tuned
    llm = ChatOllama(model="llama3", temperature=0)

    prompt = ChatPromptTemplate.from_messages([
            ("system", "You are a helpful assistant. Answer the user's question using ONLY the provided context. If you do not know the answer based on the context, say 'Unfortunately my database does not cover this data'\n\nContext:\n{context}"),
            ("human", "{input}"),
    ])

    query = "Who should be accredited for STCs?"
    

    # start the main function
    data_dict = parse_through_json_file("data/data_dict.json")
    documents = load_into_document_class(data_dict)
    vectorised_data = vectoriser(documents)

    # main area for hyper-parameter tuning
    retriever = vectorised_data.as_retriever(search_type="similarity", search_kwargs={"k": 3})

    # run a SINGULAR query
    run_a_singular_query(query, retriever, prompt, llm)

if __name__ == "__main__":
     main()
