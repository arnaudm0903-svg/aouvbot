import os
import discord
from discord.ext import commands


SALON_JEU_ID = 1526274288188133386


class ResultatDefiView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="Défi réussi", emoji="✅", style=discord.ButtonStyle.success)
    async def reussi(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.edit_message(
            content=f"✅ Défi réussi validé par {interaction.user.mention}",
            view=None
        )

    @discord.ui.button(label="Défi échoué", emoji="❌", style=discord.ButtonStyle.danger)
    async def echoue(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.edit_message(
            content=f"❌ Défi échoué validé par {interaction.user.mention}",
            view=None
        )


class ChoixView(discord.ui.View):
    def __init__(self, joueur):
        super().__init__(timeout=None)
        self.joueur = joueur

    @discord.ui.button(label="Action", emoji="🎯", style=discord.ButtonStyle.primary)
    async def action(self, interaction: discord.Interaction, button: discord.ui.Button):

        await interaction.response.edit_message(view=None)

        await interaction.channel.edit(
            name=f"🎯-action-{self.joueur.display_name}"
        )

        await interaction.channel.send(
            "🎯 Action choisie !",
            view=ResultatDefiView()
        )


    @discord.ui.button(label="Vérité", emoji="💬", style=discord.ButtonStyle.success)
    async def verite(self, interaction: discord.Interaction, button: discord.ui.Button):

        await interaction.response.edit_message(view=None)

        await interaction.channel.edit(
            name=f"💬-verite-{self.joueur.display_name}"
        )

        await interaction.channel.send(
            "💬 Vérité choisie !",
            view=ResultatDefiView()
        )


    @discord.ui.button(label="Fermer le défi", emoji="❌", style=discord.ButtonStyle.danger)
    async def fermer(self, interaction: discord.Interaction, button: discord.ui.Button):

        if not interaction.user.guild_permissions.manage_threads:
            await interaction.response.send_message(
                "❌ Tu n'as pas la permission.",
                ephemeral=True
            )
            return

        await interaction.response.send_message(
            "🔒 Défi fermé."
        )

        await interaction.channel.edit(archived=True)


intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(
    command_prefix="!",
    intents=intents
)


@bot.event
async def on_ready():
    print(f"{bot.user} est connecté !")


@bot.event
async def on_message(message):

    if message.author == bot.user:
        return

    if message.channel.id == SALON_JEU_ID:

        contenu = message.content.lower()

        if message.mentions and (
            "action ou vérité" in contenu
            or "action ou verite" in contenu
        ):

            joueur = message.mentions[0]

            thread = await message.create_thread(
                name=f"🎲-action-ou-verite-{joueur.display_name}",
                auto_archive_duration=60
            )

            await thread.send(
                f"🎲 {joueur.mention}, choisis ton défi :",
                view=ChoixView(joueur)
            )

    await bot.process_commands(message)


bot.run(os.getenv("TOKEN"))
