import time
poczatek = time.monotonic()
import sys
import discord
from discord.ext import commands
from discord.ext.commands import Bot
import asyncio
import random
import psutil
import requests
import datetime
from math import floor
from googlesearch import search
import BitBotHelper

global rokrodzin
rokurodzin = 2019

prefix = "$$"

bot = commands.Bot(command_prefix=prefix)

def sp_vip(uzytkownik):
    global vipczynie
    try:
        plik = open("/home/pi/bitbotdata/uzytkownicy/" + uzytkownik, "r")
        czyvip = plik.read()
        plik.close()
        if czyvip == "tak":
            vipczynie = 1
        else:
            vipczynie = 0
    except:
        vipczynie = 0

global spamy
spamy = 0

# Music Bot
if not discord.opus.is_loaded():
    discord.opus.load_opus('opus')

class VoiceEntry:
    def __init__(self, message, player):
        self.requester = message.author
        self.channel = message.channel
        self.player = player

    def __str__(self):
        fmt = '*{0.title}* przez **{0.uploader}** - do kolejki dodał <@{1.id}>'
        duration = self.player.duration
        if duration:
            fmt = fmt + ' (długość: {0[0]}m {0[1]}s)'.format(divmod(duration, 60))
        return fmt.format(self.player, self.requester)

class VoiceState:
    def __init__(self, bot):
        self.current = None
        self.voice = None
        self.bot = bot
        self.play_next_song = asyncio.Event()
        self.songs = asyncio.Queue()
        self.skip_votes = set()
        self.audio_player = self.bot.loop.create_task(self.audio_player_task())

    def is_playing(self):
        if self.voice is None or self.current is None:
            return False

        player = self.current.player
        return not player.is_done()

    @property
    def player(self):
        return self.current.player

    def skip(self):
        self.skip_votes.clear()
        if self.is_playing():
            self.player.stop()

    def toggle_next(self):
        self.bot.loop.call_soon_threadsafe(self.play_next_song.set)

    async def audio_player_task(self):
        while True:
            self.play_next_song.clear()
            self.current = await self.songs.get()
            await self.bot.send_message(self.current.channel, 'Teraz grane: ' + str(self.current))
            self.current.player.start()
            await self.play_next_song.wait()

class Komendy:
    def __init__(self, bot):
        self.bot = bot
        self.voice_states = {}

    def get_voice_state(self, server):
        state = self.voice_states.get(server.id)
        if state is None:
            state = VoiceState(self.bot)
            self.voice_states[server.id] = state

        return state

    async def create_voice_client(self, channel):
        voice = await self.bot.join_voice_channel(channel)
        state = self.get_voice_state(channel.server)
        state.voice = voice

    def __unload(self):
        for state in self.voice_states.values():
            try:
                state.audio_player.cancel()
                if state.voice:
                    self.bot.loop.create_task(state.voice.disconnect())
            except:
                pass

    @commands.command(pass_context=True, no_pm=True)
    async def Dołącz(self, ctx, *, channel : discord.Channel):
        try:
            await self.create_voice_client(channel)
        except discord.ClientException:
            await self.bot.say('Jestem już w kanale głosowym!')
        except discord.InvalidArgument:
            await self.bot.say('To raczej nie jest kanał głosowy.')
        else:
            await self.bot.say('Dołączyłem do ' + channel.name)

    @commands.command(pass_context=True, no_pm=True)
    async def Przywołaj(self, ctx):
        summoned_channel = ctx.message.author.voice_channel
        if summoned_channel is None:
            await self.bot.say('Hej, tą komendę się wykonuje jak jesteś w kanale głosowym.')
            return False

        state = self.get_voice_state(ctx.message.server)
        if state.voice is None:
            state.voice = await self.bot.join_voice_channel(summoned_channel)
        else:
            await state.voice.move_to(summoned_channel)
        await self.bot.say('Dołączyłem do ' + summoned_channel.name)
        return True

    @commands.command(pass_context=True, no_pm=True)
    async def Zagraj(self, ctx, *, song : str):
        state = self.get_voice_state(ctx.message.server)
        opts = {
            'default_search': 'auto',
            'quiet': True
        }

        if state.voice is None:
            success = await ctx.invoke(self.Przywołaj)
            if not success:
                return

        try:
            player = await state.voice.create_ytdl_player(song, ytdl_options=opts, after=state.toggle_next)
        except Exception as e:
            fmt = ' Ojej! Wystąpił błąd: ```\n{}: {}\n```'
            await self.bot.send_message(ctx.message.channel, fmt.format(type(e).__name__, e))
        else:
            player.volume = 0.6
            entry = VoiceEntry(ctx.message, player)
            await self.bot.say('Dodano ' + str(entry))
            await state.songs.put(entry)

    @commands.command(pass_context=True, no_pm=True)
    async def Radio(self, ctx):
        sp_vip(ctx.message.author.id)
        if not vipczynie == 1:
            if BitBotHelper.Konfiguracje.RadioJestZablokowane(ctx.message.server.id) == True:
                await bot.say("Radio jest zablokowane!")
                return
            await bot.say(nievip)
            return
        while True:
            state = self.get_voice_state(ctx.message.server)
            
            opts = {
                'default_search': 'auto',
                'quiet': True
            }

            if state.voice is None:
                success = await ctx.invoke(self.Przywołaj)
                if not success:
                    return

            try:
                songs = ["https://www.youtube.com/watch?v=SHFTHDncw0g", "https://www.youtube.com/watch?v=8U2rKAnyyDE", "https://www.youtube.com/watch?v=6FNHe3kf8_s", "https://www.youtube.com/watch?v=A56p-ZSZ5Vc", "https://www.youtube.com/watch?v=60ItHLz5WEA", "https://www.youtube.com/watch?v=8JnfIa84TnU", "https://www.youtube.com/watch?v=FzG4uDgje3M", "https://www.youtube.com/watch?v=Oa4klaedx0g", "https://www.youtube.com/watch?v=PCQs3vSJ6xA", "https://www.youtube.com/watch?v=2Vv-BfVoq4g"]
                song = songs[random.randint(0, len(songs) - 1)]
                player = await state.voice.create_ytdl_player(song, ytdl_options=opts, after=state.toggle_next)
            except Exception as e:
                fmt = ' Ojej! Wystąpił błąd: ```\n{}: {}\n```'
                await self.bot.send_message(ctx.message.channel, fmt.format(type(e).__name__, e))
            else:
                player.volume = 0.6
                entry = VoiceEntry(ctx.message, player)
                await state.songs.put(entry)
                self.player = player
                duration = self.player.duration
                if duration:
                    czekaj = int(duration)
                    await asyncio.sleep(czekaj)

    @commands.command(pass_context=True, no_pm=True)
    async def Głośność(self, ctx, value : int):
        state = self.get_voice_state(ctx.message.server)
        if state.is_playing():
            player = state.player
            player.volume = value / 100
            await self.bot.say('Ustawiono głośność na {:.0%}'.format(player.volume))

    @commands.command(pass_context=True, no_pm=True)
    async def Earrape(self, ctx):
        state = self.get_voice_state(ctx.message.server)
        if state.is_playing():
            player = state.player
            player.volume = 99999999999999999999999
            await self.bot.say("Tryb ear rape włączony!")

    @commands.command(pass_context=True, no_pm=True)
    async def Pauza(self, ctx):
        state = self.get_voice_state(ctx.message.server)
        if state.is_playing():
            player = state.player
            player.pause()
            await bot.add_reaction(ctx.message, '✅')

    @commands.command(pass_context=True, no_pm=True)
    async def Wznów(self, ctx):
        state = self.get_voice_state(ctx.message.server)
        if state.is_playing():
            player = state.player
            player.resume()
            await bot.add_reaction(ctx.message, '✅')

    @commands.command(pass_context=True, no_pm=True)
    async def Zatrzymaj(self, ctx):
        server = ctx.message.server
        state = self.get_voice_state(server)

        if state.is_playing():
            player = state.player
            player.stop()

        try:
            state.audio_player.cancel()
            del self.voice_states[server.id]
            await state.voice.disconnect()
            await bot.add_reaction(ctx.message, '✅')
        except:
            pass

    @commands.command(pass_context=True, no_pm=True)
    async def Pomiń(self, ctx):
        state = self.get_voice_state(ctx.message.server)
        if not state.is_playing():
            await self.bot.say('Teraz nic nie gra.')
            return

        voter = ctx.message.author
        if voter == state.current.requester:
            await self.bot.say('Pomijam...')
            state.skip()
        elif voter.id not in state.skip_votes:
            state.skip_votes.add(voter.id)
            total_votes = len(state.skip_votes)
            if total_votes >= 3:
                await self.bot.say('Pomijam...')
                state.skip()
            else:
                await self.bot.say('Dodano głos. Teraz jest ich {} na 3.'.format(total_votes))
        else:
            await self.bot.say('Nie oszukuj! Już zagłosowałeś na pominięcie!.')

    @commands.command(pass_context=True, no_pm=True)
    async def CoGra(self, ctx):
        state = self.get_voice_state(ctx.message.server)
        if state.current is None:
            await self.bot.say('Teraz nic nie gra.')
        else:
            skip_count = len(state.skip_votes)
            await self.bot.say('Teraz gra {} z {} na 3 pominięciami.'.format(state.current, skip_count))


@bot.event
async def on_ready():
    global uruchomionyw
    uruchomionyw = str(floor((time.monotonic() - poczatek) * 1000)) + "ms"
    print("BitBot jest gotowy.")
    gos = random.randint(1, 4)
    if gos == 1:
        await bot.change_presence(game=discord.Game(name="{} serwerów | $$Pomoc".format(str(len(bot.servers))), type=0))
    elif gos == 2:
        await bot.change_presence(game=discord.Game(name="{} serwerów | $$Pomoc".format(str(len(bot.servers))), type=1))
    elif gos == 3:
        await bot.change_presence(game=discord.Game(name="{} serwerów | $$Pomoc".format(str(len(bot.servers))), type=2))
    elif gos == 4:
        await bot.change_presence(game=discord.Game(name="{} serwerów | $$Pomoc".format(str(len(bot.servers))), type=3))

@bot.event
async def on_member_join(member):
    if not BitBotHelper.Konfiguracje.JoinDM(member.server.id) == "null":
        await bot.send_message(member, BitBotHelper.Konfiguracje.JoinDM(member.server.id))

@bot.event
async def on_member_remove(member):
    if not BitBotHelper.Konfiguracje.RemoveDM(member.server.id) == "null":
        await bot.send_message(member, BitBotHelper.Konfiguracje.RemoveDM(member.server.id))

@bot.command(pass_context=True)
async def Konfiguruj(ctx, co=None, *, wartosc=None):
    if not ctx.message.author.server_permissions.manage_server:
        await bot.say("Nie masz permisji do tego!")
        return
    if co == None:
        embed = discord.Embed(title="Konfiguruj bota:")
        embed.add_field(name="joindm", value="Prywatna wiadomość do nowego członka serwera.", inline=True)
        embed.add_field(name="removedm", value="Prywatna wiadomość do członka opuszczającego serwer.", inline=True)
        embed.add_field(name="radio", value="Odblokuj lub zablokuj radio.", inline=True)
        await bot.say(embed=embed)
    elif co == "joindm" or co == "removedm":
        if wartosc == None:
            embed = discord.Embed(title="Konfiguruj bota:")
            if co == "joindm":
                embed.add_field(name="Wartość to:", value="{}".format(BitBotHelper.Konfiguracje.JoinDM(ctx.message.server.id)), inline=True)
            else:
                embed.add_field(name="Wartość to:", value="{}".format(BitBotHelper.Konfiguracje.RemoveDM(ctx.message.server.id)), inline=True) 
            embed.set_footer(text="Jeżeli chcesz ustawić wartość, użyj {}Konfiguruj {} <wartość>.".format(prefix, co))
            await bot.say(embed=embed)
            return
        l = str(wartosc).lower()
        if l == "null":
            wartosc = "null"
        if co == "joindm":
            BitBotHelper.Konfiguracje.UstawJoinDM(ctx.message.server.id, wartosc)
        else:
            BitBotHelper.Konfiguracje.UstawRemoveDM(ctx.message.server.id, wartosc)
        await bot.add_reaction(ctx.message, "✅")
    elif co == "radio":
        if wartosc == None:
            embed = discord.Embed(title="Konfiguruj bota:")
            embed.add_field(name="Wartość to:", value="{}".format(str(BitBotHelper.Konfiguracje.RadioCzyZablokowane(ctx.message.server.id))), inline=True)
            embed.set_footer(text="Jeżeli chcesz ustawić wartość, użyj {}Konfiguruj radio <wartość>.".format(prefix))
            await bot.say(embed=embed)
            return
        l = wartosc.lower()
        if l == "tak":
            BitBotHelper.Konfiguracje.OdblokujRadio(ctx.message.server.id)
        elif l == "nie":
            BitBotHelper.Konfiguracje.ZablokujRadio(ctx.message.server.id)
        else:
            embed = discord.Embed(title="Konfiguruj bota:")
            embed.add_field(name="Hej,", value="musisz podać wartość **Tak** (*odblokuj*, False) lub **Nie** (*zablokuj*, True)!")
            await bot.say(embed=embed)
            return
        await bot.add_reaction(ctx.message, "✅")

@bot.command(pass_context=True)
async def LiteraPoLiterze(ctx, *, tekst):
    licznik = 1
    wiadomosc = str(tekst[0])
    msg = await bot.say(wiadomosc)
    while licznik < len(tekst):
        await asyncio.sleep(0.5)
        wiadomosc = wiadomosc + str(tekst[licznik])
        await bot.edit_message(msg, wiadomosc)
        licznik = licznik + 1

@bot.command(pass_context=True)
async def Urodziny(ctx):
    global rokurodzin
    dzisiaj = datetime.date.today()
    urodziny = datetime.date(rokurodzin, 4, 8)
    czasdourodzin = abs(urodziny - dzisiaj)
    if czasdourodzin.days == 0:
        await bot.say("Urodziny są dzisiaj! :tada:")
    else:
        await bot.say("Do urodzin pozostało {} dni.".format(str(czasdourodzin.days)))

@bot.command(pass_context=True)
async def Wybierz(ctx, *wybory):
    await bot.say("Hmm... Wybieram **{}**.".format(str(random.choice(wybory))))

@bot.command(pass_context=True)
async def Embed(ctx, *, tekst):
    embed = discord.Embed(title=str(tekst))
    await bot.say(embed=embed)

@bot.command(pass_context=True)
async def Losuj(ctx, minimalny : int, maksymalny : int):
    await bot.say("Wylosowana liczba to {}.".format(str(random.randint(minimalny, maksymalny))))

@bot.command(pass_context=True)
async def Nadaj(ctx, *, wiadomosc : str):
    try:
        plik = open("/home/pi/bitbotdata/publicznewiadomosci.txt", "a")
        plik.write("{}: {}\n".format(ctx.message.author.name, wiadomosc))
        plik.close()
        await bot.add_reaction(ctx.message, "✅")
    except:
        await bot.add_reaction(ctx.message, "❎")

@bot.command(pass_context=True)
async def Wiadomości(ctx):
    plik = open("/home/pi/bitbotdata/publicznewiadomosci.txt", "r")
    wiadomosci = plik.read()
    await bot.say(wiadomosci)
    plik.close()

@bot.command(pass_context=True)
async def EmojiID(ctx, emoji : discord.Emoji):
    await bot.say("A ID emotki {} to... {}".format(str(emoji), str(emoji.id)))

@bot.command(pass_context=True)
async def CustomEmoji(ctx, ename, eid : int):
    ename = ename.replace(":", "")
    await bot.say("<:{}:{}>".format(ename, str(eid)))

@bot.command(pass_context=True)
async def Ping(ctx):
    before = time.monotonic()
    message = await bot.say("Czekaj...")
    ping = (time.monotonic() - before) * 1000
    await bot.edit_message(message, "Pong! :ping_pong: **{}ms**".format(str(floor(ping))))

@bot.command(pass_context=True)
async def LiveUptime(ctx):
    sp_vip(ctx.message.author.id)
    if vipczynie == 1:
        msg = await bot.say(uptimemsg)
        while True:
            await asyncio.sleep(1)
            await bot.edit_message(msg, uptimemsg)
    else:
        await bot.say(nievip + " Trochę to obciąża komputer.")

@bot.command(pass_context=True)
async def SprawdźVIPa(ctx, user : discord.Member):
    sp_vip(user.id)
    if vipczynie == 1:
        await bot.say("Ten użytkownik ma VIPa.")
    else:
        await bot.say("Ten użytkownik nie ma VIPa.")

@bot.command(pass_context=True)
async def DodajVIPa(ctx, user : discord.Member):
    if not ctx.message.author.id == 233592407902388224:
        await bot.add_reaction(ctx.message, "❎")
        return
    sp_vip(user.id)
    if vipczynie == 1:
        await bot.add_reaction(ctx.message, "❎")
    else:
        plik = open("/home/pi/bitbotdata/uzytkownicy/" + str(user.id), "w")
        plik.write("tak")
        await bot.add_reaction(ctx.message, "✅")

@bot.command(pass_context=True)
async def kek(ctx):
    await bot.say("Hey I'm MEE6, the Discord bot!")

@bot.command(pass_context=True)
async def Spam(ctx, ilosc : int, cooldown : int, *, wiadomosc : str):
    sp_vip(ctx.message.author.id)
    if vipczynie == 1:
        licznik = 0
        global spamy
        while licznik < ilosc:
            await bot.say(wiadomosc)
            licznik = licznik + 1
            spamy = spamy + 1
            await asyncio.sleep(cooldown)
    else:
        await bot.say(nievip + " Nawet nie myśl o wykonaniu tej komendy bez VIPa.")

@bot.command(pass_context=True)
async def LiczbaSerwerów(ctx):
    await bot.say("<@432565925934268416> jest na {} serwerach.".format(str(len(bot.servers))))

@bot.command(pass_context=True)
async def Odwróć(ctx, *, tekst : str):
    tekst = tekst[::-1]
    await bot.say(tekst)

@bot.command(pass_context=True)
async def Członkowie(ctx):
    guild = ctx.message.server
    ludzie = len([member for member in guild.members if not member.bot])
    boty = len([member for member in guild.members if member.bot])
    await bot.say("Ludzie: {}, boty: {}.".format(str(ludzie), str(boty)))

@bot.command(pass_context=True)
async def Statystyki(ctx):
    global uptimemsg
    global uruchomiony
    global uruchomionyw
    embed = discord.Embed(title="Statystyki")
    embed.add_field(name="Prefix", value="{}".format(prefix), inline=True)
    embed.add_field(name="Jestem online", value="{}".format(uptimemsg), inline=True)
    embed.add_field(name="Uruchomiony od", value="{}".format(uruchomiony), inline=True)
    embed.add_field(name="Spamy czasu bota", value="{}".format(str(spamy)), inline=True)
    embed.add_field(name="Czas uruchomienia", value="{}".format(uruchomionyw), inline=True)
    embed.add_field(name="psutil.cpu_percent()", value="{}".format(str(psutil.cpu_percent())), inline=True)
    embed.add_field(name="psutil.net_io_counters()", value="{}".format(str(psutil.net_io_counters())), inline=True)
    await bot.say(embed=embed)

@bot.command(pass_context=True)
async def Napisz(ctx, kanal : discord.Channel, *, wiadomosc):
    try:
        await bot.send_message(kanal, wiadomosc)
        await bot.say("Napisałem **{}** w **<#{}>**.".format(wiadomosc, kanal.id))
    except Exception as e:
        await bot.say("Wystąpił błąd: \n```{}: {}```\n".format(type(e).__name__, e))

@bot.command(pass_context=True)
async def Pytanie(ctx, *, zapytaj):
    try:
        msg = await bot.send_message(ctx.message.channel, zapytaj)
        await bot.add_reaction(msg, "❎")
        await bot.add_reaction(msg, "✅")
    except Exception as e:
        await bot.say("Wystąpił błąd: \n```{}: {}```\n".format(type(e).__name__, e))

@bot.command(pass_context=True)
async def Milionerzy(ctx):
    pytanie = random.randint(1, 11)
    if pytanie == 1:
        answer = 2
        question = "Co jest hitem tego lata: 1) gówno 2) memy 3) szajsung galaxy s9 4) srajfon x"
    elif pytanie == 2:
        answer = 4
        question = "Jaki telefon jest najlepszy na świecie: 1) srajfon x 2) szajsung galaxy s9 3) hujawej p20 pro 4) nokija 3310 5) komputer"
    elif pytanie == 3:
        answer = 4
        question = "Jaki komputer jest najlepszy: 1) ajmak 2) srasus 3) hell 4) składak"
    elif pytanie == 4:
        answer = 2
        question = "Co lepsze: 1) ENWIDJA GjeFordze 1080 2) Jintel HD Grafiks 620 3) AEMDE Radełon ER7"
    elif pytanie == 5:
        answer = 2
        question = "Czy jestem debilem: 1) Nie 2) Tak"
    elif pytanie == 6:
        answer = 3
        question = "Jestem 1) raperem czy 2) youtuberem? A może 3) nikim?"
    elif pytanie == 7:
        answer = 2
        question = "Co się robi: 1) zupe 2) loda 3) mleko 4) wode 5) telefony 6) płyty czy 7) gówno?"
    elif pytanie == 8:
        answer = 4
        question = "Najlepszy tekst wszech czasów: 1) Chyba ty 2) Spierdalaj 3) Śmieć 4) BitBot 5) Gówniarz 6) Chuj 7) NenuuX 8) Milionerzy 9) Dolary 10) Chorwacja 11) Kredki"
    elif pytanie == 9:
        answer = 2
        question = "Kochasz mnie? 1) Nie 2) Tak"
    elif pytanie == 10:
        answer = 7
        question = "Które słowo nie jest przekleństwem? 1) Kuźwa 2) Kurwa 3) NenuuX 4) Debil 5) BitBot 6) Hujawej 7) Szajsung najlepszy 8) <@465137398863364097> 9) Kredki 10) Farbki"
    elif pytanie == 11:
        answer = 9
        question = "Jaki jest najlepszy komunikator? 1) Skuj dupe 2) Imprezord 3) Gówno Gówno 4) ŁacAp 5) Masażer 6) Srapczat 7) Tłiter 8) Fejsbug 9) Wiadomości 10) Pokémon Duel"
         
    await bot.send_message(ctx.message.channel, "{}".format(question))

    def guess_check(m):
        return m.content.isdigit()
        
    guess = await bot.wait_for_message(timeout=10.0, author=ctx.message.author, check=guess_check)
    if guess is None:
        fmt = 'Czas minął!'
        await bot.send_message(ctx.message.channel, fmt)
        return
    if int(guess.content) == answer:
        await bot.send_message(ctx.message.channel, 'Wygrałeś {}zł!'.format(random.randint(1, 1000000)))
    else:
        await bot.send_message(ctx.message.channel, 'Niepoprawna odpowiedź.')

@bot.command(pass_context=True)
async def Pokémon(ctx, pokemon):
    try:
        pokemon = pokemon.lower()
        await bot.send_file(ctx.message.channel, '/home/pi/bitbotdata/pokegifs/' + pokemon + '.gif')
    except:
        await bot.say('Hej, coś złego wystąpiło! Postaraj się to naprawić!')
        
@bot.command(pass_context=True)
async def Anonim(ctx, user : discord.Member, *, wiadomosc):
    try:
        await bot.send_message(user, wiadomosc)
        await bot.say("Wysłałem *" + wiadomosc + "* do **{}**.".format(user.name))
    except Exception as e:
        await bot.say("Wystąpił błąd: \n```{}: {}```\n".format(type(e).__name__, e))

@bot.command(pass_context=True)
async def Wyślij(ctx, user : discord.Member, *, wiadomosc):
    try:
        skladnia = "Hej, {} pisze: {}".format(ctx.message.author.name, wiadomosc)
        await bot.send_message(user, skladnia)
        await bot.say("Wysłałem *" + wiadomosc + "* do **{}**.".format(user.name))
    except Exception as e:
        await bot.say("Wystąpił błąd: \n```{}: {}```\n".format(type(e).__name__, e))

@bot.command(pass_context=True)
async def Powiedz(ctx, *, wiadomosc):
    await bot.say(wiadomosc)

@bot.command(pass_context=True)
async def Malina(ctx):
    ktory = random.randint(1, 5)
    if ktory == 1:
        await bot.send_file(ctx.message.channel, '/home/pi/bitbotdata/maliny.jpg')
    elif ktory == 2:
        await bot.send_file(ctx.message.channel, '/home/pi/bitbotdata/malinyzliscmi.jpg')
    elif ktory == 3:
        await bot.send_file(ctx.message.channel, '/home/pi/bitbotdata/dwiemaliny.jpg')
    elif ktory == 4:
        await bot.send_file(ctx.message.channel, '/home/pi/bitbotdata/trzymaliny.jpg')
    elif ktory == 5:
        await bot.send_file(ctx.message.channel, '/home/pi/bitbotdata/kilkamalin.jpg')

@bot.command(pass_context=True)
async def Wiadomość(ctx):
    ktory = random.randint(1, 12)
    if ktory == 1:
        await bot.send_file(ctx.message.channel, '/home/pi/bitbotdata/wiadomosci/1/wiadomosc')
    elif ktory == 2:
        await bot.send_file(ctx.message.channel, '/home/pi/bitbotdata/wiadomosci/2/wiadomosc')
    elif ktory == 3:
        await bot.send_file(ctx.message.channel, '/home/pi/bitbotdata/wiadomosci/3/wiadomosc')
    elif ktory == 4:
        await bot.send_file(ctx.message.channel, '/home/pi/bitbotdata/wiadomosci/4/wiadomosc')
    elif ktory == 5:
        await bot.send_file(ctx.message.channel, '/home/pi/bitbotdata/wiadomosci/5/wiadomosc')
    elif ktory == 6:
        await bot.send_file(ctx.message.channel, '/home/pi/bitbotdata/wiadomosci/6/wiadomosc')
    elif ktory == 7:
        await bot.send_file(ctx.message.channel, '/home/pi/bitbotdata/wiadomosci/7/wiadomosc')
    elif ktory == 8:
        await bot.send_file(ctx.message.channel, '/home/pi/bitbotdata/wiadomosci/8/wiadomosc')
    elif ktory == 9:
        await bot.send_file(ctx.message.channel, '/home/pi/bitbotdata/wiadomosci/9/wiadomosc')
    elif ktory == 10:
        await bot.send_file(ctx.message.channel, '/home/pi/bitbotdata/wiadomosci/10/wiadomosc')
    elif ktory == 11:
        await bot.send_file(ctx.message.channel, '/home/pi/bitbotdata/wiadomosci/11/wiadomosc')
    elif ktory == 12:
        await bot.send_file(ctx.message.channel, '/home/pi/bitbotdata/wiadomosci/12/wiadomosc')

@bot.command(pass_context=True)
async def BotLink(ctx):
    await bot.say("http://discord.gg/8hpE4xw")

@bot.command(pass_context=True)
async def Zaproś(ctx, kanal : discord.Channel):
    try:
        zaproszenie = await bot.create_invite(destination = kanal)
        await bot.say(zaproszenie)
    except Exception as e:
        await bot.say("Wystąpił błąd: \n```{}: {}```".format(type(e).__name__, e))

@bot.command(pass_context=True)
async def Gra(ctx, *, status):
    sp_vip(ctx.message.author.id)
    if vipczynie == 1:
        global rokurodzin
        dzisiaj = datetime.date.today()
        urodziny = datetime.date(rokurodzin, 4, 8)
        czasdourodzin = abs(urodziny - dzisiaj)
        status = status.replace("%servers%", str(len(bot.servers)))
        status = status.replace("%prefix%", prefix)
        status = status.replace("%urodziny%", str(czasdourodzin.days))
        await bot.change_presence(game=discord.Game(name=status, type=0))
        await bot.say("Status zmieniony na: *W grze **" + status + "***")
    else:
        await bot.say(nievip)

@bot.command(pass_context=True)
async def Streamuje(ctx, *, status):
    sp_vip(ctx.message.author.id)
    if vipczynie == 1:
        global rokurodzin
        dzisiaj = datetime.date.today()
        urodziny = datetime.date(rokurodzin, 4, 8)
        czasdourodzin = abs(urodziny - dzisiaj)
        status = status.replace("%servers%", str(len(bot.servers)))
        status = status.replace("%prefix%", prefix)
        status = status.replace("%urodziny%", str(czasdourodzin.days))
        await bot.change_presence(game=discord.Game(name=status, type=1))
        await bot.say("Status zmieniony na: *Streamuje **" + status + "***")
    else:
        await bot.say(nievip)

@bot.command(pass_context=True)
async def Słucha(ctx, *, status):
    sp_vip(ctx.message.author.id)
    if vipczynie == 1:
        global rokurodzin
        dzisiaj = datetime.date.today()
        urodziny = datetime.date(rokurodzin, 4, 8)
        czasdourodzin = abs(urodziny - dzisiaj)
        status = status.replace("%servers%", str(len(bot.servers)))
        status = status.replace("%prefix%", prefix)
        status = status.replace("%urodziny%", str(czasdourodzin.days))
        await bot.change_presence(game=discord.Game(name=status, type=2))
        await bot.say("Status zmieniony na: *Słucha **" + status + "***")
    else:
        await bot.say(nievip)

@bot.command(pass_context=True)
async def Ogląda(ctx, *, status):
    sp_vip(ctx.message.author.id)
    if vipczynie == 1:
        global rokurodzin
        dzisiaj = datetime.date.today()
        urodziny = datetime.date(rokurodzin, 4, 8)
        czasdourodzin = abs(urodziny - dzisiaj)
        status = status.replace("%servers%", str(len(bot.servers)))
        status = status.replace("%prefix%", prefix)
        status = status.replace("%urodziny%", str(czasdourodzin.days))
        await bot.change_presence(game=discord.Game(name=status, type=3))
        await bot.say("Status zmieniony na: *Ogląda **" + status + "***")
    else:
        await bot.say(nievip)

@bot.command(pass_context=True)
async def Szukaj(ctx, *, fraza):
    message = await bot.say("Szukam... :mag:")
    before = time.monotonic()
    for url in search(fraza):
        ping = (time.monotonic() - before) * 1000
        await bot.edit_message(message, url + " znalazłem w **{}ms**".format(str(floor(ping))))
        break

@bot.command(pass_context=True)
async def Pomoc(ctx, strona=None):
    if not strona == None:
        strona = int(strona)
    if strona == None or strona == 1:
        embed = discord.Embed(title="Pomoc", description="Strona 1/2", color=0xff0000)
        embed.add_field(name=prefix + "Spam <ilość spamu (liczba)> <spowolnienie (liczba)> <wiadomość (tekst)>", value="Spamuje wiadomościami.", inline=True)
        embed.add_field(name=prefix + "Anonim <użytkownik (użytkownik)> <wiadomość (tekst)>", value="Wyślij do kogoś wiadomość. Bez podpisu.", inline=True)
        embed.add_field(name=prefix + "SprawdźVIPa <użytkownik (użytkownik)>", value="Sprawdź, czy ktoś ma VIPa", inline=True)
        embed.add_field(name=prefix + "Wybierz <wybory (tekst, wybór nie może mieć spacji)>", value="Losuje jedno słowo z podanych.", inline=True)
        embed.add_field(name=prefix + "EmojiID <emotka (emoji)>", value="Sprawdza ID emotki. Działa tylko z emoji na serwerze.", inline=True)
        embed.add_field(name=prefix + "CustomEmoji <emotka z innego serwera (emoji lub tekst)> <id emotki z innego serwera (liczba)>", value="Wysyła emoji z innego serwera.", inline=True)
        embed.add_field(name=prefix + "Ping", value=":ping_pong: Pong!", inline=True)
        embed.add_field(name=prefix + "Gra/Słucha/Ogląda/Streamuje <gra (tekst)>", value="Ustawia grę.", inline=True)
        embed.add_field(name=prefix + "Napisz <kanał (kanał)> <wiadomość (tekst)>", value="Wysyła wiadomość do określonego kanału.", inline=True)
        embed.add_field(name=prefix + "Wiadomość", value="Wysyła wiadomość w pliku.", inline=True)
        embed.add_field(name=prefix + "Nazwa <użytkownik (użytkownik)> <nowa nazwa (tekst)>", value="Zmień nazwę użytkownika.", inline=True)
        embed.add_field(name=prefix + "Statystyki", value="Statystyki bota.", inline=True)
        embed.add_field(name=prefix + "LiczbaSerwerów", value="Liczba serwerów na których jestem.", inline=True)
        embed.add_field(name=prefix + "Wyślij <użytkownik (użytkownik)> <wiadomość (tekst)>", value="Wyślij użytkownikowi wiadomość. Z podpisem.", inline=True)
        embed.add_field(name=prefix + "Wiadomości", value="Wiadomości nadane za pomocą komendy {}Nadaj.".format(prefix), inline=True)
        embed.add_field(name=prefix + "Urodziny", value="Licznik dni do moich urodzin!", inline=True)
        embed.add_field(name=prefix + "Szukaj <fraza (tekst)>", value="Wyszukaj coś w Google.", inline=True)
        embed.add_field(name=prefix + "Pytanie <pytanie (tekst)>", value="Zapytaj ludzi pytaniem tak/nie.", inline=True)
        embed.add_field(name=prefix + "BotLink", value="Masz problem? Wykonaj tą komendę!", inline=True)
        embed.add_field(name=prefix + "LiveUptime", value="Czas bota na żywo.", inline=True)
        embed.add_field(name=prefix + "Odwróć <tekst (tekst)>", value="Odwróć tekst!", inline=True)
        embed.add_field(name=prefix + "Zaproś <kanał (kanał)>", value="Utwórz zaproszenie do serwera.", inline=True)
        embed.add_field(name=prefix + "Milionerzy", value="Sprawdź to. Nie polecam.", inline=True)
        embed.add_field(name=prefix + "Malina", value="Lubisz je?", inline=True)
        embed.add_field(name=prefix + "Embed <tekst (tekst)>", value="Zamiast się botować, wykonaj tą komendę.", inline=True)
    elif strona == 2:
        embed = discord.Embed(title="Pomoc", description="Strona 2/2", color=0xff0000)
        embed.add_field(name=prefix + "Powiedz <tekst (tekst)>", value="Powiem coś.", inline=True)
        embed.add_field(name=prefix + "Losuj <liczba1 (liczba)> <liczba2 (liczba)>", value="Wylosuj liczbę.", inline=True)
        embed.add_field(name=prefix + "LiteraPoLiterze <tekst (tekst)>", value="Bardzo fajna komenda!", inline=True)
        embed.add_field(name=prefix + "Nadaj <tekst (tekst)>", value="Nadaj coś!", inline=True)
        embed.add_field(name=prefix + "Informacje <użytkownik (użytkownik, opcjonalnie)>", value="Informacje o użytkowniku.", inline=True)
        embed.add_field(name=prefix + "DodajVIPa <użytkownik (użytkownik)>", value="Dodaj VIPa.", inline=True)
        embed.add_field(name=prefix + "Wykop <użytkownik (użytkownik)>", value="Wykop użytkownika.", inline=True)
        embed.add_field(name=prefix + "Zbanuj <użytkownik (użytkownik)> <powód (opcjonalnie, tekst)>", value="Zbanuj użytkownika.", inline=True)
        embed.add_field(name=prefix + "Konfiguruj", value="Więcej informacji w komendzie.", inline=True)
        embed.add_field(name=prefix + "Wyczyść <ilość (liczba)>", value="Czyści czat. Nie usuwa wiadomości sprzed 14 dni.", inline=True)
        embed.add_field(name=prefix + "Członkowie", value="Liczba członków serwera.", inline=True)
        embed.add_field(name=prefix + "Serwer", value="Informacje o serwerze.", inline=True)
    elif not strona == None or not strona == 1 or not strona == 2:
        embed = discord.Embed(title="Pomoc", description="Strona {}/2".format(str(strona)), color=0xff0000)
        embed.set_footer(text="Nie znaleziono strony!")
    await bot.say(embed=embed)

@bot.command(pass_context=True)
async def Informacje(ctx, *, user:discord.User=None):
    if user == None:
        user = ctx.message.author
    embed = discord.Embed(title="Użytkownik {}".format(user.display_name), description="Informacje", color=user.color)
    embed.add_field(name="Wyświetlam informacje o:", value="{}".format(user.name), inline=True)
    embed.add_field(name="Użytkownik jest:", value="{}".format(user.status), inline=True)
    embed.add_field(name="ID użytkownika:", value="{}".format(user.id), inline=True)
    embed.add_field(name="Użytkownik dołączył do serwera w:", value="{}".format(user.joined_at), inline=True)
    embed.add_field(name="Użytkownik stworzył konto w:", value="{}".format(user.created_at), inline=True)
    embed.add_field(name="Najwyższa rola użytkownika na tym serwerze:", value="{}".format(user.top_role), inline=True)
    embed.set_thumbnail(url=user.avatar_url)
    embed.set_footer(text=user.name)
    await bot.say(embed=embed)

@bot.command(pass_context=True)
async def Serwer(ctx):
    embed = discord.Embed(title="{}".format(ctx.message.server.name), description="Informacje")
    embed.add_field(name="ID serwera:", value="{}".format(str(ctx.message.server.id)), inline=True)
    embed.add_field(name="Ilość ról:", value="{}".format(str(len(ctx.message.server.roles))), inline=True)
    embed.add_field(name="Ludzi na serwerze:", value="{}".format(str(len([member for member in ctx.message.server.members if not member.bot]))), inline=True)
    embed.add_field(name="Botów na serwerze:", value="{}".format(str(len([member for member in ctx.message.server.members if member.bot]))), inline=True)
    embed.set_thumbnail(url=ctx.message.server.icon_url)
    embed.set_footer(text=ctx.message.server.name)
    await bot.say(embed=embed)

@bot.command(pass_context=True)
async def Nazwa(ctx, user: discord.Member, *, nazwa):
    try:
        if ctx.message.author.server_permissions.manage_nicknames:
            await bot.change_nickname(member=user, nickname=nazwa)
            await bot.add_reaction(ctx.message, "✅")
        else:
            await bot.say("Nie masz permisji do tego!")
            await bot.add_reaction(ctx.message, "❎")
    except Exception as e:
        await bot.say("Wystąpił błąd: \n```{}: {}```\n".format(type(e).__name__, e))
        await bot.add_reaction(ctx.message, "❎")

@bot.command(pass_context=True)
async def Wykop(ctx, user: discord.Member):
    if ctx.message.author.server_permissions.kick_members:
        try:
            await bot.kick(user)
            await bot.add_reaction(ctx.message, "✅")
        except Exception as e:
            await bot.say("Wystąpił błąd: \n```{}: {}```\n".format(type(e).__name__, e))
            await bot.add_reaction(ctx.message, "❎")
    else:
        await bot.say("Nie masz permisji do tego!")
        await bot.add_reaction(ctx.message, "❎")

@bot.command(pass_context=True)
async def Zbanuj(ctx, user: discord.Member, *, powod=None):
    if ctx.message.author.server_permissions.ban_members:
        try:
            await bot.ban(user)
            await bot.add_reaction(ctx.message, "✅")
        except Exception as e:
            await bot.say("Wystąpił błąd: \n```{}: {}```\n".format(type(e).__name__, e))
            await bot.add_reaction(ctx.message, "❎")
    else:
        await bot.say("Nie masz permisji do tego!")
        await bot.add_reaction(ctx.message, "❎")

@bot.command(pass_context=True)
async def Wyczyść(ctx, ilosc : int):
    try:
        if not ctx.message.author.server_permissions.manage_messages:
            await bot.say("Nie masz permisji do tego!")
            return
        await bot.delete_message(ctx.message)
        wiadomosci = []
        async for message in bot.logs_from(ctx.message.channel, limit=ilosc):
            wiadomosci.append(message)
        await bot.delete_messages(wiadomosci)
        msg = await bot.say("Usunąłem {} wiadomości!".format(str(len(wiadomosci))))
        await asyncio.sleep(5)
        await bot.delete_message(msg)
    except Exception as e:
            await bot.say("Wystąpił błąd: \n```{}: {}```\n".format(type(e).__name__, e))            

async def uptime():
    await bot.wait_until_ready()
    global uruchomiony
    uruchomiony = str(datetime.datetime.now())
    hours = 0
    minutes = 0
    seconds = 0
    global uptimemsg
    uptimemsg = "0:0:0"
    while not bot.is_closed:
        await asyncio.sleep(1)
        seconds += 1
        if seconds == 60:
            minutes += 1
            seconds = 0
        if minutes == 60:
            hours += 1
            minutes = 0
        if hours == 0:
            uptimemsg = str(minutes) + ":" + str(seconds)
        else:
            uptimemsg = str(hours) + ":" + str(minutes) + ":" + str(seconds)

bot.add_cog(Komendy(bot))

bot.loop.create_task(uptime())

token = sys.argv[1]

bot.run(token)
