#!/usr/bin/env bash
# Build the debug APK locally. Requires the Android SDK (ANDROID_SDK_ROOT set)
# and Gradle 8.7+ (or Android Studio's bundled Gradle).
set -e
cd "$(dirname "$0")"
gradle assembleDebug --no-daemon
echo "APK -> app/build/outputs/apk/debug/app-debug.apk"
