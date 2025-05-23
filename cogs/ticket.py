import discord
from discord.ext import commands

from helpers import checks, db_manager

id_cargo_atendente = 1064393279682129960  # Corrigido para inteiro

class Dropdown(discord.ui.Select):
    def __init__(self):
        options = [
            discord.SelectOption(value="comprar", label="Comprar", emoji="👋"),
            discord.SelectOption(value="duvidas", label="Duvidas", emoji="❓"),
            discord.SelectOption(value="denunciar", label="Denunciar", emoji="👮"),
            discord.SelectOption(value="parceria", label="Parcerias", emoji="🤝"),
            discord.SelectOption(value="patrocinio", label="Patrocinio", emoji="🚀"),
        ]
        super().__init__(
            placeholder="Selecione uma opção...",
            min_values=1,
            max_values=1,
            options=options,
            custom_id="persistent_view:dropdown_help"
        )

    async def callback(self, interaction: discord.Interaction):
        if self.values[0] == "comprar":
            await interaction.response.send_message("Compre cargos e vip", ephemeral=True, view=CreateTicket())
        elif self.values[0] == "parceria":
            await interaction.response.send_message("Faça parceria com nosso servidor", ephemeral=True, view=CreateTicket())
        elif self.values[0] == "patrocinio":
            await interaction.response.send_message("Solicite esse ticket para fazer seu patrocinio", ephemeral=True, view=CreateTicket())
        elif self.values[0] == "duvidas":
            await interaction.response.send_message("Tire sua duvida sobre qualquer coisa aqui", ephemeral=True, view=CreateTicket())
        elif self.values[0] == "denunciar":
            await interaction.response.send_message("Solicite esse ticket para fazer uma denuncia", ephemeral=True, view=CreateTicket())



class CreateTicket(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="Abrir Ticket", style=discord.ButtonStyle.blurple, emoji="➕", custom_id='open_ticket_button')
    async def open_ticket_button_callback(self, interaction: discord.Interaction, button: discord.ui.Button):
        ticket = None
        for thread in interaction.channel.threads:
            if f"{interaction.user.id}" in thread.name:
                if thread.archived:
                    ticket = thread
                else:
                    await interaction.response.send_message(ephemeral=True, content=f"Você já tem um atendimento em andamento!")
                    return
    
        async for thread in interaction.channel.archived_threads(private=True):
            if f"{interaction.user.id}" in thread.name:
                if thread.archived:
                    ticket = thread
                else:
                    await interaction.edit_original_response(content=f"Você já tem um atendimento em andamento!", view=None)  // Assuming this is an interaction on the panel message
                    return
        
        if ticket is not None:
            await ticket.edit(archived=False, locked=False)
            await ticket.edit(name=f"{interaction.user.name} ({interaction.user.id})", auto_archive_duration=10080, invitable=False)
        else:
            ticket = await interaction.channel.create_thread(name=f"{interaction.user.name} ({interaction.user.id})", auto_archive_duration=10080)
            await ticket.edit(invitable=False)
    
        await interaction.response.send_message(ephemeral=True, content=f"Criei um ticket para você! {ticket.mention}")
        await ticket.send(f"📩  **|** || {interaction.user.mention} <@&1064393279682129960> ||  Ticket criado com sucesso! Envie todas as informações possíveis sobre seu caso e aguarde até que um atendente responda.\n\n Após a sua questão ser resolvida, clique em ""Fechar Ticket"" para encerrar o atendimento!")
        await ticket.send(view=Close_Ticket())

    async def confirm(self, interaction:discord.Interaction, button:discord.ui.Button):
        mod = interaction.guild.get_role(id_cargo_atendente)
        if str(interaction.user.id) in interaction.channel.name or (mod and mod in interaction.user.roles):
            await interaction.response.send_message(f"O ticket foi arquivado por {interaction.user.mention}, obrigado por entrar em contato!")
            await interaction.channel.edit(archived=True, locked=True)
        else:
            await interaction.response.send_message("Você não tem permissão para fechar este ticket.")

class TicketPanelView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None) # Timeout None for persistent view
        self.add_item(Dropdown())

class Close_Ticket(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="Fechar Ticket", style=discord.ButtonStyle.red, emoji="🔒", custom_id='Close_Ticket')
    async def confirm(self, interaction:discord.Interaction, button:discord.ui.Button):
        mod = interaction.guild.get_role(id_cargo_atendente)
        if str(interaction.user.id) in interaction.channel.name or (mod and mod in interaction.user.roles):
            await interaction.response.send_message(f"O ticket foi arquivado por {interaction.user.mention}, obrigado por entrar em contato!")
            await interaction.channel.edit(archived=True, locked=True)
        else:
            await interaction.response.send_message("Você não tem permissão para fechar este ticket.")

class Ticket(commands.Cog, name="ticket"):
    def __init__(self, bot):
        self.bot = bot

    @commands.hybrid_command(
        name="painel",
        description="Comando de ticket."
    )
    @checks.is_owner()
    async def ticket(self, ctx: commands.Context):
        print(f"Painel command triggered by {ctx.author.name}")
        embed = discord.Embed(
            colour=0xabc4eb,
            title="Bem-vindo ao Cantinho de Ajuda do Neko Café!",
            description="Miau! Está com alguma dúvida ou precisa de um help da nossa staff fofinha? Sem problemas! É só clicar no botão abaixo e abrir um ticket, tá bom?\n\nRegrinhas rápidas:\n• Explique direitinho o que você precisa, com jeitinho!\n• Aguarde com paciência, vamos te responder com muito carinho!\n• Não abra vários tickets iguais, tá bom?\n\nEstamos aqui pra cuidar de você com muito amor e cafuné!"
        )
        embed.set_image(url="https://i.imgur.com/vVvNwFc.png")
        embed.set_footer(text="Equipe Neko Café")
        await ctx.send(embed=embed, view=TicketPanelView())

async def setup(bot):
    print("Loading ticket cog...")
    bot.add_view(TicketPanelView())
    print("TicketPanelView added.")
    bot.add_view(CreateTicket())
    print("CreateTicket added.")
    bot.add_view(Close_Ticket())
    print("Close_Ticket added.")
    await bot.add_cog(Ticket(bot))
    print("Ticket cog loaded.")