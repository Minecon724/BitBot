# Hej, poczekaj!
# Mam ci coś do powiedzenia!
# Po pierwsze, wersja na Heroku jest bardzo okrojona.
# Po drugie, nie ukradniesz mi tokenu.
# Po trzecie, pewnie skopiujesz ten kod ;)
# No dobra, to jest kod.

class Konfiguracje:

    def JoinDM(serwer):
        try:
            plik = open(serwer, "r")
            return plik.read()
        except:
            return "null"
        plik.close()

    def RemoveDM(serwer):
        try:
            plik = open(serwer, "r")
            return plik.read()
        except:
            return "null"
        plik.close()

    def UstawRemoveDM(serwer, wartosc):
        plik = open(serwer, "w")
        plik.write(wartosc)
        plik.close()

    def UstawJoinDM(serwer, wartosc):
        plik = open(serwer, "w")
        plik.write(wartosc)
        plik.close()

import time
poczatek = time.monotonic()
import os
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

zaufani = ["233592407902388224"]
nievip = "Hmm... Wygląda na to, że nie jesteś programistą BitBota."

global rokrodzin
rokurodzin = 2019

prefix = "$$"

bot = commands.Bot(command_prefix=prefix)

global spamy
spamy = 0

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
    if ctx.message.author.id in zaufani:
        msg = await bot.say(uptimemsg)
        while True:
            await asyncio.sleep(1)
            await bot.edit_message(msg, uptimemsg)
    else:
        await bot.say(nievip)

@bot.command(pass_context=True)
async def kek(ctx):
    await bot.say("Hey I'm MEE6, the Discord bot!")

@bot.command(pass_context=True)
async def Spam(ctx, ilosc : int, cooldown : int, *, wiadomosc : str):
    licznik = 0
    global spamy
    while licznik < ilosc:
        await bot.say(wiadomosc)
        licznik = licznik + 1
        spamy = spamy + 1
        await asyncio.sleep(cooldown)

@bot.command(pass_context=True)
async def Serwery(ctx):
    serwery = list(bot.servers)
    if ctx.message.author.id == "233592407902388224":
        for x in range(len(serwery)):
            await bot.send_message(ctx.message.author, str(serwery[x-1].name))
            await bot.say("Wysłałem listę serwerów do ciebie.")

@bot.command(pass_context=True)
async def LiczbaSerwerów(ctx):
    await bot.say("<@432565925934268416> jest na {} serwerach.".format(str(len(bot.servers))))

@bot.command(pass_context=True)
async def Odwróć(ctx, *, tekst : str):
    tekst = tekst[::-1]
    await bot.say(tekst)
    
@bot.command(pass_context=True)
async def Członkowie(ctx):
    ludzie = len([member for member in ctx.message.server.members if not member.bot])
    boty = len([member for member in ctx.message.server.members if member.bot])
    jeden_procent = 100 / (ludzie + boty)
    procent_ludzi = ludzie * jeden_procent
    procent_botów = boty * jeden_procent
    await bot.say("Ludzi jest {} ({}%), a botów jest {} ({}%).".format(ludzie, floor(procent_ludzi), boty, floor(procent_botów)))

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
    embed.add_field(name="Strefa czasowa", value="{}".format(str(datetime.datetime.now(datetime.timezone.utc).astimezone().tzname())), inline=True)
    embed.add_field(name="Obciążenie procesora", value="{}".format(str(psutil.cpu_percent())), inline=True)
    embed.add_field(name="Twórca", value="Minecon724#2556", inline=True)
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
    pytanie = random.randint(1, 12)
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
        answer = 1 or 2
        question = "Co lepsze: 1) Kokaina 2) Marihuana"
    elif pytanie == 7:
        answer = 2
        question = "Co się robi: 1) zupe 2) loda 3) mleko 4) wode 5) telefony 6) płyty czy 7) gówno?"
    elif pytanie == 8:
        answer = 4
        question = "Najlepszy tekst wszech czasów: 1) Chyba ty 2) Spierdalaj 3) Śmieć 4) BitBot 5) Gówniarz 6) Chuj 7) a 8) Milionerzy 9) Dolary 10) Chorwacja 11) Kredki"
    elif pytanie == 9:
        answer = 2
        question = "Kochasz mnie? 1) Nie 2) Tak"
    elif pytanie == 10:
        answer = 2
        question = "Które słowo nie jest przekleństwem? 1) Kuźwa 2) Kurwa 3) a 4) Debil 5) BitBot 6) Hujawej 7) Szajsung najlepszy 8) Masza 9) Kredki 10) Farbki"
    elif pytanie == 11:
        answer = 9
        question = "Jaki jest najlepszy komunikator? 1) Skuj dupe 2) Imprezord 3) Gówno Gówno 4) ŁacAp 5) Masażer 6) Srapczat 7) Tłiter 8) Fejsbug 9) Wiadomości 10) Pokémon Duel"
    elif pytanie == 12:
        answer = 1
        question = "Kim jesteś? 1) CHUJEM czy 2) DEBILEM?"
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
async def ZgadnijLiczbę(ctx, max:int=None):
    def guess_check(m):
        return m.content.isdigit()
    if max is None:
        liczba = random.randint(0, 1000)
    else:
        liczba = random.randint(0, max)
    zgadnieta = False
    proby = 0
    await bot.say("Zacznij zgadywać.")
    while not zgadnieta:
        strzal = await bot.wait_for_message(timeout=15.0, author=ctx.message.author, check=guess_check)
        proby = proby + 1
        if int(strzal.content) == liczba:
            if proby == 1:
                await bot.say("Gratulacje! Odgadłeś liczbę! Zajęło ci to 1 próbę.")
            elif proby < 5:
                await bot.say("Gratulacje! Odgadłeś liczbę! Zajęło ci to {} próby.".format(str(proby)))
            else:
                await bot.say("Gratulacje! Odgadłeś liczbę! Zajęło ci to {} prób.".format(str(proby)))
            zgadnieta = True
        elif int(strzal.content) < liczba:
            await bot.say("Wylosowana liczba jest większa.")
        elif int(strzal.content) > liczba:
            await bot.say("Wylosowana liczba jest mniejsza.")
        
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
    if ctx.message.author.id in zaufani:
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
    if ctx.message.author.id in zaufani:
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
    if ctx.message.author.id in zaufani:
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
    if ctx.message.author.id in zaufani:
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
        embed.add_field(name=prefix + "Wybierz <wybory (tekst, wybór nie może mieć spacji)>", value="Losuje jedno słowo z podanych.", inline=True)
        embed.add_field(name=prefix + "EmojiID <emotka (emoji)>", value="Sprawdza ID emotki. Działa tylko z emoji na serwerze.", inline=True)
        embed.add_field(name=prefix + "CustomEmoji <emotka z innego serwera (emoji lub tekst)> <id emotki z innego serwera (liczba)>", value="Wysyła emoji z innego serwera.", inline=True)
        embed.add_field(name=prefix + "Ping", value=":ping_pong: Pong!", inline=True)
        embed.add_field(name=prefix + "Gra/Słucha/Ogląda/Streamuje <gra (tekst)>", value="Ustawia grę.", inline=True)
        embed.add_field(name=prefix + "Napisz <kanał (kanał)> <wiadomość (tekst)>", value="Wysyła wiadomość do określonego kanału.", inline=True)
        embed.add_field(name=prefix + "Nazwa <użytkownik (użytkownik)> <nowa nazwa (tekst)>", value="Zmień nazwę użytkownika.", inline=True)
        embed.add_field(name=prefix + "Statystyki", value="Statystyki bota.", inline=True)
        embed.add_field(name=prefix + "LiczbaSerwerów", value="Liczba serwerów na których jestem.", inline=True)
        embed.add_field(name=prefix + "Wyślij <użytkownik (użytkownik)> <wiadomość (tekst)>", value="Wyślij użytkownikowi wiadomość. Z podpisem.", inline=True)
        embed.add_field(name=prefix + "Serwery", value="Lista serwerów, na których jestem. Nie bój się, nikt nie ma do nich dostępu.", inline=True)
        embed.add_field(name=prefix + "Urodziny", value="Licznik dni do moich urodzin!", inline=True)
        embed.add_field(name=prefix + "Szukaj <fraza (tekst)>", value="Wyszukaj coś w Google.", inline=True)
        embed.add_field(name=prefix + "Pytanie <pytanie (tekst)>", value="Zapytaj ludzi pytaniem tak/nie.", inline=True)
        embed.add_field(name=prefix + "BotLink", value="Masz problem? Wykonaj tą komendę!", inline=True)
        embed.add_field(name=prefix + "LiveUptime", value="Czas bota na żywo.", inline=True)
        embed.add_field(name=prefix + "Odwróć <tekst (tekst)>", value="Odwróć tekst!", inline=True)
        embed.add_field(name=prefix + "Zaproś <kanał (kanał)>", value="Utwórz zaproszenie do serwera.", inline=True)
        embed.add_field(name=prefix + "Milionerzy", value="Sprawdź to. Nie polecam.", inline=True)
        embed.add_field(name=prefix + "Embed <tekst (tekst)>", value="Zamiast się botować, wykonaj tą komendę.", inline=True)
        embed.add_field(name=prefix + "Powiedz <tekst (tekst)>", value="Powiem coś.", inline=True)
        embed.add_field(name=prefix + "Losuj <liczba1 (liczba)> <liczba2 (liczba)>", value="Wylosuj liczbę.", inline=True)
        embed.add_field(name=prefix + "LiteraPoLiterze <tekst (tekst)>", value="Bardzo fajna komenda!", inline=True)
    elif strona == 2:
        embed = discord.Embed(title="Pomoc", description="Strona 2/2", color=0xff0000)
        embed.add_field(name=prefix + "Informacje <użytkownik (użytkownik, opcjonalnie)>", value="Informacje o użytkowniku.", inline=True)
        embed.add_field(name=prefix + "Wykop <użytkownik (użytkownik)>", value="Wykop użytkownika.", inline=True)
        embed.add_field(name=prefix + "Zbanuj <użytkownik (użytkownik)>", value="Zbanuj użytkownika.", inline=True)
        embed.add_field(name=prefix + "Wyczyść <ilość (liczba)>", value="Czyści czat. Nie usuwa wiadomości sprzed 14 dni.", inline=True)
        embed.add_field(name=prefix + "Członkowie", value="Liczba członków serwera.", inline=True)
        embed.add_field(name=prefix + "Serwer", value="Informacje o serwerze.", inline=True)
        embed.add_field(name=prefix + "ZgadnijLiczbę <maksymalna (liczba, opcjonalnie)>", value="Zgadnij liczbę!", inline=True)
    elif not strona == None or not strona == 1 or not strona == 2:
        embed = discord.Embed(title="Pomoc", description="Strona {}/2".format(str(strona)), color=0xff0000)
        embed.set_footer(text="Nie znaleziono strony!")
    await bot.say(embed=embed)

@bot.command(pass_context=True)
async def Zasady(ctx):
    if ctx.message.server.id == "407103788772622336":
        await bot.say("1. Szanuj i nie obrażaj innych graczy\n2. Nie proś o rangi\n3. Nie przeklinaj (wolno po 20:00 do 06:00 czasu polskiego)\n4. Nie spamuj i nie flooduj.\n5. ABSOLUTNY ZAKAZ REKLAMOWANIA SERVERÓW I KANAŁÓW\n6. Nie nadużywaj wzmianek @here i @everyone\n\n--------Kary\n1.Upomnienie\n2.Upomnienie\n3.Upomnienie\n4.Mute na 1h\n5.Mute na 6h\n6.Mute na 12h\n7.mute na 24h\n8.Ban na 24h\n9.Ban na 7dni\n10.Ban na 30dni\n11.Ban permanentny")

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

@bot.command(pass_context=True)
async def Konfiguruj(ctx, co=None, *, wartosc=None):
    if not ctx.message.author.server_permissions.manage_server:
        await bot.say("Nie masz permisji do tego!")
        return
    if co == None:
        embed = discord.Embed(title="Konfiguruj bota:")
        embed.add_field(name="joindm", value="Prywatna wiadomość do nowego członka serwera.", inline=True)
        embed.add_field(name="removedm", value="Prywatna wiadomość do członka opuszczającego serwer.", inline=True)
        await bot.say(embed=embed)
    elif co == "joindm" or co == "removedm":
        if wartosc == None:
            embed = discord.Embed(title="Konfiguruj bota:")
            if co == "joindm":
                embed.add_field(name="Wartość to:", value="{}".format(Konfiguracje.JoinDM(ctx.message.server.id)), inline=True)
            else:
                embed.add_field(name="Wartość to:", value="{}".format(Konfcje.RemoveDM(ctx.message.server.id)), inline=True) 
            embed.set_footer(text="Jeżeli chcesz ustawić wartość, użyj *{}Konfiguruj {} <wartość>*.".format(prefix, co))
            await bot.say(embed=embed)
            return
        l = str(wartosc).lower()
        if l == "null":
            wartosc = "null"
        if co == "joindm":
            BitBotHelper.Konfiguracje.UstawJoinDM(ctx.message.server.id, wartosc)
        else:
            BitBotHelper.Konfiguracje.UstawRemoveDM(ctx.message.server.id, wartosc)
        await bot.add_reaction(ctx.message, "âś…")

            
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

bot.loop.create_task(uptime())

token = os.environ.get('TOKEN')

bot.run(token)
