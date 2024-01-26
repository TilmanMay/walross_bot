import discord
from discord.ext import commands
import asyncio
from PIL import Image, ImageFont, ImageDraw
import numpy as np
import os
import pandas as pd

cid = 842295716872323093


class Leaderboard:
    def __init__(self):
        self.data = pd.read_csv(
            "/home/pi/walross_bot/leader.csv",
            names=["Name", "Score", "Games"],
            header=0,
        )

    def search_name(self, x):
        return x in self.data.Name.values

    def add_name(self, x):
        df2 = pd.DataFrame({"Name": [x], "Score": [0], "Games": [0]})
        self.data = self.data.append(df2, ignore_index=True)

    def save(self):
        self.data.to_csv("/home/pi/walross_bot/leader.csv", index=False)

    def sort(self):
        self.data = self.data.sort_values(by="Score", ascending=False)

    def add_win(self, x):
        self.data.at[self.data[self.data.Name == x].index[0], "Score"] += 1
        self.sort()
        self.save()

    def add_game(self, x):
        self.data.at[self.data[self.data.Name == x].index[0], "Games"] += 1

    def get_name(self, ind):
        return self.data.Name[ind]

    def get_score(self, ind):
        return self.data.Score[ind]

    def get_games(self, ind):
        return self.data.Games[ind]

    def update(self, xs):
        for x in xs:
            if not self.search_name(x):
                self.add_name(x)
        self.save()

    def add_game(self, xs):
        for x in xs:
            self.add_game(x)
        self.save()

    def get_embed(self):
        embed = discord.Embed(title=f"__**Leaderboard:**__", color=0x03F8FC)
        lst = []
        for j in range(len(self.data)):
            name = self.get_name(j)
            wins = self.get_score(j)
            games = self.get_games(j)
            lst.append((name, wins, games))

        for n, w, g in lst:
            embed.add_field(
                name=f"**{n}**", value=f"> Wins: {w}\n> Games: {g}\n", inline=False
            )
        return embed


class Bingo:
    def __init__(self, name):
        self.name = name
        self.matrix = np.zeros([4, 4, 2])
        self.matrix[:, :, 1] = np.random.choice(
            np.arange(0, len(txt)), replace=False, size=(4, 4)
        )
        self.draw(self.matrix[:, :, 1])

    def update(self, zahl):
        ind = np.argwhere(self.matrix[:, :, 1] == zahl)
        if ind.size != 0:
            self.matrix[ind[0][0], ind[0][1], 0] = 1
            ind[0][0], ind[0][1] = ind[0][1], ind[0][0]
            self.cross(ind[0])

    def check(self):
        mat = self.matrix[:, :, 0]

        for j in range(4):
            if np.sum(mat[j, :]) == 4 or np.sum(mat[:, j]) == 4:
                return True
            elif (
                np.trace(self.matrix[:, :, 0]) == 4
                or np.trace(np.fliplr(self.matrix[:, :, 0])) == 4
            ):
                return True

        return False

    def draw(self, mat):
        image = Image.open("/home/pi/walross_bot/pre.png").convert("RGBA")

        image_size = image.size

        pos = image_size[0] / 8

        draw = ImageDraw.Draw(image)

        color = "rgb(255, 255, 255)"  # black color
        font = ImageFont.truetype(
            "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf", 20
        )
        i = 0
        for j in range(4):
            for k in range(4):
                (x, y) = (
                    (2 * (j + 1) - 1) * pos - pos / 2,
                    (2 * (k + 1) - 1) * pos - pos / 4,
                )
                message = txt[int(mat[k, j])]
                draw.text((x, y), message, fill=color, font=font)
                i += 1
        font = ImageFont.truetype(
            "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf", 70
        )
        draw.text(
            (4 * pos - (100 / 6) * len(self.name), 8 * pos + 10),
            self.name,
            fill=color,
            font=font,
        )
        image.save(str("/home/pi/walross_bot/bingo/" + self.name + ".png"), "PNG")

    def cross(self, tup):
        image = Image.open(
            str("/home/pi/walross_bot/bingo/" + self.name + ".png")
        ).convert("RGBA")

        image_size = image.size

        pos = image_size[0] / 8
        # draw = ImageDraw.Draw(image)
        TINT_COLOR = (0, 0, 0)  # Black
        overlay = Image.new("RGBA", image.size, TINT_COLOR + (0,))
        draw = ImageDraw.Draw(overlay)
        draw.line(
            ((2 * tup[0] * pos, (((2 * tup[1])) * pos)))
            + (((2 * (tup[0]) + 2) * pos, (((2 * tup[1] + 2)) * pos))),
            fill=(255, 0, 0, 80),
            width=20,
        )
        draw.line(
            (((2 * tup[0] + 2) * pos, (((2 * tup[1])) * pos)))
            + (((2 * (tup[0])) * pos, (((2 * tup[1] + 2)) * pos))),
            fill=(255, 0, 0, 80),
            width=20,
        )
        img = Image.alpha_composite(image, overlay)
        img = img.convert("RGB")  # Remove alpha for saving in jpg format.
        img.save(str("/home/pi/walross_bot/bingo/" + self.name + ".png"))
        # image.save("output.png", "PNG")


class Spiel:
    def __init__(self, num):
        self.game = []
        self.busy = False
        self.msg = []

        with open("/home/pi/walross_bot/meierbingo.txt", "r", encoding="utf-8") as f:
            self.lines = f.readlines()
            for x, lines in enumerate(self.lines):
                self.lines[x] = str(x + 1) + ". " + lines.replace("&", "")

        self.num = np.zeros(len(self.lines))

        for j in range(len(num)):
            self.game.append(Bingo(num[j]))

    def update(self, z):
        for j in range(len(self.game)):
            self.game[j].update(z)

    def check(self):
        k = np.zeros(len(self.game))
        for j in range(len(self.game)):
            k[j] = self.game[j].check()
        return np.argwhere(k == 1)


with open(
    "/home/pi/walross_bot/meierbingo.txt", "r", encoding="utf-8", newline="\r\n"
) as f:
    txt = f.read().splitlines()
    try:
        for x, lines in enumerate(txt):
            txt[x] = lines.replace("&", "\n")
    except:
        pass

lb = Leaderboard()


def emptydir():
    filelist = [f for f in os.listdir("bingo")]
    for f in filelist:
        os.remove(os.path.join("bingo", f))


def streich(ses, num):
    if ses.num[num] != 1:
        ses.lines[num] = ses.lines[num].replace(
            str(num + 1) + ".", str(num + 1) + ". ~~"
        )
        if num + 1 != len(ses.lines):
            ses.lines[num] = ses.lines[num].replace("\n", " ~~\n")
        else:
            ses.lines[num] = ses.lines[num] + "~~"
        ses.num[num] = 1


class MBingo(commands.Cog):
    global lb

    def __init__(self, client):
        self.client = client

    @commands.command()
    async def bingo(self, ctx, *args):
        if (
            self.client.user.id != ctx.message.author.id
            and ctx.message.channel.id == cid
        ):
            global ses
            try:
                del ses
                emptydir()
            except:
                pass
            if len(args) > 0:
                ses = Spiel(args)
                ses.busy = True
                lb.update(args)
                # await ctx.channel.purge(limit=20)
                for game in ses.game:
                    path = "/home/pi/walross_bot/bingo/" + game.name + ".png"
                    with open(path, "rb"):
                        message = await ctx.send(file=discord.File(path))
                        ses.msg.append(message)
                message = await ctx.message.channel.send("".join(ses.lines))
                ses.msg.append(message)
                ses.busy = False
            else:
                pass

    @commands.command()
    async def endbingo(self, ctx):
        if (
            self.client.user.id != ctx.message.author.id
            and ctx.message.channel.id == cid
        ):
            global ses
            try:
                await ctx.channel.delete_messages(ses.msg)
                del ses
                emptydir()
                busy = False
            except:
                pass

    @commands.command()
    async def leader(self, ctx):
        if (
            self.client.user.id != ctx.message.author.id
            and ctx.message.channel.id == cid
        ):
            await ctx.message.delete()
            await ctx.send(embed=lb.get_embed())

    @commands.Cog.listener()
    async def on_message(self, message):
        if self.client.user.id != message.author.id and message.channel.id == cid:
            if "ses" in globals():
                global ses
                if ses.busy == False:
                    msg = message.content
                    try:
                        if int(msg) <= len(txt) and int(msg) > 0:
                            ses.busy = True
                            await message.delete()
                            ses.update(int(msg) - 1)
                            streich(ses, int(msg) - 1)
                            ctx = await self.client.get_context(message)
                            # await ctx.channel.purge(limit=20)
                            await ctx.channel.delete_messages(ses.msg)
                            for game in ses.game:
                                path = (
                                    "/home/pi/walross_bot/bingo/" + game.name + ".png"
                                )
                                with open(path, "rb"):
                                    message = await ctx.send(file=discord.File(path))
                                    ses.msg.append(message)
                            v = ses.check()
                            if len(v) == 1:
                                lb.add_game()
                                lb.add_win(ses.game[v[0][0]].name)
                                await message.channel.send(
                                    "BINGO! "
                                    + ses.game[v[0][0]].name
                                    + " hat gewonnen!"
                                )
                                path = "/home/pi/walross_bot/pics/party.jpg"
                                with open(path, "rb"):
                                    await ctx.send(file=discord.File(path))
                                del ses
                                await ctx.send(embed=lb.get_embed())
                                await asyncio.sleep(1)
                                emptydir()
                            elif len(v) > 1:
                                lb.add_game()
                                names = ses.game[v[0][0]].name
                                lb.add_win(ses.game[v[0][0]].name)
                                for n in v[1:]:
                                    names = names + " und " + ses.game[n].name
                                    lb.add_win(ses.game[n].name)
                                await message.channel.send(
                                    "BINGO! " + names + " haben gewonnen!"
                                )
                                path = "/home/pi/walross_bot/pics/party.jpg"
                                with open(path, "rb"):
                                    await ctx.send(file=discord.File(path))
                                del ses
                                await ctx.send(embed=lb.get_embed())
                                await asyncio.sleep(1)
                                emptydir()
                            else:
                                message = await message.channel.send("".join(ses.lines))
                                ses.msg.append(message)
                                ses.busy = False
                    except:
                        pass


def setup(client):
    client.add_cog(MBingo(client))
