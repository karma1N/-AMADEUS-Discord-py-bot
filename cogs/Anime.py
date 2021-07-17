from discord.ext import commands
import kitsu

client = kitsu.Client()


class AnimeSearch(commands.Cog):
    """
    Online search
    """
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='anime', aliases=['anm'])
    async def anime_search(self, ctx, query: str):
        entries = await client.search('anime', query, limit=1)
        if not entries:
            await ctx.send(f'No entries found for "{query}"')
            return

        for i, anime in enumerate(entries, 1):
            await ctx.send(f'\n{i}. {anime.title}:')
            await ctx.send(f'---> Sub-Type: {anime.subtype}')
            await ctx.send(f'---> Status: {anime.status}')
            await ctx.send(f'---> Synopsis:\n{anime.synopsis}')
            await ctx.send(f'---> Episodes: {anime.episode_count}')
            await ctx.send(f'---> Age Rating: {anime.age_rating_guide}')
            await ctx.send(f'---> Ranking:')
            await ctx.send(f'-> Popularity: {anime.popularity_rank}')
            await ctx.send(f'-> Rating: {anime.rating_rank}')

            if anime.started_at:
                await ctx.send('---> Started At:' + anime.started_at.strftime('%Y-%m-%d'))
            if anime.ended_at:
                await ctx.send('---> Ended At:' + anime.ended_at.strftime('%Y-%m-%d'))

            streaming_links = await client.fetch_anime_streaming_links(anime)
            if streaming_links:
                await ctx.send('---> Streaming Links:')
                for link in streaming_links:
                    await ctx.send(f'-> {link.title}: {link.url}')

            await ctx.send('---> Kitsu Page:' + anime.url)

    @commands.command(name='manga', aliases=['mng'])
    async def manga_search(self, ctx, query):
        entries = await client.search('manga', query, limit=3)
        if not entries:
            await ctx.send(f'No entries found for "{query}"')
            return

        for i, manga in enumerate(entries, 1):
            await ctx.send(f'\n{i}. {manga.title}:')
            await ctx.send(f'---> Sub-Type: {manga.subtype}')
            await ctx.send(f'---> Status: {manga.status}')
            await ctx.send(f'---> Volumes: {manga.volume_count}')
            await ctx.send(f'---> Chapters: {manga.chapter_count}')
            await ctx.send(f'---> Synopsis:\n {manga.synopsis}')
            await ctx.send(f'---> Age Rating: {manga.age_rating_guide}')
            await ctx.send(f'---> Ranking:')
            await ctx.send(f'-> Popularity: {manga.popularity_rank}')
            await ctx.send(f'-> Rating: {manga.rating_rank}')
            await ctx.send(f'---> Kitsu Page: {manga.url}')


def setup(bot):
    bot.add_cog(AnimeSearch(bot))
