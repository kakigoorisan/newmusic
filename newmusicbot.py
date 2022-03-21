from asyncio.events import BaseDefaultEventLoopPolicy
from operator import truediv
from xmlrpc.client import Fault
import pafy
import argparse
from discord import FFmpegPCMAudio, PCMVolumeTransformer
import discord
from discord import player
from discord.errors import ClientException
import os
import asyncio
import random

#import slash_seat

from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from oauth2client.tools import argparser
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import _Response, Request

from collections import defaultdict, deque

DEVELOPER_KEY = "Your google api TOKEN here."
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"
TOKEN = "Your TOKEN here." #TOKENを入力

pafy.set_api_key("Your google TOKEN here")

FFMPEG_OPTIONS= {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5','options': '-vn'}

#様々な変数の初期値
intents = discord.Intents.all()
client = discord.Client(loop=None,heartbeat_timeout=180,intents=intents)
count_music = 1
elect = 0
titl = []
youtube_url = ""
voice = None
playerr = None
url = 0
qloo = 0
loop = 0
ended = 0
queue_dict = deque()
t = 0
videde = []
titl = [] 
sss = ""
meme = None
print_title = 0
queue_title = 0
loopskip = 0
queue = queue_dict
chanid = ""
vcid = ""



#キューの設定
def enqueue(voice_client, youtube_ur):


    queue.append(youtube_ur)
    print(queue)
    
    if not voice_client.is_playing():
        ytl(queue)
    else:
      return


#googleのapiを使ってyoutubeの動画を検索する
def youtube_search(options):
  global videde,titl
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
      videde.append(search_result["id"]["videoId"])
      titl.append(search_result["snippet"]["title"])
    else:
      return

  print("Videos:\n", "\n".join(videos), "\n")
  print("Channels:\n", "\n".join(channels), "\n")
  print("Playlists:\n", "\n".join(playlists), "\n")
  print(search_result)
 
  
  #vcで流すためにvideoIDを取得
  print (videde)

#youtubeで検索するための設定。.scで来たワードを入れる
def youtubeop(num):
  # 検索ワード
  argparser = argparse.ArgumentParser()
  argparser.add_argument("--q")
  # 検索上限
  argparser.add_argument("--max-results", help="Max results", default=num)
  args = argparser.parse_args()
  args.q = sss
  
  try:
    youtube_search(args)

    
  
  except HttpError as e:
    print("An HTTP error %d occurred:\n%s" % (e.resp.status, e.content))



#URLでyoutubeに飛んで、再生。
def ytl(que):
  ai = que[0]
  global voice,t,ended,titl,meme,loop,loopskip,videde,videid
  videid = ai
  song = pafy.new(videid) #pafyに引数を渡す
  audio= song.getbestaudio()  
  source= FFmpegPCMAudio(audio.url, **FFMPEG_OPTIONS)  
  voice.play(source,after=lambda e : ende(que)) #流す  
        
#終了後にqueueの先頭を削除
def ende(queu):
  print("done")
  print(queu)
  global ended,qloo,loop
  if qloo == 0 and loop == 0:
    if len(queu) >= 2:  
      queu.popleft()
      ytl(queu)
    elif len(queu) == 1:
      queu.popleft()
      print(queu)
      return
    else:
      return

  elif qloo == 1 and loop == 0:
    queu.append(queu[0])
    queu.popleft()
    print(queu)
    if len(queu) >= 1 :
        ytl(queu)
  elif loop == 1:
    ytl(queu)
  else:
    return

def random_choice(num,len_word):
  print(num)
  ranran =[]
  for i in range(num):
    ran = random.randint(0,len_word-1)
    print("random:"+str(ran))
    ranran.append(ran)
  print(ranran)
  return ranran
  

#ここからdiscord
@client.event #起動が完了するとコンソールにhiと送り、プレイ中の表示をさせる
async def on_ready():
    print("hi")
    await client.change_presence(activity=discord.Game(name="hi", type=1))
    await client.change_presence(activity=discord.Game(name="I'm listening to music!!", type=1))

@client.event
async def on_voice_state_update(member, before, after):
  global voice,player,youtube_url,url,sss,argparser,videde,queue_dict,ended,qloo,loop,titl,elect,meme,print_title,queue_title,count_music,loopskip,videid,chanid
  
  if voice != None and before.channel != None:
    if before.channel.id == vcid:
      name = voice.channel.members
      if len(name) == 1:
        print(name)
        qloo = 0
        loop = 0
        queue_dict.clear()
        if voice.is_playing():
          voice.stop()

        #guild = message.guild.voice_client
        await voice.disconnect()
        voice = None
        async with chanid.typing():
          await asyncio.sleep(0.5)
          await chanid.send("good bye!")
      else:
        return
    else:
      return



@client.event
async def on_message(message): #メッセージの確認
    
    global voice,player,youtube_url,url,sss,argparser,videde,queue_dict,ended,qloo,loop,titl,elect,meme,print_title,queue_title,count_music,loopskip,videid,chanid,vcid
    meme = message
    msg = message.content 
    aft = ""
    bef = msg[:msg.find(" ")]
    afneme = msg[msg.find(" "):]
    aft_temp = afneme.split(" ")
    if len(aft_temp) >= 2:
      aft = aft_temp[1]
    if msg[:1] == ".":

      print(msg)
      print(bef)
      print(aft)
      print(afneme)
    if message.author.bot: #botの場合反応しない 
        return

    if elect == 1:
      if msg.isdecimal() == False:
        elect = 0
        await message.channel.send("キャンセルしました")
        return
      inmsg = int(msg) #検索した候補を選ぶ
      if inmsg <= count_music:
        videid = videde[inmsg-1]
        q = f"https://www.youtube.com/watch?v={videid}"
        enqueue(voice ,q)
        async with message.channel.typing():
          await asyncio.sleep(0.5)
          if print_title == 0:
            await message.channel.send("キューに追加: "+titl[inmsg-1])
          elif print_title == 1:
            await message.channel.send("キューに追加: "+q)
      videde = []
      titl = []
      elect = 0

    if msg == ".move": #vcを移動する
      await voice.move_to(message.author.voice.channel)
    
    if msg == ".clear" or msg == ".c": #キューをクリア
      async with message.channel.typing():
        await asyncio.sleep(1)
        await message.channel.send("キューをリセットしました.")
      queue_dict.clear()
    
    if bef == ".remove":
      if aft.isdecimal() == False:
        return
      if aft == "1":
        await message.channel.send("現在再生している曲です")
      
      elif int(aft) > len(queue_dict):
        await message.channel.send("範囲外です")
        return
      else:
        remint = int(aft) - 1
        temp = queue_dict[remint]
        del queue_dict[remint]
        await message.channel.send(temp + " を削除しました")
        print(queue_dict)
        

    if msg == ".pr_title": #検索時にタイトルのみにする
      if print_title == 0:
        print_title = 1
        await message.channel.send("検索時にタイトルのみ表示します。")
      elif print_title == 1:
        print_title = 0
        await message.channel.send("検索時にURLも表示します。")

    if msg == "!debug":
      name = [m.name for m in message.author.voice.channel.members]
      await message.channel.send(name)
    
    if msg == "!announcement" :
      await client.change_presence(activity=discord.Game(name=msg[14:], type=1))

    if msg == ".info": #botの情報
      await message.channel.send("This bot made by kakigoori(2021) \n\n You can listen to music to use this bot. \n\n This bot is happened to occur an error or to slow down download.")

    if msg == ".help": #botのコマンド
      await message.channel.send("```.help :このメッセージを表示します。\n.play <URL>,<word> :URLでその曲、wordで検索して、流します。\n.sc <word> :wordをyoutube検索して、5個の候補を表示します。\n.q :キューの中身を表示します(ログが流れます)。\n.skip :流れている曲をスキップします。\n.clear :キューをリセットします。\n.dc :botをvcから切断させます。\n.move :vcを移動させます。\n.queueloop :キューをループさせます。\n.loop :一曲のみをループします。\n remove <キュー番号> :キューの特定の位置の曲をキューから削除します。 \n.pr_title :検索時にタイトルのみを表示します。(現在使えません)\n.info :botの情報を表示します\n.loopinfo :loopの状況のみを表示します\n.skipto :指定したキューの場所までスキップします\n.loopinfo :loopの状況のみを返します\n.pos :1曲のみ検索して、再生します\n.rap [数字] :数字で指定した数だけ検索ワードリストから言葉を持ってきます\n.racom :おすすめの曲リストからランダムに1曲再生します。\n.adw [言葉] :検索ワードリストに言葉を登録します\n```")
    
    if msg == ".dc": #切断
      qloo = 0
      loop = 0
      queue_dict.clear()
      if voice.is_playing():
        voice.stop()

      #guild = message.guild.voice_client
      await voice.disconnect()
      voice = None
      
      j = 0
      async with message.channel.typing():
        await asyncio.sleep(0.7)
        await message.channel.send("good bye!")
        ended = 0


    #if bef == ".q_title": #キューの表示時にタイトルのみ表示させたいけど、なかなか厳しいものがある
     # if queue_title == 0:
      #  queue_title = 1
      #  await message.channel.send("キューの表示時にタイトルのみ表示します。")
      #elif queue_title == 1:
      #  queue_title  = 0
      #  await message.channel.send("キューの表示時にURLも表示します。")


    if msg == ".q" or msg == ".queue": #キューの中身を表示させる。デザインを変えたいね.
     # if queue_title == 0:
      count_music = 1
      for spt in queue_dict:
        await message.channel.send(str(count_music)+":"+spt)
        count_music = count_music + 1
      if qloo == 1:
        await message.channel.send("queueloop: \N{Heavy Large Circle}")
      elif qloo == 0:
        await message.channel.send("queueloop: \N{Cross Mark}")
      if loop == 1:
        await message.channel.send("loop: \N{Heavy Large Circle}")
      if loop == 0:
        await message.channel.send("loop : \N{Cross Mark}")


    if msg == ".skip" or msg == ".s": #流れている曲をスキップ。stopするだけで、曲が終了したときの処理が起こる
      voice.stop()


    if msg == ".loop" or msg == ".lp": #一曲のみのloopをon,offする
      if loop == 0:
        loop = 1
        await message.channel.send("loopがonになりました")
      elif loop == 1:
        loop = 0
        await message.channel.send("loopがoffになりました")


    if msg == ".queueloop" or msg == ".qlp": #queueloopをon,offする。
      if qloo == 0:
        qloo = 1
        await message.channel.send("queueloopがonになりました")
      elif qloo == 1:
        qloo = 0
        await message.channel.send("queueloopがoffになりました")


    if msg == ".lp_info" or msg == ".lpinfo": #loopの状態を確認
      if qloo == 1:
        await message.channel.send("queueloop: \N{Heavy Large Circle}")
      elif qloo == 0:
        await message.channel.send("queueloop: \N{Cross Mark}")
      if loop == 1:
        await message.channel.send("loop: \N{Heavy Large Circle}")
      elif loop == 0:
        await message.channel.send("loop : \N{Cross Mark}")

    if bef == ".skipto" or bef == ".skt": #指定した曲を再生する
      if aft.isdecimal() == False:
        return
      elif aft == "1":
        await message.channel.send("現在再生している曲です")
      elif int(aft) > len(queue_dict):
        await message.channel.send("範囲外です") #範囲外か判断する
      else:
        num = int(aft) -1
        poping = int(aft)
        queue_dict.insert(1,queue_dict[num])
        del queue_dict[poping]
        voice.stop()

    if msg == ".random_reccomend" or msg == ".racom": #おすすめリストからランダムに1つURLを持ってくる
      chanid = client.get_channel(message.channel.id)
      nn = os.path.dirname(os.path.abspath(__file__))
      f = open(f'{nn}/recommend.txt', "r")
      url_list = f.readlines()
      len_url = len(url_list)
      if len_url < 0:
        await message.channel.send("おすすめリストがありません")
      elif len_url >= 1:
        if voice == None:
          voice = await message.author.voice.channel.connect(reconnect = True)
        elif message.author.voice is not None and message.guild.me not in message.author.voice.channel.members and message.guild.id == voice.guild.id: #サーバーと、ボイスチャンネルを判別
          await voice.move_to(message.author.voice.channel)
        figure = random_choice(1,len_url)
        q = url_list[figure[0]]
        enqueue(voice,q)
        async with message.channel.typing():
          await asyncio.sleep(0.5)
          await message.channel.send("キューに追加: "+q)
      f.close()


    if bef == ".randomplay" or bef == ".rap": #検索ワードリストから指定した数言葉を持ってくる
      chanid = client.get_channel(message.channel.id)
      if aft.isdecimal() == False: #指定した数が数字じゃないときは反応しない
        return
      nn = os.path.dirname(os.path.abspath(__file__))
      f = open(f'{nn}/words.txt', "r",encoding="utf-8")
      word_list = []
      for i in f:
        line = i.rstrip() #読み込んだ文字に改行文字が含まれているため改行文字を削除
        word_list.append(line)
      print(word_list)
      len_word = len(word_list)
      if len_word < int(aft):
        await message.channel.send("指定した数の検索ワードがありません")
      elif len_word >= int(aft):
        videde = []
        words = []
        figure = random_choice(int(aft),len_word)       
        for i in range(int(aft)):
          words.append(word_list[figure[i]])
        sss = (' '.join(words))
        youtubeop(1)
        if voice == None:
          voice = await message.author.voice.channel.connect(reconnect = True)
        elif message.author.voice is not None and message.guild.me not in message.author.voice.channel.members and message.guild.id == voice.guild.id: #サーバーと、ボイスチャンネルを判別
          await voice.move_to(message.author.voice.channel)
        
        videid = videde[0]
        q = f"https://www.youtube.com/watch?v={videid}"
        
        async with message.channel.typing():
          await asyncio.sleep(0.5)
          await message.channel.send("キューに追加: "+q)
        enqueue(voice,q)
      f.close()

    if bef == ".add_word" or bef == ".adw": #検索ワードリストに言葉を追加
      nn = os.path.dirname(os.path.abspath(__file__))
      f = open(f'{nn}/words.txt', "a",encoding="utf-8")
      f.write(f'{aft}\n')
      f.close()
      f = open(f'{nn}/words.txt', "r",encoding="utf-8") 
      lis = f.readlines()
      print(lis)
      f.close()



    if msg == ".recommend" or msg == ".rec": #おすすめリストを全てキューに入れる
      chanid = client.get_channel(message.channel.id)
      if voice == None:
        voice = await message.author.voice.channel.connect(reconnect = True)
        vcid = message.author.voice.channel.id

      elif message.author.voice is not None and message.guild.me not in message.author.voice.channel.members and message.guild.id == voice.guild.id: #サーバーと、ボイスチャンネルを判別
          await voice.move_to(message.author.voice.channel)  
      nn = os.path.dirname(os.path.abspath(__file__))
      f = open(f'{nn}/recommend.txt', "r")
      lis = f.readlines()
      if len(lis) >= 1:
        for line in lis:
          line = line.rstrip()  # 読み込んだ行の末尾には改行文字があるので改行文字を削除
          if line[:5] == "https":
            enqueue(voice,line)
        await message.channel.send("ADMINのおすすめの曲を再生します。(詳細は.qコマンドを使用(ログが流れます))")
      else:
        await message.channel.send("ADMINのおすすめの曲は現在ありません。")
      f.close()

    if bef == ".sc" or bef == ".search": #検索する。動画idを取得して、youtubeのURLの後にくっつけてるだけ
      chanid = client.get_channel(message.channel.id)
      titl = []
      videde = []
      if message.author.voice is None:
        await message.channel.send("ボイスチャットに参加してください.")
        return
      sss = afneme
      youtubeop(5)
      #youtube_url = f"https://www.youtube.com/watch?v={videde}"
      if voice == None:
        voice = await message.author.voice.channel.connect(reconnect = True)
      elif message.author.voice is not None and message.guild.me not in message.author.voice.channel.members and message.guild.id == voice.guild.id: #サーバーと、ボイスチャンネルを判別

          await voice.move_to(message.author.voice.channel)

      count_music = 1
      if print_title == 0:
            for spt in videde:
              await message.channel.send(str(count_music)+": https://www.youtube.com/watch?v="+spt)
              count_music = count_music + 1
              if count_music == len(videde) + 1:
                break
      elif print_title == 1:
            for spt in titl:
              await message.channel.send(str(count_music)+": "+spt)
              count_music = count_music + 1
              if count_music == len(titl) + 1:
                break
      await message.channel.send("流したい曲の番号を送信してください(.無し)")
      elect = 1
      #enqueue(voice,youtube_url)


    if bef == ".play_one_search" or bef == ".pos": #1曲のみ検索する 動作速度を優先した感じ
      chanid = client.get_channel(message.channel.id)
      if aft[:8] == "https://":
        await message.channel.send("URLではこの機能は使えません")
      else:
        videde =[]
        titl = []
        if message.author.voice is None:
          await message.channel.send("ボイスチャットに参加してください.")
          return
        sss = afneme
        youtubeop(1)
        #youtube_url = f"https://www.youtube.com/watch?v={videde}"
        if voice == None:
          voice = await message.author.voice.channel.connect(reconnect = True)
        elif message.author.voice is not None and message.guild.me not in message.author.voice.channel.members and message.guild.id == voice.guild.id: #サーバーと、ボイスチャンネルを判別

          await voice.move_to(message.author.voice.channel)
        
        videid = videde[0]
        q = f"https://www.youtube.com/watch?v={videid}"
        async with message.channel.typing():
          await asyncio.sleep(0.5)
          await message.channel.send("キューに追加: "+q)
        enqueue(voice,q)

              
    if bef == ".play" or bef == ".p": #指定されたURLの曲を流す。
        #idx = msg.find(" ")
        chanid = client.get_channel(message.channel.id)
        if aft[:8] == "https://": #youtubeのURLかを判別。
            youtube_url = aft
            if youtube_url[24:32] == "playlist": #プレイリストか判別
              temp = []
              playlist = pafy.get_playlist2(youtube_url)
              for i in range(len(playlist)):
                temp.append(playlist[i])
              print(temp[0])

              for r in range(len(playlist)):
                ten = str(temp[r])
                queue_dict.append("https://www.youtube.com/watch?v="+ten[13:24])
              print(queue_dict)

              if message.author.voice is None:
                await message.channel.send("ボイスチャットに参加してください.")
                return

              if voice == None:
                voice = await message.author.voice.channel.connect(reconnect = True)
            

              elif message.author.voice is not None and message.guild.me not in message.author.voice.channel.members and message.guild.id == voice.guild.id:            
                await voice.move_to(message.author.voice.channel)

              ytl(queue_dict)
              async with message.channel.typing():
                await asyncio.sleep(0.5)
                await message.channel.send("playlistを追加しました。")

            else: #曲のURLがそのままのとき
                if message.author.voice is None:
                  await message.channel.send("ボイスチャットに参加してください.")
                  return

                if voice == None:
                  voice = await message.author.voice.channel.connect(reconnect = True)
            

                elif message.author.voice is not None and message.guild.me not in message.author.voice.channel.members and message.guild.id == voice.guild.id:            
                  await voice.move_to(message.author.voice.channel)

                enqueue(voice,youtube_url)
                async with message.channel.typing():
                 await asyncio.sleep(0.5)
                await message.channel.send("正常に追加されました。")

        else: #URLじゃなかったんだね...
          videde =[]
          titl = []
          if message.author.voice is None:
            await message.channel.send("ボイスチャットに参加してください.")
            return
          sss = afneme
          youtubeop(5)
         #youtube_url = f"https://www.youtube.com/watch?v={videde}"
          if voice == None:
            voice = await message.author.voice.channel.connect(reconnect = True)
          elif message.author.voice is not None and message.guild.me not in message.author.voice.channel.members and message.guild.id == voice.guild.id: #サーバーと、ボイスチャンネルを判別

            await voice.move_to(message.author.voice.channel)

          count_music = 1
          if print_title == 0: #候補を5個並べる。選択の部分はまた別な場所(上の方にある)
            for spt in videde:
              await message.channel.send(str(count_music)+": https://www.youtube.com/watch?v="+spt)
              count_music = count_music + 1
              if count_music == len(videde) + 1:
                break
          elif print_title == 1:
            for spt in titl:
              await message.channel.send(str(count_music)+": "+spt)
              count_music = count_music + 1
              if count_music == len(titl) + 1:
                break
          await message.channel.send("流したい曲の番号を送信してください(.無し)") #動作速度を早めるためにはどうすればええんや...
          elect = 1
          #enqueue(voice,youtube_url)
      
if __name__ == '__main__': #起動
  client.run(TOKEN)

#やりたいことリスト
#
#
#
#
#
#
#
#
#