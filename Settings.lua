local addonName = ...
local Addon = LH_MP5
local variable = "LH_MP5_enabled"

function Addon:RefreshSettings()
    if self.notifying or not Settings or not Settings.NotifyUpdate then return end
    self.notifying = true
    Settings.NotifyUpdate(variable)
    self.notifying = false
end

local function Build(category, layout)
    Addon.category = category
    layout:AddInitializer(CreateSettingsListSectionHeaderInitializer("Five-second rule"))
    local setting = Settings.RegisterProxySetting(category, variable, "boolean", "Enable the mana regeneration timer", true,
        function() return Addon:IsEnabled() end,
        function(value) Addon:SetEnabled(value) end)
    Settings.CreateCheckbox(category, setting,
        "Show an estimated five-second timer on Blizzard's player mana bar after successful spells with a reported mana cost. Free spells and wand shots do not restart it. Hidden for other resources. Disabling clears the current timer; enabling waits for the next qualifying spell. Enabled by default; saved per character.")
end

LH_Tweaks:RegisterModule(addonName, "LH MP5", Build)
