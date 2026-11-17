"""A small fictional company for the examples: a shop database and three connectors (CRM, mail, calendar).

Everything is local and fake: the database lives in memory, and the connectors only record what they would do.
Replace these functions with your own to plug Olala 1.0 mini into real systems.
"""
from __future__ import annotations

import json
import sqlite3
from pathlib import Path

SCHEMA = """Tables (SQLite):
customers(id INTEGER, name TEXT, city TEXT, country TEXT -- ISO 2-letter code)
orders(id INTEGER, customer_id INTEGER, order_date TEXT -- YYYY-MM-DD, amount_eur REAL -- excl. VAT, status TEXT -- 'delivered' | 'cancelled' | 'in_progress')"""

_db = sqlite3.connect(":memory:", check_same_thread=False)
_db.executescript(Path(__file__).with_name("shop.sql").read_text(encoding="utf-8"))
_db.execute("PRAGMA query_only = ON")  # the model can read, never write

outbox: list[dict] = []  # what the fake connectors were asked to do


# ---------------------------------------------------------------- functions the model can call
def sql_query(query: str) -> str:
    cur = _db.execute(query)
    cols = [d[0] for d in cur.description or []]
    return json.dumps([dict(zip(cols, row)) for row in cur.fetchmany(50)], ensure_ascii=False)


def crm_search_customer(name: str) -> str:
    rows = _db.execute("SELECT * FROM customers WHERE name LIKE ?", (f"%{name}%",)).fetchall()
    return json.dumps([dict(zip(("id", "name", "city", "country"), r)) for r in rows], ensure_ascii=False)


def crm_create_ticket(customer_id: int, title: str, priority: str) -> str:
    outbox.append({"connector": "crm", "customer_id": customer_id, "title": title, "priority": priority})
    return json.dumps({"ticket_id": 500 + len(outbox), "status": "open"})


def mail_send(to: str, subject: str, body: str) -> str:
    outbox.append({"connector": "mail", "to": to, "subject": subject})
    return "sent"


def calendar_create_event(title: str, date: str, time: str) -> str:
    outbox.append({"connector": "calendar", "title": title, "date": date, "time": time})
    return json.dumps({"event": title, "date": date, "time": time})


FUNCTIONS = {f.__name__: f for f in (sql_query, crm_search_customer, crm_create_ticket, mail_send, calendar_create_event)}


# ---------------------------------------------------------------- how the model sees them
def _fn(name, description, properties, required):
    return {"type": "function", "function": {"name": name, "description": description,
            "parameters": {"type": "object", "properties": properties, "required": required}}}


SQL_TOOL = _fn("sql_query", "Database connector: run a read-only SQLite query and return the rows as JSON.",
               {"query": {"type": "string"}}, ["query"])
CONNECTORS = [
    _fn("crm_search_customer", "CRM connector: find a customer record by company name.", {"name": {"type": "string"}}, ["name"]),
    _fn("crm_create_ticket", "CRM connector: open a support ticket for a customer.",
        {"customer_id": {"type": "integer"}, "title": {"type": "string"},
         "priority": {"type": "string", "enum": ["low", "normal", "high"]}}, ["customer_id", "title", "priority"]),
    _fn("mail_send", "Mail connector: send an email.",
        {"to": {"type": "string"}, "subject": {"type": "string"}, "body": {"type": "string"}}, ["to", "subject", "body"]),
    _fn("calendar_create_event", "Calendar connector: create an event.",
        {"title": {"type": "string"}, "date": {"type": "string", "description": "YYYY-MM-DD"},
         "time": {"type": "string", "description": "HH:MM"}}, ["title", "date", "time"]),
]
ALL_TOOLS = [SQL_TOOL] + CONNECTORS

SYSTEM = ("You are a business assistant that works with tools. Never answer from memory about data: read it with the "
          "tools. Answer in the language of the request.")
