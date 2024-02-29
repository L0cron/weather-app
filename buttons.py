from typing import Optional
import discord
from discord import Button


class Celebrations(discord.ui.View):

    def __init__(self, *, func, page, max_page, author_id, timeout: float | None = 180):
        super().__init__(timeout=timeout)
        self.page = page
        self.max_page = max_page

        self.author_id = author_id

        self.func = func

        self.check_buttons()


    def check_buttons(self):
        if self.page == 1:
            self.back.disabled = True
        else:
            self.back.disabled = False
        if self.page == self.max_page:
            self.next.disabled = True
        else:
            self.next.disabled = False

    # Put this inside of the View
    @discord.ui.button(label="Назад", style=discord.ButtonStyle.red)
    async def back(self, i: discord.Interaction, selfItem:discord.ui.Button):
        if i.user.id != self.author_id:
            await i.response.send_message("Чтобы пользоваться кнопками в этой команде, вы должны быть тем, кто её вызвал", ephemeral=True)
            return
        t = await self.func(i, self.page-1)
        nview = self
        nview.page+=-1
        nview.max_page = t[1]
        nview.check_buttons()
        await i.response.edit_message(embed=t[0], view=nview)
        await self.wait()

    # Put this inside of the View
    @discord.ui.button(label="Вперёд", style=discord.ButtonStyle.green)
    async def next(self, i: discord.Interaction, selfItem:discord.ui.Button):
        if i.user.id != self.author_id:
            await i.response.send_message("Чтобы пользоваться кнопками в этой команде, вы должны быть тем, кто её вызвал", ephemeral=True)
            return
        t = await self.func(i, self.page+1)
        nview = self
        nview.page +=1
        nview.max_page = t[1]
        nview.check_buttons()
        await i.response.edit_message(embed=t[0], view=nview)
        await self.wait()
        





