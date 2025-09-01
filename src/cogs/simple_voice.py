import discord
from discord.ext import commands
import asyncio
import logging
import os
import tempfile
import edge_tts
from typing import Optional

from cogs.defaults import default_params

class SimpleVoiceCog(commands.Cog):
    '''
    Simple voice functionality using Edge TTS (no RVC required)
    '''

    def __init__(self, bot: discord.Bot) -> None:
        self.bot = bot
        self.current_voice = "en-US-AriaNeural"
        self.available_voices = [
            "en-US-AriaNeural",      # Female, clear
            "en-US-DavisNeural",     # Male, clear
            "en-US-JennyNeural",     # Female, friendly
            "en-US-GuyNeural",       # Male, friendly
            "en-GB-SoniaNeural",     # British female
            "en-GB-RyanNeural",      # British male
            "en-AU-NatashaNeural",   # Australian female
            "en-AU-WilliamNeural",   # Australian male
        ]
        
    @discord.slash_command(name="voices", description="List available voices", **default_params)
    async def list_voices(self, ctx):
        """List all available voices"""
        voice_list = "\n".join([f"• {voice}" for voice in self.available_voices])
        current = f"**Current voice:** {self.current_voice}"
        await ctx.respond(f"🎭 **Available Voices:**\n{voice_list}\n\n{current}")

    @discord.slash_command(name="set_voice", description="Set the voice to use", **default_params)
    @discord.option("voice", description="Voice name")
    async def set_voice(self, ctx, voice: str):
        """Set the voice for TTS"""
        if voice in self.available_voices:
            self.current_voice = voice
            await ctx.respond(f"✅ Voice set to: **{voice}**")
        else:
            await ctx.respond(f"❌ Voice '{voice}' not found. Use `/voices` to see available options.")

    async def text_to_speech(self, text: str, output_path: str) -> bool:
        """Convert text to speech using Edge TTS"""
        try:
            # Use Edge TTS directly
            communicate = edge_tts.Communicate(text, self.current_voice)
            await communicate.save(output_path)
            
            if os.path.exists(output_path):
                logging.info(f"TTS successful: {output_path}")
                return True
            else:
                logging.error("TTS failed: output file not created")
                return False
                
        except Exception as e:
            logging.error(f"TTS error: {e}")
            return False

    async def speak_text(self, text: str, voice_channel) -> bool:
        """Convert text to speech and play it in voice channel"""
        try:
            if not voice_channel or not voice_channel.is_connected():
                logging.error("Not connected to voice channel")
                return False

            # Create temporary file for TTS
            with tempfile.NamedTemporaryFile(suffix=".mp3", delete=False) as temp_file:
                tts_file = temp_file.name

            try:
                # Step 1: Convert text to speech
                logging.info(f"Converting text to speech: {text[:50]}...")
                if not await self.text_to_speech(text, tts_file):
                    logging.error("TTS conversion failed")
                    return False

                # Step 2: Play the audio
                logging.info("Playing TTS audio")
                source = discord.FFmpegPCMAudio(tts_file)
                voice_channel.play(source)

                # Wait for audio to finish
                while voice_channel.is_playing():
                    await asyncio.sleep(0.1)

                return True

            finally:
                # Cleanup temporary file
                if os.path.exists(tts_file):
                    os.unlink(tts_file)

        except Exception as e:
            logging.error(f"Error in speak_text: {e}")
            return False

    @discord.slash_command(name="test_voice", description="Test the current voice", **default_params)
    async def test_voice(self, ctx):
        """Test the current voice with a sample text"""
        try:
            if not ctx.author.voice:
                await ctx.respond("❌ You need to be in a voice channel to test the voice!")
                return

            voice_channel = ctx.author.voice.channel
            
            # Check if bot is in the same voice channel
            if not hasattr(self.bot, 'voice_clients') or not self.bot.voice_clients:
                await ctx.respond("❌ I need to join your voice channel first! Use `/join`")
                return

            await ctx.respond("🎤 Testing voice...")
            
            test_text = f"Hello! This is a test of the {self.current_voice} voice."
            success = await self.speak_text(test_text, self.bot.voice_clients[0])
            
            if success:
                await ctx.followup.send("✅ Voice test completed successfully!")
            else:
                await ctx.followup.send("❌ Voice test failed. Check the logs for details.")

        except Exception as e:
            logging.error(f"Voice test error: {e}")
            await ctx.respond(f"❌ Voice test failed: {str(e)}")

    @discord.slash_command(name="speak", description="Make the bot speak text", **default_params)
    @discord.option("text", description="Text to speak")
    async def speak_command(self, ctx, text: str):
        """Make the bot speak the given text"""
        try:
            if not ctx.author.voice:
                await ctx.respond("❌ You need to be in a voice channel!")
                return

            voice_channel = ctx.author.voice.channel
            
            # Check if bot is in the same voice channel
            if not hasattr(self.bot, 'voice_clients') or not self.bot.voice_clients:
                await ctx.respond("❌ I need to join your voice channel first! Use `/join`")
                return

            await ctx.respond("🎤 Speaking...")
            
            success = await self.speak_text(text, self.bot.voice_clients[0])
            
            if success:
                await ctx.followup.send("✅ Finished speaking!")
            else:
                await ctx.followup.send("❌ Failed to speak. Check the logs for details.")

        except Exception as e:
            logging.error(f"Speak command error: {e}")
            await ctx.respond(f"❌ Error: {str(e)}")

def setup(bot: discord.Bot) -> None:
    bot.add_cog(SimpleVoiceCog(bot))
