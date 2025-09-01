import discord
from discord.ext import commands
import asyncio
import logging
import os
import tempfile
import subprocess
import json
import requests
from typing import Optional, Dict, List
import edge_tts

from cogs.defaults import default_params

class RVCVoiceEnhancedCog(commands.Cog):
    '''
    Enhanced RVC Voice Conversion with Edge TTS fallback
    '''

    def __init__(self, bot: discord.Bot) -> None:
        self.bot = bot
        self.rvc_path = os.getenv("RVC_PATH", "./rvc")
        self.current_voice_model = os.getenv("DEFAULT_RVC_MODEL", "default")
        self.available_models = self._scan_voice_models()
        self.use_rvc = os.getenv("USE_RVC", "false").lower() == "true"
        self.edge_voice = "en-US-AriaNeural"  # Fallback voice
        
        # RVC API settings (if using RVC WebUI)
        self.rvc_api_url = os.getenv("RVC_API_URL", "http://localhost:7860")
        self.rvc_api_enabled = os.getenv("RVC_API_ENABLED", "false").lower() == "true"
        
        logging.info(f"RVC Voice Enhanced initialized. RVC: {self.use_rvc}, API: {self.rvc_api_enabled}")
        
    def _scan_voice_models(self) -> List[Dict]:
        """Scan for available RVC voice models"""
        models = []
        
        # Check if RVC directory exists
        if not os.path.exists(self.rvc_path):
            logging.warning(f"RVC path not found: {self.rvc_path}")
            return models
            
        try:
            # Look for model files in RVC directory
            for root, dirs, files in os.walk(self.rvc_path):
                for file in files:
                    if file.endswith('.pth') or file.endswith('.index'):
                        model_name = os.path.splitext(file)[0]
                        model_path = os.path.join(root, file)
                        models.append({
                            'name': model_name,
                            'path': model_path,
                            'type': 'pth' if file.endswith('.pth') else 'index'
                        })
                        
            logging.info(f"Found {len(models)} RVC models")
            
        except Exception as e:
            logging.error(f"Error scanning RVC models: {e}")
            
        return models

    @discord.slash_command(name="rvc_models", description="List available RVC voice models", **default_params)
    async def list_rvc_models(self, ctx):
        """List all available RVC voice models"""
        try:
            if not self.available_models:
                await ctx.respond("❌ No RVC models found. Check your RVC installation path.")
                return
                
            model_list = "🎭 **Available RVC Voice Models:**\n\n"
            for i, model in enumerate(self.available_models, 1):
                model_list += f"{i}. **{model['name']}** ({model['type']})\n"
                
            model_list += f"\n**Current Model:** {self.current_voice_model}\n"
            model_list += f"**RVC Enabled:** {'✅ Yes' if self.use_rvc else '❌ No'}\n"
            model_list += f"**RVC API:** {'✅ Yes' if self.rvc_api_enabled else '❌ No'}"
            
            await ctx.respond(model_list)
            
        except Exception as e:
            logging.error(f"Error listing RVC models: {e}")
            await ctx.respond(f"❌ Error listing models: {str(e)}")

    @discord.slash_command(name="set_rvc_model", description="Set the RVC voice model to use", **default_params)
    async def set_rvc_model(self, ctx, model_name: str):
        """Set the RVC voice model to use"""
        try:
            # Check if model exists
            model_found = None
            for model in self.available_models:
                if model['name'].lower() == model_name.lower():
                    model_found = model
                    break
                    
            if not model_found:
                await ctx.respond(f"❌ Model '{model_name}' not found. Use `/rvc_models` to see available models.")
                return
                
            self.current_voice_model = model_found['name']
            await ctx.respond(f"✅ **RVC Model Set!**\n\nNow using: **{self.current_voice_model}**\n\nUse `/test_rvc_voice` to test it!")
            
        except Exception as e:
            logging.error(f"Error setting RVC model: {e}")
            await ctx.respond(f"❌ Error setting model: {str(e)}")

    @discord.slash_command(name="toggle_rvc", description="Enable/disable RVC voice conversion", **default_params)
    async def toggle_rvc(self, ctx):
        """Toggle RVC voice conversion on/off"""
        try:
            self.use_rvc = not self.use_rvc
            
            if self.use_rvc:
                await ctx.respond("✅ **RVC Voice Conversion Enabled!**\n\nI'll now use custom RVC voices for speech!")
            else:
                await ctx.respond("🔄 **RVC Voice Conversion Disabled!**\n\nI'll use Edge TTS voices instead.")
                
        except Exception as e:
            logging.error(f"Error toggling RVC: {e}")
            await ctx.respond(f"❌ Error toggling RVC: {str(e)}")

    @discord.slash_command(name="test_rvc_voice", description="Test RVC voice conversion", **default_params)
    async def test_rvc_voice(self, ctx):
        """Test the current RVC voice model"""
        try:
            if not ctx.author.voice:
                await ctx.respond("❌ You need to be in a voice channel to test voice!")
                return

            # Check if bot is in voice channel
            if not hasattr(self.bot, 'voice_clients') or not self.bot.voice_clients:
                await ctx.respond("❌ I need to join your voice channel first! Use `/join`")
                return

            await ctx.respond("🎭 Testing RVC voice conversion...")
            
            test_text = "Hello! This is a test of the RVC voice conversion system."
            
            if self.use_rvc and self.available_models:
                success = await self._speak_with_rvc(test_text, ctx)
                if success:
                    await ctx.followup.send("✅ **RVC Voice Test Successful!**")
                else:
                    await ctx.followup.send("❌ **RVC Voice Test Failed!** Falling back to Edge TTS.")
            else:
                # Fallback to Edge TTS
                success = await self._speak_with_edge_tts(test_text, ctx)
                if success:
                    await ctx.followup.send("✅ **Edge TTS Test Successful!** (RVC not enabled)")
                else:
                    await ctx.followup.send("❌ **Voice Test Failed!**")
                    
        except Exception as e:
            logging.error(f"RVC voice test error: {e}")
            await ctx.respond(f"❌ RVC voice test failed: {str(e)}")

    async def speak_text(self, text: str, voice_client) -> bool:
        """Main method to speak text using RVC or Edge TTS"""
        try:
            if self.use_rvc and self.available_models:
                return await self._speak_with_rvc(text, voice_client)
            else:
                return await self._speak_with_edge_tts(text, voice_client)
                
        except Exception as e:
            logging.error(f"Error in speak_text: {e}")
            return False

    async def _speak_with_rvc(self, text: str, ctx) -> bool:
        """Speak text using RVC voice conversion"""
        try:
            if not self.available_models:
                logging.warning("No RVC models available, falling back to Edge TTS")
                return await self._speak_with_edge_tts(text, ctx)
                
            # Try RVC API first (if enabled)
            if self.rvc_api_enabled:
                return await self._speak_with_rvc_api(text, ctx)
            else:
                # Try local RVC processing
                return await self._speak_with_rvc_local(text, ctx)
                
        except Exception as e:
            logging.error(f"RVC speech error: {e}")
            return False

    async def _speak_with_rvc_api(self, text: str, ctx) -> bool:
        """Speak using RVC WebUI API"""
        try:
            # First generate TTS audio using Edge TTS
            tts_audio = await self._generate_edge_tts(text)
            if not tts_audio:
                return False
                
            # Send to RVC API for voice conversion
            rvc_payload = {
                "audio": tts_audio,
                "model": self.current_voice_model,
                "pitch": 0,
                "index_rate": 0.5,
                "filter_radius": 3,
                "resample_sr": 0,
                "rms_mix_rate": 0.25
            }
            
            response = requests.post(f"{self.rvc_api_url}/voice-conversion", json=rvc_payload, timeout=30)
            if response.status_code == 200:
                # Play the converted audio
                return await self._play_audio(response.content, ctx)
            else:
                logging.error(f"RVC API error: {response.status_code}")
                return False
                
        except Exception as e:
            logging.error(f"RVC API speech error: {e}")
            return False

    async def _speak_with_rvc_local(self, text: str, ctx) -> bool:
        """Speak using local RVC processing"""
        try:
            # For now, fall back to Edge TTS since local RVC requires complex setup
            logging.info("Local RVC not implemented, using Edge TTS fallback")
            return await self._speak_with_edge_tts(text, ctx)
            
        except Exception as e:
            logging.error(f"Local RVC speech error: {e}")
            return False

    async def _speak_with_edge_tts(self, text: str, ctx) -> bool:
        """Speak text using Edge TTS (fallback)"""
        try:
            # Generate TTS audio
            tts_audio = await self._generate_edge_tts(text)
            if not tts_audio:
                return False
                
            # Play the audio
            return await self._play_audio(tts_audio, ctx)
            
        except Exception as e:
            logging.error(f"Edge TTS speech error: {e}")
            return False

    async def _generate_edge_tts(self, text: str) -> Optional[bytes]:
        """Generate TTS audio using Edge TTS"""
        try:
            communicate = edge_tts.Communicate(text, self.edge_voice)
            audio_data = await communicate.get_audio()
            return audio_data
            
        except Exception as e:
            logging.error(f"Edge TTS generation error: {e}")
            return None

    async def _play_audio(self, audio_data: bytes, ctx) -> bool:
        """Play audio in voice channel"""
        try:
            # Create temporary audio file
            with tempfile.NamedTemporaryFile(suffix=".mp3", delete=False) as temp_file:
                temp_file.write(audio_data)
                temp_file.flush()
                
                # Get voice client
                voice_client = None
                if hasattr(self.bot, 'voice_clients') and self.bot.voice_clients:
                    voice_client = self.bot.voice_clients[0]
                
                if not voice_client:
                    logging.error("No voice client available")
                    return False
                
                # Play the audio
                voice_client.play(discord.FFmpegPCMAudio(temp_file.name))
                
                # Wait for audio to finish
                while voice_client.is_playing():
                    await asyncio.sleep(0.1)
                
                # Clean up
                os.unlink(temp_file.name)
                return True
                
        except Exception as e:
            logging.error(f"Audio playback error: {e}")
            return False

def setup(bot: discord.Bot) -> None:
    bot.add_cog(RVCVoiceEnhancedCog(bot))
