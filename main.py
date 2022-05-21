from calendar import c
from distutils.log import debug
from encodings import normalize_encoding
from multiprocessing.connection import answer_challenge
from operator import truediv
from shutil import get_unpack_formats
from turtle import clear
import pafy
from discord import FFmpegPCMAudio
import discord
from discord.ext import commands
from discord import player
import os
import asyncio
import random
#import slash_seat
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from oauth2client.tools import argparser
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import _Response, Request

import func_youtube


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
#APIの設定
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"

#ffmpegの設定
FFMPEG_OPTIONS= {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5','options': '-vn'}

#様々な変数の初期値
intents = discord.Intents.all()
count_music = 1
elect = 0
titl = []
youtube_url = ""
voice = {}
playerr = None
url = 0
qloo = {}
looping = {}
ended = 0
queue_dict = {}
t = 0
videde = []
titl = [] 
sss = ""
meme = None
print_title = {}
queue_title = 0
loopingskip = 0
queues = queue_dict
chanid = {}
vcid = {}
you = True
guildid = 0
channelid = {}

#devkeyの有無
if DEVELOPER_KEY == "no":
  you = False

#キューの設定
def enqueue(voice_client, youtube_ur):
    global queue_dict,guildid
    guildid = voice_client.guild.id 

    queue_dict.setdefault(guildid,[]).append(youtube_ur)
    print(queue_dict)
    
    if not voice_client.is_playing():
        ytl(queue_dict,guildid)
    else:
      return




#URLでyoutubeに飛んで、再生。
def ytl(que,guildid):
  global voice,t,ended,titl,meme,looping,loopingskip,videde,videid
  ai = que[guildid][0]
  videid = ai
  song = pafy.new(videid) #pafyに引数を渡す
  audio= song.getbestaudio()  
  source= FFmpegPCMAudio(audio.url, **FFMPEG_OPTIONS)  
  voice[guildid].play(source,after=lambda e : ende(que,guildid)) #流す  
        
#終了後にqueueの先頭を削除
def ende(queu,guildid):
  print("done")
  global ended,qloo,looping,chanid
  print(queu[guildid])
  if qloo[guildid] == 0 and looping[guildid] == 0:
    if len(queu[guildid]) >= 2:  
      del queu[guildid][0]
      ytl(queu,guildid)
    elif len(queu[guildid]) == 1:
      del queu[guildid][0]
      print(queu[guildid])
      return
    else:
      return

  elif qloo[guildid] == 1 and looping[guildid] == 0:
    queu[guildid].append(queu[guildid][0])
    del queu[guildid][0]
    print(queu[guildid])
    if len(queu[guildid]) >= 1 :
        ytl(queu,guildid)
  elif looping[guildid] == 1:
    ytl(queu,guildid)
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

#コマンドの接頭辞を設定
bot = commands.Bot(command_prefix='.')

@bot.event #起動が完了するとコンソールにhiと送り、プレイ中の表示をさせる
async def on_ready():
  global you
  print("hi")
  await bot.change_presence(activity=discord.Game(name="hi", type=1))
  await bot.change_presence(activity=discord.Game(name="I'm listening to music!!", type=1))
  if you == False:
    print("制限モードがonになっています。解除するにはTOKEN.txtのYoutube_API_KEYにYoutube v3 APIのkeyを入力してください。")

@bot.event
async def on_voice_state_update(member, before, after):
  global voice,player,youtube_url,url,sss,argparser,videde,queue_dict,ended,qloo,looping,titl,elect,meme,print_title,queue_title,count_music,loopingskip,videid,chanid,vcid
  if before.channel != None and vcid != {}:
    print("抜けた")
    befoguild = {}
    guildid = before.channel.guild.id
    befoguild[guildid] = before.channel.id
    if voice != None and before.channel != None:
      if befoguild[guildid] == vcid[guildid]:
        name = voice[guildid].channel.members
        if len(name) == 1:
          print(name)
          qloo[guildid] = 0
          looping[guildid] = 0
          queue_dict[guildid].clear()
          if voice[guildid].is_playing():
            voice[guildid].stop()

        #guild = message.guild.voice_client
          await voice[guildid].disconnect()
          async with chanid[guildid].typing():
            await asyncio.sleep(0.5)
            await chanid[guildid].send("good bye!")
          del voice[guildid] 
          del chanid[guildid]          
      else:
        return
    else:
      return

@bot.listen() #イベントを追加
async def on_message(message): #メッセージの確認

    global channelid,voice,player,youtube_url,url,sss,argparser,videde,queue_dict,ended,qloo,looping,titl,elect,meme,print_title,queue_title,count_music,loopingskip,videid,chanid,vcid,you
    if elect == 1: #候補選択 
      if message.channel != None and chanid != {}:
        guildid = message.guild.id
        mesguild = {}
        mesguild[guildid] = message.channel.id
        if mesguild[guildid] == channelid[guildid]:
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

          if msg.isdecimal() == False:
              elect = 0
              await chanid[guildid].send("キャンセルしました")
              return
          inmsg = int(msg) #検索した候補を選ぶ
          if inmsg <= count_music:
              videid = videde[inmsg-1]
              q = f"https://www.youtube.com/watch?v={videid}"
              enqueue(voice[guildid] ,q)
              async with chanid[guildid].typing():
                await asyncio.sleep(0.5)
                if print_title[guildid] == 0:
                  await chanid[guildid].send("キューに追加: "+titl[inmsg-1])
                elif print_title[guildid] == 1:
                  await chanid[guildid].send("キューに追加: "+q)
          videde = []
          titl = []
          elect = 0




#コマンドたち
@bot.command()
async def move(message): #vcを移動する
  global chanid,guildid,voice,vcid
  guildid = message.guild.id
  await voice[guildid].move_to(message.author.voice.channel)
  vcid[guildid] = message.author.voice.channel.id


@bot.command()
async def clear(message):  #キューをクリア
    global queue_dict,guildid,chanid
    guildid = message.guild.id
    async with chanid[guildid].typing():
        await asyncio.sleep(1)
        await chanid[guildid].send("キューをリセットしました.")
    queue_dict[guildid] = []



@bot.command()
async def c(message):
    global queue_dict,guildid,chanid
    guildid = message.guild.id
    async with chanid[guildid].typing():
        await asyncio.sleep(1)
        await chanid[guildid].send("キューをリセットしました.")
    queue_dict[guildid] = []


@bot.command()
async def remove(message, aft): #キューの中の曲を削除
    global queue_dict,guildid,chanid
    guildid = message.guild.id
    if aft.isdecimal() == False:
        return
    if aft == "1":
        await chanid[guildid].send("現在再生している曲です")
      
    elif int(aft) > len(queue_dict):
        await chanid[guildid].send("範囲外です")
        return
    else:
        remint = int(aft) - 1
        temp = queue_dict[guildid][remint]
        del queue_dict[guildid][remint]
        await chanid[guildid].send(temp + " を削除しました")
        print(queue_dict)
        

@bot.command()
async def pr_title(message):#検索時にタイトルのみにする
  global guildid,chanid,print_title
  guildid = message.guild.id
  if print_title[guildid] == 0:
    print_title[guildid] = 1
    await chanid[guildid].send("検索時にタイトルのみ表示します。")
  elif print_title[guildid] == 1:
    print_title[guildid] = 0
    await chanid[guildid].send("検索時にURLも表示します。")


@bot.command()
async def info(message):#botの情報
    global chanid,guildid
    guildid = message.guild.id
    await chanid[guildid].send("This bot made by kakigoori(2022) \n\n You can listen to music to use this bot. \n\n This bot is happened to occur an error or to slow down download.")

bot.remove_command('help')

@bot.command()
async def help(message):#botのコマンド
    global chanid,guildid
    guildid = message.guild.id
    await message.channel.send("```.help :このメッセージを表示します。\n.play <URL>,<word> :URLでその曲、wordで検索して、流します。\n.sc <word> :wordをyoutube検索して、5個の候補を表示します。\n.q :キューの中身を表示します(ログが流れます)。\n.skip :流れている曲をスキップします。\n.clear :キューをリセットします。\n.dc :botをvcから切断させます。\n.move :vcを移動させます。\n.queueloop :キューをループさせます。\n.loop :一曲のみをループします。\n remove <キュー番号> :キューの特定の位置の曲をキューから削除します。 \n.pr_title :検索時にタイトルのみを表示します。(現在使えません)\n.info :botの情報を表示します\n.loop :loopの状況のみを表示します\n.skipto :指定したキューの場所までスキップします\n.pos :1曲のみ検索して、再生します\n.rap [数字] :数字で指定した数だけ検索ワードリストから言葉を持ってきます\n.racom :おすすめの曲リストからランダムに1曲再生します。\n.racoms :おすすめの曲リストにある曲をすべてキューに入れます\n.adw [言葉] :検索ワードリストに言葉を登録します\n```")


@bot.command()
async def dc(message):
    global queue_dict,qloo,looping,voice,guildid,chanid#切断
    guildid = message.guild.id
    qloo[guildid] = 0
    looping[guildid] = 0
    queue_dict[guildid].clear()
    if voice[guildid].is_playing():
        voice[guildid].stop()

    #guild = message.guild.voice_client
    await voice[guildid].disconnect()
    voice = None
      
    j = 0
    async with chanid[guildid].typing():
        await asyncio.sleep(0.7)
        await chanid[guildid].send("good bye!")
    del voice[guildid] 
    del chanid[guildid] 
        


    #if bef == ".q_title": #キューの表示時にタイトルのみ表示させたいけど、なかなか厳しいものがある
     # if queue_title == 0:
      #  queue_title = 1
      #  await message.channel.send("キューの表示時にタイトルのみ表示します。")
      #elif queue_title == 1:
      #  queue_title  = 0
      #  await message.channel.send("キューの表示時にURLも表示します。")

@bot.command()
async def queue(message):#キューの中身を表示させる。デザインを変えたいね.
    global queue_dict,qloo,looping,chanid,guildid
    guildid = message.guild.id
     # if queue_title == 0:
    count_music = 1
    for spt in queue_dict[guildid]:
        await chanid[guildid].send(str(count_music)+":"+spt)
        count_music = count_music + 1
    if qloo[guildid] == 1:
        await chanid[guildid].send("queueloop: \N{Heavy Large Circle}")
    elif qloo[guildid] == 0:
        await chanid[guildid].send("queueloop: \N{Cross Mark}")
    if looping[guildid] == 1:
        await chanid[guildid].send("loop: \N{Heavy Large Circle}")
    if looping[guildid] == 0:
        await chanid[guildid].send("loop : \N{Cross Mark}")

@bot.command()
async def q(message):
    global queue_dict,qloo,looping,chanid,guildid
    guildid = message.guild.id
     # if queue_title == 0:
    count_music = 1
    for spt in queue_dict[guildid]:
        await chanid[guildid].send(str(count_music)+":"+spt)
        count_music = count_music + 1
    if qloo[guildid] == 1:
        await chanid[guildid].send("queueloop: \N{Heavy Large Circle}")
    elif qloo[guildid] == 0:
        await chanid[guildid].send("queueloop: \N{Cross Mark}")
    if looping[guildid] == 1:
        await chanid[guildid].send("loop: \N{Heavy Large Circle}")
    if looping[guildid] == 0:
        await chanid[guildid].send("loop : \N{Cross Mark}")

@bot.command()
async def skip(message):#流れている曲をスキップ。stopするだけで、曲が終了したときの処理が起こる
    global voice,queue_dict,guildid,chanid
    guildid = message.guild.id
    voice[guildid].stop()
    if len(queue_dict[guildid]) > 1:
     await chanid[guildid].send("再生: " + queue_dict[guildid][1])

@bot.command()
async def s(message):#流れている曲をスキップ。stopするだけで、曲が終了したときの処理が起こる
    global voice,queue_dict,guildid,chanid
    guildid = message.guild.id
    voice[guildid].stop()
    if len(queue_dict[guildid]) > 1:
     await chanid[guildid].send("再生: " + queue_dict[guildid][1])

@bot.command()
async def loop(message):#一曲のみのloopingをon,offする
    global looping,qloo,guildid
    guildid = message.guild.id
    if looping[guildid] == 0:
        looping[guildid] = 1
        await message.channel.send("loopがonになりました")
    elif looping[guildid] == 1:
        looping[guildid] = 0
        await message.channel.send("loopがoffになりました")

@bot.command()
async def lp(message):
    global looping,qloo,guildid
    guildid = message.guild.id
    if looping[guildid] == 0:
        looping[guildid] = 1
        await message.channel.send("loopがonになりました")
    elif looping[guildid] == 1:
        looping[guildid] = 0
        await message.channel.send("loopがoffになりました")


@bot.command()
async def queueloop(message):#queueloopingをon,offする。
    global qloo,looping,guildid,chanid
    guildid = message.guild.id
    if qloo[guildid] == 0:
        qloo[guildid] = 1
        await message.channel.send("queueloopがonになりました")
    elif qloo[guildid] == 1:
        qloo[guildid] = 0
        await message.channel.send("queueloopがoffになりました")

@bot.command()
async def qlp(message):#queueloopingをon,offする。
    global qloo,looping,guildid,chanid
    guildid = message.guild.id
    if qloo[guildid] == 0:
        qloo[guildid] = 1
        await message.channel.send("queueloopがonになりました")
    elif qloo[guildid] == 1:
        qloo[guildid] = 0
        await message.channel.send("queueloopがoffになりました")

@bot.command()
async def lpinfo(message):#loopingの状態を確認
    global qloo,looping,guildid,chanid
    guildid = message.guild.id
    if qloo[guildid] == 1:
        await chanid[guildid].send("queueloop : \N{Heavy Large Circle}")
    elif qloo[guildid] == 0:
        await chanid[guildid].send("queueloop : \N{Cross Mark}")
    if looping[guildid] == 1:
        await chanid[guildid].send("loop : \N{Heavy Large Circle}")
    elif looping[guildid] == 0:
        await chanid[guildid].send("loop : \N{Cross Mark}")


@bot.command()
async def skipto(message,aft):#指定した曲を再生する
    global queue_dict,voice,guildid,chanid
    guildid = message.guild.id
    if aft.isdecimal() == False:
        return
    elif aft == "1":
        await chanid[guildid].send("現在再生している曲です")
    elif int(aft) > len(queue_dict[guildid]):
        await chanid[guildid].send("範囲外です") #範囲外か判断する
    else:
        num = int(aft) -1
        poping = int(aft)
        queue_dict[guildid].insert(1,queue_dict[guildid][num])
        del queue_dict[guildid][poping]
        voice[guildid].stop()
        await chanid[guildid].send("再生: " + queue_dict[guildid][1])
@bot.command()
async def skt(message,aft):#指定した曲を再生する
    global queue_dict,voice,guildid,chanid
    guildid = message.guild.id
    if aft.isdecimal() == False:
        return
    elif aft == "1":
        await chanid[guildid].send("現在再生している曲です")
    elif int(aft) > len(queue_dict[guildid]):
        await chanid[guildid].send("範囲外です") #範囲外か判断する
    else:
        num = int(aft) -1
        poping = int(aft)
        queue_dict[guildid].insert(1,queue_dict[guildid][num])
        del queue_dict[guildid][poping]
        voice[guildid].stop()
        await chanid[guildid].send("再生: " + queue_dict[guildid][1])


@bot.command()
async def random_recommend(message): #おすすめリストからランダムに1つURLを持ってくる
    global guildid
    guildid = message.guild.id
    print(guildid)
    voiceid = message.author.voice
    global chanid,voice,queue_dict,vcid,sss,elect,videde,titl,channelid
    looping.setdefault(guildid,0)
    qloo.setdefault(guildid,0)
    print_title.setdefault(guildid,0)
    voice.setdefault(guildid,None)
    chanid[guildid] = bot.get_channel(message.channel.id)  
    nn = os.path.dirname(os.path.abspath(__file__))
    f = open(f'{nn}/recommend.txt', "r")
    url_list = f.readlines()
    len_url = len(url_list)
    if len_url < 0:
        await message.channel.send("おすすめリストがありません")
    elif len_url >= 1:
        if voiceid == None:
                await chanid[guildid].send("ボイスチャットに参加してください。")
                return
        elif voice[guildid] == None:
                voice[guildid] = await message.author.voice.channel.connect(reconnect = True)
                chanid[guildid] = bot.get_channel(message.channel.id)
                vcid[guildid] = message.author.voice.channel.id
                channelid[guildid] = message.channel.id
                print(channelid)
                print(channelid[guildid])
        elif vcid[guildid] != message.author.voice.channel.id:
                await voice[guildid].move_to(message.author.voice.channel)
                vcid[guildid] = message.author.voice.channel.id
        figure = random_choice(1,len_url)
        q = url_list[figure[0]]
        enqueue(voice[guildid],q)
        async with message.channel.typing():
          await asyncio.sleep(0.5)
          await message.channel.send("キューに追加: "+q)
    f.close()

@bot.command()
async def racom(message): #おすすめリストからランダムに1つURLを持ってくる
    global guildid
    guildid = message.guild.id
    print(guildid)
    voiceid = message.author.voice
    global chanid,voice,queue_dict,vcid,sss,elect,videde,titl,channelid
    looping.setdefault(guildid,0)
    qloo.setdefault(guildid,0)
    print_title.setdefault(guildid,0)
    voice.setdefault(guildid,None)
    chanid[guildid] = bot.get_channel(message.channel.id) 
    nn = os.path.dirname(os.path.abspath(__file__))
    f = open(f'{nn}/recommend.txt', "r")
    url_list = f.readlines()
    len_url = len(url_list)
    if len_url < 0:
        await message.channel.send("おすすめリストがありません")
    elif len_url >= 1:
        if voiceid == None:
                await chanid[guildid].send("ボイスチャットに参加してください。")
                return
        elif voice[guildid] == None:
                voice[guildid] = await message.author.voice.channel.connect(reconnect = True)
                chanid[guildid] = bot.get_channel(message.channel.id)
                vcid[guildid] = message.author.voice.channel.id
                channelid[guildid] = message.channel.id
                print(channelid)
                print(channelid[guildid])
        elif vcid[guildid] != message.author.voice.channel.id:
                await voice[guildid].move_to(message.author.voice.channel)
                vcid[guildid] = message.author.voice.channel.id
        figure = random_choice(1,len_url)
        q = url_list[figure[0]]
        enqueue(voice[guildid],q)
        async with message.channel.typing():
          await asyncio.sleep(0.5)
          await message.channel.send("キューに追加: "+q)
    f.close()

@bot.command()
async def randomplay(message,aft):#検索ワードリストから指定した数言葉を持ってくる
    global guildid
    guildid = message.guild.id
    print(guildid)
    voiceid = message.author.voice
    global chanid,voice,queue_dict,vcid,sss,elect,videde,titl,channelid
    if you ==False:
        await message.channel.send("制限モードでは検索機能は使えません。TOKEN.txtのYoutube_API_KEYにyoutube v3 APIのkeyを入力してください。")
        return
    looping.setdefault(guildid,0)
    qloo.setdefault(guildid,0)
    print_title.setdefault(guildid,0)
    voice.setdefault(guildid,None)
    chanid[guildid] = bot.get_channel(message.channel.id)   
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
        ff =func_youtube.youtubeop(1,sss)
        videde = list(ff[0])
        titl = list(ff[1])
        if voiceid == None:
                await chanid[guildid].send("ボイスチャットに参加してください。")
                return
        elif voice[guildid] == None:
                voice[guildid] = await message.author.voice.channel.connect(reconnect = True)
                chanid[guildid] = bot.get_channel(message.channel.id)
                vcid[guildid] = message.author.voice.channel.id
                channelid[guildid] = message.channel.id
                print(channelid)
                print(channelid[guildid])
        elif vcid[guildid] != message.author.voice.channel.id:
                await voice[guildid].move_to(message.author.voice.channel)
                vcid[guildid] = message.author.voice.channel.id
        
        videid = videde[0]
        q = f"https://www.youtube.com/watch?v={videid}"
        
        async with message.channel.typing():
          await asyncio.sleep(0.5)
          await message.channel.send("キューに追加: "+q)
        enqueue(voice[guildid],q)
    f.close()

@bot.command()
async def rap(message,aft):#検索ワードリストから指定した数言葉を持ってくる
    global guildid
    guildid = message.guild.id
    print(guildid)
    voiceid = message.author.voice
    global chanid,voice,queue_dict,vcid,sss,elect,videde,titl,channelid
    looping.setdefault(guildid,0)
    qloo.setdefault(guildid,0)
    print_title.setdefault(guildid,0)
    voice.setdefault(guildid,None)
    chanid[guildid] = bot.get_channel(message.channel.id) 
    if you ==False:
        await chanid[guildid].send("制限モードでは検索機能は使えません。TOKEN.txtのYoutube_API_KEYにyoutube v3 APIのkeyを入力してください。")
        return
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
        ff = func_youtube.youtubeop(1,sss)
        videde = list(ff[0])
        titl = list(ff[1])

        if voiceid == None:
                await chanid[guildid].send("ボイスチャットに参加してください。")
                return
        elif voice[guildid] == None:
                voice[guildid] = await message.author.voice.channel.connect(reconnect = True)
                chanid[guildid] = bot.get_channel(message.channel.id)
                vcid[guildid] = message.author.voice.channel.id
                channelid[guildid] = message.channel.id
                print(channelid)
                print(channelid[guildid])
        elif vcid[guildid] != message.author.voice.channel.id:
                await voice[guildid].move_to(message.author.voice.channel)
                vcid[guildid] = message.author.voice.channel.id
        
        videid = videde[0]
        q = f"https://www.youtube.com/watch?v={videid}"
        
        async with chanid[guildid].typing():
          await asyncio.sleep(0.5)
          await chanid[guildid].send("キューに追加: "+q)
        enqueue(voice[guildid],q)
    f.close()

@bot.command()
async def addword(message,aft):#検索ワードリストに言葉を追加
      nn = os.path.dirname(os.path.abspath(__file__))
      f = open(f'{nn}/words.txt', "a",encoding="utf-8")
      f.write(f'{aft}\n')
      f.close()
      f = open(f'{nn}/words.txt', "r",encoding="utf-8") 
      lis = f.readlines()
      print(lis)
      f.close()

@bot.command()
async def adw(message,aft):#検索ワードリストに言葉を追加
      nn = os.path.dirname(os.path.abspath(__file__))
      f = open(f'{nn}/words.txt', "a",encoding="utf-8")
      f.write(f'{aft}\n')
      f.close()
      f = open(f'{nn}/words.txt', "r",encoding="utf-8") 
      lis = f.readlines()
      print(lis)
      f.close()

@bot.command()
async def recommend(message):#おすすめリストを全てキューに入れる
    global guildid
    guildid = message.guild.id
    print(guildid)
    voiceid = message.author.voice
    global chanid,voice,queue_dict,vcid,sss,elect,videde,titl,channelid
    looping.setdefault(guildid,0)
    qloo.setdefault(guildid,0)  
    print_title.setdefault(guildid,0)
    voice.setdefault(guildid,None)
    chanid[guildid] = bot.get_channel(message.channel.id)
    if voiceid == None:
            await chanid[guildid].send("ボイスチャットに参加してください。")
            return
    elif voice[guildid] == None:
            voice[guildid] = await message.author.voice.channel.connect(reconnect = True)
            chanid[guildid] = bot.get_channel(message.channel.id)
            vcid[guildid] = message.author.voice.channel.id
            channelid[guildid] = message.channel.id
            print(channelid)
            print(channelid[guildid])
    elif vcid[guildid] != message.author.voice.channel.id:
            await voice[guildid].move_to(message.author.voice.channel)
            vcid[guildid] = message.author.voice.channel.id
    nn = os.path.dirname(os.path.abspath(__file__))
    f = open(f'{nn}/recommend.txt', "r")
    lis = f.readlines()
    if len(lis) >= 1:
        for line in lis:
          line = line.rstrip()  # 読み込んだ行の末尾には改行文字があるので改行文字を削除
          if line[:5] == "https":
            enqueue(voice[guildid],line)
        await chanid[guildid].send("ADMINのおすすめの曲を再生します。(詳細は.qコマンドを使用(ログが流れます))")
    else:
        await chanid[guildid].send("ADMINのおすすめの曲は現在ありません。")
    f.close()

@bot.command()
async def racoms(message):#おすすめリストを全てキューに入れる
    global guildid
    guildid = message.guild.id
    print(guildid)
    voiceid = message.author.voice
    global chanid,voice,queue_dict,vcid,sss,elect,videde,titl,channelid
    looping.setdefault(guildid,0)
    qloo.setdefault(guildid,0)  
    print_title.setdefault(guildid,0)
    voice.setdefault(guildid,None)
    chanid[guildid] = bot.get_channel(message.channel.id)
    if voiceid == None:
            await chanid[guildid].send("ボイスチャットに参加してください。")
            return
    elif voice[guildid] == None:
            voice[guildid] = await message.author.voice.channel.connect(reconnect = True)
            chanid[guildid] = bot.get_channel(message.channel.id)
            vcid[guildid] = message.author.voice.channel.id
            channelid[guildid] = message.channel.id
            print(channelid)
            print(channelid[guildid])
    elif vcid[guildid] != message.author.voice.channel.id:
            await voice[guildid].move_to(message.author.voice.channel)
            vcid[guildid] = message.author.voice.channel.id
    nn = os.path.dirname(os.path.abspath(__file__))
    f = open(f'{nn}/recommend.txt', "r")
    lis = f.readlines()
    if len(lis) >= 1:
        for line in lis:
          line = line.rstrip()  # 読み込んだ行の末尾には改行文字があるので改行文字を削除
          if line[:5] == "https":
            enqueue(voice[guildid],line)
        await chanid[guildid].send("ADMINのおすすめの曲を再生します。(詳細は.qコマンドを使用(ログが流れます))")
    else:
        await chanid[guildid].send("ADMINのおすすめの曲は現在ありません。")
    f.close()

@bot.command()
async def search(message,*,aft):#検索する。動画idを取得して、youtubeのURLの後にくっつけてるだけ
    global guildid
    guildid = message.guild.id
    print(guildid)
    voiceid = message.author.voice
    global chanid,voice,queue_dict,vcid,sss,elect,videde,titl,channelid,print_title
    looping.setdefault(guildid,0)
    qloo.setdefault(guildid,0)
    print_title.setdefault(guildid,0)
    voice.setdefault(guildid,None)
    chanid[guildid] = bot.get_channel(message.channel.id)
    if you ==False:
        await chanid[guildid].send("制限モードでは検索機能は使えません。TOKEN.txtのYoutube_API_KEYにyoutube v3 APIのkeyを入力してください。")
        return
    titl = []
    videde = []
    sss = aft
    ff = func_youtube.youtubeop(5,sss)
    videde = list(ff[0])
    titl = list(ff[1])
      #youtube_url = f"https://www.youtube.com/watch?v={videde}"

    if voiceid == None:
            await chanid[guildid].send("ボイスチャットに参加してください。")
            return
    elif voice[guildid] == None:
            voice[guildid] = await message.author.voice.channel.connect(reconnect = True)
            chanid[guildid] = bot.get_channel(message.channel.id)
            vcid[guildid] = message.author.voice.channel.id
            channelid[guildid] = message.channel.id
            print(channelid)
            print(channelid[guildid])
    elif vcid[guildid] != message.author.voice.channel.id:
            await voice[guildid].move_to(message.author.voice.channel)
            vcid[guildid] = message.author.voice.channel.id

    count_music = 1
    if print_title[guildid] == 0:
            for spt in videde:
              await chanid[guildid].send(str(count_music)+": https://www.youtube.com/watch?v="+spt)
              count_music = count_music + 1
              if count_music == len(videde) + 1:
                break
    elif print_title[guildid] == 1:
            for spt in titl:
              await chanid[guildid].send(str(count_music)+": "+spt)
              count_music = count_music + 1
              if count_music == len(titl) + 1:
                break
    await chanid[guildid].send("流したい曲の番号を送信してください(.無し)")
    elect = 1
    #enqueue(voice[guildid],youtube_url)


@bot.command()
async def sc(message,*,aft):#検索する。動画idを取得して、youtubeのURLの後にくっつけてるだけ
    global guildid
    guildid = message.guild.id
    print(guildid)
    voiceid = message.author.voice
    global chanid,voice,queue_dict,vcid,sss,elect,videde,titl,channelid,print_title
    looping.setdefault(guildid,0)
    qloo.setdefault(guildid,0)
    print_title.setdefault(guildid,0)
    voice.setdefault(guildid,None)
    chanid[guildid] = bot.get_channel(message.channel.id)
    if you ==False:
        await chanid[guildid].send("制限モードでは検索機能は使えません。TOKEN.txtのYoutube_API_KEYにyoutube v3 APIのkeyを入力してください。")
        return
    titl = []
    videde = []
    sss = aft
    ff = func_youtube.youtubeop(5,sss)
    videde = list(ff[0])
    titl = list(ff[1])
      #youtube_url = f"https://www.youtube.com/watch?v={videde}"

    if voiceid == None:
            await chanid[guildid].send("ボイスチャットに参加してください。")
            return
    elif voice[guildid] == None:
            voice[guildid] = await message.author.voice.channel.connect(reconnect = True)
            chanid[guildid] = bot.get_channel(message.channel.id)
            vcid[guildid] = message.author.voice.channel.id
            channelid[guildid] = message.channel.id
            print(channelid)
            print(channelid[guildid])
    elif vcid[guildid] != message.author.voice.channel.id:
            await voice[guildid].move_to(message.author.voice.channel)
            vcid[guildid] = message.author.voice.channel.id

    count_music = 1
    if print_title[guildid] == 0:
            for spt in videde:
              await chanid[guildid].send(str(count_music)+": https://www.youtube.com/watch?v="+spt)
              count_music = count_music + 1
              if count_music == len(videde) + 1:
                break
    elif print_title[guildid] == 1:
            for spt in titl:
              await chanid[guildid].send(str(count_music)+": "+spt)
              count_music = count_music + 1
              if count_music == len(titl) + 1:
                break
    await chanid[guildid].send("流したい曲の番号を送信してください(.無し)")
    elect = 1
    #enqueue(voice[guildid],youtube_url)

@bot.command()
async def play_one_song(message,*,aft):#1曲のみ検索する 動作速度を優先した感じ
    global guildid
    guildid = message.guild.id
    print(guildid)
    voiceid = message.author.voice
    global chanid,voice,queue_dict,vcid,sss,elect,videde,titl,channelid
    looping.setdefault(guildid,0)
    qloo.setdefault(guildid,0)
    print_title.setdefault(guildid,0)
    voice.setdefault(guildid,None)
    chanid[guildid] = bot.get_channel(message.channel.id)
    if you ==False:
        await chanid[guildid].send("制限モードでは検索機能は使えません。TOKEN.txtのYoutube_API_KEYにyoutube v3 APIのkeyを入力してください。")
        return

    if aft[:8] == "https://":
        await chanid[guildid].send("URLではこの機能は使えません")
    else:
        videde =[]
        titl = []
        ff = func_youtube.youtubeop(1,aft)
        videde = list(ff[0])
        titl = list(ff[1])
        #youtube_url = f"https://www.youtube.com/watch?v={videde}"
        if voiceid == None:
            await chanid[guildid].send("ボイスチャットに参加してください。")
            return
        elif voice[guildid] == None:
            voice[guildid] = await message.author.voice.channel.connect(reconnect = True)
            chanid[guildid] = bot.get_channel(message.channel.id)
            vcid[guildid] = message.author.voice.channel.id
            channelid[guildid] = message.channel.id
            print(channelid)
            print(channelid[guildid])
        elif vcid[guildid] != message.author.voice.channel.id:
            await voice[guildid].move_to(message.author.voice.channel)
            vcid[guildid] = message.author.voice.channel.id
        
        videid = videde[0]
        q = f"https://www.youtube.com/watch?v={videid}"
        async with chanid[guildid].typing():
          await asyncio.sleep(0.5)
          await chanid[guildid].send("キューに追加: "+q)
        enqueue(voice[guildid],q)    

@bot.command()
async def pos(message,*,aft):#1曲のみ検索する 動作速度を優先した感じ
    global guildid
    guildid = message.guild.id
    print(guildid)
    global chanid,voice,queue_dict,vcid,sss,elect,videde,titl,channelid,looping,qloo
    looping.setdefault(guildid,0)
    qloo.setdefault(guildid,0)
    print_title.setdefault(guildid,0)
    voice.setdefault(guildid,None)
    print(qloo[guildid])  
    if you ==False:
        await chanid[guildid].send("制限モードでは検索機能は使えません。TOKEN.txtのYoutube_API_KEYにyoutube v3 APIのkeyを入力してください。")
        return

    if aft[:8] == "https://":
        await chanid[guildid].send("URLではこの機能は使えません")
    else:
        voiceid = message.author.voice
        if voiceid == None:
            await chanid[guildid].send("ボイスチャットに参加してください。")
            return
        elif voice[guildid] == None:
            voice[guildid] = await message.author.voice.channel.connect(reconnect = True)
            chanid[guildid] = bot.get_channel(message.channel.id)
            vcid[guildid] = message.author.voice.channel.id
            channelid[guildid] = message.channel.id
            print(channelid)
            print(channelid[guildid])
        elif vcid[guildid] != message.author.voice.channel.id:
            await voice[guildid].move_to(message.author.voice.channel)
            vcid[guildid] = message.author.voice.channel.id
        videde =[]
        titl = []
        ff = func_youtube.youtubeop(1,aft)
        videde = list(ff[0])
        titl = list(ff[1])
        #youtube_url = f"https://www.youtube.com/watch?v={videde}"

        
        videid = videde[0]
        q = f"https://www.youtube.com/watch?v={videid}"
        enqueue(voice[guildid],q) 
        async with chanid[guildid].typing():
          await asyncio.sleep(0.5)
          await chanid[guildid].send("キューに追加: "+q)
       

@bot.command()
async def play(message,*,aft):#指定されたURLの曲を流す。
    global guildid
    guildid = message.guild.id
    print(guildid)
    voiceid = message.author.voice
    global chanid,voice,queue_dict,vcid,sss,elect,videde,titl,channelid,print_title
    print("aft:"+aft)
    looping.setdefault(guildid,0)
    qloo.setdefault(guildid,0)
    print_title.setdefault(guildid,0)
    voice.setdefault(guildid,None)
    #idx = msg.find(" ")
    chanid[guildid] = bot.get_channel(message.channel.id)
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
                queue_dict[guildid].append("https://www.youtube.com/watch?v="+ten[13:24])
              print(queue_dict)

              if voiceid == None:
                await chanid[guildid].send("ボイスチャットに参加してください。")
                return
              elif voice[guildid] == None:
                voice[guildid] = await message.author.voice.channel.connect(reconnect = True)
                chanid[guildid] = bot.get_channel(message.channel.id)
                vcid[guildid] = message.author.voice.channel.id
                channelid[guildid] = message.channel.id
                print(channelid)
                print(channelid[guildid])
              elif vcid[guildid] != message.author.voice.channel.id:
                await voice[guildid].move_to(message.author.voice.channel)
                vcid[guildid] = message.author.voice.channel.id
              ytl(queue_dict[guildid])
              async with chanid[guildid].typing():
                await asyncio.sleep(0.5)
                await chanid[guildid].send("playlistを追加しました。")

            else: #曲のURLがそのままのとき
                if voiceid == None:
                  await chanid[guildid].send("ボイスチャットに参加してください。")
                  return
                elif voice[guildid] == None:
                  voice[guildid] = await message.author.voice.channel.connect(reconnect = True)
                  chanid[guildid] = bot.get_channel(message.channel.id)
                  vcid[guildid] = message.author.voice.channel.id
                  channelid[guildid] = message.channel.id
                  print(channelid)
                  print(channelid[guildid])
                elif vcid[guildid] != message.author.voice.channel.id:
                  await voice[guildid].move_to(message.author.voice.channel)
                  vcid[guildid] = message.author.voice.channel.id

                enqueue(voice[guildid],youtube_url)
                async with chanid[guildid].typing():
                 await asyncio.sleep(0.5)
                await chanid[guildid].send("正常に追加されました。")

    else: #URLじゃなかったんだね...
          if you ==False:
            await message.channel.send("制限モードでは検索機能は使えません。TOKEN.txtのYoutube_API_KEYにyoutube v3 APIのkeyを入力してください。")
            return
          videde =[]
          titl = []
          sss = aft
          ff = func_youtube.youtubeop(5,sss)
          videde = list(ff[0])
          titl = list(ff[1])
          
         #youtube_url = f"https://www.youtube.com/watch?v={videde}"
          if voiceid == None:
            await chanid[guildid].send("ボイスチャットに参加してください。")
            return
          elif voice[guildid] == None:
            voice[guildid] = await message.author.voice.channel.connect(reconnect = True)
            chanid[guildid] = bot.get_channel(message.channel.id)
            vcid[guildid] = message.author.voice.channel.id
            channelid[guildid] = message.channel.id
            print(channelid)
            print(channelid[guildid])
          elif vcid[guildid] != message.author.voice.channel.id:
            await voice[guildid].move_to(message.author.voice.channel)
            vcid[guildid] = message.author.voice.channel.id

          count_music = 1
          if print_title[guildid] == 0: #候補を5個並べる。選択の部分はまた別な場所(上の方にある)
            for spt in videde:
              await chanid[guildid].send(str(count_music)+": https://www.youtube.com/watch?v="+spt)
              count_music = count_music + 1
              if count_music == len(videde) + 1:
                break
          elif print_title[guildid] == 1:
            for spt in titl:
              await chanid[guildid].send(str(count_music)+": "+spt)
              count_music = count_music + 1
              if count_music == len(titl) + 1:
                break
          await chanid[guildid].send("流したい曲の番号を送信してください(.無し)") #動作速度を早めるためにはどうすればええんや...
          elect = 1
          #enqueue(voice[guildid],youtube_url)

@bot.command()
async def p(message,*,aft):#指定されたURLの曲を流す。
  global guildid
  guildid = message.guild.id
  print(guildid)
  voiceid = message.author.voice
  global chanid,voice,queue_dict,vcid,sss,elect,videde,titl,channelid,qloo,looping,print_title
  print("aft:"+aft)
  looping.setdefault(guildid,0)
  qloo.setdefault(guildid,0)
  print_title.setdefault(guildid,0)
  voice.setdefault(guildid,None)
  chanid[guildid] = bot.get_channel(message.channel.id)
  #idx = msg.find(" ")
  #chanid = bot.get_channel(message.channel.id)
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
                queue_dict[guildid].append("https://www.youtube.com/watch?v="+ten[13:24])
              print(queue_dict)

              if voiceid == None:
                await chanid[guildid].send("ボイスチャットに参加してください。")
                return
              elif voice[guildid] == None:
                voice[guildid] = await message.author.voice.channel.connect(reconnect = True)
                chanid[guildid] = bot.get_channel(message.channel.id)
                vcid[guildid] = message.author.voice.channel.id
                channelid[guildid] = message.channel.id
                print(channelid)
                print(channelid[guildid])
              elif vcid[guildid] != message.author.voice.channel.id:
                await voice[guildid].move_to(message.author.voice.channel)
                vcid[guildid] = message.author.voice.channel.id

              ytl(queue_dict[guildid])
              async with chanid[guildid].typing():
                await asyncio.sleep(0.5)
                await chanid[guildid].send("playlistを追加しました。")

            else: #曲のURLがそのままのとき
                if voiceid == None:
                  await chanid[guildid].send("ボイスチャットに参加してください。")
                  return
                elif voice[guildid] == None:
                  voice[guildid] = await message.author.voice.channel.connect(reconnect = True)
                  chanid[guildid] = bot.get_channel(message.channel.id)
                  vcid[guildid] = message.author.voice.channel.id
                  channelid[guildid] = message.channel.id
                  print(channelid)
                  print(channelid[guildid])
                elif vcid[guildid] != message.author.voice.channel.id:
                  await voice[guildid].move_to(message.author.voice.channel)
                  vcid[guildid] = message.author.voice.channel.id

                enqueue(voice[guildid],youtube_url)
                async with chanid[guildid].typing():
                 await asyncio.sleep(0.5)
                await chanid[guildid].send("正常に追加されました。")

  else: #URLじゃなかったんだね...
          if you ==False:
            await chanid[guildid].send("制限モードでは検索機能は使えません。TOKEN.txtのYoutube_API_KEYにyoutube v3 APIのkeyを入力してください。")
            return
          videde =[]
          titl = []
          sss = aft
          ff = func_youtube.youtubeop(5,sss)
          videde = list(ff[0])
          titl = list(ff[1])
         #youtube_url = f"https://www.youtube.com/watch?v={videde}"
          if voiceid == None:
            await chanid[guildid].send("ボイスチャットに参加してください。")
            return
          elif voice[guildid] == None:
            voice[guildid] = await message.author.voice.channel.connect(reconnect = True)
            chanid[guildid] = bot.get_channel(message.channel.id)
            vcid[guildid] = message.author.voice.channel.id
            channelid[guildid] = message.channel.id
            print(channelid)
            print(channelid[guildid])
          elif vcid[guildid] != message.author.voice.channel.id:
            await voice[guildid].move_to(message.author.voice.channel)
            vcid[guildid] = message.author.voice.channel.id
            

          count_music = 1
          if print_title[guildid] == 0: #候補を5個並べる。選択の部分はまた別な場所(上の方にある)
            for spt in videde:
              await chanid[guildid].send(str(count_music)+": https://www.youtube.com/watch?v="+spt)
              count_music = count_music + 1
              if count_music == len(videde) + 1:
                break
          elif print_title[guildid] == 1:
            for spt in titl:
              await chanid[guildid].send(str(count_music)+": "+spt)
              count_music = count_music + 1
              if count_music == len(titl) + 1:
                break
          await chanid[guildid].send("流したい曲の番号を送信してください(.無し)") #動作速度を早めるためにはどうすればええんや...
          elect = 1
          #enqueue(voice[guildid],youtube_url)

if __name__ == '__main__': #起動
  bot.run(TOKEN)

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