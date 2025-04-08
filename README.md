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
Vous pouvez suivre la console pour voir les logs d'execution

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
Nous ignorons à chaque enregistrement les lignes dont l'id est existantes ainsi que les lignes ayant plus de trois champs vides.

---

### 📤`POST /send-customers`

Envoie les données en base vers une API externe 
Par défaut nous avons developper une api qui recupère les données json
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
  -d '{"question": "Combien y a-t-il de customers ?"}'
```
- Modèle sélectionné : Zephyr
Il suffit de modifier le modèle dans la variables d'environnements du dockercompose.
- Etant donné un environnement CPU, la requête prends plus de temps.Mais en surveillant 
les logs on peut suivre son évolution.
---

##  Lancer les tests
Les tests se trouvent dans le dossier `tests/`.

Pour les lancer :

```bash
docker-compose run --rm tests
```

---

## Variables d'environnements

- `.env` permet de configurer :
  - `DATABASE_PATH` (par défaut `./data/flight.db`)
  - `EXTERNAL_API_URL` ( API externe par défaut)
  - `OLAMA_MODEL` et `LLM_MODEL_VERSION` contient le nom du modèle par défaut

---

## Fonctionnement Challenges
- **Upload  CSV**
J’ai développé une fonctionnalité d’import de fichiers CSV avec détection automatique du séparateur (; ou ,). Une fonction dédiée ajuste automatiquement la lecture selon le bon séparateur, ce qui permet de rendre l’upload plus robuste et user-friendly.

- **Base de données séparée pour les tests et la production**
Pour éviter toute collision entre les environnements de test et de production, j’ai mis en place une variable d’environnement DATABASE_PATH. Elle permet de cibler dynamiquement la bonne base de données selon le contexte. Un service Docker dédié aux tests a également été ajouté dans le docker-compose.

- **Service de modèle LLM via Ollama**
Le modèle est isolé dans un service Docker ollama. Ce service peut  être facilement déployé sur le cloud (ex : AWS Bedrock), et communique avec notre backend via une URL configurable (OLLAMA_BASE_URL).

- **Architecture  avec système de routing**
L'application est structurée avec un système de routers FastAPI pour séparer les responsabilités (import, envoi, etc.), ce qui améliore la lisibilité, la scalabilité et la maintenance du projet.

- **Mécanisme de backoff résilient avec tenacity**
J’ai intégré la librairie tenacity pour gérer automatiquement les erreurs de réseau (ex: appel API). Le décorateur @retry permet d’implémenter une stratégie de wait_exponential, garantissant des retries intelligents en cas de problème temporaire.

- **agents LLM** Text to SQL
Dans le module des fonctions utiles, j’ai prévu la possibilité de changer facilement de modèle LLM (OpenAI, Mistral, etc.) afin d’adapter le système selon les besoins : vitesse, coût, qualité, ou fournisseur cloud.

## Auteur

Par **Prince Gédéon GUEDJE**
