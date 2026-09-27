# importing the models and packages

from langchain_core.documents import Document
from langchain_ollama import OllamaEmbeddings
from langchain_core.vectorstores import InMemoryVectorStore


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
    embedding_model = OllamaEmbeddings(model="nomic-embed-text") 
    vector_store = InMemoryVectorStore(embedding_model)
    return vector_store.add_documents(documents=data)



if __name__ == "__main__":
    data_dict = parse_through_json_file("data/data_dict.json")

    documents = load_into_document_class(data_dict)

    # consider saving this locally (writing up to a diff file)
    vectors_data = load_data_to_embed_model(documents)

    



