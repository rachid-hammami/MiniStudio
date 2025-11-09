from pathlib import Path

print("Chemin du fichier actuel :", Path(__file__).resolve())
print("Dossier parent :", Path(__file__).resolve().parent)
print("Dossier parent.parent :", Path(__file__).resolve().parent.parent)
