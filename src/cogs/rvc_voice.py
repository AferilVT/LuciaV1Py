import discord
from discord.ext import commands
import asyncio
import logging
import os
import tempfile
import subprocess
import json
from typing import Optional
import requests

from cogs.defaults import default_params

class RVCVoiceCog(commands.Cog):
    '''
    RVC Voice Conversion functionality for custom AI voices
    '''

    def __init__(self, bot: discord.Bot) -> None:
        self.bot = bot
        self.rvc_path = os.getenv("RVC_PATH", "./rvc")  # Path to RVC installation
        self.current_voice_model = os.getenv("DEFAULT_VOICE_MODEL", "default")
        self.available_models = self._scan_voice_models()
        self.tts_engine = os.getenv("TTS_ENGINE", "edge")  # edge, coqui, or rvc_direct
        
    def _scan_voice_models(self) -> list:
        """Scan for available RVC voice models"""
        models = []
        models_dir = os.path.join(self.rvc_path, "models")
        if os.path.exists(models_dir):
            for item in os.listdir(models_dir):
                if item.endswith(".pth"):
                    models.append(item.replace(".pth", ""))
        return models

    @discord.slash_command(name="voice_models", description="List available voice models", **default_params)
    async def list_voice_models(self, ctx):
        """List all available voice models"""
        if not self.available_models:
            await ctx.respond("❌ No voice models found. Please check your RVC installation.")
            return
        
        model_list = "\n".join([f"• {model}" for model in self.available_models])
        await ctx.respond(f"🎭 **Available Voice Models:**\n{model_list}")

    @discord.slash_command(name="set_voice", description="Set the voice model to use", **default_params)
    @discord.option("model", description="Voice model name")
    async def set_voice_model(self, ctx, model: str):
        """Set the voice model for TTS"""
        if model in self.available_models:
            self.current_voice_model = model
            await ctx.respond(f"✅ Voice model set to: **{model}**")
        else:
            await ctx.respond(f"❌ Voice model '{model}' not found. Use `/voice_models` to see available options.")

    async def text_to_speech(self, text: str, output_path: str) -> bool:
        """Convert text to speech using the selected TTS engine"""
        try:
            if self.tts_engine == "edge":
                return await self._edge_tts(text, output_path)
            elif self.tts_engine == "coqui":
                return await self._coqui_tts(text, output_path)
            elif self.tts_engine == "rvc_direct":
                return await self._rvc_direct_tts(text, output_path)
            else:
                logging.error(f"Unknown TTS engine: {self.tts_engine}")
                return False
        except Exception as e:
            logging.error(f"TTS conversion failed: {e}")
            return False

    async def _edge_tts(self, text: str, output_path: str) -> bool:
        """Use Edge TTS for initial speech generation"""
        try:
            # Edge TTS command (you'll need to install edge-tts)
            cmd = [
                "edge-tts",
                "--voice", "en-US-AriaNeural",
                "--text", text,
                "--write-media", output_path
            ]
            
            process = await asyncio.create_subprocess_exec(
                *cmd,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            
            stdout, stderr = await process.communicate()
            
            if process.returncode == 0 and os.path.exists(output_path):
                return True
            else:
                logging.error(f"Edge TTS failed: {stderr.decode()}")
                return False
                
        except Exception as e:
            logging.error(f"Edge TTS error: {e}")
            return False

    async def _coqui_tts(self, text: str, output_path: str) -> bool:
        """Use Coqui TTS for initial speech generation"""
        try:
            # This would require Coqui TTS installation
            # For now, fallback to edge-tts
            return await self._edge_tts(text, output_path)
        except Exception as e:
            logging.error(f"Coqui TTS error: {e}")
            return False

    async def _rvc_direct_tts(self, text: str, output_path: str) -> bool:
        """Direct RVC TTS (if you have a TTS model)"""
        try:
            # This would be for direct RVC TTS models
            # For now, fallback to edge-tts
            return await self._edge_tts(text, output_path)
        except Exception as e:
            logging.error(f"RVC direct TTS error: {e}")
            return False

    async def convert_voice(self, input_audio: str, output_audio: str, voice_model: str) -> bool:
        """Convert audio to target voice using RVC"""
        try:
            if not os.path.exists(self.rvc_path):
                logging.error(f"RVC path not found: {self.rvc_path}")
                return False

            # RVC inference command
            cmd = [
                "python", "infer_cli.py",
                "--model_path", f"models/{voice_model}.pth",
                "--input_path", input_audio,
                "--output_path", output_audio,
                "--f0_up_key", "0",  # Pitch adjustment
                "--index_path", f"models/{voice_model}.index",  # If you have index files
                "--protect", "0.33"  # Voice protection
            ]

            # Change to RVC directory
            original_dir = os.getcwd()
            os.chdir(self.rvc_path)

            process = await asyncio.create_subprocess_exec(
                *cmd,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )

            stdout, stderr = await process.communicate()
            os.chdir(original_dir)

            if process.returncode == 0 and os.path.exists(output_audio):
                logging.info(f"Voice conversion successful: {output_audio}")
                return True
            else:
                logging.error(f"RVC conversion failed: {stderr.decode()}")
                return False

        except Exception as e:
            logging.error(f"Voice conversion error: {e}")
            return False

    async def speak_text(self, text: str, voice_channel) -> bool:
        """Convert text to speech and play it in voice channel"""
        try:
            if not voice_channel or not voice_channel.is_connected():
                logging.error("Not connected to voice channel")
                return False

            # Create temporary files
            with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as temp_tts, \
                 tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as temp_rvc:
                
                tts_file = temp_tts.name
                rvc_file = temp_rvc.name

            try:
                # Step 1: Convert text to speech
                logging.info(f"Converting text to speech: {text[:50]}...")
                if not await self.text_to_speech(text, tts_file):
                    logging.error("TTS conversion failed")
                    return False

                # Step 2: Convert voice using RVC
                logging.info(f"Converting voice using model: {self.current_voice_model}")
                if not await self.convert_voice(tts_file, rvc_file, self.current_voice_model):
                    logging.error("Voice conversion failed")
                    return False

                # Step 3: Play the converted audio
                logging.info("Playing converted audio")
                source = discord.FFmpegPCMAudio(rvc_file)
                voice_channel.play(source)

                # Wait for audio to finish
                while voice_channel.is_playing():
                    await asyncio.sleep(0.1)

                return True

            finally:
                # Cleanup temporary files
                for file_path in [tts_file, rvc_file]:
                    if os.path.exists(file_path):
                        os.unlink(file_path)

        except Exception as e:
            logging.error(f"Error in speak_text: {e}")
            return False

    @discord.slash_command(name="test_voice", description="Test the current voice model", **default_params)
    async def test_voice(self, ctx):
        """Test the current voice model with a sample text"""
        try:
            if not ctx.author.voice:
                await ctx.respond("❌ You need to be in a voice channel to test the voice!")
                return

            voice_channel = ctx.author.voice.channel
            
            # Check if bot is in the same voice channel
            if not hasattr(self.bot, 'voice_clients') or not self.bot.voice_clients:
                await ctx.respond("❌ I need to join your voice channel first! Use `/join`")
                return

            await ctx.respond("🎤 Testing voice conversion...")
            
            test_text = "Hello! This is a test of the voice conversion system."
            success = await self.speak_text(test_text, self.bot.voice_clients[0])
            
            if success:
                await ctx.followup.send("✅ Voice test completed successfully!")
            else:
                await ctx.followup.send("❌ Voice test failed. Check the logs for details.")

        except Exception as e:
            logging.error(f"Voice test error: {e}")
            await ctx.respond(f"❌ Voice test failed: {str(e)}")

def setup(bot: discord.Bot) -> None:
    bot.add_cog(RVCVoiceCog(bot))
