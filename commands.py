import discord
from discord import app_commands
import sqlite3
import time
import datetime
import random
import asyncio
# own
import subcoms
import database as db
import buttons

defaultBotColorInt = subcoms.colorHEXint("05c5ff")
defaultBotColor = "#05c5ff"

defaultBotColorDiscord = discord.Colour.from_str(defaultBotColor)

clientID = "0"
ownerID = 412132568146771972
mainGuildID = 777162565842370592

react_chance = 0
reply_react_chance = 0
message_chance = 0

def connectDatabase():
    if db.connectDatabase():
        return True
    else:
        return False


can_send = True

cd = 120
async def cooldown():
    global can_send
    global cd
    can_send = False
    await asyncio.sleep(cd)
    can_send = True


    
    
#
# Celebration
#
#
    

async def celebrate_all():
    await do_celebrate_guild(mainGuildID, subcoms.unixToDDMM(subcoms.currentTimeUnix()+30))
    print("-> " + str(subcoms.unixToDDMM(subcoms.currentTimeUnix()+30)))
    await asyncio.sleep(24*60*60)
    await celebrate_all()


async def del_all_msgs_writes():
    writes = db.getAllTableValues('msgs_writes', 'server_id', mainGuildID)

    now = subcoms.currentTimeUnix()+10

    if writes != None:
        for i in writes:
            if int(i[4]) < now:
                try:
                    msg = await client.get_channel(int(i[2])).fetch_message(int(i[3]))
                    db.delRowFromTableByKey('msgs_writes', 'msg_id', msg.id)
                    try:
                        await msg.delete()
                        await asyncio.sleep(1.2)
                    except:
                        await asyncio.sleep(2)
                        await msg.delete()
                except:
                    db.delRowFromTableByKey('msgs_writes', 'msg_id', int(i[3]))

date = subcoms.unixToDDMM(subcoms.currentTimeUnix())
class MyClient(discord.Client):
    async def on_ready(self):
        if connectDatabase():
            await tree.sync(guild=discord.Object(id=mainGuildID))
            print(f'Logged on as {self.user}!')
            await do_celebrate_guild(mainGuildID, date)
            await del_all_msgs_writes()
            # Таймер до след поздравления
            tim = subcoms.diffBetweenNextMidnightUnix(subcoms.currentTimeUnix())
            if tim < 30:
                tim+=30
            await asyncio.sleep(tim)
            await celebrate_all()
            

    async def on_message(self, message:discord.Message):
        if message.channel.type == discord.ChannelType.text and message.guild.id == mainGuildID and (message.type == discord.MessageType.default or message.type == discord.MessageType.reply):
            
            
            if client.user in message.mentions or message.reference and message.reference.cached_message and message.reference.cached_message.author == client.user:
                emojis = message.guild.emojis
                r2 = random.randint(1,len(emojis))-1
                
                await message.reply(emojis[r2]) # ---------------------------------------------------------------------------------------------------------------------------
            else:
        
                global react_chance
                if react_chance != 0 and message.author.bot == False:
                    real_chance = (react_chance)

                    print(len(message.content), real_chance)
                    if subcoms.true_with_chance(real_chance):
                        
                        emojis = message.guild.emojis
                        r2 = random.randint(1,len(emojis))-1
                        await message.add_reaction(emojis[r2]) # ---------------------------------------------------------------------------------------------------------------------------
                
                global reply_react_chance
                if reply_react_chance != 0 and message.author.bot == False and can_send:
                    real_chance = (reply_react_chance) 
                    if subcoms.true_with_chance(real_chance):
                        
                        emojis = message.guild.emojis
                        r2 = random.randint(1,len(emojis))-1
                        
                        await message.reply(emojis[r2]) # ---------------------------------------------------------------------------------------------------------------------------
                        await cooldown()
                global message_chance
                if message_chance != 0 and message.author.bot == False and can_send:
                    real_chance = (message_chance) 
                    if subcoms.true_with_chance(real_chance):
                        listi = db.getAllTableValues("texts", 'guild_id', message.guild.id)
                        if listi != None:
                            r2 = random.randint(1,len(listi))-1
                            await message.reply(listi[r2][2]) # ---------------------------------------------------------------------------------------------------------------------------
                            await cooldown()

            
            is_deleting = db.getAllTableValues('del_channels', 'chan_id', message.channel.id)
            if is_deleting != None:
                is_deleting = is_deleting[0]
                db.addValues("msgs_writes", ['server_id', 'chan_id', 'msg_id', 'when_unix'], [mainGuildID, message.channel.id, message.id, subcoms.currentTimeUnix()+int(is_deleting[3])])
                await asyncio.sleep(int(is_deleting[3]))
                is_deleting = db.getAllTableValues('del_channels', 'chan_id', message.channel.id)
                if is_deleting != None:
                    await message.delete()
                    db.delRowFromTableByKey('msgs_writes', 'msg_id', message.id)
                    await asyncio.sleep(1.2)


intents = discord.Intents.default()

intents.members = True
intents.message_content = True
client = MyClient(intents=intents)
tree = app_commands.CommandTree(client)





# Command: test
async def test(i: discord.Interaction):
    
    
    await i.response.send_message("Понг!", ephemeral=True)




# Command: add_celebrate
async def add_celebrate(i: discord.Interaction,title:str, text:str, color:str, image:str):
    if not i.permissions.administrator:
        await i.response.send_message('Эта команда доступна только администраторам', ephemeral=True)
        return
    
    embed = discord.Embed()
    embed.title = title
    col = color
    try:
        embed.color = discord.Colour.from_str(color)
    except:
        col = '#c242f5'
        embed.color = discord.Colour.from_str("#c242f5")
    embed.description = text.replace("&", '\n')
    if image:
        embed.set_image(url=image)
    else:
        image = "None"
    length = db.getAllTableValues('celebration_templates', 'server_id', i.guild.id)
    if length:
        length = int(length[-1][2])+1
    else:
        length = 1
    db.addValues("celebration_templates", ['server_id', 'internal_id', 'title', 'description', 'color', 'image'], [i.guild.id, length, title, text,col,image])
    await i.response.send_message(f'Готово. Поздравление `{length}` создано, вот пример.', ephemeral=True, embed=embed)


# Command: recelebrate
async def recelebrate(i: discord.Interaction):
    if not i.permissions.administrator:
        await i.response.send_message('Эта команда доступна только администраторам', ephemeral=True)
        return
    
    await i.response.send_message("Перепоздравляю участников за сегодня...",ephemeral=True)
    await do_celebrate_guild(i.guild.id, subcoms.unixToDDMM(subcoms.currentTimeUnix()+30), r=True)

    

# Command: celebrations_list
async def celebrationlist(i: discord.Interaction,id:int,page:int):
    if not i.permissions.administrator:
        await i.response.send_message('Эта команда доступна только администраторам', ephemeral=True)
        return
    if id == None:
        listi = db.getAllTableValues('celebration_templates', 'server_id', i.guild.id)
        text=''
        max_page = 1
        if listi:
            max_page = int((10+len(listi))/10)
            if page >= max_page:
                page = max_page
            for j in listi:
                text+='`' +j[2] + '` - ' + j[3] + "\n" 
        else:
            text = "Здесь пусто."
            page = 1
        embed = discord.Embed()
        embed.title = "Поздравления сервера"
        embed.color = discord.Colour.from_str('#5640ff')
        embed.description = text

        embed.set_footer(text="Страница " + str(page) + "/" + str(max_page))

        await i.response.send_message(embed=embed)
    else:
        listi = db.getTableValuesByTwoKeys('celebration_templates', 'server_id', i.guild.id, 'internal_id', id)
        if listi == None:
            await i.response.send_message("`ID` не найден. Перепроверьте ID.", ephemeral=True)
        else:
            embd = discord.Embed()
            embd.title = listi[3]
            embd.description = listi[4].replace("&", '\n')
            embd.color = discord.Colour.from_str(listi[5])
            if listi[6] != "None":
                embd.set_image(url=listi[6])
            
            await i.response.send_message(f"Поздравление `{id}`",embed=embd)
        

# Command: celebrate
async def celebrate(i: discord.Interaction, member:discord.User, date:str):
    # if member.bot:
    #     await i.response.send_message("Нель")
    #     return
    roles = i.user.roles
    
    has_role = False
    if not i.permissions.administrator and not has_role:
        await i.response.send_message("Эта команда доступна только администраторам", ephemeral=True)
        return
    isalreadyin = db.getTableValuesByTwoKeys('celebrations', 'user_id', member.id, 'server_id', i.guild.id)
    if isalreadyin == None:
        spl = date.split('.')
        try:
            datetime.datetime(day=int(spl[0]), month=int(spl[1]), year=2024)
        except:
            await i.response.send_message("Дата введена неверно.", ephemeral=True)
            return 0
        db.addValues('celebrations', ['user_id', 'server_id', 'date'], [member.id, i.guild.id, subcoms.fillDDMM(date)])
        text=''
        roleid = db.getServerKey(i.guild.id, 'birthday_roleid')
        chanid = db.getServerKey(i.guild.id, 'birthday_channelid')
        
        if roleid == None:
            text +="\nУ вас не установлена роль именинника."
        if chanid == None:
            text+="\nУ вас не установлен канал для поздравлений."
        await i.response.send_message('Успешно добавлено. '+text,ephemeral=True)
    else:
        await i.response.send_message("Участник уже есть в очереди на поздравление.",ephemeral=True)




async def delcelebration(i:discord.Interaction, id:int):
    res = db.delRowFromTableByTwoKeys('celebration_templates', 'server_id', i.guild.id, 'internal_id', id)
    if res == 0:
        ind = int(db.getServerKey(i.guild.id, "last_celebrationindex"))
        if ind == None:
            ind = 0
        if ind > 0:
            ind+=-1
            db.setServerValue(i.guild.id, "last_celebrationindex", ind)
        await i.response.send_message(f"Поздравление `{id}` успешно удалено",ephemeral=True)
    else:
        await i.response.send_message(f"Произошла ошибка. Проверьте правильность ID",ephemeral=True)


# Command: setrolebday
async def setrolebday(i: discord.Interaction, roleid:str):
    if i.user.guild_permissions.administrator:
        role = i.guild.get_role(int(roleid))
        if role == None:
            await i.response.send_message("Данной роли не существует, пожалуйста перепроверьте правильность ID", ephemeral=True)
        else:
            db.setServerValue(i.guild.id, 'birthday_roleid', int(roleid))
            await i.response.send_message("Роль установлена! Не забудьте переместить роль ниже моей в списке ролей, иначе я не смогу её выдать!",ephemeral=True)
    else:
        await i.response.send_message("Эта команда доступна только администраторам сервера.", ephemeral=True)


# Command: setchannelbday
async def setchannelbday(i: discord.Interaction, chanid:str):
    if i.user.guild_permissions.administrator:
        channel = i.guild.get_channel(int(chanid))
        if channel == None:
            await i.response.send_message("Данного канала не существует, пожалуйста перепроверьте правильность ID", ephemeral=True)
        else:
            db.setServerValue(i.guild.id, 'birthday_channelid', int(chanid))
            await i.response.send_message("Канал установлен!",ephemeral=True)
    else:
        await i.response.send_message("Эта команда доступна только администраторам сервера.", ephemeral=True)



async def remove_prev_day(guild: discord.Guild, role: discord.Role):
    prev_date = subcoms.unixToDDMM(subcoms.getPrevDayUnix(subcoms.currentTimeUnix()))

    listi = db.getAllTableValuesByOneKey('celebrations', 'server_id', guild.id)
    if listi != None:
        for j in listi:
            if j[3] == prev_date:
                usr = guild.get_member(int(j[1]))
                await usr.remove_roles(role)

async def create_event(guild:discord.Guild, names:list, chanid:int=None):
    nms = str(names)[2:-2].replace("', '", ', ')
    loc = "Основной чат"
    if chanid != None:
        loc = "<#"+str(chanid)+">"
    await guild.create_scheduled_event(
        location=loc,

        name="Сегодня у кого-то день рождения!",
        description=nms,
        start_time=datetime.datetime.fromtimestamp(subcoms.currentTimeUnix()+60).astimezone(),
        end_time=subcoms.getMidnightUnix(subcoms.getNextDayUnix(subcoms.currentTimeUnix())).astimezone(),
        entity_type=discord.EntityType.external,
        privacy_level=discord.PrivacyLevel.guild_only
        
    )

async def do_celebrate_guild(guild_id: int, _date:str, r:bool=False):
    is_celebrated = db.getTableValuesByTwoKeys("writes", "server_id", guild_id, "date", _date)
    guild = client.get_guild(guild_id)
    if guild:

        roleid = db.getServerKey(guild_id, 'birthday_roleid')
        chanid = db.getServerKey(guild_id, 'birthday_channelid')
        if roleid:
            
            await remove_prev_day(guild, guild.get_role(int(roleid)))
        print("Celebrated ", is_celebrated)
        if is_celebrated == None or r:
    
            if chanid != None:
                chan = client.get_channel(int(chanid))
                role = None
                if roleid != None:
                    role = guild.get_role(int(roleid))
                if chan != None:
                    listi = db.getAllTableValuesByOneKey('celebrations', 'server_id', guild_id)
                    print(listi)
                    if listi != None:
                        mentions = ''
                        names = []
                        for i in listi:
                            if i[3] == _date:
                                usr = guild.get_member(int(i[1]))
                                mentions+=usr.mention+" "
                                names.append(usr.display_name)
                                if role:
                                    await usr.add_roles(role)
                        if mentions != '':
                            listies = db.getAllTableValuesByOneKey('celebration_templates', 'server_id', guild_id)
                            embd = discord.Embed()
                            selected = 0
                            if listies == None:
                                embd.title = "С днём рождения! :birthday:"
                                embd.color = discord.Colour.from_str("#c242f5")
                            else:
                                get_index = db.getServerKey(guild.id, "last_celebrationindex")
                                if get_index == None:
                                    get_index = 0
                                else:
                                    get_index = int(get_index)
                                selected = listies[0]
                                if get_index+1 <len(listies):
                                    selected = listies[get_index+1]
                                    get_index+=1
                                else:
                                    get_index = 0
                                db.setServerValue(guild.id, "last_celebrationindex", get_index)
                                embd.title = selected[3]
                                embd.description = selected[4].replace("&", '\n')
                                embd.color = discord.Colour.from_str(selected[5])
                                if selected[6] != "None":
                                    embd.set_image(url=selected[6])
                            await chan.send(mentions,embed=embd)
                            await create_event(guild, names, chanid)
                        db.addValues("writes", ['server_id', 'date'], [guild_id, _date])
        else:
            print("Эта гильдия уже поздравлена")
    


# PREcommand Celebrations:
async def pre_celebrations(i: discord.Interaction, page:int):
    listi = db.getAllTableValues("celebrations", "server_id", i.guild.id)
    text = ""
    max_page = int((len(listi)+10)/10)
    if listi == None:
        text = "Здесь пусто. Администраторы могут добавить поздравление `/поздравить`"
    
    if page > max_page:
        page = max_page

    # Сортировка ДР
    now = int(datetime.datetime.now().timestamp())
    after = []
    listiNew = []
    for jk in listi:
        n = subcoms.DDMMToUnix(jk[3])

        if n < now:
            after.append(jk)
        else:
            listiNew.append(jk)
    

    after = sorted(after, key=lambda x: subcoms.DDMMToUnix(x[3]))
    listiNew = sorted(listiNew, key=lambda x: subcoms.DDMMToUnix(x[3]))
    listiNew += after

    
    listi = listiNew[(page-1)*10:page*10]
    texted = False
    for j in listi:
        if subcoms.DDMMToUnix(j[3]) < now and texted == False:
            texted = True
            text+= "**Уже в " + str(datetime.datetime.now().year+1) + "**\n"
        text+= "<@"+j[1]+"> - "
        usr = client.get_user(int(j[1]))
        if usr:
            
            text += usr.display_name
            text += " `"+j[3]+"`"
            text += "\n"
        else:
            text+="Пользователь покинул сервер.\n"
    
    embed = discord.Embed()
    embed.title = "Именинники сервера"
    embed.description = text
    embed.color = discord.Colour.from_str("#c242f5")
    embed.set_footer(text="Страница " + str(page)+"/"+str(max_page))
    return [embed,max_page]


# Command: celebrations
async def celebrations(i: discord.Interaction, page:int, user:discord.User):
    if user != None:
        usr = db.getTableValuesByTwoKeys("celebrations", "server_id", i.guild.id, "user_id", user.id)
        embed = discord.Embed()
        embed.title = user.display_name
        embed.set_thumbnail(url=user.display_avatar.url)
        embed.color = discord.Colour.from_str("#c242f5")
        if usr == None:
            embed.description = "Пользователя нет в очереди для поздравления."
        else:
            embed.description = "Установлено день рождения на: `" + usr[3] + "` UTC+3"
        await i.response.send_message(embed=embed)
    else:
        
        if page:
            if page >= 1:
                if page > max_page:
                    page = max_page
                
            else:
                await i.response.send_message("Проверьте правильность набранной страницы.",ephemeral=True)
                return
        else:
            page = 1
            
        t = await pre_celebrations(i,page)
        max_page = t[1]
        embed = t[0]
        
        view = buttons.Celebrations(func=pre_celebrations,page=page, max_page=max_page,author_id=i.user.id)
        await i.response.send_message(embed=embed, view=view)
        await view.wait()




# Command: delcelebrationist
async def delcelebrationist(i: discord.Interaction, member:discord.User, id:int):
    if not i.permissions.administrator:
        await i.response.send_message("Эта команда доступна только администраторам.")
        return
    if member == None and id == None:
        await i.response.send_message("ID указан неверно.",ephemeral=True)
        return 
    if member != None:
        usr = db.getTableValuesByTwoKeys("celebrations", "server_id", i.guild.id, "user_id", member.id)
        if usr == None:
            await i.response.send_message("Пользователя нет в очереди на поздравление.",ephemeral=True)
        else:
            db.delRowFromTableByTwoKeys("celebrations", "server_id", i.guild.id, "user_id", member.id)
            await i.response.send_message("Пользоваель удален из очереди.",ephemeral=True)
    elif id != None:
        usr = db.getTableValuesByTwoKeys("celebrations", "server_id", i.guild.id, "user_id", id)
        if usr == None:
            await i.response.send_message("Пользователя нет в очереди на поздравление.",ephemeral=True)
        else:
            db.delRowFromTableByTwoKeys("celebrations", "server_id", i.guild.id, "user_id",id)
            await i.response.send("Пользоваель удален из очереди.",ephemeral=True)


#
# React
#
#
            
# Command: set_react_chance
async def set_react_chance(i: discord.Interaction, chance:int=None):
    global react_chance
    if chance != None:
        if chance >= 0 and chance <= 100:
            if i.permissions.administrator:
                react_chance = chance
                await i.response.send_message("Шанс реакции установлен на `"+str(react_chance)+"`")
            else:
                await i.response.send_message("Эта команда доступна только администраторам.")
        else:
            await i.response.send_message("Шанс указан неверно.",ephemeral=True)
    else:
        await i.response.send_message("Текущий шанс реакции - " + str(react_chance), ephemeral=True)


# Command: set_reply_react_chance
async def set_reply_react_chance(i: discord.Interaction, chance:int=None):
    global reply_react_chance
    if chance != None:
        if chance >= 0 and chance <= 100:
            if i.permissions.administrator:
                reply_react_chance = chance
                await i.response.send_message("Шанс ответной реакции установлен на `"+str(reply_react_chance)+"`")
            else:
                await i.response.send_message("Эта команда доступна только администраторам.")
        else:
            await i.response.send_message("Шанс указан неверно.",ephemeral=True)
    else:
        await i.response.send_message("Текущий шанс ответной реакции - " + str(reply_react_chance), ephemeral=True)


# Command: set_message_chance
async def set_message_chance(i: discord.Interaction, chance:int=None):
    global message_chance
    if chance != None:
        if chance >= 0 and chance <= 100:
            if i.permissions.administrator:
                message_chance = chance
                await i.response.send_message("Шанс сообщения установлен на `"+str(message_chance)+"`")
            else:
                await i.response.send_message("Эта команда доступна только администраторам.")
        else:
            await i.response.send_message("Шанс указан неверно.",ephemeral=True)
    else:
        await i.response.send_message("Текущий шанс сообщения - " + str(message_chance), ephemeral=True)



# Command: add_text
async def add_text(i: discord.Interaction, text:str):
    if not i.permissions.administrator:
        await i.response.send_message("Эта команда доступна только администраторам.")
        return
    am = 0
    for j in text.split(';'):
        if j != '' and j != ' ':
            am+=1
            db.addValues('texts', ['guild_id', 'text'], [i.guild.id, j])
    await i.response.send_message("Добавлено " + str(am) + " текстов.",ephemeral=True)


async def texts_embed(i: discord.Interaction, page:int):
    listi = db.getAllTableValues("texts", 'guild_id', i.guild.id)

    maxi_pages = (len(listi)+9) // 10

    
    listi = listi[(page-1)*10:page*10]

    embed = discord.Embed()
    embed.title = "Тексты"
    embed.color = defaultBotColorDiscord

    res = ''
    for j in listi:
        txt = j[2]
        if len(txt) > 30:
            txt = txt[:30] + "..."
        res += '`'+str(j[0])+'` - ' + txt + '\n'
    embed.description = res
    embed.set_footer(text="Страница " + str(page) + " / " + str(maxi_pages))

    return (embed,maxi_pages,)


# Command: texts
async def texts(i: discord.Interaction, id:int=None, page:int=None):
    if not i.permissions.administrator:
        await i.response.send_message("Эта команда доступна только администраторам.")
        return
    if id == None:
        listi = db.getAllTableValues("texts", 'guild_id', i.guild.id)

        maxi_pages = (len(listi)+9) // 10
        if page == None:
            page = 1
        else:
            if page > maxi_pages:
                page = maxi_pages
            elif page < 1:
                page = 1


        r = await texts_embed(i,page)
        
        my_view = buttons.Celebrations(func=texts_embed, page=page, max_page=maxi_pages, author_id=i.user.id)

        await i.response.send_message(embed=r[0], view=my_view)


    else:
        r = db.getTableValuesByTwoKeys("texts", 'guild_id', i.guild.id, 'id', id)
        if r == None:
            await i.response.send_message("Текст не найден, проверьте ID",ephemeral=True)
        else:
            await i.response.send_message(r[2])


# Command: del_text
async def del_text(i: discord.Interaction, id:str):
    if not i.permissions.administrator:
        await i.response.send_message("Эта команда доступна только администраторам.")
        return
    am = 0
    for j in id.split(';'):
        if j != '' and j != ' ':
            am+=1
            db.delRowFromTableByTwoKeys('texts', 'guild_id', i.guild.id, 'id', j)
    await i.response.send_message("Удалено " + str(am) + " текстов.",ephemeral=True)





#
# Useful
#

# Command: clear
async def clear(i: discord.Interaction, time_str:str=None, amount:int=None):
    if time_str == None and amount == None:
        await i.response.send_message("Выберите количество сообщений или в пределах какого времени удалить сообщения (1г1д1ч1м1с)",ephemeral=True)
        return
    else:
        if not i.permissions.administrator:
            await i.response.send_message("Эта команда доступна только администраторам.",ephemeral=True)
            return
        
    
    if amount != None:
        if amount >= 1 and amount <= 1000:
            if time_str != None:
                unix = subcoms.timeAnalyzer(time_str)
                now = subcoms.currentTimeUnix()

                if unix == 0 or unix == -1:
                    await i.response.send_message("Время указано неверно.",ephemeral=True)
                    return
            
                await i.response.send_message("Удалил сообщения после <t:"+str(now-unix)+">",ephemeral=True)
                await do_clear(i.channel, time_str, amount)
            else:
                await i.response.send_message("Удалил сообщения.",ephemeral=True)
                await do_clear(i.channel, time_str, amount)

        else:
            await i.response.send_message("Неверно указано количество сообщений. Не менее 1 и не более 1000.", ephemeral=True)



    elif time_str != None:

        unix = subcoms.timeAnalyzer(time_str)
        now = subcoms.currentTimeUnix()

        if unix == 0 or unix == -1:
            await i.response.send_message("Время указано неверно. -> Формат: 1г1д1ч1м1с",ephemeral=True)
            return


        await i.response.send_message("Удалил сообщения после <t:"+str(now-unix)+">",ephemeral=True)
        await do_clear(i.channel, time_str, amount)




# Command: auto_clear
async def auto_clear(i: discord.Interaction, time_str:str):
    if time_str == None:
        await i.response.send_message("Укажите время, через которое необходимо удалять каждое новое сообщение",ephemeral=True)
        return

    if not i.permissions.administrator:
        await i.response.send_message("Эта команда доступна только администраторам.",ephemeral=True)
        return
        


    unix = subcoms.timeAnalyzer(time_str)
    if unix == 0 or unix == -1:
        await i.response.send_message("Время указано неверно.",ephemeral=True)
        return
    

    is_already = db.getAllTableValues('del_channels', 'chan_id', i.channel.id)
    if is_already == None:
        db.addValues('del_channels', ['server_id', 'chan_id', 'unix'], [mainGuildID, i.channel.id, unix])
        await i.response.send_message("Готово. Сообщения в этом канале будут удалятся раз в " + time_str,ephemeral=True)

    else:
        await i.response.send_message("Сообщения в этом канале итак удаляются.", ephemeral=True)



# Command: del_auto_clear
async def del_auto_clear(i: discord.Interaction):

    if not i.permissions.administrator:
        await i.response.send_message("Эта команда доступна только администраторам.",ephemeral=True)
        return

    is_already = db.getAllTableValues('del_channels', 'chan_id', i.channel.id)

    if is_already != None:
        db.delRowFromTableByKey('del_channels', 'chan_id', i.channel.id)
        await i.response.send_message("Авто очистка отключена", ephemeral=True)
    else:
        await i.response.send_message("Авто очистка для этого канала не включена.", ephemeral=True)


async def clear_list(channel, messages):

    try:
        await channel.delete_messages(messages=messages)
    except:
        for i in messages:
            i:discord.Message
            try:
                try:
                    await asyncio.sleep(0.5)
                    await i.delete()
                except:
                    await asyncio.sleep(1)
                    await i.delete()
            except:
                pass

async def do_clear(channel:discord.TextChannel, time_str:str=None, amount:int=None):
    if amount != None:
        if amount >= 1 and amount <= 1000:
            if time_str != None:
                unix = subcoms.timeAnalyzer(time_str)
                now = subcoms.currentTimeUnix()

                msgs = []
                async for message in channel.history(limit=amount):
                    if message:
                        if now-unix < subcoms.datetimeToUnix(message.created_at):
                            msgs.append(message)
                        else:
                            break
                    else:
                        break
                
                await clear_list(channel,msgs)
            else:
                msgs = []
                async for message in channel.history(limit=amount):
                    msgs.append(message)
                await clear_list(channel,msgs)
    elif time_str != None:

        unix = subcoms.timeAnalyzer(time_str)
        now = subcoms.currentTimeUnix()

        msgs = []
        async for message in channel.history():
            if message:
                if now-unix < subcoms.datetimeToUnix(message.created_at):
                    msgs.append(message)
                else:
                    break
            else:
                break
        
        await clear_list(channel,msgs)










        


# Command: unix_now
async def unix_now(i: discord.Interaction):
    embed = discord.Embed()

    embed.title = "Текущий UNIX (UTC+3)"
    embed.description = "-> **" + str(subcoms.currentTimeUnix()) + "**"

    embed.color = discord.Colour.from_str(defaultBotColor)

    await i.response.send_message(embed=embed)