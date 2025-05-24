""""
Copyright © Krypton 2019-2023 - https://github.com/kkrypt0nn (https://krypton.ninja)
Description:
🐍 A simple template to start to code your own and personalized discord bot in Python programming language.

Version: 5.5.0
"""

import discord
from discord.ext import commands
from discord.ext.commands import Context
import logging

from helpers import checks, db_manager

logger = logging.getLogger(__name__)


# Here we name the cog and create a new class for the cog.
class Template(commands.Cog, name="template"):
    """Template para criação de novos comandos.
    
    Este arquivo serve como modelo para criar novos cogs.
    Copie este arquivo e modifique conforme necessário.
    """
    
    def __init__(self, bot):
        self.bot = bot
        logger.info(f"Cog {self.__class__.__name__} carregado")

    @commands.hybrid_command(
        name="testcommand",
        description="Comando de teste para verificar funcionalidade."
    )
    @checks.not_blacklisted()
    @checks.is_owner()
    async def testcommand(self, ctx: Context):
        """Comando de teste básico."""
        try:
            embed = discord.Embed(
                title="✅ Teste Bem-sucedido",
                description=(
                    f"Olá {ctx.author.mention}!\n\n"
                    "Este é um comando de teste que demonstra:\n"
                    "• Uso de embeds\n"
                    "• Verificações de permissão\n"
                    "• Logging de eventos\n"
                    "• Tratamento de erros\n\n"
                    f"**Servidor:** {ctx.guild.name}\n"
                    f"**Canal:** {ctx.channel.mention}\n"
                    f"**Usuário:** {ctx.author}\n"
                    f"**Timestamp:** <t:{int(ctx.message.created_at.timestamp())}:F>"
                ),
                color=0x00FF00
            )
            embed.set_footer(
                text="Template Neko Café", 
                icon_url=ctx.guild.icon.url if ctx.guild.icon else None
            )
            
            await ctx.send(embed=embed)
            logger.info(f"{ctx.author} executou o comando de teste")
            
        except Exception as e:
            logger.error(f"Erro no comando de teste: {e}")
            await ctx.send("❌ Ocorreu um erro ao executar o comando de teste.", ephemeral=True)
    
    @commands.hybrid_command(
        name="exemplo",
        description="Exemplo de comando com parâmetros."
    )
    @checks.not_blacklisted()
    async def exemplo(self, ctx: Context, *, texto: str = None):
        """Exemplo de comando que aceita parâmetros."""
        try:
            if not texto:
                embed = discord.Embed(
                    title="📝 Exemplo de Comando",
                    description=(
                        "Este comando aceita um parâmetro de texto.\n\n"
                        "**Uso:** `/exemplo <seu texto aqui>`\n\n"
                        "Exemplo: `/exemplo Olá mundo!`"
                    ),
                    color=0xF7BFCA
                )
            else:
                embed = discord.Embed(
                    title="📝 Texto Recebido",
                    description=f"Você enviou: **{texto}**",
                    color=0xF7BFCA
                )
                embed.add_field(
                    name="📊 Informações",
                    value=(
                        f"**Tamanho:** {len(texto)} caracteres\n"
                        f"**Palavras:** {len(texto.split())} palavras\n"
                        f"**Autor:** {ctx.author.mention}"
                    ),
                    inline=False
                )
            
            embed.set_footer(
                text="Template Neko Café", 
                icon_url=ctx.guild.icon.url if ctx.guild.icon else None
            )
            
            await ctx.send(embed=embed)
            logger.info(f"{ctx.author} executou comando exemplo com texto: '{texto}'")
            
        except Exception as e:
            logger.error(f"Erro no comando exemplo: {e}")
            await ctx.send("❌ Ocorreu um erro ao processar o comando.", ephemeral=True)
    
    @commands.Cog.listener()
    async def on_ready(self):
        """Evento chamado quando o bot está pronto."""
        logger.info(f"Template cog está pronto! Bot: {self.bot.user}")
    
    def cog_unload(self):
        """Chamado quando o cog é descarregado."""
        logger.info(f"Cog {self.__class__.__name__} descarregado")

async def setup(bot):
    await bot.add_cog(Template(bot))
