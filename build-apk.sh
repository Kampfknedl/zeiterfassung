#!/bin/bash
# Buildozer APK Build Script

cd /home/user/buildozer

# Accept root warning
export BUILDOZER_SKIPS_UPDATE_CHECK=1

# Run buildozer
buildozer android debug

echo ""
echo "Build abgeschlossen!"
echo "APK Datei:"
ls -lh bin/zeiterfassung*.apk 2>/dev/null || echo "Keine APK gefunden"
