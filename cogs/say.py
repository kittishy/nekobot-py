import discord
from discord.ext import commands
from discord.ext.commands import Context
import logging

from helpers import checks

logger = logging.getLogger(__name__)

class Say(commands.Cog, name="say"):
    """Comandos para enviar mensagens como bot.
    
    Este módulo permite que usuários autorizados enviem mensagens através do bot.
    """
    
    def __init__(self, bot):
        self.bot = bot
        logger.info(f"Cog {self.__class__.__name__} carregado")

    @commands.hybrid_command(
        name="say",
        description="Faz o bot enviar uma mensagem no canal."
    )
    @commands.has_permissions(manage_messages=True)
    @checks.not_blacklisted()
    async def say(self, ctx: Context, *, mensagem: str):
        """Envia uma mensagem como o bot.

        :param ctx: O contexto do comando.
        :param mensagem: A mensagem que será enviada.
        """
        try:
            # Deleta o comando original para manter apenas a mensagem do bot
            if not isinstance(ctx.channel, discord.DMChannel):
                await ctx.message.delete()
            
            # Envia a mensagem como o bot
            await ctx.send(mensagem)
            
            # Registra o uso do comando
            logger.info(f"{ctx.author} usou o comando say para enviar: '{mensagem}'")
            
        except discord.Forbidden:
            await ctx.send("❌ Não tenho permissão para deletar mensagens neste canal.", ephemeral=True)
        except Exception as e:
            logger.error(f"Erro no comando say: {e}")
            await ctx.send("❌ Ocorreu um erro ao enviar a mensagem.", ephemeral=True)
    
    def cog_unload(self):
        """Chamado quando o cog é descarregado."""
        logger.info(f"Cog {self.__class__.__name__} descarregado")

async def setup(bot):
    await bot.add_cog(Say(bot))