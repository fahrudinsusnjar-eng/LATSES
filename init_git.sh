#!/bin/bash
# LAT-CES Git Initialization Script
# Pokrenuti u korijenskom direktoriju: /workspaces/LATSES

echo "Inicijalizacija LAT-CES Git repozitorijuma..."

# 1. Kreiranje .gitignore fajla
cat <<EOF > .gitignore
__pycache__/
*.py[cod]
*$py.class
.pytest_cache/
.env
.venv/
.vscode/
data/
EOF

# 2. Inicijalizacija i dodavanje fajlova
git init
git add .
git commit -m "LAT-CES: Finalna integracija Core modula (Aerodinamika, Energetika, Pipeline)"

# 3. Priprema remote repozitorijuma (Zamijenite URL sa vašim)
# git remote add origin https://github.com/KORISNIK/LAT-CES-CORE.git
# git branch -M main
# git push -u origin main

echo "Repozitorijum spreman. Za finalni push otkomentarišite git remote komande."
