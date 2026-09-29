# importing the models and packages

from langchain_core.documents import Document
from langchain_core.vectorstores import InMemoryVectorStore
from langchain_ollama import OllamaEmbeddings, ChatOllama
from langchain_core.prompts import ChatPromptTemplate
from langchain_classic.chains.combine_documents import create_stuff_documents_chain


# importing data + functions from other python files
from data.eval_questions_dataset import eval_questions_dict, out_of_scope_dict
from data.categories_dict import categories_dict
import json
import csv


def parse_through_json_file(json_file_path):
    """
    Reads through the JSON file and outputs it in a readable and editable format

    Input:
    File Path: (str)

    Output:
    Data: (dict)
    """
    with open(json_file_path, "r") as f:
        return json.load(f)


# def parse_through_csv_file(csv_file_path):
#     data_contents = []

#     with open(csv_file_path, mode="r", newline="", encoding="utf-8") as file:
#         reader = csv.reader(file)

#         for row in reader:
#             data_contents.append(row)

#     return data_contents

# print(parse_through_csv_file("data/eval_questions.csv"))


def load_into_document_class(data_dict):
    """
    Loads the dictionary and converts the separate values for each key into a
    Document in preparation for the embedding model

    Input:
    Data Dictionary: dict

    Output:
    Documents: List[Document]
    """
    return [
        Document(page_content=values, metadata={"id": key})
        for key, values in data_dict.items()
    ]


def vectoriser(data, embedding_model):
    """
    Returns the vectorised version of any data

    Input:
    data : List[Document]
    embedding_model : an embeddings object (e.g. OllamaEmbeddings)

    Output:
    InMemoryVectorStore : vector store containing the embedded documents
    """
    return InMemoryVectorStore.from_documents(data, embedding_model)


def retrieve_chunks(query, retriever):
    """
    Runs the top_k retrieval for a query and returns the matching Documents.
    Use this in the evaluation loop, e.g.:
        ids = [d.metadata["id"] for d in retrieve_chunks(q, retriever)]

    Input:
    Query: (str)
    Retriever: LangChain retriever (contains the top_k setting)

    Output:
    List[Document]
    """
    return retriever.invoke(query)


def generate_answer(query, retrieved_chunks, prompt, llm):
    """
    Generates an answer from the LLM using the retrieved chunks as context.

    Output:
    Response: (str)
    """
    qa_chain = create_stuff_documents_chain(llm, prompt)
    return qa_chain.invoke({
        "input": query,
        "context": retrieved_chunks,
    })


def run_a_singular_query(query, retriever, prompt, llm):
    """
    Runs a SINGLE query through the baseline RAG model (input --> output) and
    prints the query, retrieved chunks and generated response.

    Input:
    Query: (str)
    Retriever: LangChain retriever (contains the top_k function)
    Prompt: ChatPromptTemplate (contains the main prompt given to the LLM)
    LLM: LangChain chat model

    Output:
    Response: (str) - also returned so it can be scored in evaluations
    """
    print(f"Query: {query}")

    retrieved_chunks = retrieve_chunks(query, retriever)

    print(f"Total chunks retrieved: {len(retrieved_chunks)}\n")

    for idx, doc in enumerate(retrieved_chunks):
        print(f"========= Top Match #{idx} =========")
        print(f"Content: {doc.page_content}")
        print(f"Metadata: {doc.metadata}\n")
        print("====================================")

    response = generate_answer(query, retrieved_chunks, prompt, llm)

    print("========== Generated Answer ==========")
    print(response)
    print("======================================")

    return response



def main():
    # main variables that can be tuned
    embedding_model = OllamaEmbeddings(model="nomic-embed-text", base_url="http://localhost:11434")
    llm = ChatOllama(model="llama3", temperature=0)

    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are a helpful assistant. Answer the user's question using ONLY the provided context. If you do not know the answer based on the context, say 'Unfortunately my database does not cover this data'\n\nContext:\n{context}"),
        ("human", "{input}"),
    ])

    query = "Who should be accredited for STCs?"

    # start the main function
    data_dict = parse_through_json_file("data/data_dict.json")
    documents = load_into_document_class(data_dict)
    vectorised_data = vectoriser(documents, embedding_model)

    # main area for hyper-parameter tuning
    retriever = vectorised_data.as_retriever(search_type="similarity", search_kwargs={"k": 3})

    # # run a SINGULAR query
    # run_a_singular_query(query, retriever, prompt, llm)

    """
    the main idea that I had was the following:

    we already have a working solution that runs the rag pipeline on one singular question. we could open the eval_question.csv file and go through each line
    and run the query on each of the questions in each line of the csv file. I think I can use the current functions to make this work
    the problem comes when I have to access the question in the database to drag out the expected anweser and the expected source documents

    so the final_eval_question_results.csv should look like this

    question id, question, expected anwser, expected source dpcuments, actual anwser, retrieved documents

    let me know if this kind of covers the required fields you need for the evaluation framework
    
    """


# if __name__ == "__main__":
#     main()



# data_contents = []

# with open("data/eval_questions.csv", mode="r", encoding="utf-8") as file:
#     reader = csv.DictReader(file)

#     for row in reader:
#         print(row)


import os

file_path = "data/eval_questions.csv"

if not os.path.exists(file_path):
    print("cant find the file")
else:
    print("i can find it youre just a dumbass")
