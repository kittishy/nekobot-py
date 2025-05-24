import discord
from discord.ext import commands
import logging

from helpers import checks, db_manager

logger = logging.getLogger(__name__)

class PersistentView(commands.Bot):
    def __init__(self):
        super().__init__()
        self.add_view(Formulario())
        

class Formulario(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
  
    @discord.ui.button(label="Seja staff", style=discord.ButtonStyle.grey, custom_id="staff_form_button")
    async def send_button(self, interaction: discord.Interaction, button):
        """Botão para acessar o formulário de staff."""
        try:
            embed = discord.Embed(
                title="📋 Formulário de Staff",
                description=(
                    "Para se candidatar à nossa equipe, preencha o formulário através do link abaixo:\n\n"
                    "[**🔗 Clique aqui para acessar o formulário**](https://docs.google.com/forms/d/e/1FAIpQLSdL3RXpLDpptARGnmccoSCYWhrRQNReORMtLXGBHhQGq8wD9Q/viewform?usp=header)\n\n"
                    "✨ **Dicas importantes:**\n"
                    "• Preencha todas as informações com cuidado\n"
                    "• Seja honesto(a) em suas respostas\n"
                    "• Demonstre sua paixão pela comunidade\n\n"
                    "Boa sorte! 🍀"
                ),
                color=0xF7BFCA
            )
            embed.set_footer(text="Equipe Neko Café", icon_url=interaction.guild.icon.url if interaction.guild.icon else None)
            
            await interaction.response.send_message(embed=embed, ephemeral=True)
            logger.info(f"{interaction.user} acessou o formulário de staff")
            
        except Exception as e:
            logger.error(f"Erro ao enviar formulário para {interaction.user}: {e}")
            await interaction.response.send_message(
                "❌ Ocorreu um erro ao processar sua solicitação. Tente novamente mais tarde.",
                ephemeral=True
            )

class Modals(commands.Cog, name="form"):
    def __init__(self, bot):
        self.bot = bot

    @commands.hybrid_command(
        name="form",
        description="Envia o painel de formulário para staff."
    )
    @checks.is_owner()
    async def form_panel(self, ctx: commands.Context):
        """Envia o painel de formulário para candidatura à staff."""
        try:
            # Embed principal
            embed = discord.Embed(
                title="🌟 Seja Staff do Neko Café!",
                description=(
                    "O Neko Café está crescendo e agora abrimos vagas para nossa equipe de Staff! "
                    "Se você é alguém fofo, responsável e adora ajudar a comunidade, essa é a sua chance de brilhar com a gente!\n\n"
                    "**📋 Áreas disponíveis:**\n"
                    "*Você pode escolher quantas quiser!*\n\n"
                    "🗞️ **Jornal:** Crie boletins com novidades, atualizações e curiosidades do servidor\n"
                    "🤝 **Parceria:** Ajude a encontrar e manter parcerias com outros servidores\n"
                    "🎤 **Mov Call:** Interaja com membros nas calls, mantendo o ambiente animado e seguro\n"
                    "💬 **Mov Chat:** Converse com os membros no chat, mantenha a conversa viva e acolhedora\n"
                    "🎉 **Eventos:** Organize eventos, dinâmicas e jogos divertidos para a comunidade\n"
                    "🎁 **Sorteios:** Cuide dos sorteios do servidor, garantindo que tudo seja justo e fofo\n"
                    "👋 **Recepcionista:** Dê boas-vindas aos novos membros e os ajude a se sentirem em casa no café\n\n"
                    "**✨ O que esperamos de você:**\n"
                    "• Responsabilidade e boa comunicação\n"
                    "• Presença ativa no servidor\n"
                    "• Vontade de colaborar com a equipe\n"
                    "• Amor por animes, jogos e gatinhos!\n\n"
                    "**📝 Como se inscrever:**\n"
                    "Clique no botão abaixo para acessar o formulário de candidatura!\n\n"
                    "Venha fazer parte da equipe que cuida com carinho do Neko Café!\n"
                    "Esperamos você com uma xícara quentinha de café e muitos miaus! ☕🐱"
                ),
                color=0xF7BFCA
            )
            
            # Adicionando a imagem
            embed.set_image(url="https://cdn.discordapp.com/attachments/1334474182049796131/1373811364618829946/seja_staff_by_aishy.png?ex=6831b3c9&is=68306249&hm=ca885596e935c31d757c1eaf6c6ccb9f948f1f8f5b8d570df8a769c29fcfa293&")
            embed.set_footer(text="Equipe Neko Café", icon_url=ctx.guild.icon.url if ctx.guild.icon else None)
            
            # Enviar embed
            await ctx.send(embed=embed)
            
            # Enviar view com botão
            view = Formulario()
            await ctx.send(view=view)
            
            logger.info(f"{ctx.author} enviou o painel de formulário de staff")
            
        except Exception as e:
            logger.error(f"Erro ao enviar painel de formulário: {e}")
            await ctx.send("❌ Ocorreu um erro ao enviar o painel de formulário.", ephemeral=True)


async def setup(bot):
   bot.add_view(Formulario())
   await bot.add_cog(Modals(bot))