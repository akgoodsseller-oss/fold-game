# Fold — a minimalist paper-folding puzzle

Fold the sheet **completely flat**. Every tile merges (overlapping numbers add up),
and the single square you're left with always equals the **goal number**. Holes in
the paper and the "a flap can't be wider than what it lands on" rule are what make
each level a puzzle: pick the right fold order or you'll get stuck.

- **Drag any edge inward** to fold that flap over.
- **Undo / Restart** anytime. 14 levels, rising in size and hole-count.
- Pure HTML/JS/CSS. No engine, no assets, no network. The whole game is one 16 KB file.

## Play it right now
Open `index.html` in any browser (desktop or phone). That's the entire game.

## Get the Android APK — two zero-setup ways

### Option A — GitHub builds it for you (no tools installed)
1. Create a new GitHub repo and upload everything in this folder
   (or push it with git). The included workflow does the rest.
2. Open the repo's **Actions** tab → the **Build Fold APK** run.
3. When it finishes (~3–4 min), download the **Fold-debug-apk** artifact.
   Inside is `app-debug.apk` — copy it to an Android phone and install
   (enable "install from unknown sources").

The pipeline is `.github/workflows/build.yml` — it installs the Android SDK,
builds with Gradle, and uploads the APK automatically.

### Option B — Android Studio (one click)
1. **Open** the `android/` folder in Android Studio (let it sync; it will
   fetch Gradle + the Android SDK the first time).
2. **Build → Build App Bundle(s) / APK(s) → Build APK(s)**, or press **Run**.
3. The APK lands in `android/app/build/outputs/apk/debug/app-debug.apk`.

### Option C — command line (if you have the Android SDK)
```
cd android
gradle assembleDebug        # or ./gradlew assembleDebug if you add a wrapper
```

## What's in here
```
index.html                     the complete, standalone game (play in a browser)
README.md                      this file
android/                       minimal WebView Android project (compiles to the APK)
  app/src/main/assets/index.html   the game, bundled into the app
  app/src/main/java/.../MainActivity.java
  app/src/main/AndroidManifest.xml
  app/build.gradle, build.gradle, settings.gradle, gradle.properties
  app/src/main/res/...          adaptive launcher icon (vector, tiny)
.github/workflows/build.yml     CI that builds + hands you the APK
tools/                          how the levels were made (Python)
  foldgen.py                    the fold engine + BFS solver
  genmain.py                    generates & validates the 14 levels
  levels.json                   the level data (also embedded in index.html)
```

## Notes
- Debug APK is unsigned for the Play Store but installs fine for testing/sharing.
  For a Play release, generate a signing key and a `release` build.
- Every level is **guaranteed solvable** — each was produced and re-verified by the
  BFS solver in `tools/`, so no level can be a dead end from the start.
- Tiny by design: the debug APK is only ~1–2 MB (mostly Android's own overhead;
  the game itself is 16 KB).
