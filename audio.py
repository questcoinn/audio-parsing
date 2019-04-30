import requests as req
from bs4 import BeautifulSoup
import json

from node import *

def printFirstPage(src):
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
    print(">> " + line)
  print()

def fetchedPage(src, home, page, customHeaders):
  datas = []
  firstPage = True

  while True:        
    if not firstPage:
      res = req.get(home + "?page=" + str(page), headers=customHeaders)

      soup = BeautifulSoup(res.content, "html.parser")
      src = soup.find("table")
      print(">> connected(page {})..".format(page))

    print(">> fetching files..")
    while True:
      src = src.find_next("a")
      if (("rel" in src) and (src["rel"] == "prev")) or (src["href"][33] == '?'):
        break
      
      linkDate = ''.join(src.find("time")["datetime"].replace('T', '-').split('-')[:3])
      linkDate = int(linkDate)
      
      if linkDate < date:
        if firstPage and src.find("span", { "class": "pinned" }):
          continue
        break
      elif linkDate > date:
        continue
      elif linkDate == date:
        link = src["href"]
        resEach = req.get(link, headers=customHeaders)

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
        print("..[ {} - {} ] done..".format(artist, title))

    if linkDate < date:
      break
    page += 1
    firstPage = False
    print(">> next page..\n")

  if len(datas) == 0:
    print(">> no files uploaded yet")
    return []
  print("\n>> fetched {} files!".format(len(datas)))
  
  return datas

def fileWrite(datas, date):
  datas.reverse()
  
  html = ElementNode("html")
  head = html.createChild("head")
  meta = head.createChild("meta")
  meta.createAttr("charset", "utf-8")
  
  style = head.createChild("link")
  style.createAttr("rel", "stylesheet")
  style.createAttr("type", "text/css")
  style.createAttr("href", "style.css")

  with open("keyframes.json", "r") as file:
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
    item.createAttr("id", data["title"])

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
      a.writeText("###")

  script = body.createChild("script")
  script.createAttr("src", "script.js")
  
  if download:
    fileName = str(date)
  else:
    fileName = str(date) + "_server"

  with open("{}.html".format(fileName), "w", encoding="utf8") as file:
    file.write("<!DOCTYPE html>\n")
    file.write(html.html())

  print(">> made web file!")
  print(">> check the {}.html file!\n".format(fileName))


search = { 1: "singles" }

while True:
  try:
    select = int(input("== where to go ==\n1. singles\n0. exit\n: "))

    if select == 0:
      break
    else:
      home = "http://www.audioswish.org/" + search[select]
      page = 1
      customHeaders = { "User-agent": "Mozilla/5.0" }
      
      res = req.get(home + "?page=" + str(page), headers=customHeaders)
      soup = BeautifulSoup(res.content, "html.parser")
      src = soup.find("table")
      
      printFirstPage(src)
      
      while True:
        try:
          control = int(input("== what to do ==\n1. make file\n0. exit\n: "))
          if control == 0:
            break
          elif control == 1:
            print("== choose date ==")
            # date
            while True:
              date = input("date(ex - 20190101): ")
              try:
                if len(date) == 8:
                  date = int(date)
                  break
                else:
                  print(">> WRONG INPUT(1)\n")
              except Exception as e:
                print(">> WRONG INPUT(2)\n{}\n".format(e))
            # download
            while True:
              download = input("download(0: false, 1: true): ")
              try:
                if download == '0' or download == '1':
                  download = int(download)
                  break
                else:
                  print(">> WRONG INPUT(3)\n")
              except Exception as e:
                print(">> WRONG INPUT(4)\n{}\n".format(e))
            print()

            datas = fetchedPage(src, home, page, customHeaders)

            fileWrite(datas, date)
            break
          else:
            print(">> WRONG INPUT(5)\n")
            
        except Exception as e:
          print(">> WRONG INPUT(6)\n{}\n".format(e))
          continue

  except Exception as e:
    print(">> WRONG INPUT(7)\n{}\n".format(e))
    continue
    
