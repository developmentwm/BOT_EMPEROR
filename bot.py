import os
os.environ["DISCORD_DISABLE_VOICE"] = "1"

import discord
from discord.ext import commands

TOKEN = os.getenv("TOKEN_BOT_DISCORD")
TARGET_ROLE_NAME = "emperor7g"

intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)


class AnnounceModal(discord.ui.Modal):
    title = "📢 Pengumuman Emperor"

    def __init__(self):
        super().__init__()

        self.announcement = discord.ui.InputText(
            label="Isi Pengumuman",
            style=discord.InputTextStyle.long,
            placeholder="Tulis pengumuman di sini...",
            required=True,
            max_length=2000
        )

        self.add_item(self.announcement)

    async def callback(self, interaction: discord.Interaction):
        role = discord.utils.get(
            interaction.guild.roles,
            name=TARGET_ROLE_NAME
        )

        if not role:
            return await interaction.response.send_message(
                f"❌ Role `{TARGET_ROLE_NAME}` tidak ditemukan.",
                ephemeral=True
            )

        await interaction.channel.send(
            f"📢 **PENGUMUMAN RESMI**\n{role.mention}\n\n{self.announcement.value}"
        )

        await interaction.response.send_message(
            "✅ Pengumuman berhasil dikirim!",
            ephemeral=True
        )


@bot.command(name="announce")
@commands.has_permissions(administrator=True)
async def announce(ctx):
    await ctx.send_modal(AnnounceModal())


@announce.error
async def announce_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("❌ Kamu tidak punya izin untuk command ini.")


@bot.event
async def on_ready():
    print(f"Bot online sebagai {bot.user}")


bot.run(TOKEN)
