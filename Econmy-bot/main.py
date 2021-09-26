import discord
from discord.ext import commands
import json
import os
import math
import random
client = commands.Bot(command_prefix = ".")
client.remove_command('help')
@client.event
async def on_ready():
    await client.change_presence(activity=discord.Activity(type =discord.ActivityType.listening, name=".help | Economy Bot"))
    print(discord.__version__)
    print("Economy Bot is now online!")
@client.command(pass_context=True)
async def bal(ctx):
    await open_account(ctx.author)
    user= ctx.author
    users = await get_bank_data()
    wallet_amt = users[str(user.id)]["wallet"]
    bank_amt = users[str(user.id)]["bank"]
    s = discord.Embed(title = f"{ctx.author.name}'s balance",color = discord.Color.green())
    s.add_field(name = "Wallet 💰", value= wallet_amt,inline = False)
    s.add_field(name = "Bank 💳", value= bank_amt,inline = False)
    await ctx.send(embed = s)
@client.command(pass_context=True)
async def beg(ctx):
    await open_account(ctx.author)
    user = ctx.author
    users = await get_bank_data()
    earnings = random.randrange(101)
    await ctx.send(f"**{ctx.author.mention}, You won {earnings} coins!!**")
    users[str(user.id)]["wallet"] += earnings
    with open("mainbank.json", "w") as f:
        json.dump(users,f)
@client.command(pass_context=True)
async def withdraw(ctx,amount = None):
    await open_account(ctx.author)
    if amount == None:
        await ctx.send(f"**{ctx.author.mention}, Please enter the amount**")
        return
    bal = await update_bank(ctx.author)
    amount = int(amount)
    if amount>bal[1]:
        await ctx.send(f"**{ctx.author.mention}, You dont have that much money!!**")
        return
    if amount<0:
        await ctx.send(f"**{ctx.author.mention}, Amount must be positive**")
        return
    await update_bank(ctx.author,amount)
    await update_bank(ctx.author,-1*amount,"bank")
    await ctx.send(f"**{ctx.author.mention}, You withdrew {amount} coins!**")
@client.command(pass_context=True)
async def dep(ctx,amount = None):
    await open_account(ctx.author)
    if amount == None:
        await ctx.send(f"**{ctx.author.mention}, Please enter the amount**")
        return
    bal = await update_bank(ctx.author)
    amount = int(amount)
    if amount>bal[0]:
        await ctx.send(f"**{ctx.author.mention}, You dont have that much money!!**")
        return
    if amount<0:
        await ctx.send(f"**{ctx.author.mention}, Amount must be positive**")
        return
    await update_bank(ctx.author,-1*amount)
    await update_bank(ctx.author,amount,"bank")
    await ctx.send(f"**{ctx.author.mention}, You deposited {amount} coins!**")
@client.command(pass_context=True)
async def send(ctx,member: discord.Member, amount = None):
    await open_account(ctx.author)
    await open_account(member)
    if amount == None:
        await ctx.send(f"**{ctx.author.mention}, Please enter the amount**")
        return
    bal = await update_bank(ctx.author)
    if amount == "all":
        amount = bal[0]
    amount = int(amount)
    if amount>bal[1]:
        await ctx.send(f"**{ctx.author.mention}, You dont have that much money!!**")
        return
    if amount<0:
        await ctx.send(f"**{ctx.author.mention}, Amount must be positive**")
        return
    await update_bank(ctx.author,-1*amount,"bank")
    await update_bank(member,amount,"bank")
    await ctx.send(f"**{ctx.author.mention}, you sent {amount} coins!**")
@client.command(pass_context=True)
async def rob(ctx,member: discord.Member):
    await open_account(ctx.author)
    await open_account(member)
    bal = await update_bank(member)
    if bal[0]<100:
        await ctx.send(f"{ctx.author.mention}, It's not worth it!")
        return
    earnings = random.randrange(0, bal[0])
    await update_bank(ctx.author,earnings)
    await update_bank(member,-1*earnings)
    await ctx.send(f"{ctx.author.mention}, You robbed and got {earnings} coins!")
@client.command(pass_context=True)
async def slots(ctx, amount = None):
    await open_account(ctx.author)
    if amount == None:
        await ctx.send(f"{ctx.author.mention}, Please enter the amount")
        return

    bal = await update_bank(ctx.author)

    amount = int(amount)

    if amount>bal[0]:
        await ctx.send(f"{ctx.author.mention}, You dont have that much money!!")
        return
    if amount<0:
        await ctx.send(f"{ctx.author.mention}, Amount must be positive")
        return

    final = []
    for i in range(3):
        a = random.choice([":cherries:", ":watermelon:", ":strawberry:",":lemon:",":banana:",":peach:"])

        final.append(a)

    await ctx.send(str(final))

    if final[0] == final[1] or final[0] == final[2] or final[2] == final[1]:
         await update_bank(ctx.author,2*amount)
         await ctx.send(f"**{ctx.author.mention},You won!**")

    else:
        await update_bank(ctx.author,-1*amount)
        await ctx.send(f"**{ctx.author.mention} ,You lost!**")
async def open_account(user):

    users = await get_bank_data()
    if str(user.id) in users:
        return False
    else:
        users[str(user.id)] = {}
        users[str(user.id)]["wallet"] = 0
        users[str(user.id)]["bank"] = 0

    with open("mainbank.json", "w") as f:
        json.dump(users,f)
    return True
async def get_bank_data():
    with open("mainbank.json", "r") as f:
        users = json.load(f)

    return users
async def update_bank(user, change=0,mode = 'wallet'):
    users = await get_bank_data()
    users[str(user.id)][mode] += change
    with open("mainbank.json", "w") as f:
        json.dump(users,f)
    bal = users[str(user.id)]["wallet"],users[str(user.id)]["bank"]
    return bal
@client.group(invoke_without_command=True)
async def help(ctx):
    em = discord.Embed(title = "Economy Bot Help", description = "Use .help <command> for extended information on a command!",color = discord.Color.green())
    em.add_field(name = "Economy Bot Help", value = "`beg, bal, dep, withdraw, send, rob, slots`")
    await ctx.reply(embed = em)
@help.command()
async def beg(ctx):
    em= discord.Embed(title = "Beg", description = "Use this command to earn random price of money!",color = discord.Color.green())
    em.add_field(name= "**Syntax**", value= ".beg")
    await ctx.reply(embed = em)
@help.command()
async def bal(ctx):
    em= discord.Embed(title = "Bal", description = "Use this command to check your balance!",color = discord.Color.green())
    em.add_field(name= "**Syntax**", value= ".bal")
    await ctx.reply(embed = em)
@help.command()
async def dep(ctx):
    em= discord.Embed(title = "Deposit", description = "Use this command to deposit your money to your bank account!",color = discord.Color.green())
    em.add_field(name= "**Syntax**", value= ".dep <amount>")
    await ctx.reply(embed = em)
@help.command()
async def withdraw(ctx):
    em= discord.Embed(title = "Withdraw", description = "Use this command to withdraw your money from your bank account to your wallet!",color = discord.Color.green())
    em.add_field(name= "**Syntax**", value= ".withdraw <amount>")
    await ctx.reply(embed = em)
@help.command()
async def send(ctx):
    em= discord.Embed(title = "Send", description = "Use this command to send money to someone!",color = discord.Color.green())
    em.add_field(name= "**Syntax**", value= ".send <amount>")
    await ctx.reply(embed = em)
@help.command()
async def rob(ctx):
    em= discord.Embed(title = "Rob", description = "Use this command to rob someone!",color = discord.Color.green())
    em.add_field(name= "**Syntax**", value= ".rob <@someone>")
    await ctx.reply(embed = em)
@help.command()
async def slots(ctx):
    em= discord.Embed(title = "Slots", description = "Use this command to play slots!",color = discord.Color.green())
    em.add_field(name= "**Syntax**", value= ".slots <amount>")
    await ctx.reply(embed = em)

client.run("ENTER YOUR DISCORD BOT TOKEN HERE")