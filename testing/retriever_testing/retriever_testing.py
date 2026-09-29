import sys
import os
# I can read this using this, but can others?
sys.path.append("/users/lukegeorge/CSDS-WIL-Group-17-RAG") 
import RAG
from data.eval_questions_dataset import eval_questions_dict, out_of_scope_dict
from data.categories_dict import categories_dict
from langchain_ollama import OllamaEmbeddings, ChatOllama
from langchain_core.prompts import ChatPromptTemplate
import json
import time

import ranx
import pandas as pd

# I can read this using this, but can others?
eval_questions = pd.read_csv("~/CSDS-WIL-Group-17-RAG/testing/retriever_testing/eval_questions.csv")

print("————————————————————————————————————————————————————————————————————————————")
print("Known and inferrred questions testing for hyperparameters.")
print("————————————————————————————————————————————————————————————————————————————")

k_value = [1, 2, 3, 5, 10]
temperature = [0, 0.2, 0.4, 0.5, 0.6, 0.8, 1]
search_type = ["similarity", "mmr"]
all_dataset = pd.DataFrame(columns = ["question_id", "query", "precision@k", "recall@k", "hit-rate@k", "mrr@k", "ndcg@k", "f1@k", "mean_total_eval_metrics_score@k", "k", "temperature", "search_type", "expected_answer", "expected_sources", "actual_sources_in_order"])
qrel_id_dict = {}
run_id_dict = {}
start = time.time()
count = 0

for temp in temperature:
    llm = ChatOllama(model="llama3", temperature=temp)
    embedding_model = OllamaEmbeddings(model="nomic-embed-text", base_url="http://localhost:11434")

    prompt = ChatPromptTemplate.from_messages([
            ("system", "You are a helpful assistant. Answer the user's question using ONLY the provided context. If you do not know the answer based on the context, say 'Unfortunately my database does not cover this data'\n\nContext:\n{context}"),
            ("human", "{input}"),
    ])
    for k in k_value:
        for search in search_type:
            for i in range(len(eval_questions)):
                question_id, query, expected_sources, expected_answer = eval_questions.iloc[i]
                run_id_dict[i] = {}
                qrel_id_dict[i] = {}
                Parsed_data = RAG.parse_through_json_file("data/data_dict.json")
                documents = RAG.load_into_document_class(Parsed_data)
                vectorised_data = RAG.vectoriser(documents, embedding_model)
                retriever = vectorised_data.as_retriever(search_type=search, search_kwargs={"k": k})
                results = RAG.run_a_singular_query(query, retriever, prompt, llm, testing = True)
                try:
                    expected_sources = [int(expected_sources)]
                    for test_value in expected_sources:
                        qrel_id_dict[i][str(test_value)] = 1
                    for value in results:
                        if type(value) == dict:
                            run_id_dict[i][value["id"]] = 1
                    actual_sources_in_order = []
                    for x in run_id_dict[i]:
                        if len(actual_sources_in_order) == 0: # I am building a reversed list so that I can reverse my dictionary
                            actual_sources_in_order.append(x)
                        else:
                            actual_sources_in_order.insert(0, x)
                    run_id_dict[i] = {}
                    for j in actual_sources_in_order:
                        run_id_dict[i][j] = 1 # reversing the list so MRR gives a proper output.
                    # Now, it is time to tackle the ranking scores: Precision, Recall, Hit-rate, MRR, NDCG and F1. (more if wanted)
                    qrels = ranx.Qrels(qrel_id_dict)
                    runs = ranx.Run(run_id_dict)
                    results = ranx.evaluate(qrels, run_id_dict, [f"precision@{k}", f"recall@{k}", f"hit_rate@{k}", f"mrr@{k}", f"ndcg@{k}", f"f1@{k}"])
                    mean_total_eval_metrics_score = (results[f"precision@{k}"] + results[f"recall@{k}"] + results[f"hit_rate@{k}"] + results[f"mrr@{k}"] + results[f"ndcg@{k}"] + results[f"f1@{k}"])/6
                    all_dataset.loc[count] = [question_id, query, results[f"precision@{k}"], results[f"recall@{k}"], results[f"hit_rate@{k}"], results[f"mrr@{k}"], results[f"ndcg@{k}"], results[f"f1@{k}"], mean_total_eval_metrics_score, k, temp, search, expected_answer, expected_sources, actual_sources_in_order]
                    del run_id_dict[i]
                    del qrel_id_dict[i]
                    count += 1
                except ValueError:
                    expected_sources = json.loads(expected_sources)
                    for test_value in expected_sources:
                        qrel_id_dict[i][str(test_value)] = 1
                    for value in results:
                        if type(value) == dict:
                            run_id_dict[i][value["id"]] = 1
                    actual_sources_in_order = []
                    for x in run_id_dict[i]:
                        if len(actual_sources_in_order) == 0: # I am building a reversed list so that I can reverse my dictionary
                            actual_sources_in_order.append(x)
                        else:
                            actual_sources_in_order.insert(0, x)
                    run_id_dict[i] = {}
                    for j in actual_sources_in_order:
                        run_id_dict[i][j] = 1 # reversing the list so MRR gives a proper output.
                    # Now, it is time to tackle the ranking scores: Precision, Recall, Hit-rate, MRR, NDCG and F1. (more if wanted)
                    qrels = ranx.Qrels(qrel_id_dict)
                    runs = ranx.Run(run_id_dict)
                    results = ranx.evaluate(qrels, run_id_dict, [f"precision@{k}", f"recall@{k}", f"hit_rate@{k}", f"mrr@{k}", f"ndcg@{k}", f"f1@{k}"])
                    mean_total_eval_metrics_score = (results[f"precision@{k}"] + results[f"recall@{k}"] + results[f"hit_rate@{k}"] + results[f"mrr@{k}"] + results[f"ndcg@{k}"] + results[f"f1@{k}"])/6
                    all_dataset.loc[count] = [question_id, query, results[f"precision@{k}"], results[f"recall@{k}"], results[f"hit_rate@{k}"], results[f"mrr@{k}"], results[f"ndcg@{k}"], results[f"f1@{k}"], mean_total_eval_metrics_score, k, temp, search, expected_answer, expected_sources, actual_sources_in_order]
                    del run_id_dict[i]
                    del qrel_id_dict[i]
                    count += 1

end = time.time()
print(f"Time taken: {end - start:.2f} seconds")

all_dataset.to_csv("ALL_RESULTS.csv")

# "Testing by Luke George"
# configuration.csv mean or median or weighted mean - mean
# I'm using mean because median might not show improvments to ther metrics
# Id number (c1k1), Question/query, evaluation metrics results, hyperparameters, expected answer, expected sources , actual sources.


