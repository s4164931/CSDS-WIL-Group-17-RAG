import pandas as pd

all_data = pd.read_csv("~/CSDS-WIL-Group-17-RAG/ALL_RESULTS.csv", index_col = 0)
configuration = pd.DataFrame(columns = ["question_id", "query", "precision@k", "recall@k", "hit-rate@k", "mrr@k", "ndcg@k", "f1@k", "mean_total_eval_metrics_score@k", "k", "temperature", "search_type", "expected_answer", "expected_sources", "actual_sources_in_order"])
group_vals = all_data.groupby(["question_id"])
count = 0
for i in group_vals:
    max_value = i[1]["mean_total_eval_metrics_score@k"].max()
    index_of_max_data = all_data[(all_data["question_id"] == i[0][0]) & (all_data["mean_total_eval_metrics_score@k"] == max_value)].index
    good_hyperparameters = all_data.loc[index_of_max_data]
    for entry in range(len(good_hyperparameters)):
        configuration.loc[count] = good_hyperparameters.iloc[entry]
        count += 1
configuration.to_csv("~/CSDS-WIL-Group-17-RAG/testing/generator_testing/configuration.csv", index = False)