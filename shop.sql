CREATE TABLE customers (
  id INTEGER PRIMARY KEY,
  name TEXT NOT NULL,
  city TEXT NOT NULL,
  country TEXT NOT NULL          -- code ISO à deux lettres
);
CREATE TABLE orders (
  id INTEGER PRIMARY KEY,
  customer_id INTEGER NOT NULL REFERENCES customers(id),
  order_date TEXT NOT NULL,      -- AAAA-MM-JJ
  amount_eur REAL NOT NULL,      -- montant HT en euros
  status TEXT NOT NULL           -- 'delivered', 'cancelled' ou 'in_progress'
);
INSERT INTO customers VALUES
 (1,'Atelier Morvan','Rennes','FR'),
 (2,'Brasserie du Port','Vannes','FR'),
 (3,'Nordlicht GmbH','Hamburg','DE'),
 (4,'Lumen Labs','Lyon','FR'),
 (5,'Casa Verde SL','Valencia','ES'),
 (6,'Baltic Freight','Gdansk','PL'),
 (7,'Helios Énergie','Lille','FR'),
 (8,'Kestrel Ltd','Leeds','GB');
INSERT INTO orders VALUES
 (1001,1,'2026-10-02',1250.00,'delivered'),
 (1002,2,'2026-10-05',380.50,'delivered'),
 (1003,3,'2026-10-07',9800.00,'delivered'),
 (1004,1,'2026-10-12',640.00,'cancelled'),
 (1005,4,'2026-10-15',2210.00,'delivered'),
 (1006,5,'2026-10-18',150.00,'delivered'),
 (1007,6,'2026-10-21',12400.00,'in_progress'),
 (1008,7,'2026-10-25',3075.25,'delivered'),
 (1009,3,'2026-10-28',4500.00,'in_progress'),
 (1010,8,'2026-11-02',780.00,'in_progress'),
 (1011,2,'2026-11-03',95.00,'delivered'),
 (1012,4,'2026-11-05',5600.00,'in_progress');
