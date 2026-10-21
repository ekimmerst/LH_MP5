from pathlib import Path
import sys

addon = Path(__file__).resolve().parent
core = addon.parent / 'LH_Tweaks'
sys.path.insert(0, str(core / '.test-runtime'))
from lupa.lua51 import LuaRuntime

for layout in ('global', 'legacy', 'modern'):
    lua = LuaRuntime()
    lua.globals().LAYOUT = layout
    lua.execute('''
frames={};SlashCmdList={};clock=100;power=0;cost=20;messages={}
function print(text) table.insert(messages,text) end
local M={}
function M:SetScript(k,v) self.scripts[k]=v end
function M:RegisterEvent() end
function M:EnableMouse(v) self.mouse=v end
function M:SetParent(p) self.parent=p end
function M:ClearAllPoints() self.point=nil end
function M:SetAllPoints(p) self.allPoints=p end
function M:SetPoint(...) self.point={...} end
function M:GetFrameLevel() return 2 end
function M:SetFrameLevel(v) self.frameLevel=v end
function M:GetWidth() return 120 end
function M:GetHeight() return 12 end
function M:SetSize(w,h) self.width=w;self.height=h end
function M:SetTexture(t) self.texture=t end
function M:SetBlendMode(m) self.blend=m end
function M:SetAlpha(a) self.alpha=a end
function M:IsShown() return self.shown end
function M:Show() self.shown=true end
function M:Hide() self.shown=false end
function M:CreateTexture() local t=CreateFrame('Texture',nil,self);self.spark=t;return t end
function CreateFrame(kind,name,parent)
 local f=setmetatable({kind=kind,parent=parent,scripts={},shown=true},{__index=M});frames[#frames+1]=f;return f
end
function GetTime() return clock end
function UnitPowerType() return power end
function UnitPower() error('Raw mana read is forbidden') end
function UnitPowerMax() error('Raw mana read is forbidden') end
secret={};inaccessible={}
function issecretvalue(v) return v==secret end
function canaccessvalue(v) return v~=inaccessible end
C_Spell={GetSpellPowerCost=function() return {{type=0,cost=cost}} end}
registry={};notices={};Settings={}
function Settings.RegisterVerticalLayoutSubcategory(parent,title)
 local c={parent=parent,title=title};function c:GetID() return self.title end
 local l={rows={}};function l:AddInitializer(row) table.insert(self.rows,row) end;c.layout=l;return c,l
end
function Settings.RegisterAddOnCategory(c) registered=c end
function Settings.RegisterProxySetting(c,v,kind,label,default,get,set)
 local s={default=default,get=get,set=set};registry[v]=s;return s
end
function Settings.CreateCheckbox(c,s,t) c.layout:AddInitializer({setting=s,tooltip=t}) end
function Settings.NotifyUpdate(v) notices[v]=(notices[v] or 0)+1 end
function Settings.OpenToCategory(id) opened=id end
function CreateSettingsListSectionHeaderInitializer(t) return {header=t} end
LH_Tweaks={modules={}}
''')
    source = (core / 'LH_Tweaks.lua').read_text()
    registration = source.split('function Hub:RegisterModule(id, title, build)')[1].split('\nfunction Hub:RestoreDefaults')[0]
    lua.execute('local Hub=LH_Tweaks\nfunction Hub:RegisterModule(id, title, build)' + registration)
    source = (core / 'Settings.lua').read_text()
    registration = source.split('function Hub:RegisterModulePage(id)')[1].split('\nlocal function RegisterSettings')[0]
    lua.execute('local Hub=LH_Tweaks\nfunction Hub:RegisterModulePage(id)' + registration)
    lua.execute((addon / 'LH_MP5.lua').read_text(), 'LH_MP5')
    lua.execute((addon / 'Settings.lua').read_text(), 'LH_MP5')
    lua.execute('''
local driver=frames[1]
local function fire(event,unit,id) driver.scripts.OnEvent(driver,event,unit,'cast',id) end
local function cast(id) fire('UNIT_SPELLCAST_SUCCEEDED','player',id or 1) end
local function tick(time) clock=time;driver.scripts.OnUpdate(driver,.1) end
assert(LH_Tweaks.modules.LH_MP5 and not registered)
fire('ADDON_LOADED','LH_MP5');assert(LH_MP5DB.enabled)
-- Late Blizzard player frame loading, for every supported mana-bar hierarchy.
target=CreateFrame('StatusBar')
if LAYOUT=='global' then PlayerFrameManaBar=target
elseif LAYOUT=='legacy' then PlayerFrame={manabar=target}
else PlayerFrame={PlayerFrameContent={PlayerFrameContentMain={ManaBarArea={ManaBar=target}}}} end
fire('ADDON_LOADED','Blizzard_UnitFrame')
local overlay,spark
for _,f in ipairs(frames) do if f.parent==target then overlay=f;spark=f.spark end end
assert(overlay and spark and not overlay.mouse and not spark.shown)
LH_Tweaks.category={};LH_Tweaks:RegisterModulePage('LH_MP5')
local setting=registry.LH_MP5_enabled
assert(registered.parent==LH_Tweaks.category and registered.title=='LH MP5')
assert(setting.default and setting.get() and #registered.layout.rows==2)
SlashCmdList.LH_MP5();assert(opened=='LH MP5')
cast();assert(spark.shown and spark.point[4]==120 and spark.height==24)
tick(102.5);assert(spark.point[4]==60)
-- Free casts and wand shots preserve the existing timer.
cost=0;cast(5019);tick(104);assert(spark.point[4]==24)
cost=20;cast();tick(106.5);assert(spark.point[4]==60,'Paid cast did not restart timer')
setting.set(false);assert(not spark.shown and not LH_MP5DB.enabled)
clock=107;cast();tick(108);assert(not spark.shown)
SlashCmdList.LH_MP5(' ON ');tick(108.1);assert(not spark.shown,'Enabling resumed old timer')
assert(setting.get() and notices.LH_MP5_enabled>0)
cast();power=3;tick(109);assert(not spark.shown,'Energy/rage should hide timer')
cast();assert(not spark.shown)
power=0;cast();fire('UNIT_DISPLAYPOWER','player');assert(not spark.shown)
cast();target.shown=false;tick(110);assert(not spark.shown)
target.shown=true;tick(111);assert(spark.shown)
tick(114);assert(not spark.shown,'Timer failed to expire')
cost=secret;cast();assert(not spark.shown)
cost=inaccessible;cast();assert(not spark.shown)
cost=20;power=secret;cast();assert(not spark.shown)
power=0;fire('UNIT_SPELLCAST_SUCCEEDED','pet',1);assert(not spark.shown)
fire('UNIT_SPELLCAST_SUCCEEDED',secret,1);assert(not spark.shown)
cast(secret);assert(not spark.shown)
-- Legacy spell-cost API and category default restore the same saved flag.
GetSpellPowerCost=C_Spell.GetSpellPowerCost;C_Spell=nil
cast();assert(spark.shown)
fire('PLAYER_ENTERING_WORLD');assert(not spark.shown)
SlashCmdList.LH_MP5('off');SlashCmdList.LH_MP5('on extra');assert(not setting.get())
setting.set(setting.default);assert(setting.get())
LH_MP5DB.enabled=false;fire('ADDON_LOADED','LH_MP5');fire('PLAYER_ENTERING_WORLD');cast()
assert(not setting.get() and not spark.shown,'Saved disabled mode lost')
''')
    print(f'PASS: {layout} mana bar, host settings, defaults, timer movement/restarts, disable/re-enable, free spells, resource changes, protected values and saved mode')

for ext in ('png', 'tga'):
    assert (addon / f'Media/Icon.{ext}').read_bytes() == (core / f'Icon.{ext}').read_bytes()
toc = (addon / 'LH_MP5.toc').read_text()
assert '## Group: LH_Tweaks' in toc and '## SavedVariablesPerCharacter: LH_MP5DB' in toc and 'Settings.lua' in toc
print('PASS: shared icon files and integration metadata')
