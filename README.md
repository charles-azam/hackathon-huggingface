# hackathon-huggingface*

Ok les loulous !

Pour installer vous avez juste à faire:

```bash
git clone https://github.com/charles-azam/hackathon-huggingface.git
cd hackathon-huggingface
uv sync
```

Ensuite, vérifiez que l'environnement python de vscode soit bien `.venv`.

## usage

Pour rajouter un package faites `uv add`. Sinon refaites un `uv sync`.

Pour vérifier que tout est bien installé, lancez:
`uv run pytest tests`

Vous pouvez aussi lancer ces commandes dans le terminal python:

```python
from loulou.hello import hello_word
print(hello_world)
```


## Git

Pour git je vous propose, afin que tout se passe bien d'utiliser le workflow suivant:

```bash
git checkout -b elias/coucou # pour faire sa branche
git add 
git commit
git commit
git commit
git rebase -i HEAD~3 # si vous avez fait plusieurs commits, il est plus simple de les squash pour éviter les conflits

# une fois que ça c'est prêt il faut se mettre à jour avec main
git checkout main # on va sur main
git pull # on s'assure d'avoir la dernière version de main
git checkout elias/coucou # on retourne sur sa branche


git rebase main # équivalent à git merge mais plus simple à debugger

git push --force-with-lease
# maintenant vous pouvez ouvrir votre PR

```