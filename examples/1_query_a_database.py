"""Ask a question about your data; Olala 1.0 mini writes the SQL, runs it, and answers in one sentence.

    python examples/1_query_a_database.py
    python examples/1_query_a_database.py "Which customer spent the most in October?"
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from olala import run  # noqa: E402
from shop import FUNCTIONS, SCHEMA, SQL_TOOL, SYSTEM  # noqa: E402

QUESTIONS = sys.argv[1:] or [
    "Quel est le montant total des commandes livrées en octobre 2026 ?",
    "Which customers are based in France?",
    "Quelle est la plus grosse commande encore en cours, et pour quel client ?",
]

for q in QUESTIONS:
    print(f"\n? {q}")
    prompt = f"{SCHEMA}\n\nAnswer the question by querying the database with sql_query, then give the answer in one sentence.\n\nQuestion: {q}"
    print("=", run(prompt, [SQL_TOOL], FUNCTIONS, system=SYSTEM))
