# linux-cps-clicker

Un auto-clicker simple pour **Linux**, qui s'utilise dans le terminal.
Il marche sur **Wayland** et sur **X11** (testé sur Ubuntu).

## Comment ça marche

1. Tu lances le programme dans le terminal.
2. Tu appuies sur **F4** pour l'activer (`[ON]`).
3. Tu **maintiens le clic gauche** : le programme envoie des clics rapides à ta place.
4. Tu relâches le clic : ça s'arrête.
5. **F4** à nouveau pour le désactiver (`[OFF]`), **F8** pour quitter.

| Touche | Action |
|---|---|
| `F4` | Activer / désactiver |
| Clic gauche maintenu | Envoie des clics répétés (si activé) |
| `F8` | Quitter |

## Installation

Il te faut Python 3 et la bibliothèque `evdev`.

```bash
sudo apt update
sudo apt install python3 python3-evdev
```

Ensuite, télécharge le projet :

```bash
git clone https://github.com/TON-PSEUDO/linux-cps-clicker.git
cd linux-cps-clicker
```

Sans Git, tu peux aussi cliquer sur le bouton vert **Code** puis **Download ZIP** sur la page GitHub, et décompresser le dossier.

## Utilisation

```bash
sudo python3 cps.py --cps 13
```

`sudo` est obligatoire, car le programme doit lire le clavier et la souris au niveau du système.

### Options

| Option | Description | Défaut |
|---|---|---|
| `--cps N` | Nombre de clics par seconde | `10` |
| `--debug` | Affiche les touches reçues (utile en cas de problème) | désactivé |

Exemple pour 15 clics par seconde :

```bash
sudo python3 cps.py --cps 15
```

## Problèmes courants

**F4 ne fait rien**
Sur beaucoup d'ordinateurs portables, les touches F servent d'abord au volume ou à la luminosité. Essaie **Fn + F4**. Lance aussi avec `--debug` pour voir si la touche est bien reçue.

**`Permission refusée`**
Tu as oublié `sudo` devant la commande.

**`ModuleNotFoundError: No module named 'evdev'`**
Installe la dépendance : `sudo apt install python3-evdev`.

**Ma souris ne bouge plus**
Appuie sur **F8** ou fais `Ctrl+C` dans le terminal : le programme relâche la souris en s'arrêtant.

**Le CPS affiché est un peu plus bas que celui demandé**
C'est normal, chaque clic prend un peu de temps. Mets une valeur légèrement plus haute dans `--cps`.

## Limites

- Fonctionne avec une **souris** (le pavé tactile n'est pas pris en charge).
- Nécessite les droits administrateur (`sudo`).
- Testé sur Ubuntu. Devrait marcher sur les autres distributions Linux.

## Avertissement

Ce projet est fourni pour un usage personnel (tests, accessibilité, jeux solo).
De nombreux jeux et serveurs en ligne interdisent les auto-clickers : leur utilisation peut entraîner un bannissement. Tu es responsable de l'usage que tu en fais.

## Licence

Projet open source sous licence **MIT**. Voir le fichier [LICENSE](LICENSE).
