import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import RAG

from data.eval_questions_revised import eval_questions_dict

from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate
from langchain_classic.chains.combine_documents import (create_stuff_documents_chain)

# settings

K_VALUES = [1, 2, 3, 5, 10]

TEMPERATURE_VALUES = [0, 0.3, 0.7, 1.0]

LIMIT = 5 # number of questions to test

# loading questions specifically for testing

questions = []

for category in eval_questions_dict:
    for question_type in eval_questions_dict[category]:
        for item in eval_questions_dict[category][question_type]:
            questions.append({
                "question": item["question"],
                "expected": item.get(
                    "expected_answer",
                    item.get("expected_answer", "")
                )
            })

if LIMIT:
    questions = questions [:LIMIT]

print(f"Testing {len(questions)} questions")

# loading data

parsed_data = RAG.parse_through_json_file("data/data_dict.json")
documents = RAG.load_into_document_class(parsed_data)
vectorised_data = RAG.vectoriser(documents)

# test 1: K

print("\n==============================")
print("Testing K")

judge_llm = ChatOllama(model="llama3", temperature=0, num_ctx=8192)

judge_prompt = ChatPromptTemplate.from_messages([
    (
        "system",
        """You are evaluating a RAG retrieval system.
Your task is to determine whether the provided context contains
enough information to correctly answer the question.

Answer ONLY with:
YES
or
NO

Do not explain your answer."""
    ),
    (
        "human",
        """Question:
{question}

Expected answer:
{expected}

Retrieved context:
{context}"""
    )
])

judge_chain = judge_prompt | judge_llm

for k in K_VALUES:
    correct = 0
    print(f"\nK = {k}")
    for question in questions:
        docs = vectorised_data.similarity_search(question["question"], k=k)

        context = "\n\n".join(doc.page_content for doc in docs)

        result = judge_chain.invoke({
            "question": question["question"],
            "expected": question["expected"],
            "context": context
        })

        result_text = result.content.strip().upper()

        if result_text.startswith("YES"):
            correct += 1

    score = correct / len(questions)

    print(
        f"Relevant context retrieved: "
        f"{correct}/{len(questions)} "
        f"({score:.0%})"
    )


# test 2: temperature

prompt = ChatPromptTemplate.from_messages([
            ("system", "You are a helpful assistant. Answer the user's question using ONLY the provided context. If you do not know the answer based on the context, say 'Unfortunately my database does not cover this data'\n\nContext:\n{context}"),
            ("human", "{input}"),
    ])

K_FOR_TEMPERATURE = 3

print("\n==============================")
print("Testing Temperature")

for temperature in TEMPERATURE_VALUES:
    print(f"\nTemperature = {temperature}")
    llm = ChatOllama(model="llama3", temperature=temperature, num_ctx=8192)
    qa_chain = create_stuff_documents_chain(llm, prompt)

    for question in questions:
        docs = vectorised_data.similarity_search(question["question"], k=K_FOR_TEMPERATURE)
        answer = qa_chain.invoke({"input": question["question"], "context": docs})
        print("\nQuestion:")
        print(question["question"])
        print("\nAnswer:")
        print(answer)
        print("-" * 50)