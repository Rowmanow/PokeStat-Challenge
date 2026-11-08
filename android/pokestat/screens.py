import random,threading,itertools
from kivy.app import App
from kivy.clock import Clock
from kivy.metrics import dp
from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.image import AsyncImage, Image
from kivy.uix.popup import Popup
from kivy.uix.checkbox import CheckBox
from kivy.uix.scrollview import ScrollView
from .data import TEXT,STAT_LABELS,STAT_ORDER,COLORS,TYPE_KEYS,GEN_RANGES
from .api import pokemon,standard_catalog,type_names

def lang():return App.get_running_app().language
def tr(k,**kw):return TEXT[lang()][k].format(**kw)
def sl(k):return STAT_LABELS[lang()][k]
def btn(text,cb,color=None,h=48):
 b=Button(text=text,size_hint_y=None,height=dp(h),background_normal="",background_color=color or COLORS["blue"],bold=True);b.bind(on_release=cb);return b
class ReplaceInput(TextInput):
 def __init__(self,**kw):super().__init__(**kw);self.arm=False;self.use_handles=False;self.bind(focus=self._focus)
 def _focus(self,_w,f):self.arm=bool(f and self.text)
 def insert_text(self,sub,from_undo=False):
  if self.arm and sub:self.text="";self.cursor=(0,0);self.arm=False
  return super().insert_text(sub,from_undo)
def num(text=""):return ReplaceInput(text=text,input_filter="int",multiline=False,halign="center",padding=[dp(4),dp(13),dp(4),0],font_size="20sp")

MEGA=["venusaur-mega","charizard-mega-x","charizard-mega-y","blastoise-mega","beedrill-mega","pidgeot-mega","alakazam-mega","slowbro-mega","gengar-mega","kangaskhan-mega","pinsir-mega","gyarados-mega","aerodactyl-mega","mewtwo-mega-x","mewtwo-mega-y","ampharos-mega","steelix-mega","scizor-mega","heracross-mega","houndoom-mega","tyranitar-mega","sceptile-mega","blaziken-mega","swampert-mega","gardevoir-mega","sableye-mega","mawile-mega","aggron-mega","medicham-mega","manectric-mega","sharpedo-mega","camerupt-mega","altaria-mega","banette-mega","absol-mega","glalie-mega","salamence-mega","metagross-mega","latias-mega","latios-mega","lopunny-mega","garchomp-mega","lucario-mega","abomasnow-mega","gallade-mega","audino-mega","diancie-mega"]
REGIONAL={
 "alola":["rattata-alola","raticate-alola","raichu-alola","sandshrew-alola","sandslash-alola","vulpix-alola","ninetales-alola","diglett-alola","dugtrio-alola","meowth-alola","persian-alola","geodude-alola","graveler-alola","golem-alola","grimer-alola","muk-alola","exeggutor-alola","marowak-alola"],
 "galar":["meowth-galar","ponyta-galar","rapidash-galar","slowpoke-galar","slowbro-galar","farfetchd-galar","weezing-galar","mr-mime-galar","articuno-galar","zapdos-galar","moltres-galar","slowking-galar","corsola-galar","zigzagoon-galar","linoone-galar","darumaka-galar","darmanitan-galar-standard","yamask-galar","stunfisk-galar"],
 "hisui":["growlithe-hisui","arcanine-hisui","voltorb-hisui","electrode-hisui","typhlosion-hisui","qwilfish-hisui","sneasel-hisui","samurott-hisui","lilligant-hisui","zorua-hisui","zoroark-hisui","braviary-hisui","sliggoo-hisui","goodra-hisui","avalugg-hisui","decidueye-hisui"],
 "paldea":["tauros-paldea-combat-breed","tauros-paldea-blaze-breed","tauros-paldea-aqua-breed","wooper-paldea"]}
FORM_GEN={"alola":7,"galar":8,"hisui":8,"paldea":9}
# Mega follows the base species generation, as requested.
def base_gen(name):
 base=name.split("-mega")[0]
 cat=standard_catalog()
 try:i=cat.index(base)+1
 except:return 1
 for g,(a,b) in GEN_RANGES.items():
  if a<=i<=b:return g
 return 9

def settings(obj):
 if not hasattr(obj,"gens"):
  obj.gens=set(range(1,10));obj.types=set(TYPE_KEYS);obj.forms={"standard","mega","regional"}
def candidates(obj):
 cat=standard_catalog();out=[]
 if "standard" in obj.forms:
  for i,n in enumerate(cat,1):
   if any(a<=i<=b and g in obj.gens for g,(a,b) in GEN_RANGES.items()):out.append(n)
 if "mega" in obj.forms:
  # Dynamic Mega pool: classic forms plus new X, Y and Z forms from PokéAPI.
  out += [n for n in cat if "-mega" in n and base_gen(n) in obj.gens]
 if "regional" in obj.forms:
  for form,names in REGIONAL.items():
   if FORM_GEN[form] in obj.gens:out+=names
 if obj.types!=set(TYPE_KEYS):
  allowed=set()
  for t in obj.types:allowed|=type_names(t)
  out=[n for n in out if n in allowed]
 return list(dict.fromkeys(out))

def check_popup(title,items,selected,on_done):
 root=BoxLayout(orientation="vertical",spacing=dp(5),padding=dp(8));scroll=ScrollView();grid=GridLayout(cols=1,size_hint_y=None,spacing=dp(2));grid.bind(minimum_height=grid.setter("height"));boxes={}
 for key,label in items:
  row=BoxLayout(size_hint_y=None,height=dp(42));cb=CheckBox(active=key in selected,size_hint_x=.2);boxes[key]=cb;row.add_widget(cb);row.add_widget(Label(text=label,halign="left"));grid.add_widget(row)
 scroll.add_widget(grid);root.add_widget(scroll);actions=BoxLayout(size_hint_y=None,height=dp(48),spacing=dp(5));pop=Popup(title=title,content=root,size_hint=(.92,.88))
 def allv(v):
  for c in boxes.values():c.active=v
 def valid(*_):on_done({k for k,c in boxes.items() if c.active} or set(selected));pop.dismiss()
 actions.add_widget(btn("TOUT",lambda *_:allv(True)));actions.add_widget(btn("AUCUN",lambda *_:allv(False),COLORS["red"]));actions.add_widget(btn("VALIDER",valid,COLORS["green"]));root.add_widget(actions);pop.open()

def filter_text(kind, values):
 if kind == "types":
  return ("TYPES : TOUS" if lang()=="fr" else "TYPES : ALL") if len(values) == len(TYPE_KEYS) else f"TYPES : {len(values)}"
 if kind == "gens":
  return (("GÉN. : TOUT" if lang()=="fr" else "GEN. : ALL") if len(values) == 9 else (("GÉN. : " if lang()=="fr" else "GEN. : ") + ",".join(str(x) for x in sorted(values))))
 return ("FORMES : TOUT" if lang()=="fr" else "FORMS : ALL") if len(values) == 3 else (("FORMES" if lang()=="fr" else "FORMS") + f" : {len(values)}")

def refresh_filter_buttons(screen):
 if hasattr(screen, "type_btn"):
  screen.type_btn.text=filter_text("types",screen.types)
  screen.gen_btn.text=filter_text("gens",screen.gens)
  screen.form_btn.text=filter_text("forms",screen.forms)

def filter_row(screen):
 row=BoxLayout(size_hint_y=None,height=dp(40),spacing=dp(4))
 screen.type_btn=btn("TYPES",screen.pick_types,COLORS["blue"],40)
 screen.gen_btn=btn("GÉN.",screen.pick_gens,COLORS["blue"],40)
 screen.form_btn=btn("FORMES",screen.pick_forms,COLORS["blue"],40)
 for button in (screen.type_btn,screen.gen_btn,screen.form_btn): button.font_size="13sp"
 row.add_widget(screen.type_btn);row.add_widget(screen.gen_btn);row.add_widget(screen.form_btn)
 Clock.schedule_once(lambda _dt:refresh_filter_buttons(screen),0)
 return row

class FilterMixin:
 def _save_filter(self,attr,value):
  setattr(self,attr,value);refresh_filter_buttons(self)
 def pick_types(self,*_):
  labels={"fire":"Feu","water":"Eau","grass":"Plante","electric":"Électrik","ice":"Glace","fighting":"Combat","poison":"Poison","ground":"Sol","flying":"Vol","psychic":"Psy","bug":"Insecte","rock":"Roche","ghost":"Spectre","dragon":"Dragon","dark":"Ténèbres","steel":"Acier","fairy":"Fée","normal":"Normal"}
  check_popup("Types",[(x,labels.get(x,x.title())) for x in TYPE_KEYS],self.types,lambda v:self._save_filter("types",v))
 def pick_gens(self,*_):
  check_popup("Générations" if lang()=="fr" else "Generations",[(g,(f"Génération {g}" if lang()=="fr" else f"Generation {g}")) for g in range(1,10)],self.gens,lambda v:self._save_filter("gens",v))
 def pick_forms(self,*_):
  items=[
   ("standard","Standards" if lang()=="fr" else "Standard"),
   ("mega","Méga" if lang()=="fr" else "Mega"),
   ("regional","Régionales" if lang()=="fr" else "Regional"),
  ]
  check_popup("Formes" if lang()=="fr" else "Forms",items,self.forms,lambda v:self._save_filter("forms",v))

class HomeScreen(Screen):
 def on_pre_enter(self,*_):self.draw()
 def refresh_texts(self):self.draw()

 def mode_card(self,title,description,action,color):
  card=BoxLayout(orientation="horizontal",size_hint_y=None,height=dp(116),spacing=dp(0))
  info=Button(text=f"[b]{title}[/b]\n[size=14sp]{description}[/size]",markup=True,halign="left",valign="middle",padding=[dp(18),dp(10)],background_normal="",background_color=color,size_hint_x=.72)
  info.bind(size=lambda w,v:setattr(w,"text_size",(v[0]-dp(36),None)))
  info.bind(on_release=action)
  play=Button(text=("JOUER  >" if lang()=="fr" else "PLAY  >"),bold=True,font_size="15sp",background_normal="",background_color=tuple(max(0,c*.78) for c in color[:3])+(1,),size_hint_x=.28)
  play.bind(on_release=action)
  card.add_widget(info);card.add_widget(play)
  return card

 def draw(self):
  self.clear_widgets()
  root=BoxLayout(orientation="vertical",padding=[dp(24),dp(22),dp(24),dp(16)],spacing=dp(12))
  logo=Image(source="assets/pokestat_home_logo.png",allow_stretch=True,keep_ratio=True,size_hint_y=.28)
  root.add_widget(logo)
  subtitle="Deux jeux, une seule mission : connaître les stats" if lang()=="fr" else "Two games, one mission: master the stats"
  root.add_widget(Label(text=subtitle,font_size="14sp",color=(.72,.76,.84,1),halign="center",size_hint_y=.07))

  language=BoxLayout(size_hint_y=None,height=dp(44),spacing=dp(6))
  fr_color=COLORS["blue"] if lang()=="fr" else (.14,.18,.27,1)
  en_color=COLORS["blue"] if lang()=="en" else (.14,.18,.27,1)
  language.add_widget(btn("FRANÇAIS",lambda *_:App.get_running_app().set_language("fr"),fr_color,44))
  language.add_widget(btn("ENGLISH",lambda *_:App.get_running_app().set_language("en"),en_color,44))
  root.add_widget(language)

  prompt="CHOISIS TON DÉFI" if lang()=="fr" else "CHOOSE YOUR CHALLENGE"
  root.add_widget(Label(text=prompt,font_size="15sp",bold=True,color=(.78,.82,.9,1),size_hint_y=.08))

  draft_title="DRAFT DE STATS" if lang()=="fr" else "STAT DRAFT"
  draft_desc="Compose ton équipe et bats l’objectif" if lang()=="fr" else "Build your team and beat the target"
  root.add_widget(self.mode_card(draft_title,draft_desc,lambda *_:setattr(self.manager,"current","draft"),COLORS["red"]))

  guess_title="STAT GUESSER"
  guess_desc="Retrouve les 6 statistiques du Pokémon" if lang()=="fr" else "Guess all 6 stats of the Pokémon"
  root.add_widget(self.mode_card(guess_title,guess_desc,lambda *_:setattr(self.manager,"current","guesser"),COLORS["blue"]))

  root.add_widget(Label(text="VERSION 1.0.3",font_size="13sp",bold=True,color=(.45,.55,.72,1),size_hint_y=.07))
  self.add_widget(root)

class GuesserScreen(FilterMixin,Screen):
 max_attempts=8
 def on_pre_enter(self,*_):settings(self);self.draw()
 def on_pre_leave(self,*_):
  for f in getattr(self,"inputs",{}).values():f.focus=False
 def refresh_texts(self):
  if self.manager and self.manager.current==self.name:self.draw()
 def draw(self):
  self.clear_widgets();self.inputs={};self.target={};self.solved=set();self.bounds={k:[None,None] for k in STAT_ORDER};r=BoxLayout(orientation="vertical",padding=dp(10),spacing=dp(4));top=BoxLayout(size_hint_y=None,height=dp(42));top.add_widget(btn("< "+tr("home"),lambda *_:setattr(self.manager,"current","home"),h=42));top.add_widget(Label(text="GUESSER",bold=True));r.add_widget(top);r.add_widget(filter_row(self));c=BoxLayout(size_hint_y=None,height=dp(45),spacing=dp(5));c.add_widget(Label(text=tr("attempts"),size_hint_x=.7));self.attempt_input=num(str(self.max_attempts));c.add_widget(self.attempt_input);c.add_widget(btn("LANCER" if lang()=="fr" else "START",self.start,COLORS["green"],45));r.add_widget(c);self.pname=Label(text=tr("ready"),font_size="21sp",bold=True,size_hint_y=None,height=dp(38));r.add_widget(self.pname);self.art=AsyncImage(size_hint_y=.24);r.add_widget(self.art);self.atlab=Label(text="",size_hint_y=None,height=dp(26));r.add_widget(self.atlab);g=GridLayout(cols=3,spacing=dp(3),size_hint_y=.5);self.bl={};g.add_widget(Label(text="STAT",bold=True));g.add_widget(Label(text="MIN / MAX",bold=True));g.add_widget(Label(text="ESSAI" if lang()=="fr" else "GUESS",bold=True))
  for k in STAT_ORDER:g.add_widget(Label(text=sl(k)));self.bl[k]=Label(text="? / ?");g.add_widget(self.bl[k]);self.inputs[k]=num();g.add_widget(self.inputs[k])
  self.bind_ime_navigation()
  r.add_widget(g);self.status=Label(text=tr("ready"),size_hint_y=None,height=dp(32));r.add_widget(self.status)
  r.add_widget(btn(tr("submit"),self.check,COLORS["gold"],50));self.add_widget(r)
 def focus_next_field(self,current_key):
  available=[k for k in STAT_ORDER if k not in self.solved and not self.inputs[k].disabled]
  if not available:return
  try:index=available.index(current_key);target=available[index+1]
  except (ValueError,IndexError):
   self.inputs[current_key].focus=False
   return
  self.inputs[current_key].focus=False
  self.inputs[target].focus=True

 def bind_ime_navigation(self):
  for key,field in self.inputs.items():
   field.write_tab=False
   field.bind(on_text_validate=lambda widget,k=key:self.focus_next_field(k))

 def start(self,*_):
  try:self.max_attempts=max(1,min(20,int(self.attempt_input.text or 8)))
  except:self.max_attempts=8
  self.attempt=1;self.target={};self.solved=set();self.bounds={k:[None,None] for k in STAT_ORDER};self.pname.text=tr("loading");self.status.text=tr("loading");self.art.source=""
  for k in STAT_ORDER:self.inputs[k].text="";self.inputs[k].disabled=False;self.inputs[k].background_color=(1,1,1,1);self.bl[k].text="? / ?"
  threading.Thread(target=self._load,daemon=True).start()
 def _load(self):
  try:
   pool=candidates(self)
   if not pool:raise ValueError("Aucun Pokémon pour ces filtres")
   d=pokemon(random.choice(pool),lang());Clock.schedule_once(lambda _dt,x=d:self._apply(x))
  except Exception as e:Clock.schedule_once(lambda _dt,msg=str(e):self._error(msg))
 def _apply(self,d):self.target=d["stats"];self.pname.text=d["name"];self.art.source=d["sprite"] or "";self.atlab.text=tr("attempt",n=1,max=self.max_attempts);self.status.text="BST : "+str(sum(self.target.values()))
 def _error(self,m):self.status.text="Erreur / Error: "+m;self.pname.text=tr("ready")
 def check(self,*_):
  if not self.target:return
  vals={}
  for k in STAT_ORDER:
   if k in self.solved:continue
   try:v=int(self.inputs[k].text)
   except:self.status.text="Valeur invalide";return
   lo,hi=self.bounds[k]
   if not 1<=v<=255 or (lo is not None and v<=lo) or (hi is not None and v>=hi):self.status.text="Valeur hors des bornes";return
   vals[k]=v
  for k,v in vals.items():
   t=self.target[k]
   if v==t:self.solved.add(k);self.inputs[k].disabled=True;self.inputs[k].background_color=(.1,.7,.3,1);self.bl[k].text="OK"
   elif v<t:self.bounds[k][0]=max(v,self.bounds[k][0] or v)
   else:self.bounds[k][1]=min(v,self.bounds[k][1] or v)
   if k not in self.solved:self.bl[k].text=f"{self.bounds[k][0] or '?'} / {self.bounds[k][1] or '?'}"
  if len(self.solved)==6:self.status.text=tr("win");return
  if self.attempt>=self.max_attempts:self.status.text=tr("lose")+" | "+" / ".join(str(self.target[k]) for k in STAT_ORDER);return
  self.attempt+=1;self.atlab.text=tr("attempt",n=self.attempt,max=self.max_attempts)

class DraftScreen(FilterMixin,Screen):
 mode="above"
 def on_pre_enter(self,*_):settings(self);self.draw()
 def refresh_texts(self):
  if self.manager and self.manager.current==self.name:self.draw()
 def draw(self):
  self.clear_widgets();self.current=None;self.chosen={};self.used=set();self.encountered=[];r=BoxLayout(orientation="vertical",padding=dp(10),spacing=dp(4));top=BoxLayout(size_hint_y=None,height=dp(42));top.add_widget(btn("< "+tr("home"),lambda *_:setattr(self.manager,"current","home"),h=42));top.add_widget(Label(text="DRAFT",bold=True));r.add_widget(top);r.add_widget(filter_row(self));c=BoxLayout(size_hint_y=None,height=dp(45),spacing=dp(4));self.modebtn=btn(self.mode_text(),self.toggle,COLORS["blue"],45);c.add_widget(self.modebtn);self.target=num("600");c.add_widget(self.target);c.add_widget(btn("LANCER" if lang()=="fr" else "START",self.start,COLORS["green"],45));r.add_widget(c);self.total=Label(text="TOTAL : 0",bold=True,size_hint_y=None,height=dp(30));r.add_widget(self.total);self.pname=Label(text=tr("ready"),font_size="21sp",bold=True,size_hint_y=None,height=dp(38));r.add_widget(self.pname);self.art=AsyncImage(size_hint_y=.28);r.add_widget(self.art);self.info=Label(text="Choisis une statistique" if lang()=="fr" else "Choose a stat",size_hint_y=None,height=dp(28));r.add_widget(self.info);g=GridLayout(cols=2,spacing=dp(3),size_hint_y=.5);self.vl={};self.bs={}
  for k in STAT_ORDER:self.vl[k]=Label(text=f"{sl(k)} : —");g.add_widget(self.vl[k]);self.bs[k]=btn("CHOISIR" if lang()=="fr" else "CHOOSE",lambda *_a,key=k:self.choose(key),COLORS["blue"],40);self.bs[k].disabled=True;g.add_widget(self.bs[k])
  r.add_widget(g);self.progress=Label(text="0 / 6",size_hint_y=None,height=dp(28));r.add_widget(self.progress);self.add_widget(r)
 def mode_text(self):
  if self.mode=="closest":return tr("closest")
  if lang()=="fr":return "AU-DESSUS" if self.mode=="above" else "EN DESSOUS"
  return "ABOVE" if self.mode=="above" else "BELOW"
 def toggle(self,*_):
  order=("above","below","closest")
  self.mode=order[(order.index(self.mode)+1)%len(order)]
  self.modebtn.text=self.mode_text()
 def start(self,*_):
  try:self.goal=max(1,int(self.target.text or 600))
  except:self.goal=600
  self.chosen={};self.used=set();self.encountered=[];self.total.text="TOTAL : 0";self.progress.text="0 / 6";self.next()
 def next(self):
  self.current=None;self.pname.text=tr("loading");self.art.source=""
  for k in STAT_ORDER:self.vl[k].text=f"{sl(k)} : {self.chosen[k]['value'] if k in self.chosen else '—'}";self.bs[k].disabled=True
  threading.Thread(target=self._load,daemon=True).start()
 def _load(self):
  try:
   pool=[x for x in candidates(self) if x not in self.used]
   if not pool:raise ValueError("Aucun Pokémon pour ces filtres")
   ident=random.choice(pool);d=pokemon(ident,lang());d["ident"]=ident;Clock.schedule_once(lambda _dt,x=d:self._apply(x))
  except Exception as e:Clock.schedule_once(lambda _dt,msg=str(e):self._error(msg))
 def _apply(self,d):
  self.current=d;self.used.add(d["ident"]);self.pname.text=d["name"];self.art.source=d["sprite"] or ""
  for k in STAT_ORDER:
   if k not in self.chosen:self.vl[k].text=f"{sl(k)} : ?";self.bs[k].disabled=False
 def _error(self,m):self.info.text="Erreur / Error: "+m
 def choose(self,k):
  if not self.current or k in self.chosen:return
  entry={"value":self.current["stats"][k],"name":self.current["name"],"stat":k,"stats":dict(self.current["stats"]),"sprite":self.current.get("sprite")}
  self.chosen[k]=entry;self.encountered.append(entry)
  total=sum(x["value"] for x in self.chosen.values());self.total.text=f"TOTAL : {total}";self.progress.text=f"{len(self.chosen)} / 6";self.vl[k].text=f"{sl(k)} : {entry['value']}"
  if len(self.chosen)==6:
   if self.mode=="closest":
    gap=abs(total-self.goal);win=gap<=20;self.info.text=tr("closest_win" if win else "closest_lose",gap=gap)
   else:
    win=total>=self.goal if self.mode=="above" else total<=self.goal;self.info.text=(("VICTOIRE !" if win else "DÉFAITE") if lang()=="fr" else ("VICTORY!" if win else "DEFEAT"))
   for b in self.bs.values():b.disabled=True
   Clock.schedule_once(lambda _dt:self.show_recap(),.35)
  else:self.next()

 def show_recap(self):
  players=list(self.encountered);best_perm=None;best_total=None
  for perm in itertools.permutations(STAT_ORDER):
   score=sum(players[i]["stats"][perm[i]] for i in range(6))
   if best_total is None or (self.mode=="above" and score>best_total) or (self.mode=="below" and score<best_total) or (self.mode=="closest" and abs(score-self.goal)<abs(best_total-self.goal)):best_total=score;best_perm=perm
  mine=sum(x["value"] for x in players)
  root=BoxLayout(orientation="vertical",padding=dp(10),spacing=dp(7))
  head=GridLayout(cols=2,size_hint_y=None,height=dp(76),spacing=dp(8))
  left=("MON ÉQUIPE" if lang()=="fr" else "MY TEAM")+f"\nTOTAL : {mine}"
  if self.mode=="closest":right=tr("closest_possible")+f"\nTOTAL : {best_total} | ÉCART : {abs(best_total-self.goal)}" if lang()=="fr" else tr("closest_possible")+f"\nTOTAL: {best_total} | GAP: {abs(best_total-self.goal)}"
  else:right=(("MEILLEUR POSSIBLE" if self.mode=="above" else "MINIMUM POSSIBLE") if lang()=="fr" else ("BEST POSSIBLE" if self.mode=="above" else "LOWEST POSSIBLE"))+f"\nTOTAL : {best_total}"
  head.add_widget(Label(text=left,bold=True,font_size="16sp",halign="center"));head.add_widget(Label(text=right,bold=True,font_size="16sp",halign="center"));root.add_widget(head)
  scroll=ScrollView(do_scroll_x=False);grid=GridLayout(cols=1,size_hint_y=None,spacing=dp(8),padding=[0,dp(4)]);grid.bind(minimum_height=grid.setter("height"))
  for i,item in enumerate(players):
   optimal=best_perm[i];same=item["stat"]==optimal
   card=BoxLayout(orientation="vertical",size_hint_y=None,height=dp(132),padding=[dp(10),dp(6)],spacing=dp(2))
   title=Label(text=item["name"],bold=True,font_size="17sp",size_hint_y=None,height=dp(30));card.add_widget(title)
   mine_label=("Mon choix" if lang()=="fr" else "My choice")+f" : {sl(item['stat'])} ({item['value']})"
   combo_label=("Combo optimal" if lang()=="fr" else "Optimal combo")+f" : {sl(optimal)} ({item['stats'][optimal]})"
   verdict=(("CHOIX IDENTIQUE" if same else "RÉPARTITION DIFFÉRENTE") if lang()=="fr" else ("SAME CHOICE" if same else "DIFFERENT ASSIGNMENT"))
   line1=Label(text=mine_label,font_size="14sp",halign="left",valign="middle",size_hint_y=None,height=dp(27));line1.bind(size=lambda w,v:setattr(w,"text_size",(v[0],None)));card.add_widget(line1)
   line2=Label(text=combo_label,font_size="14sp",halign="left",valign="middle",size_hint_y=None,height=dp(34));line2.bind(size=lambda w,v:setattr(w,"text_size",(v[0],None)));card.add_widget(line2)
   line3=Label(text=("✓ " if same else "• ")+verdict,font_size="13sp",bold=True,halign="left",size_hint_y=None,height=dp(25));line3.bind(size=lambda w,v:setattr(w,"text_size",(v[0],None)));card.add_widget(line3);grid.add_widget(card)
  scroll.add_widget(grid);root.add_widget(scroll)
  popup=Popup(title="RÉCAPITULATIF DU DRAFT" if lang()=="fr" else "DRAFT SUMMARY",content=root,size_hint=(.96,.94))
  root.add_widget(btn("FERMER" if lang()=="fr" else "CLOSE",lambda *_:popup.dismiss(),COLORS["blue"],48));popup.open()

