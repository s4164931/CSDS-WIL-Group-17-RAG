import csv
from collections import defaultdict

# settings

RESULTS_DIR = "testing/results"
ANSWERS_CSV = f"{RESULTS_DIR}/generator_testing_answers.csv"
SUMMARY_CSV = f"{RESULTS_DIR}/summary.csv"
QUESTION_FLAGS_CSV = f"{RESULTS_DIR}/question_flags.csv"
REFUSAL_PHRASE = "does not cover this data"
ROUND_TO = 3

def to_bool(value):
    return str(value).strip().lower() in ("true", "1")


def is_refusal(answer):
    return REFUSAL_PHRASE in str(answer).lower()


def rate(rows, field):
    # share of rows where the field is Trues
    if not rows:
        return None
    return round(sum(to_bool(r[field]) for r in rows) / len(rows), ROUND_TO)


def refusal_rate(rows):
    if not rows:
        return None
    return round(sum(is_refusal(r["answer"]) for r in rows) / len(rows), ROUND_TO)


def as_percent(value):
    return f"{value:.0%}" if value is not None else "n/a"

rows = []
skipped = 0
with open(ANSWERS_CSV, newline="", encoding="utf-8") as f:
    for row in csv.DictReader(f):
        if None in row or None in row.values():
            skipped += 1
            continue
        rows.append(row)

if skipped:
    print(f"warning: skipped {skipped} malformed row(s) in {ANSWERS_CSV} - check the file for a formatting issue")

print(f"loaded {len(rows)} answer rows")

inscope_rows = [r for r in rows if r["question_id"] != "ood"]
ood_rows = [r for r in rows if r["question_id"] == "ood"]

# per-temperature summary (effectiveness, faithfulness, correctness, ood refusal)

by_temp = defaultdict(list)
for r in inscope_rows:
    by_temp[r["temperature"]].append(r)

ood_by_temp = defaultdict(list)
for r in ood_rows:
    ood_by_temp[r["temperature"]].append(r)

summary_rows = []
for temp in sorted(by_temp, key=float):
    rs = by_temp[temp]
    ods = ood_by_temp.get(temp, [])
    summary_rows.append({
        "temperature": temp,
        "n_inscope_answers": len(rs),
        "effectiveness": rate(rs, "effective"),
        "faithfulness": rate(rs, "faithful"),
        "correctness": rate(rs, "correct"),
        "n_ood_answers": len(ods),
        "ood_refusal_rate": refusal_rate(ods),
    })

# overall row, all temperatures combined

summary_rows.append({
    "temperature": "ALL",
    "n_inscope_answers": len(inscope_rows),
    "effectiveness": rate(inscope_rows, "effective"),
    "faithfulness": rate(inscope_rows, "faithful"),
    "correctness": rate(inscope_rows, "correct"),
    "n_ood_answers": len(ood_rows),
    "ood_refusal_rate": refusal_rate(ood_rows),
})

SUMMARY_FIELDS = ["temperature", "n_inscope_answers", "effectiveness", "faithfulness",
                  "correctness", "n_ood_answers", "ood_refusal_rate"]
with open(SUMMARY_CSV, "w", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=SUMMARY_FIELDS)
    writer.writeheader()
    writer.writerows(summary_rows)

print(f"\nsaved per-temperature summary -> {SUMMARY_CSV}\n")
print(f"{'temperature':<12}{'n':>5}{'effectiveness':>15}{'faithfulness':>15}{'correctness':>13}{'ood_refusal':>13}")
for r in summary_rows:
    print(f"{str(r['temperature']):<12}{r['n_inscope_answers']:>5}"
          f"{as_percent(r['effectiveness']):>15}{as_percent(r['faithfulness']):>15}"
          f"{as_percent(r['correctness']):>13}{as_percent(r['ood_refusal_rate']):>13}")

by_question = defaultdict(list)
for r in inscope_rows:
    by_question[r["question_id"]].append(r)

question_rows = []
for qid, rs in by_question.items():
    correctness = rate(rs, "correct")
    effectiveness = rate(rs, "effective")
    question_rows.append({
        "question_id": qid,
        "n_answers": len(rs),
        "effectiveness": effectiveness,
        "faithfulness": rate(rs, "faithful"),
        "correctness": correctness,
        "never_correct": correctness == 0,
        "always_refuses": effectiveness == 0,
    })

question_rows.sort(key=lambda r: r["correctness"])

QUESTION_FIELDS = ["question_id", "n_answers", "effectiveness", "faithfulness",
                   "correctness", "never_correct", "always_refuses"]
with open(QUESTION_FLAGS_CSV, "w", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=QUESTION_FIELDS)
    writer.writeheader()
    writer.writerows(question_rows)