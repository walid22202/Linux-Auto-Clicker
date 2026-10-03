# linux-cps-clicker

Auto-clicker en terminal pour Linux, compatible **Wayland** et X11, basé sur `evdev` / `uinput`.

## Fonctionnement

- **F4** : armer / désarmer
- Quand c'est armé, **maintiens le clic gauche** : des clics répétés sont envoyés à la cadence choisie
- **F8** : quitter

Le script capture ta souris et la recopie via une souris virtuelle, pour pouvoir remplacer ton appui maintenu par de vrais clics séparés.

## Installation

```bash
sudo apt install python3-evdev
```

## Utilisation

```bash
sudo python3 cps.py --cps 13
```

Options :

| Option | Description |
|---|---|
| `--cps N` | clics par seconde (défaut : 10) |
| `--debug` | affiche les touches reçues |

## Limites

- Nécessite `sudo` (accès à `/dev/input` et `/dev/uinput`)
- Souris uniquement : les pavés tactiles ne sont pas pris en charge
- Le CPS réel est un peu en dessous de la cible : règle `--cps` légèrement plus haut si besoin

## Avertissement

Outil fourni à titre éducatif et pour un usage personnel (tests, accessibilité, jeux solo).
Beaucoup de jeux et serveurs en ligne interdisent les auto-clickers : leur usage peut entraîner un bannissement. Tu es seul responsable de ton utilisation.

## Licence

MIT
