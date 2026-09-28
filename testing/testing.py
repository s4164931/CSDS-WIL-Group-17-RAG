import sys
import os

# Adds the root directory (one level up from 'testing') to Python's search path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


import RAG
from data.eval_questions_revised import eval_questions_dict, out_of_scope_dict
from data.categories_dict import categories_dict
from langchain_ollama import OllamaEmbeddings, ChatOllama
from langchain_core.prompts import ChatPromptTemplate
import json
import time
test = {}
llm = ChatOllama(model="llama3", temperature=0)

prompt = ChatPromptTemplate.from_messages([
            ("system", "You are a helpful assistant. Answer the user's question using ONLY the provided context. If you do not know the answer based on the context, say 'Unfortunately my database does not cover this data'\n\nContext:\n{context}"),
            ("human", "{input}"),
    ])
k_value = 3
print("————————————————————————————————————————————————————————————————————————————")
print("Known and inferrred questions.")
print("————————————————————————————————————————————————————————————————————————————")
start = time.time()
for i in eval_questions_dict:
    for j in eval_questions_dict[i]:
        for k in eval_questions_dict[i][j]:
            query = k["question"]
            Parsed_data = RAG.parse_through_json_file("data/data_dict.json")
            documents = RAG.load_into_document_class(Parsed_data)
            vectorised_data = RAG.vectoriser(documents)
            retriever = vectorised_data.as_retriever(search_type="similarity", search_kwargs={"k": k_value})
            results = RAG.run_a_singular_query(query, retriever, prompt, llm, testing = True)
            for value in results:
                print(value)
end = time.time()
print(f"Time taken: {end - start:.2f} seconds")

# k: 1, 2, 3, 5, 10?
# temperature: 0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1
# search_type: 

# "Testing by Luke George"