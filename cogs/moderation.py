""""
Copyright © Krypton 2019-2023 - https://github.com/kkrypt0nn (https://krypton.ninja)
Description:
🐍 A simple template to start to code your own and personalized discord bot in Python programming language.

Version: 5.5.0
"""

import discord
from discord import app_commands
from discord.ext import commands
from discord.ext.commands import Context

from helpers import checks, db_manager


class Moderation(commands.Cog, name="moderation"):
    def __init__(self, bot):
        self.bot = bot

    @commands.hybrid_command(
        name="expulsar",
        description="Expulsa um usuário do servidor.",
    )
    @commands.has_permissions(kick_members=True)
    @commands.bot_has_permissions(kick_members=True)
    @checks.not_blacklisted()
    @app_commands.describe(
        user="O usuário que deve ser expulso.",
        reason="O motivo pelo qual o usuário deve ser expulso.",
    )
    async def kick(
        self, context: Context, user: discord.User, *, reason: str = "Não especificado"
    ) -> None:
        """
        Expulsa um usuário do servidor.

        :param context: O contexto do comando híbrido.
        :param user: O usuário que deve ser expulso do servidor.
        :param reason: O motivo da expulsão. Padrão é "Não especificado".
        """
        member = context.guild.get_member(user.id) or await context.guild.fetch_member(
            user.id
        )
        if member.guild_permissions.administrator:
            embed = discord.Embed(
                description="O usuário tem permissões de administrador.", color=0xE02B2B
            )
            await context.send(embed=embed)
        else:
            try:
                embed = discord.Embed(
                    description=f"**{member}** foi expulso por **{context.author}**!",
                    color=0x9C84EF,
                )
                embed.add_field(name="Motivo:", value=reason)
                await context.send(embed=embed)
                try:
                    await member.send(
                        f"Você foi expulso por **{context.author}** do servidor **{context.guild.name}**!\nMotivo: {reason}"
                    )
                except:
                    # Não foi possível enviar uma mensagem nas mensagens privadas do usuário
                    pass
                await member.kick(reason=reason)
            except:
                embed = discord.Embed(
                    description="Ocorreu um erro ao tentar expulsar o usuário. Certifique-se de que meu cargo está acima do cargo do usuário que você deseja expulsar.",
                    color=0xE02B2B,
                )
                await context.send(embed=embed)

    @commands.hybrid_command(
        name="apelido",
        description="Altera o apelido de um usuário no servidor.",
    )
    @commands.has_permissions(manage_nicknames=True)
    @commands.bot_has_permissions(manage_nicknames=True)
    @checks.not_blacklisted()
    @app_commands.describe(
        user="O usuário que deve ter um novo apelido.",
        nickname="O novo apelido que deve ser definido.",
    )
    async def nick(
        self, context: Context, user: discord.User, *, nickname: str = None
    ) -> None:
        """
        Altera o apelido de um usuário no servidor.

        :param context: O contexto do comando híbrido.
        :param user: O usuário que deve ter seu apelido alterado.
        :param nickname: O novo apelido do usuário. O padrão é None, o que irá redefinir o apelido.
        """
        member = context.guild.get_member(user.id) or await context.guild.fetch_member(
            user.id
        )
        try:
            await member.edit(nick=nickname)
            embed = discord.Embed(
                description=f"O novo apelido de **{member}** é **{nickname}**!",
                color=0x9C84EF,
            )
            await context.send(embed=embed)
        except:
            embed = discord.Embed(
                description="Ocorreu um erro ao tentar alterar o apelido do usuário. Certifique-se de que meu cargo está acima do cargo do usuário cujo apelido você deseja alterar.",
                color=0xE02B2B,
            )
            await context.send(embed=embed)

    @commands.hybrid_command(
        name="banir",
        description="Bane um usuário do servidor.",
    )
    @commands.has_permissions(ban_members=True)
    @commands.bot_has_permissions(ban_members=True)
    @checks.not_blacklisted()
    @app_commands.describe(
        user="O usuário que deve ser banido.",
        reason="O motivo pelo qual o usuário deve ser banido.",
    )
    async def ban(
        self, context: Context, user: discord.User, *, reason: str = "Não especificado"
    ) -> None:
        """
        Bane um usuário do servidor.

        :param context: O contexto do comando híbrido.
        :param user: O usuário que deve ser banido do servidor.
        :param reason: O motivo do banimento. Padrão é "Não especificado".
        """
        member = context.guild.get_member(user.id) or await context.guild.fetch_member(
            user.id
        )
        try:
            if member.guild_permissions.administrator:
                embed = discord.Embed(
                    description="O usuário tem permissões de administrador.", color=0xE02B2B
                )
                await context.send(embed=embed)
            else:
                embed = discord.Embed(
                    description=f"**{member}** foi banido por **{context.author}**!",
                    color=0x9C84EF,
                )
                embed.add_field(name="Motivo:", value=reason)
                await context.send(embed=embed)
                try:
                    await member.send(
                        f"Você foi banido por **{context.author}** do servidor **{context.guild.name}**!\nMotivo: {reason}"
                    )
                except:
                    # Não foi possível enviar uma mensagem nas mensagens privadas do usuário
                    pass
                await member.ban(reason=reason)
        except:
            embed = discord.Embed(
                title="Erro!",
                description="Ocorreu um erro ao tentar banir o usuário. Certifique-se de que meu cargo está acima do cargo do usuário que você deseja banir.",
                color=0xE02B2B,
            )
            await context.send(embed=embed)

    @commands.hybrid_group(
        name="advertencia",
        description="Gerencia advertências de um usuário no servidor.",
    )
    @commands.has_permissions(manage_messages=True)
    @checks.not_blacklisted()
    async def warning(self, context: Context) -> None:
        """
        Gerencia advertências de um usuário no servidor.

        :param context: O contexto do comando híbrido.
        """
        if context.invoked_subcommand is None:
            embed = discord.Embed(
                description="Por favor, especifique um subcomando.\n\n**Subcomandos:**\n`adicionar` - Adiciona uma advertência a um usuário.\n`remover` - Remove uma advertência de um usuário.\n`listar` - Lista todas as advertências de um usuário.",
                color=0xE02B2B,
            )
            await context.send(embed=embed)

    @warning.command(
        name="adicionar",
        description="Adiciona uma advertência a um usuário no servidor.",
    )
    @checks.not_blacklisted()
    @commands.has_permissions(manage_messages=True)
    @app_commands.describe(
        user="O usuário que deve ser advertido.",
        reason="O motivo pelo qual o usuário deve ser advertido.",
    )
    async def warning_add(
        self, context: Context, user: discord.User, *, reason: str = "Não especificado"
    ) -> None:
        """
        Adverte um usuário em suas mensagens privadas.

        :param context: O contexto do comando híbrido.
        :param user: O usuário que deve ser advertido.
        :param reason: O motivo da advertência. Padrão é "Não especificado".
        """
        member = context.guild.get_member(user.id) or await context.guild.fetch_member(
            user.id
        )
        total = await db_manager.add_warn(
            user.id, context.guild.id, context.author.id, reason
        )
        embed = discord.Embed(
            description=f"**{member}** foi advertido por **{context.author}**!\nTotal de advertências para este usuário: {total}",
            color=0x9C84EF,
        )
        embed.add_field(name="Motivo:", value=reason)
        await context.send(embed=embed)
        try:
            await member.send(
                f"Você foi advertido por **{context.author}** no servidor **{context.guild.name}**!\nMotivo: {reason}"
            )
        except:
            # Não foi possível enviar uma mensagem nas mensagens privadas do usuário
            await context.send(
                f"{member.mention}, você foi advertido por **{context.author}**!\nMotivo: {reason}"
            )

    @warning.command(
        name="remover",
        description="Remove uma advertência de um usuário no servidor.",
    )
    @checks.not_blacklisted()
    @commands.has_permissions(manage_messages=True)
    @app_commands.describe(
        user="O usuário que deve ter sua advertência removida.",
        warn_id="O ID da advertência que deve ser removida.",
    )
    async def warning_remove(
        self, context: Context, user: discord.User, warn_id: int
    ) -> None:
        """
        Remove uma advertência de um usuário.

        :param context: O contexto do comando híbrido.
        :param user: O usuário que deve ter sua advertência removida.
        :param warn_id: O ID da advertência que deve ser removida.
        """
        member = context.guild.get_member(user.id) or await context.guild.fetch_member(
            user.id
        )
        total = await db_manager.remove_warn(warn_id, user.id, context.guild.id)
        embed = discord.Embed(
            description=f"Removi a advertência **#{warn_id}** de **{member}**!\nTotal de advertências para este usuário: {total}",
            color=0x9C84EF,
        )
        await context.send(embed=embed)

    @warning.command(
        name="listar",
        description="Mostra as advertências de um usuário no servidor.",
    )
    @commands.has_guild_permissions(manage_messages=True)
    @checks.not_blacklisted()
    @app_commands.describe(user="O usuário do qual você deseja ver as advertências.")
    async def warning_list(self, context: Context, user: discord.User):
        """
        Mostra as advertências de um usuário no servidor.

        :param context: O contexto do comando híbrido.
        :param user: O usuário do qual você deseja ver as advertências.
        """
        warnings_list = await db_manager.get_warnings(user.id, context.guild.id)
        embed = discord.Embed(title=f"Advertências de {user}", color=0x9C84EF)
        description = ""
        if len(warnings_list) == 0:
            description = "Este usuário não tem advertências."
        else:
            for warning in warnings_list:
                description += f"• Advertido por <@{warning[2]}>: **{warning[3]}** (<t:{warning[4]}>) - ID da Advertência #{warning[5]}\n"
        embed.description = description
        await context.send(embed=embed)

    @commands.hybrid_command(
        name="limpar",
        description="Deleta um número de mensagens.",
    )
    @commands.has_guild_permissions(manage_messages=True)
    @commands.bot_has_permissions(manage_messages=True)
    @checks.not_blacklisted()
    @app_commands.describe(amount="A quantidade de mensagens que devem ser deletadas.")
    async def purge(self, context: Context, amount: int) -> None:
        """
        Deleta um número de mensagens.

        :param context: O contexto do comando híbrido.
        :param amount: O número de mensagens que devem ser deletadas.
        """
        await context.send(
            "Deletando mensagens..."
        )  // Uma maneira um pouco improvisada de garantir que o bot responda à interação e não receba uma resposta "Interação Desconhecida"
        purged_messages = await context.channel.purge(limit=amount + 1)
        embed = discord.Embed(
            description=f"**{context.author}** limpou **{len(purged_messages)-1}** mensagens!",
            color=0x9C84EF,
        )
        await context.channel.send(embed=embed)

    @commands.hybrid_command(
        name="banir_id",
        description="Bane um usuário sem que ele precise estar no servidor.",
    )
    @commands.has_permissions(ban_members=True)
    @commands.bot_has_permissions(ban_members=True)
    @checks.not_blacklisted()
    @app_commands.describe(
        user_id="O ID do usuário que deve ser banido.",
        reason="O motivo pelo qual o usuário deve ser banido.",
    )
    async def hackban(
        self, context: Context, user_id: str, *, reason: str = "Não especificado"
    ) -> None:
        """
        Bane um usuário sem que ele precise estar no servidor.

        :param context: O contexto do comando híbrido.
        :param user_id: O ID do usuário que deve ser banido.
        :param reason: O motivo do banimento. Padrão é "Não especificado".
        """
        try:
            await self.bot.http.ban(user_id, context.guild.id, reason=reason)
            user = self.bot.get_user(int(user_id)) or await self.bot.fetch_user(
                int(user_id)
            )
            embed = discord.Embed(
                description=f"**{user}** (ID: {user_id}) foi banido por **{context.author}**!",
                color=0x9C84EF,
            )
            embed.add_field(name="Motivo:", value=reason)
            await context.send(embed=embed)
        except Exception as e:
            embed = discord.Embed(
                description="Ocorreu um erro ao tentar banir o usuário. Certifique-se de que o ID é um ID existente que pertence a um usuário.",
                color=0xE02B2B,
            )
            await context.send(embed=embed)


async def setup(bot):
    await bot.add_cog(Moderation(bot))
