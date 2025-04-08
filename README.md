# 🧠 test_agentapi

### Fonctionnalités :
- Importe des fichiers CSV clients et achats dans une base SQLite
- Envoie ces données vers une API externe avec résilience
- Permet de poser des questions en langage naturel sur les données (via un agent LLM)

---

## Installation 

### 🖥️ Installation locale

###  Avec Docker
```bash
docker compose up --build
```

- L’API sera dispo sur : `http://localhost:8000`
- Documentation :  `http://localhost:8000/docs`
---

## 📬 Endpoints & Exemples `curl`

### 📥 `POST /import-csv`
Upload de deux fichiers CSV : `customers` et `purchases`.

```bash
curl -X POST http://localhost:8000/import-csv \
  -F "customers_file=@./data/customers.csv" \
  -F "purchases_file=@./data/purchases.csv"
```

---

### 📤 `POST /send-customers`

Envoie les données en base vers une API externe 

```bash
curl -X POST http://localhost:8000/send-customers
```
Ou vers une API externe spécifique :
```bash
curl -X POST "http://localhost:8000/send-customers?api_url=https://tonapi.com"
```
Nous avons developper une api qui récupère json dans notre dockercompose pour effectuer 
une simulation

---

### 🤖 `POST /query-sql`
Interroge les données à partir du texte (avec un agent LLM connecté à la DB) :
```bash
curl -X POST http://localhost:8000/query-sql \
  -H "Content-Type: application/json" \
  -d '{"question": "Combien y a-t-il de clients ?"}'
```
- Modèle sélectionné : Phi3
---

##  Lancer les tests

### 📁 Structure de test

Les tests se trouvent dans le dossier `tests/`.

Pour les lancer :

```bash
docker-compose run --rm tests
```

---

## 🧱 Architecture du projet

```bash
.
├── app/
│   ├── main.py                # Entrée principale FastAPI
│   ├── routers/
│   │   ├── import_csv.py      # Route d’import CSV
│   │   ├── send_customers.py  # Route d’envoi vers API
│   │   └── llm_query.py       # Route LLM
│   ├── core/
│   │   └── utils/             # Fonctions utilitaires (tools, constants, agent_sql)
├── data/
│   └── flight.db              # Base SQLite (auto-générée si absente)
├── tests/
│   └── test_send_customers.py # Exemple de test
├── docker-compose.yml
├── Dockerfile
└── README.md
```

---

## Variables d'environnements

- `.env` permet de configurer :
  - `DATABASE_PATH` (par défaut `./data/flight.db`)
  - `EXTERNAL_API_URL` (mock API par défaut)

---

## Auteur

Par **Prince Gédéon GUEDJE**
