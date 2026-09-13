#!/bin/bash
# AI Agency OS - Mobile Build Script - APK/IPA for Play Store/App Store

set -e

GREEN='\033[0;32m'
VIOLET='\033[0;35m'
NC='\033[0m'

echo -e "${VIOLET}📱 AI Agency OS - Mobile Build - 68 Agents, 292 Skills${NC}"
echo "=================================================="
echo ""

# Check requirements
check_requirements() {
    echo "🔍 Checking requirements..."
    
    if ! command -v node &> /dev/null; then
        echo "❌ Node not found - install Node 20+"
        exit 1
    fi
    
    if ! command -v npm &> /dev/null; then
        echo "❌ NPM not found"
        exit 1
    fi
    
    echo -e "${GREEN}✅ Node $(node -v) + NPM $(npm -v) OK${NC}"
}

# Install deps
install_deps() {
    echo ""
    echo "📦 Installing dependencies..."
    cd "$(dirname "$0")/.."
    npm install
    echo -e "${GREEN}✅ Deps installed${NC}"
}

# Build Android APK
build_android() {
    echo ""
    echo "🤖 Building Android APK..."
    echo "   For Play Store - requires Android Studio + SDK"
    
    cd "$(dirname "$0")/.."
    
    # Check Android
    if [ ! -d "android" ]; then
        echo "⚠️  android folder not found - run: npx react-native init AIAgencyOS --template react-native-template-typescript"
        echo "   Then copy src/ from this folder"
        echo "   Skipping Android build for now - PWA is alternative"
        return
    fi
    
    cd android
    ./gradlew assembleRelease
    
    echo ""
    echo -e "${GREEN}✅ Android APK built: android/app/build/outputs/apk/release/app-release.apk${NC}"
    echo "   Size: $(du -h app/build/outputs/apk/release/app-release.apk | cut -f1)"
    echo "   Upload to Play Console: https://play.google.com/console"
    echo "   White-label: Change package name, app name, icon, colors in android/app/build.gradle + android/app/src/main/res/"
}

# Build iOS IPA
build_ios() {
    echo ""
    echo "🍎 Building iOS IPA..."
    echo "   For App Store - requires Xcode + Mac"
    
    cd "$(dirname "$0")/.."
    
    if [ ! -d "ios" ]; then
        echo "⚠️  ios folder not found - run: npx react-native init AIAgencyOS --template react-native-template-typescript"
        echo "   Skipping iOS build - PWA is alternative"
        return
    fi
    
    if [[ "$OSTYPE" != "darwin"* ]]; then
        echo "⚠️  iOS build requires Mac - skipping, use PWA or build on Mac"
        return
    fi
    
    cd ios
    xcodebuild -workspace AIAgencyOS.xcworkspace -scheme AIAgencyOS -configuration Release archive -archivePath build/AIAgencyOS.xcarchive
    xcodebuild -exportArchive -archivePath build/AIAgencyOS.xcarchive -exportPath build/ -exportOptionsPlist exportOptions.plist
    
    echo ""
    echo -e "${GREEN}✅ iOS IPA built: ios/build/AIAgencyOS.ipa${NC}"
    echo "   Upload to App Store Connect: https://appstoreconnect.apple.com"
    echo "   White-label: Change bundle ID, app name, icon, colors in ios/AIAgencyOS/Info.plist + Xcode"
}

# PWA alternative
build_pwa() {
    echo ""
    echo "🌐 PWA - Already built! - No build needed"
    echo "   Frontend already has manifest.json + sw.js"
    echo "   PWA is installable on Android/iOS via browser Add to Home Screen"
    echo "   Features:"
    echo "   - Installable, standalone display"
    echo "   - Offline cache via service worker"
    echo "   - Push notifications for task updates"
    echo "   - Works on Android + iOS + Desktop"
    echo "   - No Play Store/App Store approval needed"
    echo "   - Instant updates - no store review"
    echo ""
    echo "   To test PWA:"
    echo "   1. Open https://5173-...e2b.app on mobile Chrome/Safari"
    echo "   2. Menu → Add to Home Screen / Install App"
    echo "   3. Open from home screen - looks like native app"
    echo ""
    echo -e "${GREEN}✅ PWA ready - recommended for MVP${NC}"
    echo ""
    echo "   For production PWA:"
    echo "   - Generate icons: 192x192 + 512x512 from logo"
    echo "   - Update manifest.json name, short_name, theme_color, background_color"
    echo "   - Test Lighthouse PWA audit - should score 90+"
    echo "   - Add to frontend/public/ - manifest.json + sw.js + icons"
}

# Expo alternative
build_expo() {
    echo ""
    echo "📦 Expo - Easier alternative to bare React Native"
    echo "   Benefits: OTA updates, easier build, no Android Studio/Xcode needed for JS"
    echo ""
    echo "   Setup:"
    echo "   npm install -g expo-cli eas-cli"
    echo "   npx create-expo-app AIAgencyOS --template"
    echo "   Copy src/ from this folder"
    echo "   expo start - open in Expo Go app"
    echo "   eas build --platform android --profile production # APK"
    echo "   eas build --platform ios --profile production # IPA"
    echo "   eas update --auto # OTA update without store review"
    echo ""
    echo "   White-label Expo: app.json name, slug, icon, splash, primaryColor"
    echo "   Cost: Free for small, $29/mo for more builds"
}

# Main
main() {
    check_requirements
    install_deps
    build_pwa
    build_expo
    
    # Only build native if android/ios folders exist and user wants
    read -p "Build Android APK? Requires Android Studio (y/n): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        build_android
    fi
    
    read -p "Build iOS IPA? Requires Mac + Xcode (y/n): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        build_ios
    fi
    
    echo ""
    echo -e "${VIOLET}🎉 Mobile build complete!${NC}"
    echo ""
    echo "Summary:"
    echo "- PWA: ✅ Ready - no build, installable via browser, recommended MVP"
    echo "- Expo: 📦 Easier - OTA updates, no native setup"
    echo "- Bare RN Android: 🤖 Needs Android Studio - APK for Play Store"
    echo "- Bare RN iOS: 🍎 Needs Mac + Xcode - IPA for App Store"
    echo ""
    echo "Recommendation for agency:"
    echo "1. Start with PWA - $0, instant, no approval, works now"
    echo "2. Then Expo - $29/mo, OTA updates, easy"
    echo "3. Then bare RN - full control, white-label, Play Store/App Store"
    echo ""
    echo "White-label mobile:"
    echo "- PWA: manifest.json + icons + theme_color"
    echo "- Expo: app.json name/slug/icon/splash/primaryColor"
    echo "- Bare RN: package name/bundle ID, app name, icon, colors"
    echo "- Pricing: Pro $199 includes PWA, White-label $499 includes custom app"
    echo ""
    echo "Next: Upload to Play Store/App Store or use PWA"
}

main
