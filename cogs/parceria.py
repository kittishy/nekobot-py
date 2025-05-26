import discord
from discord.ext import commands
from helpers import checks

class Parceria(commands.Cog, name="parceria"):
    def __init__(self, bot):
        self.bot = bot

    @commands.hybrid_command(
        name="parceria",
        description="Mostra os requisitos e informações para fazer parceria com o Neko Café"
    )
    @checks.not_blacklisted()
    async def parceria(self, context: commands.Context):
        embed = discord.Embed(
            color=16039839,
            title="Seja parceiro!",
            description="Seja bem-vindo(a) à área de parcerias do Neko Café! Nosso servidor está sempre em busca de conexões com outras comunidades que compartilhem interesses em animes, mangás, jogos, cultura otaku e ambientes acolhedores. Prezamos por parcerias justas, equilibradas e que tragam benefícios mútuos para ambas as partes.\n\nAntes de fazer seu pedido de parceria, leia atentamente os requisitos e regras abaixo. Eles foram criados para garantir que todas as parcerias sejam bem estruturadas, organizadas e duradouras.\n\n\n---\n\nRequisitos obrigatórios para solicitar parceria:\n\n1. Mínimo de 100 membros reais no servidor parceiro.\n\nNão aceitamos servidores com grande parte dos membros inativos ou bots que inflacionem o número de usuários.\n\n\n\n2. O servidor parceiro deve ser ativo, ter um bom nível de engajamento e ser visualmente organizado, com canais claros e um sistema de moderação funcional.\n\n\n3. É obrigatória a presença de um representante da parceria no Neko Café.\n\nEsse representante será o responsável por manter contato com nossa equipe em caso de atualizações, eventos conjuntos ou revisões.\n\nSe o representante sair do nosso servidor sem dar aviso prévio ou sem enviar um novo responsável, a parceria será automaticamente cancelada.\n\n\n\n4. O servidor parceiro deve garantir visibilidade equivalente à que oferecemos no Neko Café.\n\nIsso inclui a criação de um canal ou mensagem de divulgação para parceiros, fixação da nossa divulgação (caso aplicável) e/ou participação em eventos colaborativos quando possível.\n\n\n\n5. Esperamos respeito mútuo e alinhamento de valores entre as comunidades.\n\nAtitudes tóxicas, preconceituosas ou qualquer tipo de discriminação por parte de membros ou da staff do servidor parceiro resultarão no encerramento imediato da parceria.\n\n\n\n\n\n---\n\nInformações adicionais:\n\nAs parcerias são revisadas periodicamente. Caso notemos inatividade extrema, quebra de regras ou perda de contato com o representante, a parceria poderá ser desfeita.\n\nParcerias temporárias para eventos também são aceitas, desde que cumpram os requisitos mínimos.\n\nAo solicitar parceria, você automaticamente concorda com todas as diretrizes descritas acima.\n\n\n\n---\n\nCaso seu servidor se encaixe nesses critérios e você deseje se juntar à rede de parceiros do Neko Café, abra um ticket em <#1361808252706361547>"
        )
        embed.set_image(url="https://cdn.discordapp.com/attachments/1334474182049796131/1373811365692702740/req_de_parcerias_by_aishy.png?ex=6835a849&is=683456c9&hm=ee4a1dff3ef89b0336b27040f747d60b3c613cbcaa8463e51cff92ca32203a5d&")
        await context.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Parceria(bot))