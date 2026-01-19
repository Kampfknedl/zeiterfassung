# Quick Build Guide - Local Docker APK

## One-Time Setup

```powershell
cd "C:\Users\Bene\Desktop\Python_Programme"
docker build -t zeiterfassung-buildozer .
```

## Build APK (any time)

```powershell
cd "C:\Users\Bene\Desktop\Python_Programme"
docker run --rm -v "${PWD}:/app" -w /app zeiterfassung-buildozer buildozer -v android debug
```

**Output**: `bin/zeiterfassung-2.0-arm64-v8a_armeabi-v7a-debug.apk`

---

## Tips

- **Fast rebuilds**: Image is cached; only project files recompiled (~3 min)
- **Clean build**: Add `--force-build` to buildozer command to rebuild recipes
- **Release build**: Replace `debug` with `release` (requires signing config in buildozer.spec)
- **Logs**: Build logs saved in `.buildozer/` directory

---

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Docker image not found | Run `docker build -t zeiterfassung-buildozer .` first |
| Permission denied | Ensure Docker is running and user has access |
| APK not in bin/ | Check `.buildozer/android/platform/build-arm64-v8a_armeabi-v7a/bin/` |
| Build timeout | Increase Docker desktop memory/CPU allocation |

---

## File References

- **Configuration**: `buildozer.spec` (SDK/NDK paths, requirements, archs)
- **Docker**: `Dockerfile` (image definition, system packages)
- **App Code**: `main.py`, `db.py`, `zeiterfassung.kv`
- **Resources**: `res/xml/fileprovider_paths.xml` (for PDF sharing)
- **Dependencies**: `requirements.txt` (for local desktop testing)

---

**Status**: ✅ APK building locally via Docker  
**Latest Build**: `zeiterfassung-2.0-arm64-v8a_armeabi-v7a-debug.apk` (51.7 MB)
