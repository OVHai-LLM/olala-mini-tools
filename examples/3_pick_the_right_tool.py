"""Give a request in plain words; Olala 1.0 mini picks the right connector and fills in its parameters.

The connectors here are fake (see shop.py): they record what they would do. Plug in your own functions.

    python examples/3_pick_the_right_tool.py
    python examples/3_pick_the_right_tool.py "Envoie un mail à compta@example.com pour confirmer la facture 1005."
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from olala import run  # noqa: E402
from shop import ALL_TOOLS, FUNCTIONS, SYSTEM, outbox  # noqa: E402

REQUESTS = sys.argv[1:] or [
    "Trouve la fiche client de la Brasserie du Port.",
    "Open a high-priority ticket for customer 6: the delivery is stuck at the port of Gdansk.",
    "Planifie une réunion « Revue trimestrielle » le 20 novembre 2026 à 14 h 30.",
    "Send an email to ops@example.com with the subject 'Stock alert' saying that item 42 is out of stock.",
]

for r in REQUESTS:
    print(f"\n? {r}")
    print("=", run(f"Use the appropriate tool to handle the request. Today is 17 November 2026.\n\nRequest: {r}",
                   ALL_TOOLS, FUNCTIONS, system=SYSTEM))

print("\nWhat the connectors were asked to do:")
for item in outbox:
    print(" ", item)
