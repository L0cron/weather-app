import discord
from discord import app_commands, SelectOption

# own
import commands
import subcoms

mainGuildID = commands.mainGuildID

client = commands.client
tree = commands.tree






@tree.command(name = 'пинг', description = "Пинг!", guild=discord.Object(mainGuildID))
async def command(i: discord.Interaction):
    await commands.test(i)










@tree.command(name = 'создать_поздравление', description = "Создать заготовку поздравления", guild=discord.Object(mainGuildID))
@app_commands.describe(заголовок='Оглавление поздравления', текст_поздравления="Текст поздравления. & - для переноса строки.", цвет="Цвет сообщения", картинка_url="URL картинки поздравления")
async def command(i: discord.Interaction, заголовок:str, текст_поздравления:str, цвет:str='#c242f5', картинка_url:str=None):
    await commands.add_celebrate(i,заголовок,текст_поздравления,цвет,картинка_url)

@tree.command(name = 'поздравления', description = "Посмотреть заготовки поздправлений", guild=discord.Object(mainGuildID))
@app_commands.describe(id="ID для просмотра определённого поздравления", страница="Страница")
async def command(i: discord.Interaction, id:int=None, страница:int=1):
    await commands.celebrationlist(i,id,страница)

@tree.command(name = 'удалить_поздравление', description = "Удалить заготовку поздравления", guild=discord.Object(mainGuildID))
@app_commands.describe(id="ID поздравления")
async def command(i: discord.Interaction, id:int):
    await commands.delcelebration(i,id)


@tree.command(name = 'добавить_именинника', description = "Поздравить участника с днём рождения и выдать роль именинника (если она имеется)", guild=discord.Object(mainGuildID))
@app_commands.describe(участник="Участник", дата='Когда? (ДД.ММ)')
async def command(i: discord.Interaction, участник:discord.User, дата:str):
    await commands.celebrate(i,участник,дата)


@tree.command(name = 'удалить_именинника', description = "Удалить именинника из очереди на отправку поздравлений", guild=discord.Object(mainGuildID))
@app_commands.describe(участник="Участник", id="ID пользователя")
async def command(i: discord.Interaction, участник:discord.User=None, id:int=None):
    await commands.delcelebrationist(i,участник,id)



@tree.command(name = 'именинники', description = "Посмотреть список именинников", guild=discord.Object(mainGuildID))
@app_commands.describe(страница="Страница", участник="Пользователь для проверки")
async def command(i: discord.Interaction, страница:int=None, участник:discord.User=None):
    await commands.celebrations(i,страница, участник)


@tree.command(name = 'перепоздравить', description = "Перепоздравить всех участников за сегодня заново, если что-то пошло не так", guild=discord.Object(mainGuildID))
async def command(i: discord.Interaction):
    await commands.recelebrate(i)




@tree.command(name = 'роль_именинника', description = "Установить роль именинника", guild=discord.Object(mainGuildID))
@app_commands.describe(id_роли="ID роли")
async def command(i: discord.Interaction, id_роли:str):
    await commands.setrolebday(i,id_роли)

@tree.command(name = 'канал_именинников', description = "Установить канал именинников", guild=discord.Object(mainGuildID))
@app_commands.describe(id_канала="ID канала")
async def command(i: discord.Interaction, id_канала:str):
    await commands.setchannelbday(i,id_канала)


# Useful
    
@tree.command(name = 'очистить', description = "Очистить этот канал", guild=discord.Object(mainGuildID))
@app_commands.describe(время="За какой промежуток удалить сообщения? (Формат: 1г1д1ч1м1с)", количество="Сколько сообщений удалить?")
async def command(i: discord.Interaction, время:str=None, количество:int=None):
    await commands.clear(i,время,количество)

@tree.command(name = 'авто_очистка', description = "Автоматически удалять каждое новое сообщение по прошествии N времени", guild=discord.Object(mainGuildID))
@app_commands.describe(время="N (Формат: 1г1д1ч1м1с)")
async def command(i: discord.Interaction, время:str):
    await commands.auto_clear(i,время)

@tree.command(name = 'убрать_авто_очистку', description = "Отменить все запланированные удаления сообщений", guild=discord.Object(mainGuildID))
@app_commands.describe()
async def command(i: discord.Interaction):
    await commands.del_auto_clear(i)



@tree.command(name = 'текущий_unix', description = "Получить время в секундах c 1 января 1970г. (UTC+3)", guild=discord.Object(mainGuildID))
@app_commands.describe()
async def command(i: discord.Interaction):
    await commands.unix_now(i)
    


@tree.command(name = 'установить_шанс_реакции', description = "Устанавливает шанс реакции на ваше сообщение рандомным emoji сервера", guild=discord.Object(mainGuildID))
@app_commands.describe(шанс='0-100%')
async def command(i: discord.Interaction, шанс:int=None):
    await commands.set_react_chance(i,шанс)
    

@tree.command(name = 'установить_шанс_ответной_реакции', description = "Устанавливает шанс ответа на сообщения других пользователей, содержащее рандомное emoji сервера", guild=discord.Object(mainGuildID))
@app_commands.describe(шанс='0-100%')
async def command(i: discord.Interaction, шанс:int=None):
    await commands.set_reply_react_chance(i,шанс)
    

@tree.command(name = 'установить_шанс_сообщения', description = "Устанавливает шанс рандомного сообщения, добавленного в /добавить_текст", guild=discord.Object(mainGuildID))
@app_commands.describe(шанс='0-100%')
async def command(i: discord.Interaction, шанс:int=None):
    await commands.set_message_chance(i,шанс)
    
@tree.command(name = 'добавить_текст', description = "Добавляет текст, который будет отправляться с каким-то шансом (Несколько через `;`)", guild=discord.Object(mainGuildID))
@app_commands.describe(текст='Текст сообщения')
async def command(i: discord.Interaction, текст:str):
    await commands.add_text(i,текст)


@tree.command(name = 'тексты', description = "Просмотреть текущие тексты", guild=discord.Object(mainGuildID))
@app_commands.describe(id='ID текста(ов)', страница='Страница для отображения')
async def command(i: discord.Interaction, id:int=None, страница:int=None):
    await commands.texts(i,id,страница)


@tree.command(name = 'удалить_текст', description = "Удаляет текст, который отправляется с каким-то шансом (Несколько через `;`)", guild=discord.Object(mainGuildID))
@app_commands.describe(id='ID текста(ов)')
async def command(i: discord.Interaction, id:str):
    await commands.del_text(i,id)





with open('./token.txt', 'r') as f:
    token = f.readline()


client.run(token)






