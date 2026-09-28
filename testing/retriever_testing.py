import sys
import os

# Adds the root directory (one level up from 'testing') to Python's search path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import RAG
from data.eval_questions_dataset import eval_questions_dict, out_of_scope_dict
from data.categories_dict import categories_dict
from langchain_ollama import OllamaEmbeddings, ChatOllama
from langchain_core.prompts import ChatPromptTemplate
import json
import time
k_value = 5
def Precision_at_k(predicted, expected, question_type): # should precision only be looking at right things selected? 
    #Even if k is higher than number of source ids?
    True_positive = 0
    true_and_false_positives = 0
    if question_type == "known":
        expected = [expected]
        for i in predicted["id"]:
            if int(i) in expected:
                True_positive += 1
                true_and_false_positives += 1
            else:
                true_and_false_positives += 1
 #               True_positive = 1
 #               true_and_false_positives = 1
 #               break
 #           else:
 #               continue
    else:
        for i in predicted["id"]:
            if int(i) in expected:
                True_positive += 1
                true_and_false_positives += 1
            else:
                true_and_false_positives += 1
#            if True_positive == len(expected):
#                true_and_false_positives = True_positive # 100% precision, as in, all the documents were found
#                break
    if true_and_false_positives == 0:
        precision = 0.0
    else:
        precision = True_positive/true_and_false_positives
    return precision

test = {}
llm = ChatOllama(model="llama3", temperature=0)

prompt = ChatPromptTemplate.from_messages([
            ("system", "You are a helpful assistant. Answer the user's question using ONLY the provided context. If you do not know the answer based on the context, say 'Unfortunately my database does not cover this data'\n\nContext:\n{context}"),
            ("human", "{input}"),
    ])
print("————————————————————————————————————————————————————————————————————————————")
print("Known and inferrred questions.")
print("————————————————————————————————————————————————————————————————————————————")
data_id_dict = {}
temp_list = []
start = time.time()
for i in eval_questions_dict:
    id_type = i
    for j in eval_questions_dict[i]:
        question_type = j
        for k in eval_questions_dict[i][j]:
            query = k["question"]
            Parsed_data = RAG.parse_through_json_file("data/data_dict.json")
            documents = RAG.load_into_document_class(Parsed_data)
            vectorised_data = RAG.vectoriser(documents)
            retriever = vectorised_data.as_retriever(search_type="similarity", search_kwargs={"k": k_value})
            results = RAG.run_a_singular_query(query, retriever, prompt, llm, testing = True)
            print(k)
            expected_sources = k["source_id"]
            for value in results:
                if type(value) == dict:
                    temp_list.append(value["id"])
                else:
                    answer = value
            data_id_dict["id"] = temp_list
            temp_list = []
            # Now, it is time to tackle the ranking scores: Precision, Recall, Hit-rate, MRR and NDCG. (more if wanted)
            print(Precision_at_k(data_id_dict, expected_sources, question_type))

end = time.time()
print(f"Time taken: {end - start:.2f} seconds")

# k: 1, 2, 3, 5, 10?
# temperature: 0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1
# search_type: 

# @k - known questions only have 1, inferred have more?

# "Testing by Luke George"