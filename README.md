# ICT-347 Python Flask Hello World

Projet du module I347 (TP6171, sujet 2 : application Python Flask "Hello World").

Le but est de mettre une petite application Flask dans un conteneur Docker. L'application affiche "Hello, World!" et un message en dessous. Ce message peut être changé au lancement du conteneur avec la variable d'environnement `MESSAGE`.

## Contenu du projet

- `main.py` : l'application Flask
- `requirements.txt` : les dépendances Python (Flask)
- `Dockerfile` : pour construire l'image
- `.dockerignore` : les fichiers qu'on ne veut pas copier dans l'image
- `docker-compose.yml` : pour lancer le projet avec Docker Compose

## Prérequis

Il faut avoir Docker Desktop installé et démarré. On peut le télécharger sur https://www.docker.com/products/docker-desktop/ ou, sur Mac avec Homebrew :

```bash
brew install --cask docker-desktop
```

Ensuite il faut ouvrir l'application Docker une première fois et attendre qu'elle soit lancée. Pour vérifier que ça marche :

```bash
docker --version
docker run hello-world
```

## Récupérer le projet

```bash
git clone https://github.com/iagoleplubo/ICT-347_Python_Flask_Hello_world.git
cd ICT-347_Python_Flask_Hello_world
```

## Construire l'image

```bash
docker build -t flask-hello .
```

On peut vérifier que l'image a bien été créée avec `docker images`.

## Lancer le conteneur

```bash
docker run --rm --name flask-hello -p 8080:5000 flask-hello
```

Puis aller sur http://localhost:8080 dans un navigateur. On doit voir :

```
Hello, World!
Bienvenue depuis Docker
```

Explication des options :

- `--rm` : le conteneur est supprimé quand on l'arrête, donc à chaque lancement il repart de zéro
- `--name flask-hello` : le nom du conteneur
- `-p 8080:5000` : le port 8080 de l'ordinateur est redirigé vers le port 5000 du conteneur (c'est le port sur lequel Flask tourne)

Pour arrêter le conteneur, on fait `Ctrl + C` dans le terminal ou `docker stop flask-hello` dans un autre terminal.

Remarque : sur Mac, le port 5000 est déjà utilisé par AirPlay, c'est pour ça qu'on utilise le port 8080. On peut mettre n'importe quel port libre avant les `:`.

## Changer le message et le port

Le message se change avec `-e MESSAGE="..."` et le port avec `-p` :

```bash
docker run --rm --name flask-hello -p 9000:5000 -e MESSAGE="Bonjour la classe" flask-hello
```

Ici la page est sur http://localhost:9000 et affiche "Bonjour la classe" sous le Hello World.

On peut aussi le lancer en arrière-plan avec `-d` et regarder les logs :

```bash
docker run -d --rm --name flask-hello -p 8080:5000 -e MESSAGE="test" flask-hello
docker logs flask-hello
docker stop flask-hello
```

On peut aussi tester sans navigateur avec curl :

```bash
curl http://localhost:8080
```

## Test : le conteneur repart de zéro

Si on modifie quelque chose dans le conteneur, la modification est perdue quand on l'arrête (à cause du `--rm`) :

```bash
docker run -d --rm --name flask-hello -p 8080:5000 flask-hello
docker exec flask-hello sh -c "echo test > /app/test.txt"
docker exec flask-hello ls /app
```

`test.txt` apparaît dans la liste. Ensuite on arrête et on relance :

```bash
docker stop flask-hello
docker run -d --rm --name flask-hello -p 8080:5000 flask-hello
docker exec flask-hello ls /app
docker stop flask-hello
```

Le fichier `test.txt` n'est plus là, le conteneur est revenu à l'état de l'image.

## Avec Docker Compose

Le fichier `docker-compose.yml` permet de tout lancer avec une seule commande :

```bash
docker compose up --build
```

La page est sur http://localhost:8080. Pour changer le message ou le port :

```bash
MESSAGE="Lancé avec compose" PORT=9000 docker compose up --build
```

Pour tout arrêter :

```bash
docker compose down
```

## Le Dockerfile

```dockerfile
FROM python:3.12-slim
ENV PYTHONUNBUFFERED=1
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY main.py .
ENV MESSAGE="Bienvenue depuis Docker"
EXPOSE 5000
CMD ["python", "main.py"]
```

- `FROM` : on part d'une image Python 3.12 légère
- `PYTHONUNBUFFERED=1` : pour que les logs de Flask s'affichent directement
- `WORKDIR` : le dossier de travail dans le conteneur
- `COPY requirements.txt` puis `RUN pip install` : on installe Flask. On copie d'abord seulement le requirements.txt pour que Docker garde cette étape en cache si on modifie juste le code
- `COPY main.py` : on copie le code
- `ENV MESSAGE` : le message par défaut si on ne met pas `-e MESSAGE`
- `EXPOSE 5000` : le port utilisé par Flask
- `CMD` : la commande qui démarre l'application

Dans `main.py`, le message est récupéré avec `os.environ.get("MESSAGE", " ... ")`.

## Problèmes possibles

- `command not found: docker` : Docker Desktop n'est pas installé ou pas démarré, il faut l'ouvrir puis ouvrir un nouveau terminal
- `Cannot connect to the Docker daemon` : Docker Desktop n'est pas lancé
- `port is already allocated` : le port est déjà utilisé, il faut en prendre un autre (par exemple `-p 8081:5000`)
- `The container name "/flask-hello" is already in use` : un ancien conteneur existe encore, on le supprime avec `docker rm -f flask-hello`
