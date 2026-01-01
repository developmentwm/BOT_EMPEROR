import os
os.environ["DISCORD_DISABLE_VOICE"] = "1"  # WAJIB: cegah error voice di Railway

import discord
from discord.ext import commands

TOKEN = os.getenv("TOKEN_BOT_DISCORD")  # ambil dari Railway ENV
TARGET_ROLE_NAME = "emperor7g"  # Ganti sesuai role tujuan

intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)

class AnnouncementModal(discord.ui.Modal, title="📢 Pengumuman Emperor"):
    message = discord.ui.InputText(
        label="Isi Pengumuman",
        style=discord.InputTextStyle.long,
        placeholder="Tulis pengumuman di sini...",
        required=True,
        max_length=2000
    )

    async def callback(self, interaction: discord.Interaction):
        guild = interaction.guild
        role = discord.utils.get(guild.roles, name=TARGET_ROLE_NAME)

        if not role:
            await interaction.response.send_message(
                f"❌ Role `{TARGET_ROLE_NAME}` tidak ditemukan.",
                ephemeral=True
            )
            return

        content = f"📢 **PENGUMUMAN RESMI**\n{role.mention}\n\n{self.message.value}"

        await interaction.channel.send(content)
        await interaction.response.send_message(
            "✅ Pengumuman berhasil dikirim!",
            ephemeral=True
        )


@bot.command(name="announce")
@commands.has_permissions(administrator=True)
async def announce(ctx):
    modal = AnnouncementModal()
    await ctx.send_modal(modal)


@announce.error
async def announce_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("❌ Kamu tidak punya izin menggunakan command ini.")


@bot.event
async def on_ready():
    print(f"Bot aktif sebagai {bot.user}")


bot.run(TOKEN)
