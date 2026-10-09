#!/bin/sh
set -eu

# Xealth two-environment contract; adapt the variable prefix for another app.
: "${CI_PRIMARY_REPOSITORY_PATH:?Missing Xcode Cloud repository path}"
: "${CI_BRANCH:?Missing Xcode Cloud branch}"
: "${CI_BUILD_NUMBER:?Missing Xcode Cloud build number}"
: "${XEALTH_APP_ENVIRONMENT:?Set XEALTH_APP_ENVIRONMENT to development or production in the Xcode Cloud workflow}"

# Verified Flutter 3.47.6 release revision; update deliberately with its tag.
FLUTTER_REPOSITORY=https://github.com/flutter/flutter.git
FLUTTER_REVISION=5fc346839b5d0eef006ed8404392afb4dfae428d

case "$XEALTH_APP_ENVIRONMENT" in
  development) FLUTTER_TARGET=lib/main_dev.dart ;;
  production) FLUTTER_TARGET=lib/main_prod.dart ;;
  *) echo "Unsupported XEALTH_APP_ENVIRONMENT: $XEALTH_APP_ENVIRONMENT" >&2; exit 1 ;;
esac

branch="${CI_BRANCH#refs/heads/}"
if [ "$branch" != "$XEALTH_APP_ENVIRONMENT" ]; then
  echo "Xcode Cloud environment $XEALTH_APP_ENVIRONMENT must build its matching branch, not $branch." >&2
  exit 1
fi

case "$CI_BUILD_NUMBER" in
  ''|*[!0-9]*|0) echo "CI_BUILD_NUMBER must be a positive integer." >&2; exit 1 ;;
esac

cd "$CI_PRIMARY_REPOSITORY_PATH"
test -f "$FLUTTER_TARGET" || { echo "Missing Flutter entrypoint: $FLUTTER_TARGET" >&2; exit 1; }
echo "Configuring iOS for $XEALTH_APP_ENVIRONMENT using $FLUTTER_TARGET as build $CI_BUILD_NUMBER"

if [ ! -d "$HOME/flutter/.git" ]; then
  git init -q "$HOME/flutter"
  git -C "$HOME/flutter" remote add origin "$FLUTTER_REPOSITORY"
fi
# Release tags are required for Flutter's pub SDK constraint detection.
git -C "$HOME/flutter" fetch -q --depth 1 --tags origin "$FLUTTER_REVISION"
git -C "$HOME/flutter" checkout -q --detach "$FLUTTER_REVISION"
export PATH="$HOME/flutter/bin:$PATH"

flutter --version
if ! flutter --version --machine | grep -Eq '"frameworkVersion"[[:space:]]*:[[:space:]]*"[1-9][0-9]*\.'; then
  echo "Pinned Flutter has no valid release version; check its Git release tags." >&2
  exit 1
fi

flutter precache --ios
flutter pub get
if [ ! -f ios/Podfile ]; then
  # Reconcile checked-in Swift pins with Flutter's generated plugin graph.
  defaults write com.apple.dt.Xcode IDEDisableAutomaticPackageResolution -bool NO
  defaults write com.apple.dt.Xcode IDEPackageOnlyUseVersionsFromResolvedFile -bool NO
fi
flutter build ios \
  --release \
  --config-only \
  --no-codesign \
  --build-number "$CI_BUILD_NUMBER" \
  -t "$FLUTTER_TARGET"

if [ -f ios/Podfile ]; then
  cd ios
  pod install --repo-update
fi
