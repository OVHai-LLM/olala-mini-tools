"""Sort incoming messages into a fixed list of categories, for example to route them to the right team.

    python examples/4_classify.py
    python examples/4_classify.py "Mon mot de passe ne fonctionne plus depuis la mise à jour."
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from olala import run  # noqa: E402

LABELS = ["billing", "delivery", "technical", "sales", "complaint"]
MESSAGES = sys.argv[1:] or [
    "Bonjour, notre facture d'octobre mentionne deux fois la même ligne de maintenance.",
    "The parcel still hasn't arrived and tracking has been stuck since Monday.",
    "Could you send us a quote for 20 additional licences?",
    "L'application plante dès qu'on ouvre l'onglet Rapports.",
]

for m in MESSAGES:
    label = run(f"Classify the message into exactly one category among: {', '.join(LABELS)}. "
                f"Reply with the category only.\n\nMessage: {m}", verbose=False)
    print(f"{label.strip().lower():>10}  ←  {m}")
