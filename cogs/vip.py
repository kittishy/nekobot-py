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
                title="Seja vip!",
                description="No Neko Café, oferecemos cargos VIP especiais para quem deseja apoiar o servidor e receber algumas regalias exclusivas! Cada nível de VIP garante vantagens únicas e acesso a benefícios especiais. Confira abaixo:\n\n<@&1361859905081966785>  | VIP Macaron\nO pacote perfeito para quem quer começar a apoiar o Neko Café!\nBenefícios:\n\nAcesso a um chat exclusivo para VIPs\n\nCargo personalizado com cor diferenciada\n\nPrioridade em eventos e sorteios\n\nEmoji exclusivo do servidor\n\nGanha 200k de sonhos por mês.\n\n( Preço: 200k sonhos por mês | 20$ ano )\n\n\n<@&1361860092450046092>  | VIP Cupcake\nUm passo acima, para quem quer mais destaque e mimos!\nBenefícios:\n\nTodos os benefícios do VIP macaron\n\nPedido de um emoji personalizado (com aprovação da staff)\n\nAcesso antecipado a eventos especiais\n\nRecompensas únicas em eventos do servidor\n\nPode pedir 1 arte/ícone personalizado em eventos de arte (limitado)\n\nGanha 300k de sonhos por mês.\n\n( Preço: 300k sonhos por mês | 30$ anos )\n\n\n<@&1361860208304980048>  | VIP Boba tea\nO cargo supremo dos apoiadores do Neko Café!\nBenefícios:\n\nTodos os benefícios anteriores\n\nPode sugerir canais/eventos que serão considerados com prioridade\n\nAcesso a áreas secretas do servidor\n\nGanha 400k de sonhos por mês.\n\n( Preço: 500k sonhos por mês | 50$ ano )\n\nPara pedir seu Vip abra um ticket em <#1361808252706361547> e escolha a opção \"Compre vip\" que um staff irá te atender e vc irá comprar com ele(a).")
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