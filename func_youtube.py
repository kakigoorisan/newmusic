from distutils.log import debug
from multiprocessing.connection import answer_challenge
from operator import truediv
from turtle import clear, title
import argparse
import asyncio
import os
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from oauth2client.tools import argparser
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import _Response, Request
videde ={}
titl={}
ser = {}
sati = {}
playlist_video={}
titles = {}
samn = {}
#Tokenを取得
nn = os.path.dirname(os.path.abspath(__file__))
with open(f"{nn}/TOKEN.txt", "r",encoding="utf-8") as temp_file:
  temp_TOKEN_n = temp_file.readlines()
  temp_TOKEN = [line.strip() for line in temp_TOKEN_n]

  TOKEN_list = [line for line in temp_TOKEN if line.startswith("TOKEN =")]
  DEVELOPER_KEY_list = [line for line in temp_TOKEN if line.startswith("Youtube_API_KEY =")]
  
  TOKEN = str(TOKEN_list[0].lstrip("TOKEN"))
  TOKEN = TOKEN.lstrip(" =")

  DEVELOPER_KEY = str(DEVELOPER_KEY_list[0].lstrip("Youtube_API_KEY"))
  DEVELOPER_KEY = DEVELOPER_KEY.lstrip(" =")
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"


#googleのapiを使ってyoutubeの動画を検索する
async def youtube_search(options,guildid):
  global videde,titl,ser
  videde.setdefault(guildid,[])
  titl.setdefault(guildid,[])
  videde[guildid] = []
  titl[guildid] = []
  youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION,
    developerKey=DEVELOPER_KEY)

  search_response = youtube.search().list(
    q=options.q,
    part="id,snippet",
    maxResults=options.max_results
  ).execute()

  videos = []
  channels = [] #リストを作成
  playlists = []
  
  for search_result in search_response.get("items", []):
    if search_result["id"]["kind"] == "youtube#video":
      videde[guildid].append(search_result["id"]["videoId"])
      titl[guildid].append(search_result["snippet"]["title"])
    else:
      return

  print("Videos:\n", "\n".join(videos), "\n")
  print("Channels:\n", "\n".join(channels), "\n")
  print("Playlists:\n", "\n".join(playlists), "\n")
  print(search_result)
 
  
  #vcで流すためにvideoIDを取得
  print (videde[guildid])
  return (videde,titl,guildid)

#youtubeで検索するための設定。.scで来たワードを入れる
async def youtubeop(num,sss,guildid):
  global ser,sati
  sati[guildid] = sss
  # 検索ワード
  argparser = argparse.ArgumentParser()
  argparser.add_argument("--q")
  # 検索上限
  argparser.add_argument("--max-results", help="Max results", default=num)
  args = argparser.parse_args()
  args.q = sati[guildid]  
  try:
    ser[guildid] = await youtube_search(args,guildid)
    guildid = ser[guildid][2]
    print(ser[guildid][0])
    videde = ser[guildid][0]
    if len(videde) >= 2:
      print("len>=2")
      await asyncio.sleep(0.5)
    titl = ser[guildid][1]
    print (f"aaa {videde}")
    return (videde,titl,guildid)

  except HttpError as e:
    print("An HTTP error %d occurred:\n%s" % (e.resp.status, e.content))


#playlistが渡されたときの対応 .playlistで対応
async def youtube_list(url,guildid):
  global playlist_video
  playlist_video[guildid]=[]
  youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION,
    developerKey=DEVELOPER_KEY)
  playlist_setting = youtube.playlistItems().list(
    part="id",
    playlistId = url
  ).execute()
  temp = playlist_setting.get("pageInfo")
  print(temp["totalResults"])
  number_of = int(temp["totalResults"])

  playlist_response = youtube.playlistItems().list( 
    part="id,snippet,contentDetails",
    maxResults = number_of,
    playlistId = url
  ).execute()
  for play_list in playlist_response.get("items", []):
    if play_list["kind"] == "youtube#playlistItem":
      playlist_video[guildid].append(play_list["contentDetails"]["videoId"])
  print(playlist_video[guildid])
  return(playlist_video,guildid)

#IDからサムネURL,titleを取得
async def youtube_title(ids,guildid):
  global titles,samn
  titles[guildid] = ""
  samn[guildid] = ""
  youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION,
    developerKey=DEVELOPER_KEY)
  getting_id = youtube.videos().list(
    part ="id,snippet",
    id = ids
  ).execute()
  thum = getting_id.get("items",[])
  if thum[0]["kind"] == "youtube#video":
      titles[guildid] = thum[0]["snippet"]["title"]
      samn[guildid] = thum[0]["snippet"]["thumbnails"]["default"]["url"]
  print(titles)
  print(samn)
  return titles[guildid],samn[guildid]


