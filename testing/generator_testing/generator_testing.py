import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

import RAG

try:
    from data.eval_questions_dataset import out_of_scope_dict
except ImportError:
    out_of_scope_dict = {}

from langchain_ollama import ChatOllama, OllamaEmbeddings
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.documents import Document
import csv
import ast

# settings

CONFIG_CSV = "testing/generator_testing/configuration.csv"
DATA_JSON_PATH = "data/data_dict.json"
TEMPERATURE_VALUES = [0.7, 1.0] # testing just these two as the others have already been parsed through overnight
LIMIT = None # number of questions to test
REPEATS = 3 # how many times to repeat each temperature (other than 0)
RESULTS_DIR = "testing/results"
os.makedirs(RESULTS_DIR, exist_ok=True)
REFUSAL_PHRASE = "does not cover this data"

# loading questions from the retrieval (question, k, search_type, temperature)

seen = {}
with open(CONFIG_CSV, newline="", encoding="utf-8") as f:
    for row in csv.DictReader(f):
        qid = row["question_id"]
        if qid not in seen:
            seen[qid] = row

questions = []
for qid, row in seen.items():
    questions.append({
        "id": qid,
        "question": row["query"],
        "expected": row["expected_answer"],
        "source_ids": [str(s) for s in ast.literal_eval(row["actual_sources_in_order"])],
    })

if LIMIT:
    questions = questions[:LIMIT]

ood_questions = list(out_of_scope_dict.values())[:LIMIT] if LIMIT else list(out_of_scope_dict.values())

print(f"Testing {len(questions)} in-scope questions" + (f" + {len(ood_questions)} out-of-scope questions" if ood_questions else ""))

# building the context for each question from each actual_sources_in_order

passages = RAG.parse_through_json_file(DATA_JSON_PATH)

contexts = {}
for q in questions:
    docs = []
    for source_id in q["source_ids"]:
        if source_id not in passages:
            print(f"warning: {q['id']} references passage {source_id}, not found in {DATA_JSON_PATH}")
            continue
        docs.append(Document(page_content=passages[source_id], metadata={"id": source_id}))
    contexts[q["id"]] = docs

# handling out of scope/document questions

ood_retriever = None
if ood_questions:
    embedding_model = OllamaEmbeddings(model="nomic-embed-text", base_url="http://localhost:11434")
    all_documents = RAG.load_into_document_class(passages)
    vectorised_data = RAG.vectoriser(all_documents, embedding_model)
    ood_retriever = vectorised_data.as_retriever(search_type="similarity", search_kwargs={"k": 5})

# judges

judge_llm = ChatOllama(model="llama3", temperature=0, num_ctx=8192)

# im judging whether the generated answer is factually correct compared to the expected answer

correctness_judge_prompt = ChatPromptTemplate.from_messages([
    (
        "system",
        """You are checking whether a generated answer is factually correct.
Compare the generated answer to the expected answer.

Judge the meaning of the generated answer, not whether it uses the same wording as the expected answer.
The generated answer should be marked YES if it reaches the same factual conclusion as the expected answer, even if it uses different wording or gives a more detailed explanation.

Do not require the generated answer to contain the same words or phrases as the expected answer.

Answer ONLY with:
YES - the generated answer conveys the same correct information
NO - the generated answer is missing or wrong

Do not explain your answer."""
    ),
    (
        "human",
        """Question:
{question}

Expected answer:
{expected}

Generated answer:
{answer}"""
    )
])
correctness_judge_chain = correctness_judge_prompt | judge_llm

# judging whether the generated answer is actually supported by the retrieved context

faithfulness_judge_prompt = ChatPromptTemplate.from_messages([
    (
        "system",
        """You are checking whether a generated answer is supported by the provided context.

Judge only whether the claims made in the generated answer are supported by the context.

Answer YES if the generated answer is fully supported by the context.
Answer NO if the generated answer contains claims that are unsupported or contradicted by the context.

Do not judge whether the answer matches an expected answer.
Do not judge the quality or wording of the answer.

Answer ONLY with:
YES
or
NO

Do not explain your answer."""
    ),
    (
        "human",
        """Context:
{context}

Generated answer:
{answer}"""
    )
])
faithfulness_judge_chain = faithfulness_judge_prompt | judge_llm

def is_refusal(answer):
    return REFUSAL_PHRASE in answer.lower()

def judge_yes(chain, inputs):
    result = chain.invoke(inputs)
    return result.content.strip().upper().startswith("YES")

# main generation prompt

prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful assistant. Answer the user's question using ONLY the provided context. If you do not know the answer based on the context, say 'Unfortunately my database does not cover this data'\n\nContext:\n{context}"),
    ("human", "{input}"),
])

def score_one_answer(question, expected, answer, context_text):
    effective = not is_refusal(answer)
    faithful = judge_yes(faithfulness_judge_chain, {"context": context_text, "answer": answer})
    correct = judge_yes(correctness_judge_chain, {"question": question, "expected": expected, "answer": answer})
    return {"effective": effective, "faithful": faithful, "correct": correct}

def run_setting(label, temperature, csv_writer, qualitative_log, repeat_num):
    llm = ChatOllama(model="llama3", temperature=temperature, num_ctx=8192)

    rows = []
    for i, q in enumerate(questions):
        docs = contexts[q["id"]]
        context_text = "\n\n".join(d.page_content for d in docs)
        answer = RAG.generate_answer(q["question"], docs, prompt, llm)
        scores = score_one_answer(q["question"], q["expected"], answer, context_text)
        rows.append(scores)

        csv_writer.writerow([label, temperature, repeat_num, q["id"], q["question"], q["expected"], answer, scores["effective"], scores["faithful"], scores["correct"]])

        if i < 3 and repeat_num == 0:
            qualitative_log.append({
                "label": label,
                "question": q["question"],
                "expected": q["expected"],
                "answer": answer,
                **scores
            })

    ood_refusals = 0
    for question in ood_questions:
        retrieved = RAG.retrieve_chunks(question, ood_retriever)
        answer = RAG.generate_answer(question, retrieved, prompt, llm)
        if is_refusal(answer):
            ood_refusals += 1
        csv_writer.writerow([label, temperature, repeat_num, "ood", question, "(out-of-scope)", answer, "", "", ""])

    n = len(rows)
    return {
        "label": label, "temperature": temperature, "repeat": repeat_num,
        "effectiveness": sum(r["effective"] for r in rows) / n,
        "faithfulness": sum(r["faithful"] for r in rows) / n,
        "correctness": sum(r["correct"] for r in rows) / n,
        "ood_refusal_rate": (ood_refusals / len(ood_questions)) if ood_questions else None,
    }

# averaging the metrics across repeats of the same temp

def average_repeats(runs):
    n = len(runs)
    avg = {"label": runs[0]["label"], "temperature": runs[0]["temperature"], "repeats": n}
    for metric in ["effectiveness", "faithfulness", "correctness", "ood_refusal_rate"]:
        values = [r[metric] for r in runs if r[metric] is not None]
        if values:
            avg[metric] = sum(values) / len(values)
            avg[f"{metric}_range"] = max(values) - min(values)
        else:
            avg[metric] = None
            avg[f"{metric}_range"] = None
    return avg

def print_summary(rows):
    print(f"\n{'setting':<16}{'repeats':>8}{'effectiveness':>15}{'faithfulness':>15}{'correctness':>13}{'ood_refusal':>13}")
    for r in rows:
        ood = f"{r['ood_refusal_rate']:.0%}" if r["ood_refusal_rate"] is not None else "n/a"
        print(f"{r['label']:<16}{r['repeats']:>8}{r['effectiveness']:>15.0%}{r['faithfulness']:>15.0%}{r['correctness']:>13.0%}{ood:>13}")

SUMMARY_FIELDS = ["label", "temperature", "repeats", "effectiveness", "effectiveness_range",
                  "faithfulness", "faithfulness_range", "correctness", "correctness_range",
                  "ood_refusal_rate", "ood_refusal_rate_range"]
answer_log_path = f"{RESULTS_DIR}/generator_testing_answers.csv"
qualitative = []

with open(answer_log_path, "a", newline="", encoding="utf-8") as f:
    log = csv.writer(f)

    # test: temperature

    print("\n============================")
    print("Testing Temperature")

    t_results = []
    for temperature in TEMPERATURE_VALUES:
        n_repeats = 1 if temperature == 0 else REPEATS
        print(f"\nTemperature = {temperature}  ({n_repeats} run{'s' if n_repeats > 1 else ''})")

        runs = []
        for repeat_num in range(n_repeats):
            runs.append(run_setting(f"T={temperature}", temperature, log, qualitative, repeat_num))
        t_results.append(average_repeats(runs))

    print_summary(t_results)
    with open(f"{RESULTS_DIR}/temperature_results.csv", "a", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=SUMMARY_FIELDS)
        writer.writeheader()
        writer.writerows(t_results)

print(f"\nsaved: {RESULTS_DIR}/temperature_results.csv, {answer_log_path}")

# quick qualitative check

print("\nFirst few answers kept for qualitative review:")
print(f"Number of qualitative results: {len(qualitative)}")

for row in qualitative[:6]:
    print(f"\n{'='*80}")
    print(f"[{row['label']}]")
    print(f"QUESTION: {row['question']}")
    print(f"\nEXPECTED ANSWER:\n{row['expected']}")
    print(f"\nGENERATED ANSWER:\n{row['answer']}")
    print(f"\nRESULTS:")
    print(f"  effective={row['effective']}")
    print(f"  faithful={row['faithful']}")
    print(f"  correct={row['correct']}")