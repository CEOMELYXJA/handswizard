# Handswizard — souris aérienne Windows 11

Le mode principal utilise ta webcam pour déplacer le **vrai curseur Windows**, y compris dans tes autres applications. Le mode iPhone reste disponible séparément. Cette version est un prototype : les gestes et la compatibilité matérielle doivent être vérifiés sur ton PC.

## Mains libres avec Python 3.15

1. Télécharge la branche de développement depuis GitHub (Code → Download ZIP), puis extrais-la.
2. Installe Python 3.15 pour Windows avec le lanceur Python, si nécessaire. Double-clique sur `lancer.bat`, puis choisis **1**.
3. Garde la fenêtre noire ouverte. Une page locale s'ouvre dans ton navigateur. Clique sur **Activer la webcam**, autorise la caméra, puis clique sur **Activer la souris**.
4. Garde l'onglet de suivi ouvert et visible pendant que tu utilises les autres fenêtres. Le suivi cesse lorsque l'onglet est caché ou que la connexion est perdue. La webcam doit voir ta main; ce n'est pas un suivi 3D dans toute la pièce.

| Geste | Action |
| --- | --- |
| Bouger la main | Déplacer le curseur |
| Pincer pouce et index | Clic gauche; garder pincé pour glisser, relâcher pour déposer |
| Pincer pouce et majeur | Clic droit |
| Index et majeur levés, autres doigts repliés | Bouger la main verticalement pour défiler |

L'application démarre en pause. Utilise **Arrêt immédiat** ou ferme la fenêtre noire avec Ctrl+C; le bouton maintenu est relâché après une perte de suivi ou de connexion. Une souris physique demeure utile pour reprendre le contrôle. Les écrans Windows protégés, comme l'invite UAC et l'écran verrouillé, ne sont pas contrôlables normalement par une application ordinaire.

Le traitement des images est effectué dans le navigateur sur le PC. Internet est nécessaire pour télécharger le moteur MediaPipe et son modèle au démarrage; la vidéo n'est pas envoyée à la passerelle. La passerelle écoute uniquement sur `127.0.0.1:8765`, vérifie l'origine et un jeton temporaire, et n'accepte que des commandes de souris. Ne l'expose jamais sur Internet, par tunnel public ou redirection de port. Ne partage pas l'adresse complète contenant le jeton.

## iPhone (secondaire)

Choisis **2** dans le lanceur. Ce mode utilise `aiohttp` et `pyautogui`, installés séparément; leur installation sous Python 3.15 doit encore être validée. Installe Tailscale sur les deux appareils, connectés au même réseau privé, puis sur le PC :

```powershell
& "C:\Program Files\Tailscale\tailscale.exe" serve --bg http://127.0.0.1:8766
& "C:\Program Files\Tailscale\tailscale.exe" serve status
```

Ouvre l'adresse HTTPS privée affichée sur Safari, entre le code d'appairage affiché sur le PC, autorise le gyroscope, calibre et démarre. Le téléphone contrôle le curseur par inclinaison, pas par suivi de position 3D. N'active jamais Funnel ni un tunnel public. Pour arrêter le partage privé : `tailscale serve reset`. Ne lance pas les deux modes simultanément.

## Dépannage

- Si la caméra ne démarre pas, vérifie les permissions Windows et celles du navigateur, ferme les autres applications qui l'utilisent et vérifie Internet.
- Si le curseur ne bouge pas, vérifie que la fenêtre noire est ouverte, que l'onglet reste visible et que la souris est activée. Rapproche ta main et améliore l'éclairage.
- Pour arrêter rapidement, utilise le bouton d'arrêt ou Ctrl+C dans la fenêtre noire.
- La page publique GitHub Pages ne peut pas contrôler directement la souris : le programme local est nécessaire.

Tests sans matériel : `py -3.15 -m unittest discover -s tests -v`. Aucun essai physique de webcam, de souris Windows ou d'iPhone n'est revendiqué par les tests automatisés.
