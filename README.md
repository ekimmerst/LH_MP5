# LH_MP5

Version: 1.3.3

LH_MP5 is a lightweight World of Warcraft AddOn that displays an estimated five-second-rule timer directly on Blizzard's default player mana bar.

## Features

- A subtle spark moves from right to left across the mana bar over five seconds.
- Successful spells with a reported mana cost restart the timer.
- Wand shots and spells with no reported mana cost leave an existing timer running.
- Automatically hides for rage, energy, and other resources.
- No configuration, slash commands, or dependencies.

## Installation

1. Copy the addon files into your WoW client's `Interface/AddOns` directory.
2. Name the AddOn folder `LH_MP5`. It should contain `LH_MP5.toc` and `LH_MP5.lua` directly.
3. Restart WoW and enable **LH_MP5** in the character selection screen's AddOns list.

After updating an existing installation, use `/reload` to load the changes.

## Upgrading from MiniMP5

Replace the old `MiniMP5` folder with `LH_MP5` and fully restart WoW. Enable **LH_MP5** in the AddOns list. Do not enable both versions together. There are no saved settings to migrate.

## Usage

Play a character that uses mana with Blizzard's default player frame visible. After a successful spell with a reported mana cost, a spark appears at the right edge of the mana bar. It travels left for five seconds, then disappears. Another qualifying spell restarts the timer.

## Limitations

The timer estimates the five-second rule from spell costs reported by the game API. It does not measure actual mana spent or detect the start of mana regeneration. Temporary cost reductions are reflected only when the API reports them; unreadable spell data is skipped.

LH_MP5 attaches to Blizzard's player mana bar. Replacement unit frames are not supported.

## Changelog

### 1.3.3 - 2026-10-21

- Renamed MiniMP5 to LH_MP5, including the addon folder, Lua/TOC filenames, metadata and documentation.
- Timer behavior is unchanged; no configuration or slash commands are required.
