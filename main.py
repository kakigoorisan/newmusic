import pafy
from discord import FFmpegPCMAudio
import discord
from discord.ext import commands
from discord import player
import os
import asyncio
from asyncio import run
import random
#import slash_seat
from oauth2client.tools import argparser
import func_youtube as fy

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
youtube_url = ""
voice = {}
playerr = None
url = 0
qloo = {}
looping = {}
ended = 0
queue_dict = {}
t = 0
videde = {}
titl = {}
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
error_count = 0
error_check = False
play_queue = {}
#devkeyの有無
if DEVELOPER_KEY == "no":
  you = False

#キューの設定
async def enqueue(voice_client, youtube_ur):
    global queue_dict,guildid,play_queue
    guildid = voice_client.guild.id 
    play_queue.setdefault(guildid,[]).append(youtube_ur)
    queue_dict.setdefault(guildid,{})
    queue_dict[guildid].setdefault(youtube_ur,[])
    id_temp = youtube_ur.split("=")
    ids = id_temp[1]
    title_thum = await fy.youtube_title(ids,guildid)
    queue_dict[guildid][youtube_ur] = title_thum
    print(play_queue)
    print(queue_dict)
    
    if not voice_client.is_playing():
        await ytl(play_queue,guildid)
    else:
      return

#URLでyoutubeに飛んで、再生。
async def ytl(que,guildid):
  global voice,t,ended,titl,meme,looping,loopingskip,videde,videid,error_count,chanid,error_check
  ai = que[guildid][0]
  videid = ai
  try:
    song = pafy.new(videid) #pafyに引数を渡す
    audio= song.getbestaudio()  
    source= FFmpegPCMAudio(audio.url, **FFMPEG_OPTIONS)  
    voice[guildid].play(source,after= lambda e : run(ende(que,guildid,ai))) #流す 
  except:
    error_count = error_count + 1
    if error_count <= 5:
      print(error_count)
      await ytl(que,guildid)
    elif error_count >= 6:
      error_check = True
      await chanid[guildid].send("エラーが発生しました。")
      print("I have too many ERRORs! Please check the code!")
      await ende(que,guildid)

#終了後にqueueの先頭を削除
async def ende(queu,guildid,sen):
  print("done")
  global ended,qloo,looping,chanid,error_count,queue_dict
  error_count = 0
  print(queu[guildid])
  if qloo[guildid] == 0 and looping[guildid] == 0:
    if len(queu[guildid]) >= 2: 
      del queu[guildid][0]
      if sen not in queu[guildid]:
        del queue_dict[guildid][sen]
      await ytl(queu,guildid)
    elif len(queu[guildid]) == 1:
      del queu[guildid][0]
      if sen not in queu[guildid]:
        del queue_dict[guildid][sen]
      print(queue_dict[guildid])
      print(queu[guildid])
      return
    else:
      return

  elif qloo[guildid] == 1 and looping[guildid] == 0:
    queu[guildid].append(queu[guildid][0])
    del queu[guildid][0]
    print(queu[guildid])
    if len(queu[guildid]) >= 1 :
        await ytl(queu,guildid)
  elif looping[guildid] == 1:
    await ytl(queu,guildid)
  else:
    return

async def random_choice(num,len_word):
  print(num)
  ranran =[]
  for i in range(num):
    ran = random.randint(0,len_word-1)
    print("random:"+str(ran))
    ranran.append(ran)
  print(ranran)
  return ranran
  
async def random_tips():
  ran = random.randint(0,10)
  return (ran)
#ここからdiscord

#コマンドの接頭辞を設定
bot = commands.Bot(command_prefix='.',intents=intents)
@bot.event #起動が完了するとコンソールにhiと送り、プレイ中の表示をさせる
async def on_ready():
  global you,voice,looping,qloo,print_title,play_queue,queue_dict
  async for guild in bot.fetch_guilds(limit=150):
    print(guild.id)
    voice.setdefault(guildid, None)
    looping.setdefault(guildid, 0)
    qloo.setdefault(guildid, 0)
    print_title.setdefault(guildid, 0)
    play_queue.setdefault(guildid, [])
    queue_dict.setdefault(guildid, {})

  print("hi")
  await bot.change_presence(activity=discord.Game(name="hi", type=1))
  await asyncio.sleep(5)
  await bot.change_presence(activity=discord.Game(name="I'm listening to music!!", type=1))
  if you == False:
    print("制限モードがonになっています。解除するにはTOKEN.txtのYoutube_API_KEYにYoutube v3 APIのkeyを入力してください。")

@bot.event
async def on_voice_state_update(member, before, after):
  global voice,player,youtube_url,url,sss,argparser,videde,queue_dict,play_queue,ended,qloo,looping,titl,elect,meme,print_title,queue_title,count_music,loopingskip,videid,chanid,vcid

  if before.channel != None and vcid != {}:
    befoguild = {}
    guildid = before.channel.guild.id
    befoguild[guildid] = before.channel.id
    keycheck = guildid in voice
    if keycheck == True and voice[guildid] != None and before.channel != None:
      if befoguild[guildid] == vcid[guildid]:
        print("抜けた")
        name = voice[guildid].channel.members
        if len(name) == 1:
          print(name)
          qloo[guildid] = 0
          looping[guildid] = 0
          queue_dict[guildid].clear()
          play_queue[guildid].clear()
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
    global channelid,voice,player,youtube_url,url,sss,argparser,videde,queue_dict,play_queue,ended,qloo,looping,titl,elect,meme,print_title,queue_title,count_music,loopingskip,videid,chanid,vcid,you
    guildid = message.guild.id
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
          print(inmsg)
          print(count_music)
          if inmsg <= count_music:
              videid = videde[guildid][inmsg-1]
              q = f"https://www.youtube.com/watch?v={videid}"
              await enqueue(voice[guildid] ,q)
              async with chanid[guildid].typing():
                await asyncio.sleep(0.5)
                if print_title[guildid] == 0:
                  await chanid[guildid].send("キューに追加: "+titl[guildid][inmsg-1])
                elif print_title[guildid] == 1:
                  await chanid[guildid].send("キューに追加: "+q)
          videde[guildid] = []
          titl[guildid] = []
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
    global queue_dict,guildid,chanid,play_queue
    guildid = message.guild.id
    async with chanid[guildid].typing():
        await asyncio.sleep(1)
        await chanid[guildid].send("キューをリセットしました.")
    queue_dict[guildid] = {}
    play_queue[guildid] = []
    ff = await random_tips()
    ran = ff
    if ran == 1:
      await chanid[guildid].send("Tips: .clでもキューをクリアできます")
    

@bot.command()
async def pause(message):
  global voice,guildid
  guildid = message.guild.id
  if voice[guildid].is_paused() == False:
    await message.channel.send("曲を一時停止します")
    voice[guildid].pause()
  elif voice[guildid].is_paused() == True:
    await message.channel.send("曲を再生します")
    voice[guildid].resume()


@bot.command()
async def cl(message):
    global queue_dict,guildid,chanid,play_queue
    guildid = message.guild.id
    async with chanid[guildid].typing():
        await asyncio.sleep(1)
        await chanid[guildid].send("キューをリセットしました.")
    queue_dict[guildid] = {}
    play_queue[guildid] = []


@bot.command()
async def remove(message, aft): #キューの中の曲を削除
    global queue_dict,guildid,chanid,play_queue
    guildid = message.guild.id
    if aft.isdecimal() == False:
        return
    if aft == "1":
        await chanid[guildid].send("現在再生している曲です")
      
    elif int(aft) > len(play_queue[guildid]):
        await chanid[guildid].send("範囲外です")
        return
    else:
        remint = int(aft) - 1
        temp = play_queue[guildid][remint]
        del queue_dict[guildid][temp]
        del play_queue[guildid][remint]
        await chanid[guildid].send(temp + " を削除しました")
        print(queue_dict)
        print(play_queue)

@bot.command()
async def info(message):#botの情報
    global chanid,guildid
    guildid = message.guild.id
    await message.channel.send("This bot was made by kakigoori(2021-2023) \n\n If you would like to listen to music, you should use this bot. \n\n This bot is often happened to occur an error or to slow down download.")

bot.remove_command('help')

@bot.command()
async def help(message):#botのコマンド
    global chanid,guildid
    guildid = message.guild.id
    await message.channel.send("**.play(.p)のように括弧されているコマンドは短縮コマンドとして利用できるものです。**```\n.help :このメッセージを表示します。\n.play(.p) <URL>,<word> :URLでその曲、wordで検索して、流します。\n.sc <word> :wordをyoutube検索して、5個の候補を表示します。\n.queue(.q) :キューの中身を表示します(ログが流れます)。\n.shuflle(.shl) :キューの中身をシャッフルします。\n.pause :流れている曲を一時停止します。\n.skip(.s) :流れている曲をスキップします。\n.clear(.cl) :キューをリセットします。\n.dc :botをvcから切断させます。\n.move :vcを移動させます。\n.queueloop(.qlp) :キューをループさせます。\n.loop(.lp) :一曲のみをループします。\n remove <キュー番号> :キューの特定の位置の曲をキューから削除します。 \n.pr_title :検索時にタイトルのみを表示します。(現在使えません)\n.info :botの情報を表示します\n.lpinfo :loopの状況のみを表示します\n.skipto(.skt) :指定したキューの場所までスキップします\n.pos :1曲のみ検索して、再生します\n.rap [数字] :数字で指定した数だけ検索ワードリストから言葉を持ってきます\n.racom :おすすめの曲リストからランダムに1曲再生します。\n.adw [言葉] :検索ワードリストに言葉を登録します\n.playlist(.pl) [URL] :URLで指定されたプレイリストを再生します。このコマンドではプレイリストの任意の曲のURLを指定した場合もプレイリストとして判断されます。\n```")


@bot.command()
async def dc(message):
    global queue_dict,qloo,looping,voice,guildid,chanid,play_queue#切断
    guildid = message.guild.id
    chanid[guildid] = bot.get_channel(message.channel.id)
    qloo[guildid] = 0
    looping[guildid] = 0
    queue_dict[guildid].clear()
    play_queue.clear()
    if voice[guildid].is_playing():
        voice[guildid].stop()

    #guild = message.guild.voice_client
    await voice[guildid].disconnect()
    #guild = message.guild.voice_client          
    async with chanid[guildid].typing():
        await asyncio.sleep(0.7)
        await chanid[guildid].send("good bye!")
    del voice[guildid] 
    del chanid[guildid]
        
@bot.command()
async def join(message):
  global voice,guildid,queue_dict,play_queue
  voiceid = message.author.voice
  guildid = message.guild.id
  voice.setdefault(guildid,None)
  if voice[guildid] == None:
                            voice[guildid] = await message.author.voice.channel.connect(reconnect = True)
                            chanid[guildid] = bot.get_channel(message.channel.id)
                            vcid[guildid] = message.author.voice.channel.id
                            channelid[guildid] = message.channel.id
                            queue_dict.setdefault(guildid,{})
                            play_queue.setdefault(guildid,[])
                            print(channelid)
                            print(channelid[guildid])
  elif vcid[guildid] != message.author.voice.channel.id:
                  await voice[guildid].move_to(message.author.voice.channel)
                  vcid[guildid] = message.author.voice.channel.id
  elif voiceid == None:
              await message.channel.send("ボイスチャットに参加してください")
              return

    #if bef == ".q_title": #キューの表示時にタイトルのみ表示させたいけど、なかなか厳しいものがある
     # if queue_title == 0:
      #  queue_title = 1
      #  await message.channel.send("キューの表示時にタイトルのみ表示します。")
      #elif queue_title == 1:
      #  queue_title  = 0
      #  await message.channel.send("キューの表示時にURLも表示します。")

@bot.command()
async def queue(message):#キューの中身を表示させる。
    global queue_dict, qloo, looping, chanid, guildid
    guildid = message.guild.id
    avatar = message.author.avatar
    # if queue_title == 0:
    count_music = 1
    channels = chanid[guildid]
    loop_info = looping[guildid]
    qlp_info = qloo[guildid]
    queue_info = play_queue[guildid]
    embed = discord.Embed(
        title="Queue", description="現在のQueueの内容", color=discord.Colour.red())

    embed.set_thumbnail(url=queue_dict[guildid][play_queue[guildid][0]][1])
    qlp_icon = ""
    loop_icon = ""
    if qlp_info == 1:
        qlp_icon = "queueloop: \N{Heavy Large Circle}"
    elif qlp_info == 0:
        qlp_icon = "queueloop: \N{Cross Mark}"
    if loop_info == 1:
        loop_icon = "loop: \N{Heavy Large Circle}"
    if loop_info == 0:
        loop_icon = "loop: \N{Cross Mark}"
    embed.set_footer(
        text=f"Generated by {message.author.name}                                                                                    {loop_icon} | {qlp_icon}", icon_url=avatar)
    print(f"aaaa{embed.footer}")
    if len(queue_info) <= 25:
      for spt in queue_info:
          embed.add_field(
              name=f"`{count_music}` {queue_dict[guildid][spt][0]}", value=f"( {spt} )", inline=False)
          count_music = count_music + 1
      await channels.send(embed=embed)
    elif len(queue_info) > 25:
      s = 0
      for content in queue_info:
          info_temp = queue_info[s:s+25:1]
          print(info_temp)

          for spt in info_temp:
            embed.add_field(
                name=f"`{count_music}` {queue_dict[guildid][spt][0]}", value=f"( {spt} )", inline=False)
            count_music = count_music + 1
          if s >= len(queue_info):
            break

          await channels.send(embed=embed)
          embed.clear_fields()
          s = s + 25
    ff = await random_tips()
    ran = ff
    if ran == 1:
      await chanid[guildid].send("Tips: .qでもキューを表示できます")


@bot.command()
async def q(message):  # キューの中身を表示させる。
    global queue_dict, qloo, looping, chanid, guildid
    guildid = message.guild.id
    avatar = message.author.avatar
    # if queue_title == 0:
    count_music = 1
    channels = chanid[guildid]
    loop_info = looping[guildid]
    qlp_info = qloo[guildid]
    queue_info = play_queue[guildid]
    embed = discord.Embed(title="Queue", description="現在のQueueの内容",color=discord.Colour.red())
    
    embed.set_thumbnail(url=queue_dict[guildid][play_queue[guildid][0]][1])
    qlp_icon = ""
    loop_icon = ""
    if qlp_info == 1:
              qlp_icon = "queueloop: \N{Heavy Large Circle}"
    elif qlp_info == 0:
              qlp_icon = "queueloop: \N{Cross Mark}"
    if loop_info == 1:
              loop_icon = "loop: \N{Heavy Large Circle}"
    if loop_info == 0:
              loop_icon = "loop: \N{Cross Mark}" 
    embed.set_footer(text=f"Generated by {message.author.name}                                                                                    {loop_icon} | {qlp_icon}",icon_url=avatar)
    print(f"aaaa{embed.footer}")
    if len(queue_info) <= 25:
      for spt in queue_info:
          embed.add_field(name=f"`{count_music}` {queue_dict[guildid][spt][0]}", value=f"( {spt} )",inline=False)
          count_music = count_music + 1
      await channels.send(embed=embed)
    elif len(queue_info) > 25:
      s = 0
      for content in queue_info:
          info_temp = queue_info[s:s+25:1]
          print(info_temp)

          for spt in info_temp:
            embed.add_field(name=f"`{count_music}` {queue_dict[guildid][spt][0]}",value= f"( {spt} )",inline=False)
            count_music = count_music + 1
          if s >= len(queue_info):
            break

          await channels.send(embed=embed)
          embed.clear_fields()
          s = s + 25


@bot.command()
async def shuffle(message):
  global voice, queue_dict, play_queue, guildid, chanid
  guildid = message.guild.id
  await chanid[guildid].send("キューをシャッフルします")
  temp = play_queue[guildid][0]
  del play_queue[guildid][0]
  random.shuffle(play_queue[guildid])
  play_queue[guildid].insert(0, temp)
  print(play_queue)

@bot.command()
async def shl(message):
  global voice,queue_dict,play_queue,guildid,chanid
  guildid = message.guild.id
  await chanid[guildid].send("キューをシャッフルします")
  temp = play_queue[guildid][0]
  del play_queue[guildid][0]
  random.shuffle(play_queue[guildid])
  play_queue[guildid].insert(0,temp)
  print(play_queue)

@bot.command()
async def skip(message):#流れている曲をスキップ。stopするだけで、曲が終了したときの処理が起こる
    global voice,queue_dict,guildid,chanid,play_queue
    guildid = message.guild.id
    voice[guildid].stop()
    if len(play_queue[guildid]) > 1:
     await chanid[guildid].send("再生: " + play_queue[guildid][1])
    ff = await random_tips()
    ran = ff
    if ran == 1:
      await chanid[guildid].send("Tips: .sでもスキップできます")

@bot.command()
async def s(message):#流れている曲をスキップ。stopするだけで、曲が終了したときの処理が起こる
    global voice,queue_dict,guildid,chanid,play_queue
    guildid = message.guild.id
    voice[guildid].stop()
    if len(play_queue[guildid]) > 1:
     await chanid[guildid].send("再生: " + play_queue[guildid][1])

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
    ff = await random_tips()
    ran = ff
    if ran == 1:
      await chanid[guildid].send("Tips: .lpでもループできます")

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
    ff = await random_tips()
    ran = ff
    if ran == 1:
      await chanid[guildid].send("Tips: .qlpでもキューループできます")

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
        await chanid[guildid].send("queueloop: \N{Heavy Large Circle}")
    elif qloo[guildid] == 0:
        await chanid[guildid].send("queueloop: \N{Cross Mark}")
    if looping[guildid] == 1:
        await chanid[guildid].send("loop: \N{Heavy Large Circle}")
    elif looping[guildid] == 0:
        await chanid[guildid].send("loop: \N{Cross Mark}")


@bot.command()
async def skipto(message,aft):#指定した曲を再生する
    global queue_dict,voice,guildid,chanid,play_queue
    guildid = message.guild.id
    if aft.isdecimal() == False:
        return
    elif aft == "1":
        await chanid[guildid].send("現在再生している曲です")
    elif int(aft) > len(play_queue[guildid]):
        await chanid[guildid].send("範囲外です") #範囲外か判断する
    else:
        num = int(aft) -1
        poping = int(aft)
        play_queue[guildid].insert(1,play_queue[guildid][num])
        del play_queue[guildid][poping]
        voice[guildid].stop()
        await chanid[guildid].send("再生: " + play_queue[guildid][1])
    ff = await random_tips()
    ran = ff
    if ran == 1:
      await chanid[guildid].send("Tips: .sktでもskip toできます")

@bot.command()
async def skt(message,aft):#指定した曲を再生する
    global queue_dict, voice, guildid, chanid, play_queue
    guildid = message.guild.id
    if aft.isdecimal() == False:
        return
    elif aft == "1":
        await chanid[guildid].send("現在再生している曲です")
    elif int(aft) > len(play_queue[guildid]):
        await chanid[guildid].send("範囲外です")  # 範囲外か判断する
    else:
        num = int(aft) - 1
        poping = int(aft)
        play_queue[guildid].insert(1, play_queue[guildid][num])
        del play_queue[guildid][poping]
        voice[guildid].stop()
        await chanid[guildid].send("再生: " + play_queue[guildid][1])


@bot.command()
async def random_recommend(message): #おすすめリストからランダムに1つURLを持ってくる
    global guildid
    guildid = message.guild.id
    print(guildid)
    voiceid = message.author.voice
    global chanid,voice,queue_dict,vcid,sss,elect,videde,titl,channelid,play_queue
    chanid = bot.get_channel(message.channel.id)
    looping.setdefault(guildid,0)
    qloo.setdefault(guildid,0)
    voice.setdefault(guildid,None)
    print_title.setdefault(guildid,0)   
    nn = os.path.dirname(os.path.abspath(__file__))
    f = open(f'{nn}/recommend.txt', "r")
    url_list = f.readlines()
    len_url = len(url_list)
    if len_url < 0:
        await message.channel.send("おすすめリストがありません")
    elif len_url >= 1:
        if voice[guildid] == None and voiceid != None:
                                    voice[guildid] = await message.author.voice.channel.connect(reconnect = True)
                                    chanid[guildid] = bot.get_channel(message.channel.id)
                                    vcid[guildid] = message.author.voice.channel.id
                                    channelid[guildid] = message.channel.id
                                    print(channelid)
                                    print(channelid[guildid])
        elif voiceid == None:
                      await message.channel.send("ボイスチャットに参加してください")
                      return
        elif vcid[guildid] != message.author.voice.channel.id:
                          await voice[guildid].move_to(message.author.voice.channel)
                          vcid[guildid] = message.author.voice.channel.id
        figure = await random_choice(1,len_url)
        q = url_list[figure[0]]
        await enqueue(voice[guildid],q)
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
    global chanid,voice,queue_dict,vcid,sss,elect,videde,titl,channelid,play_queue
    chanid = bot.get_channel(message.channel.id)
    looping.setdefault(guildid,0)
    qloo.setdefault(guildid,0)
    voice.setdefault(guildid,None)
    print_title.setdefault(guildid,0)   
    nn = os.path.dirname(os.path.abspath(__file__))
    f = open(f'{nn}/recommend.txt', "r")
    url_list = f.readlines()
    len_url = len(url_list)
    if len_url < 0:
        await message.channel.send("おすすめリストがありません")
    elif len_url >= 1:
        if voice[guildid] == None and voiceid != None:
                                    voice[guildid] = await message.author.voice.channel.connect(reconnect = True)
                                    chanid[guildid] = bot.get_channel(message.channel.id)
                                    vcid[guildid] = message.author.voice.channel.id
                                    channelid[guildid] = message.channel.id
                                    print(channelid)
                                    print(channelid[guildid])
        elif voiceid == None:
                      await message.channel.send("ボイスチャットに参加してください")
                      return
        elif vcid[guildid] != message.author.voice.channel.id:
                          await voice[guildid].move_to(message.author.voice.channel)
                          vcid[guildid] = message.author.voice.channel.id
        figure = await random_choice(1,len_url)
        q = url_list[figure[0]]
        await enqueue(voice[guildid],q)
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
    global chanid,voice,queue_dict,vcid,sss,elect,videde,titl,channelid,play_queue
    if you ==False:
        await message.channel.send("制限モードでは検索機能は使えません。TOKEN.txtのYoutube_API_KEYにyoutube v3 APIのkeyを入力してください。")
        return
    chanid = bot.get_channel(message.channel.id)
    looping.setdefault(guildid,0)
    qloo.setdefault(guildid,0)
    voice.setdefault(guildid,None)
    print_title.setdefault(guildid,0)    
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
        videde[guildid] = []
        words = []
        figure = await random_choice(int(aft),len_word)       
        for i in range(int(aft)):
          words.append(word_list[figure[i]])
        sss = (' '.join(words))
        ff =await fy.youtubeop(1,sss,guildid)
        videde[guildid] = list(ff[0])
        titl[guildid] = list(ff[1])
        if voice[guildid] == None and voiceid != None:
                                    voice[guildid] = await message.author.voice.channel.connect(reconnect = True)
                                    chanid[guildid] = bot.get_channel(message.channel.id)
                                    vcid[guildid] = message.author.voice.channel.id
                                    channelid[guildid] = message.channel.id
                                    print(channelid)
                                    print(channelid[guildid])
        elif voiceid == None:
                      await message.channel.send("ボイスチャットに参加してください")
                      return
        elif vcid[guildid] != message.author.voice.channel.id:
                          await voice[guildid].move_to(message.author.voice.channel)
                          vcid[guildid] = message.author.voice.channel.id
        
        videid = videde[guildid][0]
        q = f"https://www.youtube.com/watch?v={videid}"
        
        async with message.channel.typing():
          await asyncio.sleep(0.5)
          await message.channel.send("キューに追加: "+q)
        await enqueue(voice[guildid],q)
    f.close()

@bot.command()
async def rap(message,aft):#検索ワードリストから指定した数言葉を持ってくる
    global guildid
    guildid = message.guild.id
    print(guildid)
    voiceid = message.author.voice
    global chanid,voice,queue_dict,vcid,sss,elect,videde,titl,channelid,play_queue
    chanid[guildid] = bot.get_channel(message.channel.id)
    looping.setdefault(guildid,0)
    qloo.setdefault(guildid,0)
    voice.setdefault(guildid,None)
    print_title.setdefault(guildid,0)   
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
        videde[guildid] = []
        words = []
        figure = await random_choice(int(aft),len_word)       
        for i in range(int(aft)):
          words.append(word_list[figure[i]])
        sss = (' '.join(words))
        ff = await fy.youtubeop(1,sss,guildid)
        videde[guildid] = list(ff[0])
        titl[guildid] = list(ff[1])

        if voice[guildid] == None and voiceid != None:
                                    voice[guildid] = await message.author.voice.channel.connect(reconnect = True)
                                    chanid[guildid] = bot.get_channel(message.channel.id)
                                    vcid[guildid] = message.author.voice.channel.id
                                    channelid[guildid] = message.channel.id
                                    print(channelid)
                                    print(channelid[guildid])
        elif voiceid == None:
                      await message.channel.send("ボイスチャットに参加してください")
                      return
        elif vcid[guildid] != message.author.voice.channel.id:
                          await voice[guildid].move_to(message.author.voice.channel)
                          vcid[guildid] = message.author.voice.channel.id
        
        videid = videde[guildid][0]
        q = f"https://www.youtube.com/watch?v={videid}"
        
        async with chanid[guildid].typing():
          await asyncio.sleep(0.5)
          await chanid[guildid].send("キューに追加: "+q)
        await enqueue(voice[guildid],q)
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
    global chanid,voice,queue_dict,vcid,sss,elect,videde,titl,channelid,play_queue
    chanid[guildid] = bot.get_channel(message.channel.id)
    looping.setdefault(guildid,0)
    qloo.setdefault(guildid,0)
    voice.setdefault(guildid,None)  
    print_title.setdefault(guildid,0) 
    if voice[guildid] == None and voiceid != None:
                                voice[guildid] = await message.author.voice.channel.connect(reconnect = True)
                                chanid[guildid] = bot.get_channel(message.channel.id)
                                vcid[guildid] = message.author.voice.channel.id
                                channelid[guildid] = message.channel.id
                                print(channelid)
                                print(channelid[guildid])
    elif voiceid == None:
                  await message.channel.send("ボイスチャットに参加してください")
                  return
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
            await enqueue(voice[guildid],line)
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
    global chanid,voice,queue_dict,vcid,sss,elect,videde,titl,channelid,play_queue
    chanid[guildid] = bot.get_channel(message.channel.id)
    looping.setdefault(guildid,0)
    qloo.setdefault(guildid,0)  
    voice.setdefault(guildid,None)
    print_title.setdefault(guildid,0) 
    if voice[guildid] == None and voiceid != None:
                                voice[guildid] = await message.author.voice.channel.connect(reconnect = True)
                                chanid[guildid] = bot.get_channel(message.channel.id)
                                vcid[guildid] = message.author.voice.channel.id
                                channelid[guildid] = message.channel.id
                                print(channelid)
                                print(channelid[guildid])
    elif voiceid == None:
                  await message.channel.send("ボイスチャットに参加してください")
                  return
    elif vcid[guildid] != message.author.voice.channel.id:
                      await voice[guildid].move_to(message.author.voice.channel)
                      vcid[guildid] = message.author.voice.channel.id
    nn = os.path.dirname(os.path.abspath(__file__))
    fileing = open(f'{nn}/recommend.txt', "r")
    lis = fileing.readlines()
    if len(lis) >= 1:
        for line in lis:
          line = line.rstrip()  # 読み込んだ行の末尾には改行文字があるので改行文字を削除
          if line[:5] == "https":
            await enqueue(voice[guildid],line)
        await chanid[guildid].send("ADMINのおすすめの曲を再生します。(詳細は.qコマンドを使用(ログが流れます))")
    else:
        await chanid[guildid].send("ADMINのおすすめの曲は現在ありません。")
    fileing.close()

@bot.command()
async def search(message,*,aft):#検索する。動画idを取得して、youtubeのURLの後にくっつけてるだけ
    global guildid
    guildid = message.guild.id
    print(guildid)
    voiceid = message.author.voice
    global chanid,voice,queue_dict,vcid,sss,elect,videde,titl,channelid,print_title,count_music,play_queue
    chanid[guildid] = bot.get_channel(message.channel.id)
    looping.setdefault(guildid,0)
    qloo.setdefault(guildid,0)
    voice.setdefault(guildid,None)
    print_title.setdefault(guildid,0)   
    if you ==False:
        await chanid[guildid].send("制限モードでは検索機能は使えません。TOKEN.txtのYoutube_API_KEYにyoutube v3 APIのkeyを入力してください。")
        return
    titl[guildid] = []
    videde[guildid] = []
    sss = aft
    ff = await fy.youtubeop(5,sss,guildid)
    videde[guildid] = list(ff[0])
    titl[guildid] = list(ff[1])
      #youtube_url = f"https://www.youtube.com/watch?v={videde[guildid]}"

    if voice[guildid] == None and voiceid != None:
                                voice[guildid] = await message.author.voice.channel.connect(reconnect = True)
                                chanid[guildid] = bot.get_channel(message.channel.id)
                                vcid[guildid] = message.author.voice.channel.id
                                channelid[guildid] = message.channel.id
                                print(channelid)
                                print(channelid[guildid])
    elif voiceid == None:
                  await message.channel.send("ボイスチャットに参加してください")
                  return
    elif vcid[guildid] != message.author.voice.channel.id:
                      await voice[guildid].move_to(message.author.voice.channel)
                      vcid[guildid] = message.author.voice.channel.id

    count_music = 1
    if print_title[guildid] == 0:
            for spt in videde[guildid]:
              await chanid[guildid].send(str(count_music)+": https://www.youtube.com/watch?v="+spt)
              
              if count_music == len(videde[guildid]):
                break
              count_music = count_music + 1
    elif print_title[guildid] == 1:
            for spt in titl[guildid]:
              await chanid[guildid].send(str(count_music)+": "+spt)
              
              if count_music == len(titl[guildid]):
                break
              count_music = count_music + 1
    await chanid[guildid].send("流したい曲の番号を送信してください(.無し)")
    elect = 1
    #await enqueue(voice[guildid],youtube_url)

@bot.command()
async def sc(message,*,aft):#検索する。動画idを取得して、youtubeのURLの後にくっつけてるだけ
    global guildid
    guildid = message.guild.id
    print(guildid)
    voiceid = message.author.voice
    global chanid,voice,queue_dict,vcid,sss,elect,videde,titl,channelid,print_title,count_music,play_queue
    chanid[guildid] = bot.get_channel(message.channel.id)
    looping.setdefault(guildid,0)
    qloo.setdefault(guildid,0)
    voice.setdefault(guildid,None)
    print_title.setdefault(guildid,0)   
    if you ==False:
        await chanid[guildid].send("制限モードでは検索機能は使えません。TOKEN.txtのYoutube_API_KEYにyoutube v3 APIのkeyを入力してください。")
        return
    titl[guildid] = []
    videde[guildid] = []
    sss = aft
    ff = await fy.youtubeop(5,sss,guildid)
    videde[guildid] = list(ff[0])
    titl[guildid] = list(ff[1])
      #youtube_url = f"https://www.youtube.com/watch?v={videde[guildid]}"

    if voice[guildid] == None and voiceid != None:
                                voice[guildid] = await message.author.voice.channel.connect(reconnect = True)
                                chanid[guildid] = bot.get_channel(message.channel.id)
                                vcid[guildid] = message.author.voice.channel.id
                                channelid[guildid] = message.channel.id
                                print(channelid)
                                print(channelid[guildid])
    elif voiceid == None:
                  await message.channel.send("ボイスチャットに参加してください")
                  return
    elif vcid[guildid] != message.author.voice.channel.id:
                      await voice[guildid].move_to(message.author.voice.channel)
                      vcid[guildid] = message.author.voice.channel.id

    count_music = 1
    if print_title[guildid] == 0:
            for spt in videde[guildid]:
              await chanid[guildid].send(str(count_music)+": https://www.youtube.com/watch?v="+spt)
              
              if count_music == len(videde[guildid]):
                break
              count_music = count_music + 1
    elif print_title[guildid] == 1:
            for spt in titl[guildid]:
              await chanid[guildid].send(str(count_music)+": "+spt)
              
              if count_music == len(titl[guildid]):
                break
              count_music = count_music + 1
    await chanid[guildid].send("流したい曲の番号を送信してください(.無し)")
    elect = 1
    #await enqueue(voice[guildid],youtube_url)

@bot.command()
async def play_one_song(message,*,aft):#1曲のみ検索する 動作速度を優先した感じ
    global guildid
    guildid = message.guild.id
    print(guildid)
    voiceid = message.author.voice
    global chanid,voice,queue_dict,vcid,sss,elect,videde,titl,channelid,count_music,play_queue
    chanid[guildid] = bot.get_channel(message.channel.id)
    looping.setdefault(guildid,0)
    qloo.setdefault(guildid,0)
    voice.setdefault(guildid,None)
    print_title.setdefault(guildid,0)  
    
    if you ==False:
        await chanid[guildid].send("制限モードでは検索機能は使えません。TOKEN.txtのYoutube_API_KEYにyoutube v3 APIのkeyを入力してください。")
        return
    if aft[:8] == "https://":
        await chanid[guildid].send("URLではこの機能は使えません")
    else:
        videde[guildid] =[]
        titl[guildid] = []
        ff = await fy.youtubeop(1,aft,guildid)
        videde[guildid] = list(ff[0])
        titl[guildid] = list(ff[1])
        #youtube_url = f"https://www.youtube.com/watch?v={videde[guildid]}"
        if voice[guildid] == None and voiceid != None:
                                voice[guildid] = await message.author.voice.channel.connect(reconnect = True)
                                chanid[guildid] = bot.get_channel(message.channel.id)
                                vcid[guildid] = message.author.voice.channel.id
                                channelid[guildid] = message.channel.id
                                print(channelid)
                                print(channelid[guildid])
        elif voiceid == None:
                  await message.channel.send("ボイスチャットに参加してください")
                  return
        elif vcid[guildid] != message.author.voice.channel.id:
                      await voice[guildid].move_to(message.author.voice.channel)
                      vcid[guildid] = message.author.voice.channel.id
        
        videid = videde[guildid][0]
        q = f"https://www.youtube.com/watch?v={videid}"
        async with chanid[guildid].typing():
          await asyncio.sleep(0.5)
          await chanid[guildid].send("キューに追加: "+q)
        await enqueue(voice[guildid],q)    

@bot.command()
async def pos(message,*,aft):#1曲のみ検索する 動作速度を優先した感じ
    global guildid
    guildid = message.guild.id
    print(guildid)
    global chanid,voice,queue_dict,vcid,sss,elect,videde,titl,channelid,looping,qloo,count_music,play_queue
    await asyncio.sleep(0.1)
    chanid[guildid] = bot.get_channel(message.channel.id)
    looping.setdefault(guildid,0)
    qloo.setdefault(guildid,0)
    voice.setdefault(guildid,None)
    print_title.setdefault(guildid,0) 
    print(qloo[guildid])
    if you ==False:
        await chanid[guildid].send("制限モードでは検索機能は使えません。TOKEN.txtのYoutube_API_KEYにyoutube v3 APIのkeyを入力してください。")
        return
    if aft[:8] == "https://":
        await chanid[guildid].send("URLではこの機能は使えません")
    else:
        videde[guildid] =[]
        titl[guildid] = []
        ff = await fy.youtubeop(1,aft,guildid)
        videde= ff[0]
        titl = ff[1]
        voiceid = message.author.voice
        if voice[guildid] == None and voiceid != None:
                                voice[guildid] = await message.author.voice.channel.connect(reconnect = True)
                                chanid[guildid] = bot.get_channel(message.channel.id)
                                vcid[guildid] = message.author.voice.channel.id
                                channelid[guildid] = message.channel.id
                                print(channelid)
                                print(channelid[guildid])
        elif voiceid == None:
                  await message.channel.send("ボイスチャットに参加してください")
                  return
        elif vcid[guildid] != message.author.voice.channel.id:
                      await voice[guildid].move_to(message.author.voice.channel)
                      vcid[guildid] = message.author.voice.channel.id


        #youtube_url = f"https://www.youtube.com/watch?v={videde[guildid]}"

        
        videid = videde[guildid][0]
        q = f"https://www.youtube.com/watch?v={videid}"
        await enqueue(voice[guildid],q) 
        async with chanid[guildid].typing():
          await asyncio.sleep(0.5)
          await chanid[guildid].send("キューに追加: "+q)


#playlistを展開しキューに入れる
@bot.command()
async def playlist(message,*,aft):
  global guildid
  guildid = message.guild.id
  print(guildid)
  voiceid = message.guild.id
  global chanid,voice,queue_dict,vcid,looping,qloo,print_title,play_queue
  print("aft: "+aft)
  voice.setdefault(guildid,None)
  looping.setdefault(guildid,0)
  qloo.setdefault(guildid,0)
  print_title.setdefault(guildid,0) 
  if aft[:8] != "https://":
    await message.channel.send("URLを指定してください")
  else:
    youtube_url = aft
    playlist_url=""
    if "playlist" in youtube_url == False:
      await message.channel.send("playlistのみ対応しているコマンドです")
    else:
      try:
        step_one = youtube_url.split("&")[1]
        playlist_url = step_one.replace("list=", "")
      except:
        step_two = youtube_url.split("?")[1]
        playlist_url = step_two.replace("list=", "")
      pl = await fy.youtube_list(playlist_url, guildid)
      guildid = pl[1]
      playlist_video = pl[0]
      videoids = playlist_video[guildid]
      if voice[guildid] == None and voiceid != None:
        voice[guildid] = await message.author.voice.channel.connect(reconnect=True)
        chanid[guildid] = bot.get_channel(message.channel.id)
        vcid[guildid] = message.author.voice.channel.id
        channelid[guildid] = message.channel.id
        print(channelid)
        print(channelid[guildid])
      elif voiceid == None:
        await message.channel.send("ボイスチャットに参加してください")
        return
      elif vcid[guildid] != message.author.voice.channel.id:
        await voice[guildid].move_to(message.author.voice.channel)
        vcid[guildid] = message.author.voice.channel.id

      for i in videoids:
        q = f"https://www.youtube.com/watch?v={i}"
        await enqueue(voice[guildid], q)
      async with chanid[guildid].typing():
        await asyncio.sleep(0.5)
        await chanid[guildid].send("プレイリストが追加されました。詳細は.qで見ることができます。(ログが流れます)")


@bot.command()
async def pl(message, *, aft):
  global guildid
  guildid = message.guild.id
  print(guildid)
  voiceid = message.guild.id
  global chanid, voice, queue_dict, vcid, looping, qloo, print_title,play_queue
  print("aft: "+aft)
  voice.setdefault(guildid, None)
  looping.setdefault(guildid, 0)
  qloo.setdefault(guildid, 0)
  print_title.setdefault(guildid, 0)
  if aft[:8] != "https://":
    await message.channel.send("URLを指定してください")
  else:
    youtube_url = aft
    playlist_url = ""
    if "playlist" in youtube_url == False:
      await message.channel.send("playlistのみ対応しているコマンドです")
    else:
      try:
        step_one = youtube_url.split("&")[1]
        playlist_url = step_one.replace("list=", "")
      except:
        step_two = youtube_url.split("?")[1]
        playlist_url = step_two.replace("list=", "")
      pl = await fy.youtube_list(playlist_url, guildid)
      guildid = pl[1]
      playlist_video = pl[0]
      videoids = playlist_video[guildid]
      if voice[guildid] == None and voiceid != None:
        voice[guildid] = await message.author.voice.channel.connect(reconnect=True)
        chanid[guildid] = bot.get_channel(message.channel.id)
        vcid[guildid] = message.author.voice.channel.id
        channelid[guildid] = message.channel.id
        print(channelid)
        print(channelid[guildid])
      elif voiceid == None:
        await message.channel.send("ボイスチャットに参加してください")
        return
      elif vcid[guildid] != message.author.voice.channel.id:
        await voice[guildid].move_to(message.author.voice.channel)
        vcid[guildid] = message.author.voice.channel.id

      for i in videoids:
        q = f"https://www.youtube.com/watch?v={i}"
        await enqueue(voice[guildid], q)
      async with chanid[guildid].typing():
        await asyncio.sleep(0.5)
        await chanid[guildid].send("プレイリストが追加されました。詳細は.qで見ることができます。(ログが流れます)")

@bot.command()
async def play(message,*,aft):#指定されたURLの曲を流す。
  global guildid
  guildid = message.guild.id
  print(guildid)
  voiceid = message.author.voice
  global chanid, voice, queue_dict, vcid, sss, elect, videde, titl, channelid, qloo, looping, print_title, count_music, error_check, play_queue
  print("aft:"+aft)
  voice.setdefault(guildid, None)
  looping.setdefault(guildid, 0)
  qloo.setdefault(guildid, 0)
  print_title.setdefault(guildid, 0)
  # idx = msg.find(" ")
  # chanid = bot.get_channel(message.channel.id)
  if aft[:8] == "https://":  # youtubeのURLかを判別。
          youtube_url = aft
          playlist_url = ""
          if "playlist" in youtube_url:  # プレイリストか判別
              try:
                step_one = youtube_url.split("&")[1]
                playlist_url = step_one.replace("list=", "")
              except:
                step_two = youtube_url.split("?")[1]
                playlist_url = step_two.replace("list=", "")
              pl = await fy.youtube_list(playlist_url, guildid)
              guildid = pl[1]
              playlist_video = pl[0]
              videoids = playlist_video[guildid]

              if voice[guildid] == None and voiceid != None:
                                  voice[guildid] = await message.author.voice.channel.connect(reconnect=True)
                                  chanid[guildid] = bot.get_channel(message.channel.id)
                                  vcid[guildid] = message.author.voice.channel.id
                                  channelid[guildid] = message.channel.id
                                  print(channelid)
                                  print(channelid[guildid])
              elif voiceid == None:
                  await message.channel.send("ボイスチャットに参加してください")
                  return
              elif vcid[guildid] != message.author.voice.channel.id:
                      await voice[guildid].move_to(message.author.voice.channel)
                      vcid[guildid] = message.author.voice.channel.id

              for i in videoids:
                q = f"https://www.youtube.com/watch?v={i}"
                await enqueue(voice[guildid], q)
              async with chanid[guildid].typing():
                await asyncio.sleep(0.5)
                await chanid[guildid].send("プレイリストが追加されました。詳細は.qで見ることができます。(ログが流れます)")

          else:  # 曲のURLがそのままのとき
               if voice[guildid] == None and voiceid != None:
                              voice[guildid] = await message.author.voice.channel.connect(reconnect=True)
                              chanid[guildid] = bot.get_channel(message.channel.id)
                              vcid[guildid] = message.author.voice.channel.id
                              channelid[guildid] = message.channel.id
                              print(channelid)
                              print(channelid[guildid])
               elif voiceid == None:
                  await message.channel.send("ボイスチャットに参加してください")
                  return
               elif vcid[guildid] != message.author.voice.channel.id:
                    await voice[guildid].move_to(message.author.voice.channel)
                    vcid[guildid] = message.author.voice.channel.id
               if "list" in youtube_url:
                  youtube_url_list = youtube_url.split("&")
                  youtube_url_play = youtube_url_list[0]
                  await enqueue(voice[guildid], youtube_url_play)
               else:
                  await enqueue(voice[guildid], youtube_url)
               if error_check == False:
                  async with chanid[guildid].typing():
                   await asyncio.sleep(0.5)
                  if "list" in youtube_url:
                    await chanid[guildid].send("プレイリスト中の曲が追加されました。プレイリスト全体を追加するには .playlist [URL] コマンドを使用してください。")
                  else:
                    await chanid[guildid].send("正常に追加されました。")
               elif error_check == True:
                  error_check = False
  else: #URLじゃなかったんだね...
          if you ==False:
            await chanid[guildid].send("制限モードでは検索機能は使えません。TOKEN.txtのYoutube_API_KEYにyoutube v3 APIのkeyを入力してください。")
            return
          videde[guildid] =[]
          titl[guildid] = []
          sss = aft
          ff = await fy.youtubeop(5,sss,guildid)
          videde = ff[0]
          titl = ff[1]
          print(f"videde[guildid]: {videde[guildid]}")
         #youtube_url = f"https://www.youtube.com/watch?v={videde[guildid]}"
          if voice[guildid] == None and voiceid != None:
                                voice[guildid] = await message.author.voice.channel.connect(reconnect = True)
                                chanid[guildid] = bot.get_channel(message.channel.id)
                                vcid[guildid] = message.author.voice.channel.id
                                channelid[guildid] = message.channel.id
                                print(channelid)
                                print(channelid[guildid])
          elif voiceid == None:
                  await message.channel.send("ボイスチャットに参加してください")
                  return
          elif vcid[guildid] != message.author.voice.channel.id:
                      await voice[guildid].move_to(message.author.voice.channel)
                      vcid[guildid] = message.author.voice.channel.id

          count_music = 1
          if print_title[guildid] == 0: #候補を5個並べる。選択の部分はまた別な場所(上の方にある)
            for spt in videde[guildid]:
              await chanid[guildid].send(str(count_music)+": https://www.youtube.com/watch?v="+spt)

              if count_music == len(videde[guildid]):
                break
              count_music = count_music + 1
          elif print_title[guildid] == 1:
            for spt in titl[guildid]:
              await chanid[guildid].send(str(count_music)+": "+spt)
              
              if count_music == len(titl[guildid]):
                break
              count_music = count_music + 1
          await chanid[guildid].send("流したい曲の番号を送信してください(.無し)") #動作速度を早めるためにはどうすればええんや...
          elect = 1
          #await enqueue(voice[guildid],youtube_url)

@bot.command()
async def p(message,*,aft):#指定されたURLの曲を流す。
  global guildid
  guildid = message.guild.id
  print(guildid)
  voiceid = message.author.voice
  global chanid, voice, queue_dict, vcid, sss, elect, videde, titl, channelid, qloo, looping, print_title, count_music, error_check,play_queue
  print("aft:"+aft)
  voice.setdefault(guildid, None)
  looping.setdefault(guildid, 0)
  qloo.setdefault(guildid, 0)
  print_title.setdefault(guildid, 0)
  # idx = msg.find(" ")
  # chanid = bot.get_channel(message.channel.id)
  if aft[:8] == "https://":  # youtubeのURLかを判別。
          youtube_url = aft
          playlist_url = ""
          if "playlist" in youtube_url:  # プレイリストか判別
              try:
                step_one = youtube_url.split("&")[1]
                playlist_url = step_one.replace("list=", "")
              except:
                step_two = youtube_url.split("?")[1]
                playlist_url = step_two.replace("list=","")
              pl = await fy.youtube_list(playlist_url, guildid)
              guildid = pl[1]
              playlist_video = pl[0]
              videoids = playlist_video[guildid]

              if voice[guildid] == None and voiceid != None:
                                  voice[guildid] = await message.author.voice.channel.connect(reconnect=True)
                                  chanid[guildid] = bot.get_channel(message.channel.id)
                                  vcid[guildid] = message.author.voice.channel.id
                                  channelid[guildid] = message.channel.id
                                  print(channelid)
                                  print(channelid[guildid])
              elif voiceid == None:
                    await message.channel.send("ボイスチャットに参加してください")
                    return
              elif vcid[guildid] != message.author.voice.channel.id:
                        await voice[guildid].move_to(message.author.voice.channel)
                        vcid[guildid] = message.author.voice.channel.id

              for i in videoids:
                q = f"https://www.youtube.com/watch?v={i}"
                await enqueue(voice[guildid], q)
              async with chanid[guildid].typing():
                await asyncio.sleep(0.5)
                await chanid[guildid].send("プレイリストが追加されました。詳細は.qで見ることができます。(ログが流れます)")

          else:  # 曲のURLがそのままのとき
                if voice[guildid] == None and voiceid != None:
                              voice[guildid] = await message.author.voice.channel.connect(reconnect=True)
                              chanid[guildid] = bot.get_channel(message.channel.id)
                              vcid[guildid] = message.author.voice.channel.id
                              channelid[guildid] = message.channel.id
                              print(channelid)
                              print(channelid[guildid])
                elif voiceid == None:
                  await message.channel.send("ボイスチャットに参加してください")
                  return
                elif vcid[guildid] != message.author.voice.channel.id:
                    await voice[guildid].move_to(message.author.voice.channel)
                    vcid[guildid] = message.author.voice.channel.id
                if "list" in youtube_url:
                  youtube_url_list = youtube_url.split("&")
                  youtube_url_play = youtube_url_list[0]
                  await enqueue(voice[guildid], youtube_url_play)
                else:
                  await enqueue(voice[guildid], youtube_url)
                if error_check == False:
                  async with chanid[guildid].typing():
                   await asyncio.sleep(0.5)
                  if "list" in youtube_url:
                    await chanid[guildid].send("プレイリスト中の曲が追加されました。プレイリスト全体を追加するには .playlist [URL] コマンドを使用してください。")
                  else:
                    await chanid[guildid].send("正常に追加されました。")
                elif error_check == True:
                  error_check = False
  else:  # URLじゃなかったんだね...
          if you == False:
            await chanid[guildid].send("制限モードでは検索機能は使えません。TOKEN.txtのYoutube_API_KEYにyoutube v3 APIのkeyを入力してください。")
            return
          videde[guildid] = []
          titl[guildid] = []
          sss = aft
          ff = await fy.youtubeop(5, sss, guildid)
          videde = ff[0]
          titl = ff[1]
          print(f"videde[guildid]: {videde[guildid]}")
         # youtube_url = f"https://www.youtube.com/watch?v={videde[guildid]}"
          if voice[guildid] == None and voiceid != None:
                              voice[guildid] = await message.author.voice.channel.connect(reconnect = True)
                              chanid[guildid] = bot.get_channel(message.channel.id)
                              vcid[guildid] = message.author.voice.channel.id
                              channelid[guildid] = message.channel.id
                              print(channelid)
                              print(channelid[guildid])
          elif voiceid == None:
                await message.channel.send("ボイスチャットに参加してください")
                return
          elif vcid[guildid] != message.author.voice.channel.id:
                    await voice[guildid].move_to(message.author.voice.channel)
                    vcid[guildid] = message.author.voice.channel.id

          count_music = 1
          if print_title[guildid] == 0:  # 候補を5個並べる。選択の部分はまた別な場所(上の方にある)
            for spt in videde[guildid]:
              await chanid[guildid].send(str(count_music)+": https://www.youtube.com/watch?v="+spt)

              if count_music == len(videde[guildid]):
                break
              count_music = count_music + 1
          elif print_title[guildid] == 1:
            for spt in titl[guildid]:
              await chanid[guildid].send(str(count_music)+": "+spt)

              if count_music == len(titl[guildid]):
                break
              count_music = count_music + 1
          # 動作速度を早めるためにはどうすればええんや...
          await chanid[guildid].send("流したい曲の番号を送信してください(.無し)")
          elect = 1
          # await enqueue(voice[guildid],youtube_url)

if __name__ == '__main__': #起動
  bot.run(TOKEN)

#やりたいことリスト
#
#
#
#
#