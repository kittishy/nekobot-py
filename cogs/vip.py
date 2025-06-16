import discord
from discord.ext import commands
from discord.ext.commands import Context
import logging
from helpers import checks

logger = logging.getLogger(__name__)

class VIP(commands.Cog, name="vip"):
    def __init__(self, bot):
        self.bot = bot
        logger.info(f"Cog {self.__class__.__name__} carregado")

    @commands.hybrid_command(
        name="vip",
        description="Exibe informações sobre os planos VIP."
    )
    @checks.not_blacklisted()
    async def vip(self, ctx: Context):
        """Exibe informações sobre os planos VIP disponíveis."""
        try:
            embed = discord.Embed(
                color=9879032,
                title="☕✨ VIPs do Neko Café ✨🍰",
                description="Quer apoiar o Neko Café e ainda receber regalias super especiais? Conheça nossos cargos VIP e escolha o que combina mais com você! Cada nível oferece mimos únicos e benefícios incríveis! 💖\n---\n💗 <@&1361859905081966785> | VIP Macaron\nO pacote perfeito para quem quer começar a apoiar o Neko Café com carinho! 🎀\nBenefícios:\nAcesso a um chat exclusivo para VIPs 🗨️\nCargo personalizado com cor diferenciada 🎨\nPrioridade em eventos e sorteios 🎉\nEmoji exclusivo do servidor 💫\nPreço:\n・Mensal: 200k sonhos\n・Anual: 300k sonhos ou R$ 20,00\n---\n🍰 <@&1361860092450046092> | VIP Cupcake\nPara quem quer mais destaque, mimos e exclusividades! 💝\nBenefícios:\nTodos os benefícios do VIP Macaron 🍬\nPedido de 1 emoji personalizado (com aprovação da staff) 🧁\nAcesso antecipado a eventos especiais 🎟️\nRecompensas únicas em eventos do servidor 🎁\nPode pedir 1 arte/ícone personalizado em eventos de arte (limitado) 🎨\nPreço:\n・Mensal: 300k sonhos\n・Anual: 400k sonhos ou R$ 30,00\n---\n🧋 <@&1361860208304980048> | VIP Boba Tea\nO cargo supremo para os maiores apoiadores do Neko Café! 👑\nBenefícios:\nTodos os benefícios anteriores 🍓\nPode sugerir canais/eventos que serão considerados com prioridade 🌟\nAcesso a áreas secretas do servidor 🔐\nPreço:\n・Mensal: 500k sonhos\n・Anual: 1 milhão de sonhos ou R$ 50,00\n---\n💬 Como adquirir seu VIP?\nAbra um ticket em <#1361808252706361547> e selecione a opção \"Compre VIP\"!\nUm staff vai te atender e te ajudar com a compra. 💌\n\n*Compre somente com <@&1357103935047073974> e <@&1366948874861936671>")
            embed.set_image(url="https://cdn.discordapp.com/attachments/1334474182049796131/1373811364207919287/seja_vip_by_aishy.png?ex=6835a849&is=683456c9&hm=536575233612f0c51872dc3d76f308a193b5104ccce6a446b06c6efe4c050723&")
           
            await ctx.send(embed=embed)
            logger.info(f"Comando VIP executado por {ctx.author.name}")
        except Exception as e:
            logger.error(f"Erro ao executar comando VIP: {str(e)}")
            await ctx.send("Ocorreu um erro ao exibir as informações VIP.")

    def cog_unload(self):
        """Chamado quando o cog é descarregado."""
        logger.info(f"Cog {self.__class__.__name__} descarregado")

async def setup(bot):
    await bot.add_cog(VIP(bot))