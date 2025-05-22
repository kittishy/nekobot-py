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
        await interaction.response.send_modal(FormularioModal())

class FormularioModal(discord.ui.Modal):
    def __init__(self):
        super().__init__(title="Formulário")

        self.user_name = discord.ui.TextInput(label='Insira seu id, nome e idade', placeholder="EX. (1051233527510880276, 916shoco#000, 18)", required=True, max_length=100)
        self.staff = discord.ui.TextInput(label='Em qual área você deseja entrar', placeholder="Ex. (MOV.CHAT, MOV.CALL, JORNALISTA, PARCERIA)", required=True, max_length=100)
        self.xp = discord.ui.TextInput(label='Tem experiencia como staf? se sim, qual área', placeholder="DIGITE AQUI", required=False, max_length=100)
        self.quest = discord.ui.TextInput(label='O que significa maturidade para você?', placeholder="DIGITE AQUI", required=True, max_length=100)
        self.quest2 = discord.ui.TextInput(label='Por que deseja fazer parte da nossa equipe?', placeholder="DIGITE AQUI", required=False, max_length=100)


        self.add_item(self.user_name)
        self.add_item(self.staff)
        self.add_item(self.xp)
        self.add_item(self.quest)
        self.add_item(self.quest2)

    async def on_submit(self, interaction: discord.Interaction):
        await interaction.response.send_message(f"Obrigado por fazer o formulário, {interaction.user.mention}! Iremos conferir as suas respostas.", ephemeral = True)

        channel = discord.utils.get(interaction.guild.text_channels, name="👥﹒log-form")
        if channel is not None:
            await channel.send(f"Formulário enviado por {interaction.user.mention}\nNome: {self.user_name}\nÁrea: {self.staff}\nExperiencia: {self.xp}\nQ1: {self.quest}\nQ2: {self.quest2}")
        else:
            await interaction.followup.send("Canal de logs não encontrado.", ephemeral=True)
            
class Modals(commands.Cog, name="form"):
    def __init__(self, bot):
        self.bot = bot

    @commands.hybrid_command(
        name="form",
        description="Formulário staff."
    )
    @checks.is_owner()
    async def textbox(self, ctx: commands.Context):
        
        embed = discord.Embed(
            colour=discord.Color.pink(),
            title="Faça parte da nossa equipe! Leia abaixo alguns requisitos para você fazer parte da nossa equipe:",
            description="<:a_heart:1175980769039101973> Ter mais de 14 anos.\n<:a_heart:1175980769039101973> Ter responsabilidade e maturidade.\n<:a_heart:1175980769039101973> Seguir todas as nossas regras.\n<:a_heart:1175980769039101973> Ter comprometimento com os seus deveres de staff.\nCaso você tenha todos esses requisitos, clique em (Seja staff) e faça seu formulário.\n\n<:a_deco:1145911754484895804> **Vagas disponíveis:**\n<a:a_heart:1175980873775054898> : <@&1133969535574229082>\n<a:a_heart:1175980873775054898> : <@&1169758814657061058>\n<a:a_heart:1175980873775054898> : <@&1134495509973835916>\n<a:a_heart:1175980873775054898> : <@&1064393279682129960>\n<a:a_heart:1175980873775054898> : <@&1162591389205401600>\n<a:a_heart:1175980873775054898> : <@&1021795328657207498>"
            )
        embed.set_image(url="https://media.discordapp.net/attachments/1134194576563904522/1176244265962180708/539_Sem_Titulo4_20230806102355.png?ex=656e29d6&is=655bb4d6&hm=ca48aff47f471d7e798838e0c9e759aedb27bf1e51450fb4d1219ad1bc797138&=")
        await ctx.send(embed=embed)
        
        view = discord.ui.View
        view = Formulario()
        await ctx.send(view=view)


async def setup(bot):
   bot.add_view(Formulario())
   await bot.add_cog(Modals(bot))