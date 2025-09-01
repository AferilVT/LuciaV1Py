import discord
import logging
from discord.ext import commands
from utils.service.Ollama_worker import OllamaWorker
from cogs.cogs import setup_cogs
from typing import Any

class Lucia(discord.Bot):
    def __init__(self) -> None:
        intents = discord.Intents.default()
        intents.message_content = True
        intents.voice_states = True  # Required for voice functionality
        intents.guilds = True  # Required for voice channels
        super().__init__(intents=intents)
        self.llm_worker = OllamaWorker()
        setup_cogs(self)

    async def on_ready(self) -> None:
        logging.info("on_ready event triggered")
        try:
            logging.info(f"Lucia is awake, User: {self.user}")
            await self.change_presence(
                activity=discord.Activity(
                    type=discord.ActivityType.listening,
                    name="Aferil's Playlists"
                )
            )
            # DM you on startup
            user_id = 781846995954171916  # Your Discord user ID
            user = await self.fetch_user(user_id)
            try:
                await user.send("Good morning, Aferil! I'm awake now")
                logging.info("DM sent to you on startup.")
            except discord.Forbidden:
                logging.warning("Could not DM you (forbidden). Check your privacy settings.")
            except Exception as e:
                logging.error(f"Failed to DM you: {e}", exc_info=True)
        except Exception as e:
            logging.exception("Exception in on_ready")
        logging.info("on_ready event completed")

    async def on_message(self, message: discord.Message) -> None:
        if message.author.bot or not message.content:
            return
        is_mentioned = self.user in message.mentions
        is_reply = message.reference and message.reference.resolved \
                  and message.reference.resolved.author.id == self.user.id
        if not (is_mentioned or is_reply):
            return
        content = message.content.replace(f'<@{self.user.id}>', '').strip()
        if not content:
            await message.reply("Please provide a message for me to respond to!")
            return
        logging.debug(f"Processing message from {message.author}: {content}")
        try:
            async with message.channel.typing():
                response = self.llm_worker.generate_response(content)
                if len(response) > 2000:
                    chunks = [response[i:i + 1990] for i in range(0, len(response), 1990)]
                    for i, chunk in enumerate(chunks):
                        if i == 0:
                            await message.reply(f"{chunk}\n[1/{len(chunks)}]")
                        else:
                            await message.channel.send(f"{chunk}\n[{i+1}/{len(chunks)}]")
                else:
                    await message.reply(response)
        except Exception as e:
            logging.exception("Error in message handling")
            await message.reply(
                "I apologize, but something went wrong while processing your message. "
                "Please try again later."
            )

    async def on_error(self, event_method: str, *args: Any, **kwargs: Any) -> None:
        logging.exception(f"Error in event {event_method}")

    async def on_command_error(self, ctx: commands.Context, error: Exception) -> None:
        if isinstance(error, commands.CommandOnCooldown):
            await ctx.send(
                f"This command is on cooldown. Try again in {error.retry_after:.1f} seconds.",
                delete_after=5
            )
        else:
            logging.error(f"Error in command {getattr(ctx, 'command', None)}: {error}", exc_info=True)
        

