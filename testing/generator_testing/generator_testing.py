import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
import RAG

from data.eval_questions_dataset import eval_questions_dict
try:
    from data.eval_questions_dataset import out_of_scope_dict
except ImportError:
    out_of_scope_dict = {}  # skips the OOD test if this dict doesn't exist yet

from langchain_ollama import ChatOllama, OllamaEmbeddings
from langchain_core.prompts import ChatPromptTemplate
from langchain_classic.chains.combine_documents import (create_stuff_documents_chain)
import csv

# settings

K = 5

TEMPERATURE_VALUES = [0, 0.3, 0.7, 1.0]

LIMIT = 5  # number of questions to test

RESULTS_DIR = "testing/results"
os.makedirs(RESULTS_DIR, exist_ok=True)

REFUSAL_PHRASE = "does not cover this data"

# loading questions specifically for testing

questions = []

for category in eval_questions_dict:
    for question_type in eval_questions_dict[category]:
        for item in eval_questions_dict[category][question_type]:
            questions.append({
                "question": item["question"],
                "expected": item.get(
                    "expected_answer",
                    item.get("expected_anwser", "")  # fixed: was checking "expected_answer" twice
                )
            })

if LIMIT:
    questions = questions[:LIMIT]

ood_questions = list(out_of_scope_dict.values())[:LIMIT] if LIMIT else list(out_of_scope_dict.values())

print(f"Testing {len(questions)} in-scope questions" + (f" + {len(ood_questions)} out-of-scope questions" if ood_questions else ""))

# loading data

embedding_model = OllamaEmbeddings(model="nomic-embed-text", base_url="http://localhost:11434")

parsed_data = RAG.parse_through_json_file("data/data_dict.json")
documents = RAG.load_into_document_class(parsed_data)
vectorised_data = RAG.vectoriser(documents, embedding_model)

# judges

judge_llm = ChatOllama(model="llama3", temperature=0, num_ctx=8192)

# judges whether the generated answer is factually correct, compared to the expected answer
correctness_judge_prompt = ChatPromptTemplate.from_messages([
    (
        "system",
        """You are checking whether a generated answer is factually correct.
Compare the generated answer to the expected answer.

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

# judges whether the generated answer is actually supported by the retrieved context
faithfulness_judge_prompt = ChatPromptTemplate.from_messages([
    (
        "system",
        """You are checking whether a generated answer is fully supported by the given context.
The answer should not contain any claim, number or detail that isn't in the context.

Answer ONLY with:
YES - every part of the answer is supported by the context
NO - the answer contains something not in the context

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


def score_one_answer(question, expected, answer, context):
    # effectiveness is a free string check, faithfulness and correctness each cost one judge call
    effective = not is_refusal(answer)
    faithful = judge_yes(faithfulness_judge_chain, {"context": context, "answer": answer})
    correct = judge_yes(correctness_judge_chain, {"question": question, "expected": expected, "answer": answer})
    return {"effective": effective, "faithful": faithful, "correct": correct}


def run_setting(label, temperature, csv_writer, qualitative_log):
    llm = ChatOllama(model="llama3", temperature=temperature, num_ctx=8192)
    qa_chain = create_stuff_documents_chain(llm, prompt)

    rows = []
    for i, q in enumerate(questions):
        docs = vectorised_data.similarity_search(q["question"], k=K)
        context = "\n\n".join(doc.page_content for doc in docs)
        answer = qa_chain.invoke({"input": q["question"], "context": docs})
        scores = score_one_answer(q["question"], q["expected"], answer, context)
        rows.append(scores)
        csv_writer.writerow([label, temperature, q["question"], q["expected"], answer,
                             scores["effective"], scores["faithful"], scores["correct"]])
        if i < 3:  # keep the first 3 answers per setting for the qualitative write-up
            qualitative_log.append({"label": label, "question": q["question"], "answer": answer, **scores})

    ood_refusals = 0
    for question in ood_questions:
        docs = vectorised_data.similarity_search(question, k=K)
        answer = qa_chain.invoke({"input": question, "context": docs})
        if is_refusal(answer):
            ood_refusals += 1
        csv_writer.writerow([label, temperature, question, "(out-of-scope)", answer, "", "", ""])

    n = len(rows)
    return {
        "label": label, "temperature": temperature,
        "effectiveness": sum(r["effective"] for r in rows) / n,
        "faithfulness": sum(r["faithful"] for r in rows) / n,
        "correctness": sum(r["correct"] for r in rows) / n,
        "ood_refusal_rate": (ood_refusals / len(ood_questions)) if ood_questions else None,
    }


def print_summary(rows):
    print(f"\n{'setting':<16}{'effectiveness':>15}{'faithfulness':>15}{'correctness':>13}{'ood_refusal':>13}")
    for r in rows:
        ood = f"{r['ood_refusal_rate']:.0%}" if r["ood_refusal_rate"] is not None else "n/a"
        print(f"{r['label']:<16}{r['effectiveness']:>15.0%}{r['faithfulness']:>15.0%}{r['correctness']:>13.0%}{ood:>13}")


SUMMARY_FIELDS = ["label", "temperature", "effectiveness", "faithfulness", "correctness", "ood_refusal_rate"]
answer_log_path = f"{RESULTS_DIR}/generator_testing_answers.csv"
qualitative = []

with open(answer_log_path, "w", newline="", encoding="utf-8") as f:
    log = csv.writer(f)
    log.writerow(["label", "temperature", "question", "expected", "answer", "effective", "faithful", "correct"])

    # test: temperature (K fixed at 5)

    print("\n==============================")
    print(f"Testing Temperature (K={K})")

    t_results = []
    for temperature in TEMPERATURE_VALUES:
        print(f"\nTemperature = {temperature}")
        result = run_setting(f"T={temperature}", temperature, log, qualitative)
        t_results.append(result)

    print_summary(t_results)
    with open(f"{RESULTS_DIR}/temperature_results.csv", "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=SUMMARY_FIELDS)
        writer.writeheader()
        writer.writerows(t_results)

print(f"\nsaved: {RESULTS_DIR}/temperature_results.csv, {answer_log_path}")

# qualitative notes (optional, light) - the 3 answers kept per setting are in `qualitative` and in the CSV
# above. read a handful by hand and write 1-2 sentences per setting for the report, e.g. "at T=1.0 two
# answers stated a number not in the context". not scored - just evidence for why the numbers moved.

print("\nFirst few answers kept for qualitative review:")
for row in qualitative[:6]:
    print(f"\n[{row['label']}] {row['question']}")
    print(f"  answer: {row['answer'][:150]}")
    print(f"  effective={row['effective']}  faithful={row['faithful']}  correct={row['correct']}")