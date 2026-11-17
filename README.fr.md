# Olala 1.0 mini : des outils qui marchent

*[English version](README.md)*

Olala 1.0 mini est un modèle compact fait pour travailler avec des outils : il lit vos données à travers eux au lieu de répondre de mémoire. Ce dépôt, ce sont quatre petits exemples qui tournent en une minute, à modifier ensuite pour votre propre cas.

| Exemple | Ce que fait Olala 1.0 mini | Outils |
|---|---|---|
| [`1_query_a_database.py`](examples/1_query_a_database.py) | Transforme une question sur vos données en SQL, l'exécute, et répond en une phrase | `sql_query` |
| [`2_sql_operations.py`](examples/2_sql_operations.py) | Compte, additionne, fait des moyennes, groupe et joint | `sql_query` |
| [`3_pick_the_right_tool.py`](examples/3_pick_the_right_tool.py) | Lit une demande en langage courant, choisit le bon connecteur (CRM, mail, agenda) et remplit ses paramètres | CRM, mail, agenda |
| [`4_classify.py`](examples/4_classify.py) | Range les messages entrants dans une liste fermée de catégories | aucun |

Chaque exemple fonctionne en français et en anglais.

## Le lancer

Il faut Python 3.10 ou plus et un endpoint compatible OpenAI qui sert Olala 1.0 mini (vLLM, llama-server, LM Studio, Ollama…).

```bash
python3 -m venv .venv && .venv/bin/pip install -r requirements.txt
cp .env.example .env        # puis renseignez OLALA_BASE_URL, OLALA_API_KEY et OLALA_MODEL
.venv/bin/python examples/1_query_a_database.py
```

Posez votre propre question en la passant en ligne de commande :

```bash
.venv/bin/python examples/1_query_a_database.py "Quel client a le plus dépensé en octobre ?"
```

Chaque exécution affiche les appels d'outils au fil de l'eau (`→` l'appel, `←` ce que l'outil a renvoyé), puis la réponse (`=`).

## Comment ça marche

Deux fichiers courts contiennent tout :

- **[`olala.py`](olala.py)** est la boucle d'appels d'outils, en une soixantaine de lignes. Elle envoie la question et la description des outils, exécute chaque outil demandé par le modèle, renvoie les résultats, et s'arrête à la première réponse en texte. Elle parle à l'endpoint avec le client `openai` standard.
- **[`shop.py`](shop.py)** est une petite entreprise fictive : une base de boutique (clients et commandes, en mémoire, en lecture seule) et trois faux connecteurs qui se contentent de noter ce qu'ils feraient.

Le prompt système pose une seule règle : ne jamais répondre de mémoire sur des données, les lire avec les outils. Olala 1.0 mini est entraîné à cette habitude.

## L'adapter

- **Vos données :** branchez `sql_query` sur votre propre base, et décrivez ses tables dans le prompt, comme le fait `shop.SCHEMA`. Un schéma court, avec le sens des codes et des unités, aide plus qu'un schéma long.
- **Vos outils :** écrivez une fonction Python, décrivez-la au modèle (nom, rôle, paramètres), et ajoutez les deux à l'appel : voyez comment `shop.py` déclare ses connecteurs. `olala.tool()` construit la description d'un outil dont tous les paramètres sont du texte.
- **Vos catégories :** changez `LABELS` dans `4_classify.py`. Gardez une liste fermée et des catégories bien distinctes.

Quelques habitudes aident :
- **Nommez l'outil et dites quoi rendre :** « interroge la base avec sql_query, puis réponds en une phrase ».
- **Une demande, une tâche.** Pour un travail plus long, enchaînez plusieurs demandes courtes dans votre code plutôt qu'une seule longue.
- **Donnez la date quand elle compte**, comme `3_pick_the_right_tool.py` : le modèle n'a pas d'horloge.

## Licences et crédits

- **Ce code** est sous [licence MIT](LICENSE).
- **Olala 1.0 mini**, le modèle, est sous licence Apache 2.0.

Bibliothèques utilisées :
- **[`openai`](https://github.com/openai/openai-python)** (Apache-2.0), le client Python qui appelle l'endpoint. Il apporte ses propres dépendances (`httpx2`, `httpcore2`, `anyio`, `pydantic`, `jiter`, `idna`…), sous licences Apache-2.0, BSD-3-Clause, MIT ou PSF-2.0.
- **La bibliothèque standard de Python** (PSF-2.0), dont `sqlite3`, qui embarque **[SQLite](https://www.sqlite.org/copyright.html)** (domaine public).

Les données de la boutique (clients, commandes, personnes) sont fictives.
