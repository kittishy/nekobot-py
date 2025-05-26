import discord
from discord.ext import commands

from helpers import checks

class Rules(commands.Cog, name="rules"):
    def __init__(self, bot):
        self.bot = bot

    @commands.hybrid_command(
        name="regras",
        description="Exibe as regras do servidor."
    )
    @checks.is_owner()
    async def regras(self, ctx: commands.Context):  # Renomeado de 'ticket' para 'regras'
        print(f"Regras command triggered by {ctx.author.name}")
        embed = discord.Embed(
            title="Regras do Neko Café",
            description="""Seja bem-vindos ao Neko Café! Aqui prezamos por um ambiente acolhedor, divertido e seguro para todos. Ao participar do servidor, você concorda em seguir as regras abaixo:

1. Respeito em primeiro lugar
Trate todos com educação e empatia. Bullying, preconceito, assédio ou discurso de ódio não serão tolerados.

2. Proibido conteúdo impróprio ou NSFW
Este é um servidor para todas as idades. Qualquer conteúdo sexual, chocante ou perturbador será removido e pode levar a punição.

3. Sem spam ou flood
Evite enviar muitas mensagens repetidas, links aleatórios ou divulgação não autorizada. Isso atrapalha a convivência no café!

4. Nada de brigas ou discussões pesadas
Debates são bem-vindos quando feitos com respeito, mas tretas, provocação e toxicidade serão advertidas ou punidas.

5. Use os canais corretamente
Cada canal tem sua função. Evite postar conteúdos fora do tema proposto.

6. Proibido divulgar outros servidores ou redes sem permissão
Se quiser divulgar algo, peça permissão para a staff antes. Divulgação sem autorização leva a ban.

7. Nicknames e avatares adequados
Evite nomes ou imagens ofensivas, sensuais ou que possam confundir os membros e a staff.

8. Siga as Diretrizes da Comunidade do Discord
Isso inclui:

Não se passar por outra pessoa

Não promover atividades ilegais

Não utilizar bots ou scripts para spam

Não compartilhar informações pessoais suas ou de terceiros
[Leia as diretrizes completas aqui](https://discord.com/guidelines)


9. Respeite a staff
A equipe está aqui para ajudar. Qualquer tentativa de burlar regras ou desrespeitar decisões pode resultar em banimento.

10. Divirta-se e aproveite o café!
Nosso cantinho é feito com carinho para quem ama animes, jogos e cultura otaku. Faça amigos, participe dos eventos e aproveite ao máximo!""",
            color=16240606  # Cor da embed original convertida
        )
        embed.set_image(url="https://cdn.discordapp.com/attachments/1334474182049796131/1374372618710417509/regras_by_aishy.png?ex=6831c43e&is=683072be&hm=4ee2c472c7fdd013e978b451b3ffd87baa8b8c3654fcee712beb831105d605a6&")
        embed.set_footer(text="Equipe Neko Café")
        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Rules(bot))