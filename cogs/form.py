import discord
from discord.ext import commands

from helpers import checks, db_manager

class PersistentView(commands.Bot):
    def __init__(self):
        self.add_view(Formulario())
        

class Formulario(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
  
    @discord.ui.button(label="Seja staff", style=discord.ButtonStyle.grey, custom_id="1")
    async def send_button(self, interaction: discord.Interaction, button):
        # Agora apenas envia uma mensagem direcionando para o Google Forms
        await interaction.response.send_message(
            "📋 **Formulário de Staff**\n\n"
            "Para se candidatar à nossa equipe, preencha o formulário através do link:\n"
            "[**Clique aqui para acessar o formulário**](https://docs.google.com/forms/d/e/1FAIpQLSdL3RXpLDpptARGnmccoSCYWhrRQNReORMtLXGBHhQGq8wD9Q/viewform?usp=header)\n\n"
            "Boa sorte! 🍀",
            ephemeral=True
        )

class Modals(commands.Cog, name="form"):
    def __init__(self, bot):
        self.bot = bot

    @commands.hybrid_command(
        name="form",
        description="Formulário staff."
    )
    @checks.is_owner()
    async def textbox(self, ctx: commands.Context):
        
        # Embed atualizada baseada no JSON fornecido
        embed = discord.Embed(
            title="Seja Staff do Neko Café!",
            description="O Neko Café está crescendo e agora abrimos vagas para nossa equipe de Staff! Se você é alguém fofo, responsável e adora ajudar a comunidade, essa é a sua chance de brilhar com a gente!\n\nÁreas disponíveis:\n\nVocê pode escolher quantas quiser!\n\nJornal: Crie boletins com novidades, atualizações e curiosidades do servidor.\n\nParceria: Ajude a encontrar e manter parcerias com outros servidores!\n\nMov Call: Interaja com membros nas calls, mantendo o ambiente animado e seguro.\n\nMov Chat: Converse com os membros no chat, mantenha a conversa viva e acolhedora!\n\nEventos: Organize eventos, dinâmicas e jogos divertidos para a comunidade.\n\nSorteios: Cuide dos sorteios do servidor, garantindo que tudo seja justo e fofo!\n\nRecepcionista: Dê boas-vindas aos novos membros e os ajude a se sentirem em casa no café!\n\n\nO que esperamos de você:\n\nResponsabilidade e boa comunicação\n\nPresença ativa no servidor\n\nVontade de colaborar com a equipe\n\nAmor por animes, jogos e gatinhos!\n\n\nComo se inscrever:\n\nBasta preencher o formulário abaixo com cuidado e escolher as áreas que mais combinam com você:\n[Formulário de inscrição - Clique aqui](https://docs.google.com/forms/d/e/1FAIpQLSdL3RXpLDpptARGnmccoSCYWhrRQNReORMtLXGBHhQGq8wD9Q/viewform?usp=header)\n\nVenha fazer parte da equipe que cuida com carinho do Neko Café!\nEsperamos você com uma xícara quentinha de café e muitos miaus!",
            color=0xF7BFCA  # 16234970 em hexadecimal
        )
        
        # Adicionando a imagem da embed
        embed.set_image(url="https://cdn.discordapp.com/attachments/1334474182049796131/1373811364618829946/seja_staff_by_aishy.png?ex=6831b3c9&is=68306249&hm=ca885596e935c31d757c1eaf6c6ccb9f948f1f8f5b8d570df8a769c29fcfa293&")
        
        await ctx.send(embed=embed)
        
        view = discord.ui.View
        view = Formulario()
        await ctx.send(view=view)


async def setup(bot):
   bot.add_view(Formulario())
   await bot.add_cog(Modals(bot))