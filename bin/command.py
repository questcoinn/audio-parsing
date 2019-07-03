from sys import path, exit as sys_exit
from datetime import datetime
import requests as req
import json

from bs4 import BeautifulSoup
from pytz import timezone

path.append("absolute path of the bin directory")
from node import ElementNode

def connect(home, page, customHeader={ "User-agent": "Mozilla/5.0" }):
  prompt = "connectting page " + page + "..."
  print("{:<32}".format(prompt), end="")
  res = req.get(home + "?page=" + page, headers=customHeader)
  print("[ok]")

  print("{:<32}".format("finding table..."), end="")
  soup = BeautifulSoup(res.content, "html.parser")
  src = soup.find("table")
  print("[ok]")

  return src

def getData(home, date, customHeader={ "User-agent": "Mozilla/5.0" }):
  datas = []
  page = 1

  while True:
    src = connect(home, str(page))

    while True:
      src = src.find_next("a")
      
      if (src.has_attr("rel") and (src["rel"] == ["prev"])) or (src["href"][33] == '?'):
        break
      
      linkDate = ''.join(src.find("time")["datetime"].replace('T', '-').split('-')[:3])
      linkDate = int(linkDate)
      
      if linkDate < date:
        if page == 1 and src.find("span", { "class": "pinned" }):
          continue
        break
      elif linkDate > date:
        continue
      elif linkDate == date:
        link = src["href"]
        resEach = req.get(link, headers=customHeader)

        html = BeautifulSoup(resEach.content, "html.parser")

        artist  = html.find("strong", { "class": "artist" }).text
        title   = html.find("span", { "class": "title" }).text
        try:
          audio = html.find("div", { "class": "player-init" })["data-file"]
          isRight = True
        except:
          audio = html.find("a", { "class": "download" })["href"]
          isRight = False
        artwork = html.find("img")["src"]
        
        datas.append({ "artist": artist, "title": title, "audio": audio, "artwork": artwork, "isRight": isRight })
        print("[ {} - {} ] DONE".format(artist, title))

    if linkDate < date:
      break
    page += 1

  if len(datas) == 0:
    print("no files uploaded yet")
    return []
  print("got {} datas".format(len(datas)))
  
  return datas

def writeFile(datas, date, download=True):
  print("{:<32}".format("generating web file..."), end="")

  datas.reverse()
  
  html = ElementNode("html")
  head = html.createChild("head")
  meta = head.createChild("meta")
  meta.createAttr("charset", "utf-8")
  title = html.createChild("title")
  title.writeText(str(date))
  
  style = head.createChild("link")
  style.createAttr("rel", "stylesheet")
  style.createAttr("type", "text/css")
  style.createAttr("href", "../style/style.css")

  with open("style/keyframes.json", "r") as file:
    keyframesObj = json.loads(file.read())

  keyframes = head.createChild("style")
  keyframes.writeText(keyframesObj["rotate"] + '\n' + keyframesObj["turn-back"])
  
  body = html.createChild("body")

  header = body.createChild("header")
  headerP = header.createChild("p")
  headerP.writeText(str(date))
  line = body.createChild("div")
  line.createAttr("class", "line")

  container = body.createChild("div")
  container.createAttr("class", "container")

  for data in datas:
    item = container.createChild("div")
    item.createAttr("class", "item")
    item.createAttr("id", data["title"].replace(" ", ""))

    artwork = item.createChild("img")
    artwork.createAttr("src", data["artwork"])
    title = item.createChild("div")
    title.createAttr("class", "title")
    title.writeText("{} - {}".format(data["artist"], data["title"]))
    if data["isRight"]:
      loadBtn = item.createChild("input")
      loadBtn.createAttr("type", "button")
      loadBtn.createAttr("value", "Load")
      loadBtn.createAttr("class", "load")
      loadBtn.createAttr("src", data["audio"])
      if not download:
        loadBtn.createAttr("download", "0")
    else:
      a = item.createChild("a")
      if download:
        a.createAttr("href", data["audio"])
        a.createAttr("target", "_blank")
      a.writeText("Something weird happened...")

  script = body.createChild("script")
  script.createAttr("src", "../script/script.js")
  
  if download:
    fileName = str(date)
  else:
    fileName = str(date) + "_nd"

  with open("pages/{}.html".format(fileName), "w", encoding="utf8") as file:
    file.write("<!DOCTYPE html>\n")
    file.write(html.html())

  print("[ok]")

###########
# command #
###########

def _help(*opt):
  if not opt:
    print("command list: help, exit, today, spread, get")
    print("to see details, just type: help [command]")
  else:
    print("still working with this..")
    print('''ex)
help or ?
exit or quit

today [-t Asia/Seoul]
spread -t singles -p 1
get -t singles -d [20190703 || today || yesterday] [--nodownload]''')

def today(opt={ 't': "Asia/Seoul" }):
  tz = timezone(opt['t'])
  print("{:<32}{}".format("UTC", str(datetime.utcnow())[:-7]))
  print("{:<32}{}".format(str(tz), str(datetime.now(tz))[:-13]))

def spread(opt):
  src = connect("http://www.audioswish.org/" + opt['t'], opt['p'])
  
  # 아래는 singles일때만임
  # lp 추가해야함
  table = []

  while True:
    src = src.find_next("a")
    if (("rel" in src) and (src["rel"] == "prev")) or (src["href"].find('?') > -1):
      break

    artist = src.find("span", { "class": "artist" }).text
    title  = src.find("span", { "class": "title" }).text
    time   = src.find("time")["datetime"].replace('T', ' ').split('+')[0]
    lit    = True if src.find("span", { "class": "pinned" }) else False
    
    table.append({ "artist": artist, "title": title, "time": time, "lit": lit })

  for tableData in table:
    line = tableData["time"] + " " + tableData["artist"] + " - " + tableData["title"]

    if tableData["lit"]:
      line += " [LIT]"

    print(line)

def get(opt):
  today = int(str(datetime.utcnow().date()).replace('-', ''))

  if opt['d'] == "today":
    date = today
  elif opt['d'] == "yesterday":
    date = today - 1
  else:
    date = int(opt['d'])

  download = True if "nodownload" not in opt else opt["nodownload"]

  datas = getData("http://www.audioswish.org/" + opt['t'], date)
  writeFile(datas, date, download)

###################
# switch commands #
###################

def match(name):
  return name in { "help", "?", "exit", "quit", "today", "spread", "get" }

def _exec(string):
  if string == '':
    print(end="")
    return

  option = {}

  if string[:4] == "help":
    line = string.split()
  else:
    line = string.split(" -")

  name = line.pop(0)

  if not match(name):
    print("invalid command")
    return

  for _ in line:
    arr = _.split()
    length = len(arr)
    
    if length == 2:
      option[arr[0]] = arr[1]

    elif length == 1:
      option[arr[0].replace('-', '')] = True

    else:
      print("invalid option")
      return

  if name in { "exit", "quit" }:
    print("bye")
    sys_exit(0)
  
  try:
    if name in { "help", "?" }:
      if option:
        _help(option)
      else:
        _help()
    elif name == "today":
      if option:
        today(option)
      else:
        today()
    elif name == "spread":
      spread(option)
    elif name == "get":
      get(option)
    
    else:
      print("unexpected error")

  except:
    print("invalid syntax")