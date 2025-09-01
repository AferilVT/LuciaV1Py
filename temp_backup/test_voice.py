#!/usr/bin/env python3
"""
Test script to diagnose voice connection issues
"""

import discord
import asyncio
import logging

# Set up logging
logging.basicConfig(level=logging.DEBUG)

class VoiceTestBot(discord.Bot):
    def __init__(self):
        intents = discord.Intents.default()
        intents.message_content = True
        super().__init__(intents=intents)

    async def on_ready(self):
        print(f"Bot is ready: {self.user}")
        print("Voice connection test bot loaded successfully!")

    @discord.slash_command(name="test_voice", description="Test voice connection")
    async def test_voice(self, ctx, channel: discord.VoiceChannel):
        """Test basic voice connection"""
        try:
            print(f"Attempting to connect to {channel.name}")
            await ctx.respond("Testing voice connection...")
            
            # Try to connect
            voice_client = await channel.connect()
            print(f"Successfully connected to {channel.name}")
            
            await ctx.followup.send(f"✅ Successfully connected to {channel.name}!")
            
            # Disconnect after a short delay
            await asyncio.sleep(2)
            await voice_client.disconnect()
            await ctx.followup.send("✅ Voice connection test completed successfully!")
            
        except discord.ClientException as e:
            print(f"ClientException: {e}")
            await ctx.followup.send(f"❌ ClientException: {e}")
        except discord.ConnectionClosed as e:
            print(f"ConnectionClosed: {e}")
            await ctx.followup.send(f"❌ ConnectionClosed: {e}")
        except Exception as e:
            print(f"Unexpected error: {e}")
            await ctx.followup.send(f"❌ Unexpected error: {e}")

async def main():
    # Load token from .env file
    import os
    from dotenv import load_dotenv
    
    load_dotenv()
    token = os.getenv('TOKEN')
    
    if not token:
        print("❌ No token found in .env file!")
        return
    
    bot = VoiceTestBot()
    await bot.start(token)

if __name__ == "__main__":
    asyncio.run(main()) 