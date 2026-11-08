import json, ssl, urllib.request
from pathlib import Path
import certifi
from kivy.app import App
API="https://pokeapi.co/api/v2"
def cache_dir():
 p=Path(App.get_running_app().user_data_dir)/"cache";p.mkdir(parents=True,exist_ok=True);return p
def get_json(url,name):
 p=cache_dir()/name
 if p.exists():
  try:return json.loads(p.read_text(encoding="utf-8"))
  except:pass
 req=urllib.request.Request(url,headers={"User-Agent":"PokeStat-Mobile/0.7"})
 ctx=ssl.create_default_context(cafile=certifi.where())
 with urllib.request.urlopen(req,timeout=30,context=ctx) as r:d=json.load(r)
 p.write_text(json.dumps(d,ensure_ascii=False),encoding="utf-8");return d
def standard_catalog():
 # Keep the 1,025 standard species and add every Mega entry exposed by PokéAPI.
 # A new cache name prevents an old 1,025-only catalog from hiding Z-A forms.
 d=get_json(f"{API}/pokemon?limit=100000&offset=0","catalog_standard_and_megas_v2.json")
 catalog=[]
 for item in d.get("results",[]):
  name=item["name"]
  try:
   number=int(item["url"].rstrip("/").split("/")[-1])
  except (TypeError,ValueError,IndexError):
   number=0
  if 1<=number<=1025 or "-mega" in name:
   catalog.append(name)
 return catalog
def type_names(type_name):
 d=get_json(f"{API}/type/{type_name}",f"type_{type_name}.json")
 return {x["pokemon"]["name"] for x in d["pokemon"]}
def pokemon(identifier,language):
 key=str(identifier);d=get_json(f"{API}/pokemon/{key}",f"pokemon_{key}.json")
 sp=get_json(d["species"]["url"],f"species_{d['species']['name']}.json")
 base=next((x["name"] for x in sp.get("names",[]) if x["language"]["name"]==language),d["species"]["name"].title())
 api=d["name"]; suffix=""
 labels={"-alola":(" d’Alola"," Alolan"),"-galar":(" de Galar"," Galarian"),"-hisui":(" de Hisui"," Hisuian"),"-paldea":(" de Paldea"," Paldean")}
 if "-mega" in api:
  # Supports classic Mega, X/Y variants and the new Z variants from Legends Z-A.
  mega_tail=api.split("-mega",1)[1].strip("-")
  if mega_tail:
   suffix=" "+" ".join(part.upper() if len(part)==1 else part.title() for part in mega_tail.split("-"))
  name=("Méga-" if language=="fr" else "Mega ")+base+suffix
 else:
  name=base
  for tag,(fr,en) in labels.items():
   if tag in api:name=base+(fr if language=="fr" else en);break
 spr=d.get("sprites",{});art=spr.get("other",{}).get("official-artwork",{}).get("front_default") or spr.get("front_default")
 return {"name":name,"api_name":api,"stats":{x["stat"]["name"]:x["base_stat"] for x in d["stats"]},"types":[x["type"]["name"] for x in d["types"]],"sprite":art}
