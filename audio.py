import requests as req
from bs4 import BeautifulSoup
import datetime

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
        audio   = html.find("div", { "class": "player-init" })["data-file"]
        artwork = html.find("img")["src"]
        
        datas.append({ "artist": artist, "title": title, "audio": audio, "artwork": artwork })
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

  style = '''@import url('https://fonts.googleapis.com/css?family=Dosis');
body {
  font-family: 'Dosis', sans-serif;
  background-color: #bbb;
  margin: 0;
}
header {
  background-color: #fff;
  width: 100%;
  text-align: center;
  box-shadow: 0px 4px 20px;
  z-index: 999;
  position: fixed;
  top: 0;
}
header p {
  margin: 0;
  font-size: 5rem;
}
.line {
  position: fixed;
  top: 97px;
  border: 2px solid red;
  z-index: 1000;
}
.container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  background-color: #fff;
  margin: 0 auto;
  width: 80%;
  padding-top: 130px;
}
img { width: 200px }
.item {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 10px;
  margin-bottom: 20px;
  box-shadow: 0px 0px 20px;
  border-radius: 5px;
}
.title {
  margin: 5px 0;
  background-color: aliceblue;
}'''

  script = '''window.onscroll = () => {
  bodyHeight = document.body.offsetHeight;
  innerHeight = window.innerHeight;
  scroll = document.body.scrollTop;

  size = bodyHeight === innerHeight ? 100 : scroll / (bodyHeight - innerHeight) * 100;
  document.querySelector(".line").style.width = `${size}%`
}'''
  
  if download:
    fileName = str(date)
  else:
    fileName = str(date) + "_server"

  with open("{}.html".format(fileName), "w", encoding="utf8") as file:
    file.write("<head>")
    file.write("<style>{}</style>".format(style))
    file.write("</head>")
    
    file.write("<body>")
    
    file.write("<header><p>{}</p></header>".format(date))
    file.write("<div class=\"line\"></div>")
    file.write("<div class=\"container\">")
    
    for data in datas:
      file.write("<div class=\"item\">")
      
      artwork = "<img src=\"{}\">".format(data["artwork"])
      title   = "<div class=\"title\">{} - {}</div>".format(data["artist"], data["title"])
      if download:
        audio = "<audio controls src=\"{}\"></audio>".format(data["audio"])
      else:
        audio = "<audio controls controlsList=\"nodownload\" src=\"{}\"></audio>".format(data["audio"])

      file.write(artwork)
      file.write(title)
      file.write(audio)
      
      file.write("</div>")
      
    file.write("</div>")

    file.write("<script>{}</script>".format(script))
      
    file.write("</body>")

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
                  print(">> WRONG INPUT\n")
              except:
                print(">> WRONG INPUT\n")
            # download
            while True:
              download = input("download(0: false, 1: true): ")
              try:
                if download == '0' or download == '1':
                  download = int(download)
                  break
                else:
                  print(">> WRONG INPUT\n")
              except:
                print(">> WRONG INPUT\n")
            print()

            datas = fetchedPage(src, home, page, customHeaders)

            fileWrite(datas, date)
            break
          else:
            print(">> WRONG INPUT\n")
            
        except:
          print(">> WRONG INPUT\n")
          continue

  except:
    print(">> WRONG INPUT\n")
    continue
    
