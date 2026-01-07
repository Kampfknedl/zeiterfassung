# GitHub Actions APK Builder - Anleitung 🚀

Du hast bereits einen **funktionierenden GitHub Actions Workflow** eingerichtet! Das ist super.

## Wie funktioniert's:

### 1️⃣ Code zu GitHub pushen
```bash
git add .
git commit -m "Update: Zeiterfassung v2.0 mit KivyMD Material Design und PDF Export"
git push origin main
```

### 2️⃣ Workflow manuell starten (optional)
- Gehe zu: **GitHub → Actions → Build APK**
- Klick auf **"Run workflow"** (rechts oben)
- Workflow startet automatisch mit deinem neuesten Code

### 3️⃣ Build-Prozess überwachen
- Der Build läuft auf Ubuntu in der Cloud ☁️ (dauert ca. 15-20 Minuten)
- Du kannst den Progress unter **Actions** sehen
- Log wird angezeigt, wenn du draufklickst

### 4️⃣ APK herunterladen
Nach erfolgreichem Build:
- **Actions → neuester Run → Artifacts**
- Download: `zeiterfassung-apk` 
- Entpacken → `.apk` Datei ist darin

## Was wurde aktualisiert?

✅ **buildozer.spec** - jetzt mit:
- `main_new.py` als Hauptdatei (Material Design App)
- KivyMD, Plyer, ReportLab Dependencies
- Cython für bessere Performance
- PDF Export Support

## Was ist neu in der App?

| Feature | v1.0 | v2.0 |
|---------|------|------|
| UI | Kivy Basic | KivyMD Material Design |
| PDF Export | ❌ | ✅ |
| Android Support | ✅ | ✅ |
| iOS Support | ❌ | ✅ (vorbereitet) |
| Sharing | ❌ | ✅ |
| Cross-Platform | ❌ | ✅ |

## Fehlerbehandlung

**Build schlägt fehl?**
- Schau das Build-Log an: **Actions → Workflow → Logs**
- Häufige Probleme:
  - Missing dependencies → `requirements` in buildozer.spec checken
  - Syntax-Fehler in main_new.py oder zeiterfassung.kv

**APK funktioniert nicht?**
- Desktop testen: `python main_new.py`
- Logs auf dem Handy: `adb logcat | grep python`

## Automatischer Build bei jedem Push

Der Workflow in `.github/workflows/build-apk.yml` läuft automatisch bei:
- ✅ Push zu `main` Branch
- ✅ Pull Requests
- ✅ Manueller Trigger über "Run workflow"

## Schnell-Tipps

**Release-Build statt Debug:**
```yaml
# In build-apk.yml, ändere:
run: python -m buildozer -v android debug
# zu:
run: python -m buildozer -v android release
```

**Build lokal testen (ohne Docker):**
```bash
pip install buildozer cython
buildozer android debug
```

---

**Nächste Schritte:**
1. Push deinen Code: `git push`
2. Actions → "Run workflow"
3. Warte auf den Build
4. Download APK
5. Auf Android Handy installieren

**Viel Erfolg!** 🎉
