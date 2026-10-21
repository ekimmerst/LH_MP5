local DURATION = 5
local driver = CreateFrame("Frame")
local overlay, spark, bar, castEnd

local function Readable(value)
    if issecretvalue and issecretvalue(value) then return false end
    if canaccessvalue and not canaccessvalue(value) then return false end
    return true
end

local function UsesMana()
    local powerType = UnitPowerType("player")
    return Readable(powerType) and powerType == 0
end

local function CostsMana(spellID)
    if not Readable(spellID) or type(spellID) ~= "number" then return false end
    local getCosts = C_Spell and C_Spell.GetSpellPowerCost or GetSpellPowerCost
    if not getCosts then return false end
    local costs = getCosts(spellID)
    if not Readable(costs) or type(costs) ~= "table" then return false end
    for _, info in ipairs(costs) do
        if Readable(info.type) and info.type == 0
            and Readable(info.cost) and type(info.cost) == "number" and info.cost > 0 then
            return true
        end
    end
    return false
end

local function Attach()
    local player = PlayerFrame
    local main = player and player.PlayerFrameContent
        and player.PlayerFrameContent.PlayerFrameContentMain
    local target = PlayerFrameManaBar or (player and player.manabar)
        or (main and main.ManaBarArea and main.ManaBarArea.ManaBar)
    if not target then return end
    if not overlay then
        overlay = CreateFrame("Frame", nil, target)
        overlay:EnableMouse(false)
        spark = overlay:CreateTexture(nil, "OVERLAY")
        spark:SetTexture("Interface\\CastingBar\\UI-CastingBar-Spark")
        spark:SetBlendMode("ADD")
        spark:SetAlpha(0.65)
        spark:Hide()
    end
    if bar ~= target then
        overlay:SetParent(target)
        overlay:ClearAllPoints()
        overlay:SetAllPoints(target)
        bar = target
    end
    overlay:SetFrameLevel(bar:GetFrameLevel() + 5)
end

local function Reset()
    castEnd = nil
    if spark then spark:Hide() end
end

local function Update()
    if not castEnd then return end
    if not UsesMana() then
        Reset()
        return
    end
    local remaining = castEnd - GetTime()
    if remaining <= 0 then
        Reset()
    elseif spark then
        if bar:IsShown() then
            spark:SetSize(16, bar:GetHeight() * 2)
            spark:ClearAllPoints()
            spark:SetPoint("CENTER", overlay, "LEFT", bar:GetWidth() * remaining / DURATION, 0)
            spark:Show()
        else
            spark:Hide()
        end
    end
end

driver:SetScript("OnEvent", function(_, event, unit, castGUID, spellID)
    if event == "PLAYER_ENTERING_WORLD" then
        Attach()
        Reset()
    elseif event == "ADDON_LOADED" then
        Attach()
    elseif Readable(unit) and unit == "player" then
        if event == "UNIT_DISPLAYPOWER" then
            Attach()
            Reset()
        elseif event == "UNIT_SPELLCAST_SUCCEEDED" and UsesMana() and CostsMana(spellID) then
            -- Estimate from spell costs; current mana may be a protected value.
            castEnd = GetTime() + DURATION
            Update()
        end
    end
end)
driver:SetScript("OnUpdate", Update)
for _, event in ipairs({ "PLAYER_ENTERING_WORLD", "ADDON_LOADED",
    "UNIT_SPELLCAST_SUCCEEDED", "UNIT_DISPLAYPOWER" }) do
    driver:RegisterEvent(event)
end
