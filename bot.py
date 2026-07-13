import os
import discord
from discord.ext import commands

class ChoixView(discord.ui.View):
    def __init__(self, createur, joueur):
        super().__init__()
        self.createur = createur
        self.joueur = joueur

    async def interaction_check(self, interaction: discord.Interaction):
        return True

    @discord.ui.button(label="Action", emoji="🎯", style=discord.ButtonStyle.primary)
    async def action(self, interaction: discord.Interaction, button: discord.ui.Button):
        for item in self.children:
            if item.label != "Fermer le défi":
                item.disabled = True

        await interaction.response.edit_message(view=self) 
        await interaction.channel.edit(name=f"🎯 Action - {self.joueur.display_name}")
        await interaction.followup.send("🎯 Action choisie !", view=ResultatDefiView(self.createur))
    @discord.ui.button(label="Vérité", emoji="💬", style=discord.ButtonStyle.success)
    async def verite(self, interaction: discord.Interaction, button: discord.ui.Button):
        for item in self.children:
            if item.label != "Fermer le défi":
                item.disabled = True

        await interaction.response.edit_message(view=self)
        await interaction.channel.edit(name=f"💬 Vérité - {self.joueur.display_name}")
        await interaction.followup.send("💬 Vérité choisie !", view=ResultatDefiView(self.createur))

    @discord.ui.button(label="Fermer le défi", emoji="❌", style=discord.ButtonStyle.danger)
    async def fermer(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user.id != self.createur.id and not interaction.user.guild_permissions.administrator:
            await interaction.response.send_message("❌ Tu n'as pas la permission de fermer ce défi.", ephemeral=True)
            return

        await interaction.response.send_message("🔒 Défi fermé.")
        await interaction.channel.edit(archived=True)

class ResultatDefiView(discord.ui.View):
    def __init__(self, createur):
        super().__init__()
        self.createur = createur

    async def interaction_check(self, interaction: discord.Interaction):
        if interaction.user.id != self.createur.id:
            await interaction.response.send_message("❌ Seul le lanceur du défi peut valider le résultat.", ephemeral=True)
            return False
        return True

    @discord.ui.button(label="Défi réussi", emoji="✅", style=discord.ButtonStyle.success)
    async def reussi(self, interaction: discord.Interaction, button: discord.ui.Button):
        for item in self.children:
            item.disabled = True

        await interaction.response.edit_message(view=self)
        await interaction.followup.send(f"✅ Défi réussi validé par {interaction.user.mention} !")

    @discord.ui.button(label="Défi échoué", emoji="❌", style=discord.ButtonStyle.danger)
    async def echoue(self, interaction: discord.Interaction, button: discord.ui.Button):
        for item in self.children:
            item.disabled = True

        await interaction.response.edit_message(view=self)
        await interaction.followup.send(f"❌ Défi échoué validé par {interaction.user.mention}.")

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

SALON_JEU_ID = 1526274288188133386

@bot.event
async def on_ready():
    print(f"{bot.user} est connecté !")

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    if message.channel.id == SALON_JEU_ID:
        if message.mentions and ("action ou vérité" in message.content.lower() or "action ou verite" in 
message.content.lower()):
            joueur = message.mentions[0]

            thread = await message.create_thread(name=f"🎲 Action ou Vérité {joueur.display_name}", auto_archive_duration=60) 
            await thread.send(f"🎲 {joueur.mention}, choisis :", view=ChoixView(message.author, joueur))
    await bot.process_commands(message)

bot.run(os.getenv("TOKEN"))
