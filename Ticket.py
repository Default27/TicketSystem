import nextcord
from nextcord.ext import commands
import asyncio

class OpenAndCloseW(nextcord.ui.View):
    def __init__(self):
        super().__init__()
        self.value = None

    @nextcord.ui.button(label="Delete", style=nextcord.ButtonStyle.danger)
    async def delete(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        await channel.send("Ticket Delete in few seconds.")
        await channel.delete()

class CloseConfirm(nextcord.ui.View):
    def __init__(self):
        super().__init__()
        self.value=None

    @nextcord.ui.button(label="Cancel", style=nextcord.ButtonStyle.grey)
    async def cancel(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        pass
    @nextcord.ui.button(label="Confirm", style=nextcord.ButtonStyle.danger)
    async def confirm(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        overwrites = {
            interaction.guild.default_role: nextcord.PermissionOverwrite(view_channel=False),
            interaction.guild.me: nextcord.PermissionOverwrite(view_channel=True),
            interaction.user: nextcord.PermissionOverwrite(view_channel=False)
        }
        await channel.edit(name=f"closed-{interaction.user}", overwrites=overwrites)
        await channel.send("Ticket Closed", view=OpenAndCloseW())
    
class Close(nextcord.ui.View):
    def __init__(self):
        super().__init__()
        self.value = None
    
    @nextcord.ui.button(label="Close", style=nextcord.ButtonStyle.red)
    async def close(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        await interaction.response.send_message("Are you Sure?", view=CloseConfirm(), ephemeral=True)

class Created(nextcord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        self.value = None

    @nextcord.ui.button(label='Confirm', style=nextcord.ButtonStyle.green)
    async def confirm(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        overwrites = {
            interaction.guild.default_role: nextcord.PermissionOverwrite(view_channel=False),
            interaction.guild.me: nextcord.PermissionOverwrite(view_channel=True),
            interaction.user: nextcord.PermissionOverwrite(view_channel=True)
        }
        global channel
        channel=await interaction.guild.create_text_channel(name=f"ticket-{interaction.user}", overwrites=overwrites)
        embed = nextcord.Embed(description=f"Ticket Created by: {interaction.user.mention}\nClick Button 🔒 to close this ticket", color=nextcord.Colour(0x0f0f0f))
        msg = await channel.send(f"{interaction.user.mention}", embed=embed, view=Close())
        await msg.pin()
        self.value = True
        self.stop()

class Create(nextcord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        self.value = None

    @nextcord.ui.button(label='Create', style=nextcord.ButtonStyle.grey, emoji="✉️")
    async def confirm(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        await interaction.response.send_message("Are you sure?", view=Created(), ephemeral=True)
        await asyncio.sleep(10)
        button.disabled
        

class Ticket(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def ticket(self, ctx):
        embed = nextcord.Embed(
            title = 'Ticket System',
            description = 'Click Button 📩 to make a ticket.',
            timestamp=ctx.message.created_at,
            color=nextcord.Colour(0x0f0f0f)
        )
        await ctx.send(embed=embed, view=Create())

def setup(bot):
    bot.add_cog(Ticket(bot))
