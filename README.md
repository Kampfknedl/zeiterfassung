# Kivy PoC — Stundenerfassung (Android)

Kurzanleitung:

1. Diese PoC zeigt eine minimalistische UI zur Erfassung von Kunden und Stunden.
2. Zum Bauen einer APK verwende Buildozer (läuft unter Linux). Empfohlen: WSL2/Ubuntu oder ein Linux-Container.

Beispiel (Ubuntu):

```bash
sudo apt update && sudo apt install -y python3-pip build-essential git
pip install --user buildozer
# Im Projektordner
cd mobile/kivy_poc
buildozer init
# prüfe buildozer.spec (requirements=kivy)
buildozer android debug
```

Hinweise:
- Android‑Builds benötigen Java/Android SDK/NDK — siehe Buildozer‑Dokumentation.
- Testen lokal: `python main.py` (Desktop Kivy muss installiert sein: `pip install kivy`).
