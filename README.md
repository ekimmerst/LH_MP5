# LH_MP5

Version: 1.4.0

LH_MP5 is a lightweight World of Warcraft AddOn that displays an estimated five-second-rule timer directly on Blizzard's default player mana bar.

## Features

- A subtle spark moves from right to left across the mana bar over five seconds.
- Successful spells with a reported mana cost restart the timer.
- Wand shots and spells with no reported mana cost leave an existing timer running.
- Automatically hides for rage, energy, and other resources.
- Native enable/disable control under LH Tweaks, saved per character; enabled by default.

## Installation

1. Copy the addon files into your WoW client's `Interface/AddOns` directory.
2. Name the AddOn folder `LH_MP5`. Keep LH_MP5.toc, LH_MP5.lua, Settings.lua and the Media folder. Install and enable LH_Tweaks as well.
3. Restart WoW and enable **LH MP5**, grouped under **LH Tweaks**, in the character selection screen's AddOns list.

Fully restart WoW after updating to 1.4.0 because the TOC loads a new settings file and adds saved-variable, grouping and icon metadata.

## Upgrading from MiniMP5

Replace the old `MiniMP5` folder with `LH_MP5` and fully restart WoW. Enable **LH MP5** in the AddOns list. Do not enable both versions together. Versions before 1.4.0 had no saved settings to migrate.

## Usage

Play a character that uses mana with Blizzard's default player frame visible. After a successful spell with a reported mana cost, a spark appears at the right edge of the mana bar. It travels left for five seconds, then disappears. Another qualifying spell restarts the timer.

Open WoW Settings > AddOns > LH Tweaks > LH MP5, or type `/lh_mp5`, to enable or disable the timer. You can also use `/lh_mp5 on` and `/lh_mp5 off`. Both paths update the existing runtime immediately: disabling clears the current spark and timer; enabling waits for the next qualifying spell. The setting defaults to enabled to preserve the previous behavior and is saved per character as `LH_MP5DB.enabled`. Blizzard's Defaults for this category restores enabled mode.

The AddOn list uses the shared LH icon. Media/Icon.png and Media/Icon.tga are exact copies of LH_Tweaks' gold LH artwork, using Spoken's chamfered gold frame as the reference. There is no runtime Spoken dependency.

## Limitations

The timer estimates the five-second rule from spell costs reported by the game API. It does not measure actual mana spent or detect the start of mana regeneration. Temporary cost reductions are reflected only when the API reports them; unreadable spell data is skipped.

LH_MP5 attaches to Blizzard's player mana bar. Replacement unit frames are not supported.

## Verification

`.settings-test.py` passed Lua 5.1 simulations for all three supported Blizzard mana-bar hierarchies, late frame loading, native host registration, default/saved settings, command/UI synchronization, immediate disable, re-enable without resuming an old timer, spark movement and expiry, qualifying casts, free/wand casts, other units, resource changes, hidden mana bars and protected/unreadable values. Modern and legacy spell-cost APIs are covered, and raw mana reads are forbidden by the harness. Shared icons are verified byte-for-byte against LH_Tweaks; `git diff --check` passed.

Run `python LH_MP5/.settings-test.py` from the AddOns folder with Lupa available in `LH_Tweaks/.test-runtime`. In-game rendering remains pending: fully restart WoW, open `/lh_mp5`, cast a mana-cost spell, toggle the timer during its animation and check the saved setting after `/reload`.

## Changelog

### 1.4.0 - 2026-10-21

- Added a native LH MP5 options page under LH Tweaks, with an enabled-by-default per-character activation checkbox.
- Added `/lh_mp5` to open settings and `/lh_mp5 on|off` for immediate toggling. Disabling clears the current timer; enabling starts no timer until the next qualifying cast.
- Added the shared LH icon and native AddOn list grouping under LH Tweaks.
- Preserved the five-second duration, appearance, reported-mana-cost detection and supported Blizzard mana-bar layouts.

### 1.3.3 - 2026-10-21

- Renamed MiniMP5 to LH_MP5, including the addon folder, Lua/TOC filenames, metadata and documentation.
- Timer behavior is unchanged; no configuration or slash commands are required.

## Required core addon

Install and enable **LH_Tweaks** alongside this addon. LH_Tweaks is the shared LiteHawk configuration host and must load first. CurseForge releases must list LH_Tweaks as a required dependency so the client installs it automatically.
