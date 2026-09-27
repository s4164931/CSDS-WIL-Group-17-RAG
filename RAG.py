from langchain_core.documents import Document
from langchain_ollama import OllamaEmbeddings
from langchain_core.vectorstores import InMemoryVectorStore


## LOAD

## for whoevers constructing the categories in the database, could you put the categories in this dictionary above ^^
## just sort of structured like 1: standards, 2: STC claims, etc. for all 48 points of data
## found out this impacts how the loading section is structured, so ive made it considering that these are filled out, but should also work if only some are, just will be abit more general.


documents = []
skipped = []

for i, passage in data_dict.items():
    if not passage.strip():
        skipped.append(i)
        continue

    category = categories_dict.get(i, "general")

    documents.append(
        Document(
            page_content=f"[{category}] {passage}",
            metadata={"id": i, "category": category, "question": eval_questions_dict.get(i, "")}
        )
    )

## categories are empty as of now

print(f"Loaded {len(documents)} documents, skipped {len(skipped)}: {skipped}")

## EMBED


embeddings = OllamaEmbeddings(model="nomic-embed-text") 

## i think we'll all have to each download ollama and nomic add-on on our devices locally, ill put that in the readme

## STORE


vector_store = InMemoryVectorStore(embeddings)
vector_store.add_documents(documents=documents)
print(f"Indexed {len(documents)} documents.")

## just stored on the RAM in memory ^^