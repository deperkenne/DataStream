# Utiliser une image Python de base adaptée
FROM python:3.10-slim

# Passer en mode root pour installer des dépendances système
USER root

# Mettre à jour les paquets et installer Vim et d'autres dépendances si nécessaire
RUN apt-get update && apt-get install -y \
    vim \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Créer un utilisateur non root pour éviter les problèmes de permissions
RUN useradd -m flaskuser

# Définir le répertoire de travail dans l'image
WORKDIR /opt/flask_app

# Copier le fichier requirements.txt dans l'image
COPY requirements.txt .

USER flaskuser
# Installer les dépendances Python
RUN pip install --no-cache-dir -r requirements.txt

# Copier le code source de l'application dans l'image
COPY . .

# Démarrer le serveur Flask
CMD ["python", "app.py"]
# Exposer le port sur lequel Flask tournera
EXPOSE 5002




