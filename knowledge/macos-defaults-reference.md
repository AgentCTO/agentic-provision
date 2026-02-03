# macOS Defaults Reference

A comprehensive guide to configuring macOS system preferences via the `defaults` command. This reference is used by the provisioning agent to guide users through Mac configuration.

---

## Agent Configuration Profiles

The agent should offer these preset configurations during the "Mac Settings" phase of provisioning.

### Profile: Developer Essentials
**For:** All developers
**Changes:** Finder shows hidden files, fast key repeat, disable auto-correct, expand save dialogs

```bash
# Finder: Show hidden files and extensions
defaults write com.apple.finder AppleShowAllFiles -bool true
defaults write NSGlobalDomain AppleShowAllExtensions -bool true
defaults write com.apple.finder ShowPathbar -bool true
defaults write com.apple.finder ShowStatusBar -bool true
defaults write com.apple.finder _FXShowPosixPathInTitle -bool true

# Finder: Use column view, search current folder
defaults write com.apple.finder FXPreferredViewStyle -string "clmv"
defaults write com.apple.finder FXDefaultSearchScope -string "SCcf"

# Disable annoying warnings
defaults write com.apple.finder FXEnableExtensionChangeWarning -bool false
defaults write NSGlobalDomain NSNavPanelExpandedStateForSaveMode -bool true
defaults write NSGlobalDomain NSNavPanelExpandedStateForSaveMode2 -bool true

# Keyboard: Fast repeat, no auto-correct
defaults write NSGlobalDomain KeyRepeat -int 2
defaults write NSGlobalDomain InitialKeyRepeat -int 15
defaults write NSGlobalDomain ApplePressAndHoldEnabled -bool false
defaults write NSGlobalDomain NSAutomaticCapitalizationEnabled -bool false
defaults write NSGlobalDomain NSAutomaticSpellingCorrectionEnabled -bool false
defaults write NSGlobalDomain NSAutomaticQuoteSubstitutionEnabled -bool false
defaults write NSGlobalDomain NSAutomaticDashSubstitutionEnabled -bool false
defaults write NSGlobalDomain AppleKeyboardUIMode -int 3

# Save to disk, not iCloud
defaults write NSGlobalDomain NSDocumentSaveNewDocumentsToCloud -bool false

# TextEdit: Plain text by default
defaults write com.apple.TextEdit RichText -int 0
```

### Profile: Minimal Dock
**For:** Users who want a clean, fast Dock
**Changes:** Auto-hide, no recents, small icons, fast animations

```bash
# Small icons, auto-hide
defaults write com.apple.dock tilesize -int 36
defaults write com.apple.dock autohide -bool true
defaults write com.apple.dock autohide-delay -float 0
defaults write com.apple.dock autohide-time-modifier -float 0.3

# No recents, no rearranging spaces
defaults write com.apple.dock show-recents -bool false
defaults write com.apple.dock mru-spaces -bool false

# Fast minimize
defaults write com.apple.dock mineffect -string "scale"
defaults write com.apple.dock minimize-to-application -bool true
```

### Profile: Power User Dock
**For:** Users who want more from their Dock
**Changes:** Left position, magnification, medium size

```bash
defaults write com.apple.dock orientation -string "left"
defaults write com.apple.dock tilesize -int 48
defaults write com.apple.dock magnification -bool true
defaults write com.apple.dock largesize -int 72
defaults write com.apple.dock autohide -bool false
defaults write com.apple.dock show-recents -bool false
```

### Profile: Screenshot Pro
**For:** Developers who take lots of screenshots
**Changes:** PNG format, dedicated folder, no shadows

```bash
defaults write com.apple.screencapture type -string "png"
defaults write com.apple.screencapture disable-shadow -bool true
defaults write com.apple.screencapture location -string "~/Screenshots"
defaults write com.apple.screencapture include-date -bool true
mkdir -p ~/Screenshots
```

### Profile: Safari Developer
**For:** Web developers using Safari
**Changes:** Developer menu, Web Inspector, full URLs

```bash
defaults write com.apple.Safari IncludeDevelopMenu -bool true
defaults write com.apple.Safari WebKitDeveloperExtrasEnabledPreferenceKey -bool true
defaults write com.apple.Safari com.apple.Safari.ContentPageGroupIdentifier.WebKit2DeveloperExtrasEnabled -bool true
defaults write NSGlobalDomain WebKitDeveloperExtras -bool true
defaults write com.apple.Safari ShowFullURLInSmartSearchField -bool true
defaults write com.apple.Safari ShowStatusBar -bool true
defaults write com.apple.Safari AutoOpenSafeDownloads -bool false
```

### Profile: Trackpad Power User
**For:** Laptop users who want maximum trackpad productivity
**Changes:** Tap to click, three-finger drag, fast tracking

```bash
# Tap to click
defaults write com.apple.AppleMultitouchTrackpad Clicking -bool true
defaults write com.apple.driver.AppleBluetoothMultitouch.trackpad Clicking -bool true
defaults -currentHost write NSGlobalDomain com.apple.mouse.tapBehavior -int 1

# Three-finger drag
defaults write com.apple.AppleMultitouchTrackpad TrackpadThreeFingerDrag -bool true
defaults write com.apple.driver.AppleBluetoothMultitouch.trackpad TrackpadThreeFingerDrag -bool true

# Fast tracking
defaults write NSGlobalDomain com.apple.trackpad.scaling -float 2.5

# Secondary click
defaults write com.apple.AppleMultitouchTrackpad TrackpadRightClick -bool true
```

### Profile: Privacy Focused
**For:** Security-conscious users
**Changes:** Disable analytics, secure keyboard, minimal telemetry

```bash
# Disable crash reporter dialog
defaults write com.apple.CrashReporter DialogType -string "none"

# Don't send search queries to Apple
defaults write com.apple.Safari UniversalSearchEnabled -bool false
defaults write com.apple.Safari SuppressSearchSuggestions -bool true

# Secure keyboard entry in Terminal
defaults write com.apple.terminal SecureKeyboardEntry -bool true

# Safari: Do Not Track
defaults write com.apple.Safari SendDoNotTrackHTTPHeader -bool true

# Disable Siri suggestions
defaults write com.apple.Siri SiriPrefStashedStatusMenuVisible -bool false
defaults write com.apple.Siri VoiceTriggerUserEnabled -bool false
```

---

## Agent Question Flow

The agent should present Mac settings configuration using these questions:

### Question 1: Developer Defaults
```
Would you like to configure macOS for development?

A) Yes - Apply developer-friendly defaults (show hidden files, fast key repeat, disable auto-correct)
B) Minimal - Just the essentials (show hidden files and extensions)
C) Skip - Keep current settings
D) Custom - Let me choose individual settings
```

### Question 2: Dock Configuration
```
How would you like your Dock configured?

A) Minimal - Auto-hide, small icons, no recents, fast animations
B) Power User - Left side, magnification, medium icons
C) Default - Keep macOS default Dock settings
D) Custom - Let me configure specific options
```

### Question 3: Keyboard Settings
```
Configure keyboard for coding?

A) Speed Demon - Fastest key repeat, no delays
B) Balanced - Fast but not extreme
C) Default - Keep macOS defaults
D) Custom - Let me adjust specific settings
```

### Question 4: Screenshots
```
Set up a screenshots workflow?

A) Pro Setup - PNG format, ~/Screenshots folder, no shadows
B) Quick Setup - Just change location to ~/Screenshots
C) Skip - Keep default screenshot behavior
```

### Question 5: Trackpad (if laptop detected)
```
Optimize trackpad for development?

A) Power User - Tap to click, three-finger drag, fast tracking
B) Minimal - Just enable tap to click
C) Skip - Keep current trackpad settings
```

### Question 6: Safari Developer Tools (if Safari chosen as browser)
```
Enable Safari developer features?

A) Yes - Developer menu, Web Inspector, full URLs
B) Skip - Keep Safari defaults
```

---

## Understanding macOS Defaults

### What Are Defaults?
macOS stores preferences in property list (plist) files. The `defaults` command reads and writes these preferences.

### Basic Syntax
```bash
# Read a preference
defaults read <domain> <key>

# Write a preference
defaults write <domain> <key> <type> <value>

# Delete a preference (revert to default)
defaults delete <domain> <key>

# List all keys in a domain
defaults read <domain>

# Find all domains
defaults domains
```

### Common Types
- `-bool true/false` - Boolean
- `-int <number>` - Integer
- `-float <number>` - Float
- `-string "text"` - String
- `-array <items>` - Array
- `-dict <key> <value>` - Dictionary

### Applying Changes
Many defaults require restarting the affected application:
```bash
killall Finder
killall Dock
killall SystemUIServer
```

Some require logging out and back in.

---

## Complete Reference by Category

### Finder Settings

#### Show Hidden Files
```bash
# Show hidden files
defaults write com.apple.finder AppleShowAllFiles -bool true

# Hide hidden files (default)
defaults write com.apple.finder AppleShowAllFiles -bool false
```

#### Show File Extensions
```bash
# Always show extensions
defaults write NSGlobalDomain AppleShowAllExtensions -bool true
```

#### Path Bar and Status Bar
```bash
# Show path bar
defaults write com.apple.finder ShowPathbar -bool true

# Show status bar
defaults write com.apple.finder ShowStatusBar -bool true

# Show full path in title bar
defaults write com.apple.finder _FXShowPosixPathInTitle -bool true
```

#### Default View
```bash
# Icon view (icnv), List view (Nlsv), Column view (clmv), Gallery view (glyv)
defaults write com.apple.finder FXPreferredViewStyle -string "clmv"
```

#### Search Scope
```bash
# Search current folder by default
defaults write com.apple.finder FXDefaultSearchScope -string "SCcf"
```

#### File Dialogs
```bash
# Expand save panel by default
defaults write NSGlobalDomain NSNavPanelExpandedStateForSaveMode -bool true
defaults write NSGlobalDomain NSNavPanelExpandedStateForSaveMode2 -bool true

# Expand print panel by default
defaults write NSGlobalDomain PMPrintingExpandedStateForPrint -bool true
defaults write NSGlobalDomain PMPrintingExpandedStateForPrint2 -bool true
```

#### Disable Warnings
```bash
# Disable warning when changing file extension
defaults write com.apple.finder FXEnableExtensionChangeWarning -bool false

# Disable warning when emptying trash
defaults write com.apple.finder WarnOnEmptyTrash -bool false
```

#### Desktop Icons
```bash
# Show icons on desktop
defaults write com.apple.finder CreateDesktop -bool true

# Show hard drives on desktop
defaults write com.apple.finder ShowHardDrivesOnDesktop -bool true

# Show external drives on desktop
defaults write com.apple.finder ShowExternalHardDrivesOnDesktop -bool true

# Show mounted servers on desktop
defaults write com.apple.finder ShowMountedServersOnDesktop -bool true

# Show removable media on desktop
defaults write com.apple.finder ShowRemovableMediaOnDesktop -bool true
```

#### New Finder Window Location
```bash
# New windows open in home folder
defaults write com.apple.finder NewWindowTarget -string "PfHm"
defaults write com.apple.finder NewWindowTargetPath -string "file://${HOME}/"

# New windows open in Downloads
defaults write com.apple.finder NewWindowTarget -string "PfLo"
defaults write com.apple.finder NewWindowTargetPath -string "file://${HOME}/Downloads/"
```

#### Apply Finder Changes
```bash
killall Finder
```

---

### Dock Settings

#### Size and Magnification
```bash
# Set dock icon size (pixels)
defaults write com.apple.dock tilesize -int 48

# Enable magnification
defaults write com.apple.dock magnification -bool true

# Set magnified icon size
defaults write com.apple.dock largesize -int 64
```

#### Position
```bash
# Position: left, bottom, right
defaults write com.apple.dock orientation -string "left"
```

#### Auto-hide
```bash
# Enable auto-hide
defaults write com.apple.dock autohide -bool true

# Remove auto-hide delay
defaults write com.apple.dock autohide-delay -float 0

# Speed up auto-hide animation
defaults write com.apple.dock autohide-time-modifier -float 0.5
```

#### Minimize Effect
```bash
# Minimize effect: genie, scale
defaults write com.apple.dock mineffect -string "scale"

# Minimize windows into application icon
defaults write com.apple.dock minimize-to-application -bool true
```

#### Recent Items and Recents
```bash
# Don't show recent applications
defaults write com.apple.dock show-recents -bool false

# Remove all persistent apps (start fresh)
defaults write com.apple.dock persistent-apps -array
```

#### Spaces and Mission Control
```bash
# Don't automatically rearrange Spaces based on recent use
defaults write com.apple.dock mru-spaces -bool false

# Group windows by application in Mission Control
defaults write com.apple.dock expose-group-apps -bool true

# Speed up Mission Control animation
defaults write com.apple.dock expose-animation-duration -float 0.1
```

#### Hot Corners
```bash
# Hot corner actions:
# 0: no-op, 2: Mission Control, 3: Application Windows, 4: Desktop
# 5: Start Screen Saver, 6: Disable Screen Saver, 7: Dashboard
# 10: Put Display to Sleep, 11: Launchpad, 12: Notification Center
# 13: Lock Screen, 14: Quick Note

# Top left: Mission Control
defaults write com.apple.dock wvous-tl-corner -int 2
defaults write com.apple.dock wvous-tl-modifier -int 0

# Top right: Desktop
defaults write com.apple.dock wvous-tr-corner -int 4
defaults write com.apple.dock wvous-tr-modifier -int 0

# Bottom left: Start Screen Saver
defaults write com.apple.dock wvous-bl-corner -int 5
defaults write com.apple.dock wvous-bl-modifier -int 0

# Bottom right: Launchpad
defaults write com.apple.dock wvous-br-corner -int 11
defaults write com.apple.dock wvous-br-modifier -int 0
```

#### Apply Dock Changes
```bash
killall Dock
```

---

### Keyboard Settings

#### Key Repeat Speed
```bash
# Fast key repeat (lower = faster, minimum 1)
defaults write NSGlobalDomain KeyRepeat -int 2

# Short delay before key repeat (lower = shorter, minimum 10)
defaults write NSGlobalDomain InitialKeyRepeat -int 15

# Extreme speed (may be too fast for some)
defaults write NSGlobalDomain KeyRepeat -int 1
defaults write NSGlobalDomain InitialKeyRepeat -int 10
```

#### Press and Hold
```bash
# Disable press-and-hold for keys (enable key repeat everywhere)
defaults write NSGlobalDomain ApplePressAndHoldEnabled -bool false

# Re-enable press-and-hold (for accented characters)
defaults write NSGlobalDomain ApplePressAndHoldEnabled -bool true
```

#### Function Keys
```bash
# Use F1, F2, etc. as standard function keys
defaults write NSGlobalDomain com.apple.keyboard.fnState -bool true
```

#### Auto-Correction and Smart Features
```bash
# Disable automatic capitalization
defaults write NSGlobalDomain NSAutomaticCapitalizationEnabled -bool false

# Disable auto-correct
defaults write NSGlobalDomain NSAutomaticSpellingCorrectionEnabled -bool false

# Disable automatic period substitution (double-space to period)
defaults write NSGlobalDomain NSAutomaticPeriodSubstitutionEnabled -bool false

# Disable smart quotes (converts "" to "")
defaults write NSGlobalDomain NSAutomaticQuoteSubstitutionEnabled -bool false

# Disable smart dashes (converts -- to —)
defaults write NSGlobalDomain NSAutomaticDashSubstitutionEnabled -bool false

# Disable text replacement
defaults write NSGlobalDomain NSAutomaticTextReplacementEnabled -bool false
```

#### Keyboard Navigation
```bash
# Full keyboard access for all controls (Tab through all UI elements)
defaults write NSGlobalDomain AppleKeyboardUIMode -int 3
```

---

### Trackpad and Mouse

#### Trackpad Tap and Click
```bash
# Enable tap to click
defaults write com.apple.AppleMultitouchTrackpad Clicking -bool true
defaults write com.apple.driver.AppleBluetoothMultitouch.trackpad Clicking -bool true
defaults -currentHost write NSGlobalDomain com.apple.mouse.tapBehavior -int 1

# Enable three-finger drag
defaults write com.apple.AppleMultitouchTrackpad TrackpadThreeFingerDrag -bool true
defaults write com.apple.driver.AppleBluetoothMultitouch.trackpad TrackpadThreeFingerDrag -bool true

# Enable secondary click (two-finger click)
defaults write com.apple.AppleMultitouchTrackpad TrackpadRightClick -bool true
```

#### Scroll Direction
```bash
# Natural scrolling (true = natural, false = traditional)
defaults write NSGlobalDomain com.apple.swipescrolldirection -bool true
```

#### Tracking Speed
```bash
# Trackpad tracking speed (0 to 3, can go higher)
defaults write NSGlobalDomain com.apple.trackpad.scaling -float 2.0

# Mouse tracking speed
defaults write NSGlobalDomain com.apple.mouse.scaling -float 2.0
```

#### Gestures
```bash
# Swipe between pages with two fingers
defaults write NSGlobalDomain AppleEnableSwipeNavigateWithScrolls -bool true

# Swipe between full-screen apps with three fingers
defaults write com.apple.AppleMultitouchTrackpad TrackpadThreeFingerHorizSwipeGesture -int 2
```

---

### Screenshots

#### Format
```bash
# Format: png, jpg, gif, pdf, tiff
defaults write com.apple.screencapture type -string "png"
```

#### Location
```bash
# Change default location
defaults write com.apple.screencapture location -string "~/Screenshots"
mkdir -p ~/Screenshots

# Reset to default (Desktop)
defaults delete com.apple.screencapture location
```

#### Shadow and Appearance
```bash
# Disable shadow in window screenshots
defaults write com.apple.screencapture disable-shadow -bool true

# Re-enable shadow
defaults write com.apple.screencapture disable-shadow -bool false
```

#### Filename
```bash
# Include date in screenshot name
defaults write com.apple.screencapture include-date -bool true

# Change base name (default: "Screenshot")
defaults write com.apple.screencapture name -string "Capture"
```

#### Apply Changes
```bash
killall SystemUIServer
```

---

### Safari Developer Settings

```bash
# Show Develop menu
defaults write com.apple.Safari IncludeDevelopMenu -bool true

# Enable Web Inspector
defaults write com.apple.Safari WebKitDeveloperExtrasEnabledPreferenceKey -bool true
defaults write com.apple.Safari com.apple.Safari.ContentPageGroupIdentifier.WebKit2DeveloperExtrasEnabled -bool true

# Add context menu item for Web Inspector in all apps
defaults write NSGlobalDomain WebKitDeveloperExtras -bool true

# Show full URL in address bar
defaults write com.apple.Safari ShowFullURLInSmartSearchField -bool true

# Show status bar
defaults write com.apple.Safari ShowStatusBar -bool true

# Prevent Safari from opening safe files automatically
defaults write com.apple.Safari AutoOpenSafeDownloads -bool false

# Enable Do Not Track
defaults write com.apple.Safari SendDoNotTrackHTTPHeader -bool true

# Disable Safari suggestions
defaults write com.apple.Safari UniversalSearchEnabled -bool false
defaults write com.apple.Safari SuppressSearchSuggestions -bool true
```

---

### Terminal Settings

```bash
# Use UTF-8 only
defaults write com.apple.terminal StringEncodings -array 4

# Enable Secure Keyboard Entry
defaults write com.apple.terminal SecureKeyboardEntry -bool true

# Focus follows mouse (click-through in Terminal)
defaults write com.apple.terminal FocusFollowsMouse -bool true
```

---

### System-Wide Settings

#### Save Location
```bash
# Save to disk instead of iCloud by default
defaults write NSGlobalDomain NSDocumentSaveNewDocumentsToCloud -bool false
```

#### Crash Reporter
```bash
# Disable crash reporter dialog
defaults write com.apple.CrashReporter DialogType -string "none"

# Show crash reporter as notification
defaults write com.apple.CrashReporter DialogType -string "notification"
```

#### Time Machine
```bash
# Don't prompt to use new drives as Time Machine backup
defaults write com.apple.TimeMachine DoNotOfferNewDisksForBackup -bool true
```

#### App Store
```bash
# Enable automatic updates
defaults write com.apple.commerce AutoUpdate -bool true

# Check for updates daily
defaults write com.apple.SoftwareUpdate ScheduleFrequency -int 1
```

#### Disk Images
```bash
# Disable disk image verification (faster mounting)
defaults write com.apple.frameworks.diskimages skip-verify -bool true
defaults write com.apple.frameworks.diskimages skip-verify-locked -bool true
defaults write com.apple.frameworks.diskimages skip-verify-remote -bool true

# Auto-open a new Finder window when a volume is mounted
defaults write com.apple.frameworks.diskimages auto-open-ro-root -bool true
defaults write com.apple.frameworks.diskimages auto-open-rw-root -bool true
defaults write com.apple.finder OpenWindowForNewRemovableDisk -bool true
```

#### Bluetooth Audio
```bash
# Improve Bluetooth audio quality
defaults write com.apple.BluetoothAudioAgent "Apple Bitpool Min (editable)" -int 40
```

---

### Menu Bar

#### Battery
```bash
# Show battery percentage
defaults write com.apple.menuextra.battery ShowPercent -string "YES"
```

#### Clock
```bash
# Show date in menu bar clock
defaults write com.apple.menuextra.clock DateFormat -string "EEE d MMM HH:mm"

# Show seconds
defaults write com.apple.menuextra.clock DateFormat -string "EEE d MMM HH:mm:ss"

# Flash separators
defaults write com.apple.menuextra.clock FlashDateSeparators -bool true
```

---

### TextEdit

```bash
# Use plain text by default
defaults write com.apple.TextEdit RichText -int 0

# Open and save files as UTF-8
defaults write com.apple.TextEdit PlainTextEncoding -int 4
defaults write com.apple.TextEdit PlainTextEncodingForWrite -int 4

# Disable smart quotes in TextEdit
defaults write com.apple.TextEdit SmartQuotes -bool false
```

---

### Activity Monitor

```bash
# Show all processes
defaults write com.apple.ActivityMonitor ShowCategory -int 0

# Sort by CPU usage
defaults write com.apple.ActivityMonitor SortColumn -string "CPUUsage"
defaults write com.apple.ActivityMonitor SortDirection -int 0

# Show CPU usage in Dock icon
defaults write com.apple.ActivityMonitor IconType -int 5

# Show all CPUs in Dock icon
defaults write com.apple.ActivityMonitor IconType -int 6
```

---

### Xcode (if installed)

```bash
# Show build times
defaults write com.apple.dt.Xcode ShowBuildOperationDuration -bool true

# Enable internal debug menu
defaults write com.apple.dt.Xcode ShowDVTDebugMenu -bool true

# Add counterpart to jump bar
defaults write com.apple.dt.Xcode IDEAdditionalCounterpartSuffixes -array-add "ViewModel" "View"
```

---

## Detecting Current Settings

Before making changes, the agent should check current values:

```bash
# Check if hidden files are shown
defaults read com.apple.finder AppleShowAllFiles 2>/dev/null || echo "not set"

# Check dock auto-hide
defaults read com.apple.dock autohide 2>/dev/null || echo "not set"

# Check key repeat speed
defaults read NSGlobalDomain KeyRepeat 2>/dev/null || echo "not set"
```

---

## Reverting Changes

```bash
# Delete a specific default to revert to system default
defaults delete <domain> <key>

# Reset entire application preferences
defaults delete <domain>

# Example: Reset all Finder preferences
defaults delete com.apple.finder
killall Finder
```

---

## Important Notes

### System Integrity Protection (SIP)
Some defaults cannot be changed with SIP enabled. These are generally not recommended to modify.

### macOS Version Differences
Some defaults may change between macOS versions. The agent should test commands before executing.

### Login Required
Some changes require logging out and back in to take effect:
- Keyboard settings
- Trackpad settings
- Some system-wide preferences

### Common Domains
- `NSGlobalDomain` - System-wide preferences
- `com.apple.finder` - Finder
- `com.apple.dock` - Dock
- `com.apple.Safari` - Safari
- `com.apple.terminal` - Terminal
- `com.apple.screencapture` - Screenshots
- `com.apple.TextEdit` - TextEdit
- `com.apple.ActivityMonitor` - Activity Monitor

### Finding New Defaults
```bash
# Compare before and after changing a setting in System Preferences
defaults read > before.txt
# Change setting in UI
defaults read > after.txt
diff before.txt after.txt
```
