import time
poczatek = time.monotonic()

class Konfiguracje:

    def JoinDM(serwer):
        try:
            plik = open("JoinDM" + serwer, "r")
            return plik.read()
        except:
            return "null"

    def RemoveDM(serwer):
        try:
            plik = open("RemoveDM" + serwer, "r")
            return plik.read()
        except:
            return "null"
    
    def Jezyk(serwer):
        try:
            plik = open("Jezyk" + serwer, "r")
            return plik.read()
        except:
            return "null"

    def UstawRemoveDM(serwer, wartosc):
        plik = open("RemoveDM" + serwer, "w")
        plik.write(wartosc)
        plik.close()

    def UstawJoinDM(serwer, wartosc):
        plik = open("JoinDM" + serwer, "w")
        plik.write(wartosc)
        plik.close()
    
    def UstawJezyk(serwer, wartosc):
        plik = open("Lang" + serwer, "w")
        plik.write(wartosc)
        plik.close()

import os
token = os.environ.get('TOKEN')

import discord
from discord.ext import commands
from discord.ext.commands import Bot
import asyncio
import random
import psutil
import requests
import datetime
import re
import yaml
from math import floor
from googlesearch import search

zaufani = [233592407902388224]
nievip = "Hmm... Wygląda na to, że nie jesteś programistą BitBota."

global rokrodzin
rokurodzin = 2021

prefix = "$$"

intents = discord.Intents.default()
intents.typing = False
intents.presences = False

bot = commands.Bot(command_prefix=prefix, intents=intents, case_insensitive=True)

djezyki = {}

for i in os.listdir("lang"):
    ld = yaml.load(i, Loader=yaml.FullLoader)
    {i.replace(".yml", ""): ld}.update(djezyki)



@bot.event
async def on_ready():
    global uruchomionyw
    uruchomionyw = str(floor((time.monotonic() - poczatek) * 1000)) + "ms"
    print("BitBot jest gotowy.")

@bot.event
async def on_member_join(member):
    if not Konfiguracje.JoinDM(member.guild.id) == "null":
        await member.send(Konfiguracje.JoinDM(member.guild.id))

@bot.event
async def on_member_remove(member):
    if not Konfiguracje.RemoveDM(member.guild.id) == "null":
        await member.send(Konfiguracje.RemoveDM(member.guild.id))

@bot.event
async def on_command_error(ctx, exception):
    await ctx.send("Wystąpił błąd: \n```{}: {}```\n".format(type(e).__name__, e))
        
@bot.command(pass_context=True)
async def LiteraPoLiterze(ctx, *, tekst):
    licznik = 1
    wiadomosc = str(tekst[0])
    msg = await ctx.send(wiadomosc)
    while licznik < len(tekst):
        await asyncio.sleep(0.5)
        wiadomosc = wiadomosc + str(tekst[licznik])
        await msg.edit(content=wiadomosc)
        licznik = licznik + 1

@bot.command(pass_context=True)
async def Urodziny(ctx):
    global rokurodzin
    dzisiaj = datetime.date.today()
    urodziny = datetime.date(rokurodzin, 4, 8)
    czasdourodzin = abs(urodziny - dzisiaj)
    lata = int(str(abs(datetime.date(2018, 4, 8) - dzisiaj).days / 365)[0])
    if lata > 1:
        latastr = str(lata) + " lata"
    else:
        latastr = str(lata) + " rok"
    if czasdourodzin.days == 0:
        await ctx.reply("Urodziny są dzisiaj! :tada: {}!".format(latastr))
    else:
        await ctx.reply("Do urodzin pozostało {} dni. Obecnie BitBot ma {}.".format(str(czasdourodzin.days), latastr))

@bot.command(pass_context=True)
async def Wybierz(ctx, *wybory):
    await ctx.reply("Hmm... Wybieram **{}**.".format(str(random.choice(wybory))))

@bot.command(pass_context=True)
async def Embed(ctx, *, tekst):
    embed = discord.Embed(title=str(tekst))
    await ctx.send(embed=embed)

@bot.command(pass_context=True)
async def Losuj(ctx, minimalny : int, maksymalny : int):
    await ctx.reply("Wylosowana liczba to {}.".format(str(random.randint(minimalny, maksymalny))))

@bot.command(pass_context=True)
async def EmojiID(ctx, emoji : discord.Emoji):
    await ctx.reply("A ID emotki {} to... {}".format(str(emoji), str(emoji.id)))

@bot.command(pass_context=True)
async def Ping(ctx):
    before = time.monotonic()
    message = await ctx.reply("Czekaj...")
    ping = (time.monotonic() - before) * 1000
    await message.edit(content="Pong! :ping_pong: **{}ms**".format(str(floor(ping))))
 
@bot.command(pass_context=True)
async def Serwery(ctx):
    if ctx.message.author.id in zaufani:
        await ctx.reply("Wysłałem listę serwerów do ciebie.")
        wysl = ""
        serwery = list(bot.guilds)
        for serwer in serwery:
            wysl += serwer.name + "\n"
        await ctx.message.author.send(wysl)

@bot.command(pass_context=True)
async def LiczbaSerwerów(ctx):
    await ctx.reply("<@432565925934268416> jest na {} serwerach.".format(str(len(bot.guilds))))

@bot.command(pass_context=True)
async def Odwróć(ctx, *, tekst : str):
    tekst = tekst[::-1]
    await ctx.reply(tekst)
    
@bot.command(pass_context=True)
async def Członkowie(ctx):
    ludziel = []
    botyl = []
    for member in ctx.message.guild.members:
        if not member.bot:
            ludziel.append(member)
        else:
            botyl.append(member)
    ludzie = len(ludziel)
    boty = len(botyl)
    jeden_procent = 100 / (ludzie + boty)
    procent_ludzi = ludzie * jeden_procent
    procent_botów = boty * jeden_procent
    await ctx.reply("Ludzi jest {} ({}%), a botów jest {} ({}%).".format(ludzie, floor(procent_ludzi), boty, floor(procent_botów)))

@bot.command(pass_context=True)
async def Statystyki(ctx):
    global uptimemsg
    global uruchomiony
    global uruchomionyw
    embed = discord.Embed(title="Statystyki")
    embed.add_field(name="Prefix", value="{}".format(prefix), inline=True)
    embed.add_field(name="Jestem online", value="{}".format(uptimemsg), inline=True)
    embed.add_field(name="Uruchomiony od", value="{}".format(uruchomiony), inline=True)
    embed.add_field(name="Czas uruchomienia", value="{}".format(uruchomionyw), inline=True)
    embed.add_field(name="Strefa czasowa", value="{}".format(str(datetime.datetime.now(datetime.timezone.utc).astimezone().tzname())), inline=True)
    embed.add_field(name="Obciążenie procesora", value="{}%".format(str(psutil.cpu_percent())), inline=True)
    embed.add_field(name="Twórca", value="Minecon724#2477", inline=True)
    await ctx.reply(embed=embed)

@bot.command(pass_context=True)
async def Pytanie(ctx, *, zapytaj):
    msg = await ctx.send(zapytaj)
    await msg.add_reaction("❎")
    await msg.add_reaction("✅")

@bot.command(pass_context=True)
async def Milionerzy(ctx):
    pytanie = random.randint(1, 12)
    if pytanie == 1:
        answer = 2
        question = "Co jest hitem tego lata: 1) gówno 2) memy 3) szajsung galaxy s9 4) srajfon x"
    elif pytanie == 2:
        answer = 4
        question = "Jaki telefon jest najlepszy na świecie: 1) srajfon x 2) szajsung galaxy s9 3) hujawej p20 pro 4) nokija 3310 5) komputer"
    elif pytanie == 3:
        answer = 4 or 3
        question = "Jaki komputer jest najlepszy: 1) ajmak 2) hujawej 3) BitBot 4) składak"
    elif pytanie == 4:
        answer = 2
        question = "Co lepsze: 1) ENWIDJA GjeFordze 1080 2) Jintel HD Grafiks 620 3) AEMDE Radełon piećsetczydziesci"
    elif pytanie == 5:
        answer = 2
        question = "Czy jestem debilem: 1) Nie 2) Tak"
    elif pytanie == 6:
        answer = 1 or 2
        question = "Co lepsze: 1) BitBot 2) BitBot"
    elif pytanie == 7:
        answer = 2 or 1
        question = "Żyjesz? 1) Nie 2) Nie 3) Tak"
    elif pytanie == 8:
        answer = 4
        question = "Najlepszy tekst wszech czasów: 1) Chyba ty 2) Spierdalaj 3) Śmieć 4) BitBot 5) Gówniarz 6) Chuj 7) a 8) Milionerzy 9) Dolary 10) Chorwacja 11) Kredki"
    elif pytanie == 9:
        answer = 2
        question = "Kochasz mnie? 1) Nie 2) Tak"
    elif pytanie == 10:
        answer = 5
        question = "Które słowo nie jest przekleństwem? 1) Kuźwa 2) Kurwa 3) a 4) Debil 5) BitBot 6) Masza"
    elif pytanie == 11:
        answer = 9
        question = "Jaki jest najlepszy komunikator? 1) Skuj dupe 2) Imprezord 3) Gówno Gówno 4) ŁacAp 5) Masażer 6) Srapczat 7) Tłiter 8) Fejsbug 9) Wiadomości"
    elif pytanie == 12:
        answer = 1 or 2
        question = "Kim jesteś? 1) CHUJEM czy 2) DEBILEM?"
    await ctx.reply("{}".format(question))

    def guess_check(m):
        return m.content.isdigit() and m.author == ctx.message.author and m.channel == ctx.message.channel
        
    try:
        guess = await bot.wait_for('message', timeout=15.0, check=guess_check)
    except asyncio.TimeoutError:
        await ctx.reply("Czas minął!")
        return
    if int(guess.content) == answer:
        await guess.reply('Wygrałeś {}zł!'.format(random.randint(1, 1000000)))
    else:
        await guess.reply('Niepoprawna odpowiedź.')

@bot.command(pass_context=True)
async def ZgadnijLiczbę(ctx, max:int=None):
    def guess_check(m):
        return m.content.isdigit() and m.author == ctx.message.author and m.channel == ctx.message.channel
    if max is None:
        liczba = random.randint(0, 1000)
    else:
        liczba = random.randint(0, max)
    zgadnieta = False
    proby = 0
    await ctx.reply("Zacznij zgadywać.")
    while not zgadnieta:
        try:
            strzal = await bot.wait_for('message', timeout=15.0, check=guess_check)
        except asyncio.TimeoutError:
            await ctx.reply("Czas minął!")
            return
        proby = proby + 1
        if int(strzal.content) == liczba:
            if proby == 1:
                await strzal.reply("Gratulacje! Odgadłeś liczbę! Zajęło ci to 1 próbę.")
            elif proby < 5:
                await strzal.reply("Gratulacje! Odgadłeś liczbę! Zajęło ci to {} próby.".format(str(proby)))
            else:
                await strzal.reply("Gratulacje! Odgadłeś liczbę! Zajęło ci to {} prób.".format(str(proby)))
            zgadnieta = True
        elif int(strzal.content) < liczba:
            await strzal.reply("Wylosowana liczba jest większa.")
        elif int(strzal.content) > liczba:
            await strzal.reply("Wylosowana liczba jest mniejsza.")
        
@bot.command(pass_context=True)
async def Powiedz(ctx, *, wiadomosc):
    await ctx.reply(wiadomosc)

@bot.command(pass_context=True)
async def BotLink(ctx):
    await ctx.reply("http://discord.gg/8hpE4xw")

@bot.command(pass_context=True)
async def Zaproś(ctx, kanal):
    if not type(kanal) == discord.TextChannel:
        raise discord.InvalidArgument("Argument musi być kanałem tekstowym")
    zaproszenie = await kanal.create_invite()
    await ctx.reply(zaproszenie)

@bot.command(pass_context=True)
async def Gra(ctx, *, status):
    if ctx.message.author.id in zaufani:
        global rokurodzin
        dzisiaj = datetime.date.today()
        urodziny = datetime.date(rokurodzin, 4, 8)
        czasdourodzin = abs(urodziny - dzisiaj)
        status = status.replace("%servers%", str(len(bot.guilds)))
        status = status.replace("%prefix%", prefix)
        status = status.replace("%urodziny%", str(czasdourodzin.days))
        await bot.change_presence(activity=discord.Game(name=status))
        await ctx.reply("Status zmieniony na: *W grze **" + status + "***")
    else:
        await ctx.reply(nievip)

@bot.command(pass_context=True)
async def Streamuje(ctx, *, status):
    if ctx.message.author.id in zaufani:
        global rokurodzin
        dzisiaj = datetime.date.today()
        urodziny = datetime.date(rokurodzin, 4, 8)
        czasdourodzin = abs(urodziny - dzisiaj)
        status = status.replace("%servers%", str(len(bot.guilds)))
        status = status.replace("%prefix%", prefix)
        status = status.replace("%urodziny%", str(czasdourodzin.days))
        await bot.change_presence(activity=discord.Game(name=status, type=discord.ActivityType.streaming))
        await ctx.reply("Status zmieniony na: *Streamuje **" + status + "***")
    else:
        await ctx.reply(nievip)

@bot.command(pass_context=True)
async def Słucha(ctx, *, status):
    if ctx.message.author.id in zaufani:
        global rokurodzin
        dzisiaj = datetime.date.today()
        urodziny = datetime.date(rokurodzin, 4, 8)
        czasdourodzin = abs(urodziny - dzisiaj)
        status = status.replace("%servers%", str(len(bot.guilds)))
        status = status.replace("%prefix%", prefix)
        status = status.replace("%urodziny%", str(czasdourodzin.days))
        await bot.change_presence(activity=discord.Game(name=status, type=discord.ActivityType.listening))
        await ctx.reply("Status zmieniony na: *Słucha **" + status + "***")
    else:
        await ctx.reply(nievip)

@bot.command(pass_context=True)
async def Ogląda(ctx, *, status):
    if ctx.message.author.id in zaufani:
        global rokurodzin
        dzisiaj = datetime.date.today()
        urodziny = datetime.date(rokurodzin, 4, 8)
        czasdourodzin = abs(urodziny - dzisiaj)
        status = status.replace("%servers%", str(len(bot.servers)))
        status = status.replace("%prefix%", prefix)
        status = status.replace("%urodziny%", str(czasdourodzin.days))
        await bot.change_presence(activity=discord.Game(name=status, type=discord.ActivityType.watching))
        await ctx.reply("Status zmieniony na: *Ogląda **" + status + "***")
    else:
        await ctx.reply(nievip)

@bot.command(pass_context=True)
async def Szukaj(ctx, *, fraza):
    message = await ctx.reply("Szukam... :mag:")
    before = time.monotonic()
    for url in search(fraza):
        ping = (time.monotonic() - before) * 1000
        await message.edit(content="{}\nZnalazłem w **{}ms**".format(url, str(floor(ping))))
        break

@bot.command(pass_context=True)
async def Pomoc(ctx, strona=None):
    if not strona == None:
        strona = int(strona)
    if strona == None or strona == 1:
        embed = discord.Embed(title="To jest Twoja pomoc, {}!".format(ctx.message.author.name), description="Strona 1/2", color=0xff0000)
        embed.add_field(name=prefix + "Wybierz <wybory (tekst, wybór nie może mieć spacji)>", value="Losuje jedno słowo z podanych.", inline=True)
        embed.add_field(name=prefix + "EmojiID <emotka (emoji)>", value="Sprawdza ID emotki. Działa tylko z emoji na serwerze.", inline=True)
        embed.add_field(name=prefix + "Ping", value=":ping_pong: Pong!", inline=True)
        embed.add_field(name=prefix + "Gra/Słucha/Ogląda/Streamuje <gra (tekst)>", value="Ustawia grę.", inline=True)
        embed.add_field(name=prefix + "Nazwa <użytkownik (użytkownik)> <nowa nazwa (tekst)>", value="Zmień nazwę użytkownika.", inline=True)
        embed.add_field(name=prefix + "Statystyki", value="Statystyki bota.", inline=True)
        embed.add_field(name=prefix + "LiczbaSerwerów", value="Liczba serwerów na których jestem.", inline=True)
        embed.add_field(name=prefix + "Serwery", value="Lista serwerów, na których jestem. Nie bój się, nikt nie ma do nich dostępu.", inline=True)
        embed.add_field(name=prefix + "Urodziny", value="Licznik dni do moich urodzin!", inline=True)
        embed.add_field(name=prefix + "Szukaj <fraza (tekst)>", value="Wyszukaj coś w Google.", inline=True)
        embed.add_field(name=prefix + "Pytanie <pytanie (tekst)>", value="Zapytaj ludzi pytaniem tak/nie.", inline=True)
        embed.add_field(name=prefix + "BotLink", value="Masz problem? Wykonaj tą komendę!", inline=True)
        embed.add_field(name=prefix + "Odwróć <tekst (tekst)>", value="Odwróć tekst!", inline=True)
        embed.add_field(name=prefix + "Zaproś <kanał (kanał)>", value="Utwórz zaproszenie do serwera.", inline=True)
        embed.add_field(name=prefix + "Milionerzy", value="Sprawdź to. Nie polecam.", inline=True)
        embed.add_field(name=prefix + "Embed <tekst (tekst)>", value="Zamiast się botować, wykonaj tą komendę.", inline=True)
        embed.add_field(name=prefix + "Powiedz <tekst (tekst)>", value="Powiem coś.", inline=True)
        embed.add_field(name=prefix + "Losuj <liczba1 (liczba)> <liczba2 (liczba)>", value="Wylosuj liczbę.", inline=True)
        embed.add_field(name=prefix + "LiteraPoLiterze <tekst (tekst)>", value="Bardzo fajna komenda!", inline=True)
        embed.add_field(name=prefix + "Informacje <użytkownik (użytkownik, opcjonalnie)>", value="Informacje o użytkowniku.", inline=True)
    elif strona == 2:
        embed = discord.Embed(title="Pomoc", description="Strona 2/2", color=0xff0000)
        embed.add_field(name=prefix + "Wykop <użytkownik (użytkownik)>", value="Wykop użytkownika.", inline=True)
        embed.add_field(name=prefix + "Zbanuj <użytkownik (użytkownik)>", value="Zbanuj użytkownika.", inline=True)
        embed.add_field(name=prefix + "Wyczyść <ilość (liczba)>", value="Czyści czat. Nie usuwa wiadomości sprzed 14 dni.", inline=True)
        embed.add_field(name=prefix + "Członkowie", value="Liczba członków serwera.", inline=True)
        embed.add_field(name=prefix + "Serwer", value="Informacje o serwerze.", inline=True)
        embed.add_field(name=prefix + "ZgadnijLiczbę <maksymalna (liczba, opcjonalnie)>", value="Zgadnij liczbę!", inline=True)
        embed.add_field(name=prefix + "Konfiguruj", value="Konfiguruj serwer i bota. Pomoc uzyskasz po wpisaniu komendy.", inline=True)
    elif not strona == None or not strona == 1 or not strona == 2:
        embed = discord.Embed(title="Pomoc", description="Strona {}/2".format(str(strona)), color=0xff0000)
        embed.set_footer(text="Nie znaleziono strony!")
    await ctx.reply(embed=embed)

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
    embed.set_footer(text=user)
    await ctx.reply(embed=embed)

@bot.command(pass_context=True)
async def Serwer(ctx):
    embed = discord.Embed(title="{}".format(ctx.message.guild.name), description="Informacje")
    embed.add_field(name="ID serwera:", value="{}".format(str(ctx.message.guild.id)), inline=True)
    embed.add_field(name="Ilość ról:", value="{}".format(str(len(ctx.message.guild.roles))), inline=True)
    embed.add_field(name="Ludzi na serwerze:", value="{}".format(str(len([member for member in ctx.message.guild.members if not member.bot]))), inline=True)
    embed.add_field(name="Botów na serwerze:", value="{}".format(str(len([member for member in ctx.message.guild.members if member.bot]))), inline=True)
    embed.set_thumbnail(url=ctx.message.guild.icon_url)
    embed.set_footer(text=ctx.message.guild.name)
    await ctx.reply(embed=embed)

@bot.command(pass_context=True)
async def Nazwa(ctx, user: discord.Member, *, nazwa):
    if ctx.message.author.guild_permissions.manage_nicknames:
        await user.edit(nick=nazwa)
        await ctx.message.add_reaction("✅")
    else:
        await ctx.reply("Nie masz permisji do tego!")
        await ctx.message.add_reaction("❎")

@bot.command(pass_context=True)
async def Wykop(ctx, user: discord.Member, *, powod=None):
    if ctx.message.author.guild_permissions.kick_members:
        await user.kick(reason=powod)
        await ctx.message.add_reaction("✅")
    else:
        await ctx.reply("Nie masz permisji do tego!")
        await ctx.message.add_reaction("❎")

@bot.command(pass_context=True)
async def Zbanuj(ctx, user: discord.Member, *, powod=None):
    if ctx.message.author.guild_permissions.ban_members:
        await user.ban(reason=powod)
        await ctx.message.add_reaction("✅")
    else:
        await ctx.reply("Nie masz permisji do tego!")
        await ctx.message.add_reaction("❎")

@bot.command(pass_context=True)
async def Wyczyść(ctx, ilosc : int):
    if not ctx.message.author.guild_permissions.manage_messages:
        await ctx.reply("Nie masz permisji do tego!")
        return
    await ctx.message.delete()
    await ctx.message.channel.purge(limit=ilosc, bulk=True)
    msg = await ctx.send("Usunąłem {} wiadomości!".format(str(ilosc)))
    await msg.delete(delay=5)
            
@bot.command(pass_context=True)
async def Konfiguruj(ctx, co=None, *, wartosc=None):
    if not ctx.message.author.guild_permissions.manage_guild:
        await ctx.reply("Nie masz permisji do tego!")
        return
    if co == None:
        embed = discord.Embed(title="Konfiguruj bota:")
        embed.add_field(name="joindm", value="Prywatna wiadomość do nowego członka serwera.", inline=True)
        embed.add_field(name="removedm", value="Prywatna wiadomość do członka opuszczającego serwer.", inline=True)
        embed.add_field(name="lang", value="Ustaw język.", inline=True)
        await ctx.reply(embed=embed)
    elif co == "joindm" or co == "removedm" or co == "lang":
        if wartosc == None:
            embed = discord.Embed(title="Konfiguruj bota:")
            if co == "joindm":
                embed.add_field(name="Wartość to:", value="{}".format(Konfiguracje.JoinDM(str(ctx.message.guild.id))), inline=True)
            elif co == "removedm":
                embed.add_field(name="Wartość to:", value="{}".format(Konfiguracje.RemoveDM(str(ctx.message.guild.id))), inline=True)
            elif co == "lang":
                embed.add_field(name="Wartość to:", value="{}".format(Konfiguracje.RemoveDM(str(ctx.message.guild.id))), inline=True)
            embed.set_footer(text="Jeżeli chcesz ustawić wartość, użyj *{}Konfiguruj {} <wartość>*.".format(prefix, co))
            await ctx.reply(embed=embed)
            return
        l = str(wartosc).lower()
        if co == "joindm":
            Konfiguracje.UstawJoinDM(str(ctx.message.guild.id), wartosc)
        elif co == "removedm":
            Konfiguracje.UstawRemoveDM(str(ctx.message.guild.id), wartosc)
        elif co == "lang":
            Konfiguracje.UstawJezyk(str(ctx.message.guild.id), wartosc)
            if not wartosc in djezyki.keys():
                await ctx.message.reply("Dostepne jezyki: " + ', '.join(djezyki.keys()))
                return
        await ctx.message.add_reaction("✅")

            
async def uptime():
    await bot.wait_until_ready()
    global uruchomiony
    uruchomiony = str(datetime.datetime.now())
    hours = 0
    minutes = 0
    seconds = 0
    global uptimemsg
    uptimemsg = "0:0:0"
    while not bot.is_closed():
        await asyncio.sleep(1)
        if seconds % 20 == 0:
            typ = random.choice([discord.ActivityType.playing, discord.ActivityType.listening, discord.ActivityType.streaming, discord.ActivityType.watching])
            status = random.choice([discord.Status.idle, discord.Status.dnd, discord.Status.online])
            await bot.change_presence(status=status, activity=discord.Game(name="{} serwerów | $$Pomoc".format(str(len(bot.guilds))), type=typ))
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

bot.loop.create_task(uptime())
bot.remove_command('help')
bot.run(token)
