# Olala 1.0 mini: tools that work

*[Version française](README.fr.md)*

Olala 1.0 mini is a compact model built to work with tools: it reads your data through them instead of answering from memory. This repo is four small examples you can run in a minute, then change to fit your own case.

| Example | What Olala 1.0 mini does | Tools |
|---|---|---|
| [`1_query_a_database.py`](examples/1_query_a_database.py) | Turns a question about your data into SQL, runs it, and answers in one sentence | `sql_query` |
| [`2_sql_operations.py`](examples/2_sql_operations.py) | Counts, sums, averages, groupings and joins | `sql_query` |
| [`3_pick_the_right_tool.py`](examples/3_pick_the_right_tool.py) | Reads a request in plain words, picks the right connector (CRM, mail, calendar) and fills in its parameters | CRM, mail, calendar |
| [`4_classify.py`](examples/4_classify.py) | Sorts incoming messages into a fixed list of categories | none |

Each example works in French and in English.

## Run it

You need Python 3.10 or later and an OpenAI-compatible endpoint that serves Olala 1.0 mini: `llama-server` from the
[llama.cpp fork](https://github.com/OVHai-LLM/llama.cpp/tree/olala-master) (GGUF files), the
[vLLM fork](https://github.com/OVHai-LLM/vllm) (NVIDIA GPU) or the [mlx-engine](https://github.com/OVHai-LLM/mlx-engine)
server (Mac). See the [model card](https://huggingface.co/OVHaiLLM/Olala-v1.0-mini-7A1B) for the commands.
Upstream llama.cpp, vLLM, LM Studio and Ollama cannot load the `olala` architecture yet.

```bash
python3 -m venv .venv && .venv/bin/pip install -r requirements.txt
cp .env.example .env        # then set OLALA_BASE_URL, OLALA_API_KEY and OLALA_MODEL
.venv/bin/python examples/1_query_a_database.py
```

Ask your own question by passing it on the command line:

```bash
.venv/bin/python examples/1_query_a_database.py "Which customer spent the most in October?"
```

Each run prints the tool calls as they happen (`→` the call, `←` what the tool returned), then the answer (`=`).

## How it works

Two short files hold everything:

- **[`olala.py`](olala.py)** is the tool-calling loop, in about sixty lines. It sends the question and the tool descriptions, runs each tool the model asks for, sends the results back, and stops at the first text answer. It talks to the endpoint with the standard `openai` client.
- **[`shop.py`](shop.py)** is a small fictional company: a shop database (customers and orders, in memory, read-only) and three fake connectors that only record what they would do.

The system prompt sets one rule: never answer from memory about data, read it with the tools. Olala 1.0 mini is trained for that habit.

## Make it yours

- **Your data:** point `sql_query` at your own database, and describe its tables in the prompt, as `shop.SCHEMA` does. A short schema, with the meaning of codes and units, helps more than a long one.
- **Your tools:** write a Python function, describe it to the model (name, purpose, parameters), and add both to the call: see how `shop.py` declares its connectors. `olala.tool()` builds a description for tools whose parameters are all text.
- **Your categories:** change `LABELS` in `4_classify.py`. Keep the list closed and the labels distinct.

A few habits help:
- **Name the tool and say what to return:** "query the database with sql_query, then answer in one sentence".
- **Keep each request to one job.** For longer work, chain several short requests in your code rather than one long one.
- **Give the date when it matters**, as `3_pick_the_right_tool.py` does: the model has no clock.

## Licences and credits

- **This code** is under the [MIT licence](LICENSE).
- **Olala 1.0 mini**, the model, is under the Apache 2.0 licence.

Libraries used:
- **[`openai`](https://github.com/openai/openai-python)** (Apache-2.0), the Python client used to call the endpoint. It brings its own dependencies (`httpx2`, `httpcore2`, `anyio`, `pydantic`, `jiter`, `idna`…), under Apache-2.0, BSD-3-Clause, MIT or PSF-2.0 licences.
- **Python's standard library** (PSF-2.0), including `sqlite3`, which embeds **[SQLite](https://www.sqlite.org/copyright.html)** (public domain).

The shop data (customers, orders, people) is fictional.
