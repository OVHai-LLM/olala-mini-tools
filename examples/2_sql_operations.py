"""Counts, sums, averages, groupings and joins: the everyday SQL behind a business question.

    python examples/2_sql_operations.py
    python examples/2_sql_operations.py "Combien de commandes par pays ?"
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from olala import run  # noqa: E402
from shop import FUNCTIONS, SCHEMA, SQL_TOOL, SYSTEM  # noqa: E402

QUESTIONS = sys.argv[1:] or [
    "How many orders are there in each status?",
    "Quel est le montant moyen d'une commande, arrondi au centime ?",
    "Which customers have never had an order delivered?",
    "Combien de clients différents ont commandé en novembre 2026 ?",
]

for q in QUESTIONS:
    print(f"\n? {q}")
    prompt = f"{SCHEMA}\n\nUse sql_query to answer. Show the figures the query returned.\n\nQuestion: {q}"
    print("=", run(prompt, [SQL_TOOL], FUNCTIONS, system=SYSTEM))
