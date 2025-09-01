import discord
from discord.ext import commands
import asyncio
import logging
import os
import tempfile
import speech_recognition as sr
import whisper
from typing import Optional, Dict, Any
import json

from cogs.defaults import default_params
from utils.service.Ollama_worker import OllamaWorker

class VoiceInteractionCog(commands.Cog):
    '''
    Voice interaction system: Speech → AI → Voice Response
    '''

    def __init__(self, bot: discord.Bot) -> None:
        self.bot = bot
        self.recognizer = sr.Recognizer()
        self.whisper_model = None
        self.voice_channels = {}  # Track active voice interactions
        self.ai_worker = OllamaWorker()
        self.interaction_enabled = {}  # Track servers with voice interaction enabled
        
    async def _load_whisper_model(self):
        """Load Whisper model for offline transcription"""
        if self.whisper_model is None:
            try:
                logging.info("Loading Whisper model...")
                self.whisper_model = whisper.load_model("base")
                logging.info("Whisper model loaded successfully")
            except Exception as e:
                logging.error(f"Failed to load Whisper model: {e}")
                self.whisper_model = None

    @discord.slash_command(name="voice_ai", description="Enable voice AI interaction", **default_params)
    async def enable_voice_ai(self, ctx):
        """Enable voice AI interaction for this server"""
        try:
            guild_id = ctx.guild.id
            self.interaction_enabled[guild_id] = True
            await ctx.respond("🤖 **Voice AI Interaction Enabled!**\n\nI'll now listen to voice chat, process your requests through AI, and respond both in text and voice!")
        except Exception as e:
            logging.error(f"Error enabling voice AI: {e}")
            await ctx.respond(f"Error enabling voice AI: {str(e)}")

    @discord.slash_command(name="disable_voice_ai", description="Disable voice AI interaction", **default_params)
    async def disable_voice_ai(self, ctx):
        """Disable voice AI interaction for this server"""
        try:
            guild_id = ctx.guild.id
            if guild_id in self.interaction_enabled:
                del self.interaction_enabled[guild_id]
            await ctx.respond("🛑 **Voice AI Interaction Disabled!**\n\nI'll no longer process voice interactions.")
        except Exception as e:
            logging.error(f"Error disabling voice AI: {e}")
            await ctx.respond(f"Error disabling voice AI: {str(e)}")

    @discord.slash_command(name="voice_ai_status", description="Check voice AI interaction status", **default_params)
    async def voice_ai_status(self, ctx):
        """Check the current voice AI interaction status"""
        try:
            guild_id = ctx.guild.id
            ai_enabled = guild_id in self.interaction_enabled
            
            # Check if currently processing any voice interactions
            active_channels = []
            for channel_id, data in self.voice_channels.items():
                if data.get('ctx', {}).guild.id == ctx.guild.id:
                    channel = ctx.guild.get_channel(channel_id)
                    if channel:
                        active_channels.append(channel.name)
            
            status_msg = f"🤖 **Voice AI Interaction Status**\n\n"
            status_msg += f"**Voice AI:** {'✅ Enabled' if ai_enabled else '❌ Disabled'}\n"
            
            if active_channels:
                status_msg += f"**Active interactions:** {', '.join(active_channels)}\n"
            else:
                status_msg += "**Active interactions:** None\n"
            
            status_msg += f"\n**Commands:**\n"
            status_msg += "• `/voice_ai` - Enable voice AI interaction\n"
            status_msg += "• `/voice_ai_status` - Check status\n"
            status_msg += "• `/test_voice_ai` - Test the system\n"
            
            await ctx.respond(status_msg)
            
        except Exception as e:
            logging.error(f"Error checking voice AI status: {e}")
            await ctx.respond(f"Error checking status: {str(e)}")

    @discord.slash_command(name="test_voice_ai", description="Test the voice AI interaction system", **default_params)
    async def test_voice_ai(self, ctx):
        """Test the voice AI interaction system"""
        try:
            # Check if user is in voice channel
            if not ctx.author.voice:
                await ctx.respond("❌ You need to be in a voice channel to test voice AI!")
                return

            voice_channel = ctx.author.voice.channel
            
            # Check if bot is in the same voice channel
            if not hasattr(self.bot, 'voice_clients') or not self.bot.voice_clients:
                await ctx.respond("❌ I need to join your voice channel first! Use `/join`")
                return

            # Check if voice AI is enabled
            guild_id = ctx.guild.id
            if guild_id not in self.interaction_enabled:
                await ctx.respond("❌ Voice AI is not enabled! Use `/voice_ai` first.")
                return

            await ctx.respond("🤖 Testing voice AI interaction...")
            
            # Simulate a voice interaction
            test_query = "Hello! Can you tell me a short joke?"
            logging.info(f"Starting voice AI test with query: {test_query}")
            await self._process_voice_interaction(ctx, test_query, is_test=True)
            
        except Exception as e:
            logging.error(f"Voice AI test error: {e}")
            await ctx.respond(f"❌ Voice AI test failed: {str(e)}")

    @discord.slash_command(name="test_ai_only", description="Test AI response without voice", **default_params)
    async def test_ai_only(self, ctx):
        """Test AI response generation without voice requirements"""
        try:
            await ctx.respond("🤖 Testing AI response generation...")
            
            test_query = "Hello! Can you tell me a short joke?"
            logging.info(f"Testing AI with query: {test_query}")
            
            ai_response = await self._get_ai_response(test_query)
            if ai_response:
                await ctx.followup.send(f"✅ **AI Test Successful!**\n\n**Query:** {test_query}\n**Response:** {ai_response}")
            else:
                await ctx.followup.send("❌ **AI Test Failed!** Could not get response from Ollama.")
                
        except Exception as e:
            logging.error(f"AI test error: {e}")
            await ctx.respond(f"❌ AI test failed: {str(e)}")

    async def _process_voice_interaction(self, ctx, user_query: str, is_test: bool = False) -> bool:
        """Process a voice interaction: Query → AI → Response → Voice"""
        try:
            logging.info(f"Processing voice interaction: {user_query[:50]}...")
            
            # Step 1: Get AI response
            ai_response = await self._get_ai_response(user_query)
            if not ai_response:
                await ctx.followup.send("❌ Failed to get AI response")
                return False

            # Step 2: Send text response to chat
            if is_test:
                await ctx.followup.send(f"🤖 **AI Response:** {ai_response}")
            else:
                await ctx.channel.send(f"🤖 **AI Response:** {ai_response}")

            # Step 3: Convert response to voice and play it
            voice_success = await self._speak_ai_response(ai_response, ctx)
            
            if voice_success:
                logging.info("Voice interaction completed successfully")
                return True
            else:
                logging.error("Voice interaction failed at speech stage")
                return False

        except Exception as e:
            logging.error(f"Error in voice interaction: {e}")
            return False

    async def _get_ai_response(self, query: str) -> Optional[str]:
        """Get AI response using Ollama or other AI service"""
        try:
            logging.info(f"Getting AI response for: {query[:50]}...")
            # Use the existing Ollama worker
            response = self.ai_worker.generate_response(query)
            if response:
                logging.info(f"AI response received: {response[:100]}...")
                return response
            else:
                logging.error("AI response was empty")
                return None
        except Exception as e:
            logging.error(f"Error getting AI response: {e}")
            return None

    async def _speak_ai_response(self, text: str, ctx) -> bool:
        """Speak the AI response using enhanced RVC voice system"""
        try:
            # Try enhanced RVC voice cog first
            rvc_cog = self.bot.get_cog("RVCVoiceEnhancedCog")
            if rvc_cog:
                logging.info("Using enhanced RVC voice system")
                success = await rvc_cog.speak_text(text, ctx)
                if success:
                    return True
                else:
                    logging.warning("RVC voice failed, falling back to simple voice")
            
            # Fallback to simple voice cog
            voice_cog = self.bot.get_cog("SimpleVoiceCog")
            if not voice_cog:
                logging.error("No voice cog found")
                return False

            # Check if bot is in voice channel
            if not hasattr(self.bot, 'voice_clients') or not self.bot.voice_clients:
                logging.error("Bot not in voice channel")
                return False

            voice_client = self.bot.voice_clients[0]
            
            # Use the simple voice cog to speak the text
            success = await voice_cog.speak_text(text, voice_client)
            return success

        except Exception as e:
            logging.error(f"Error speaking AI response: {e}")
            return False

    async def _transcribe_audio(self, audio_data: bytes) -> Optional[str]:
        """Transcribe audio data to text"""
        try:
            # Try Whisper first (offline)
            if self.whisper_model:
                with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as temp_file:
                    temp_file.write(audio_data)
                    temp_file.flush()
                    
                    result = self.whisper_model.transcribe(temp_file.name)
                    os.unlink(temp_file.name)
                    
                    if result and result.get('text'):
                        return result['text'].strip()

            # Fallback to Google Speech Recognition (online)
            audio = sr.AudioData(audio_data, sample_rate=16000, sample_width=2)
            text = self.recognizer.recognize_google(audio)
            return text

        except Exception as e:
            logging.error(f"Transcription failed: {e}")
            return None

    async def _handle_voice_message(self, message: discord.Message):
        """Handle voice messages for transcription and AI processing"""
        try:
            if not message.attachments:
                return

            # Simplified: process voice messages if voice AI is enabled anywhere
            if not self.interaction_enabled:
                return

            # Process voice attachments
            for attachment in message.attachments:
                if attachment.content_type and 'audio' in attachment.content_type:
                    await self._process_voice_attachment(message, attachment)

        except Exception as e:
            logging.error(f"Error handling voice message: {e}")

    async def _process_voice_attachment(self, message: discord.Message, attachment: discord.Attachment):
        """Process a voice attachment for AI interaction"""
        try:
            await message.channel.send("🎤 Processing voice message...")
            
            # Download the audio file
            audio_data = await attachment.read()
            
            # Transcribe the audio
            transcription = await self._transcribe_audio(audio_data)
            if not transcription:
                await message.channel.send("❌ Failed to transcribe voice message")
                return

            # Send transcription to chat
            await message.channel.send(f"📝 **Transcription:** {transcription}")
            
            # Process with AI and respond
            await self._process_voice_interaction(message, transcription)

        except Exception as e:
            logging.error(f"Error processing voice attachment: {e}")
            await message.channel.send(f"❌ Error processing voice message: {str(e)}")

    async def on_message(self, message: discord.Message):
        """Handle incoming messages for voice AI processing"""
        if message.author.bot:
            return

        # Handle voice messages
        if message.attachments:
            await self._handle_voice_message(message)

        # Handle mentions for voice AI
        if self.bot.user in message.mentions:
            # Simplified: process mentions if voice AI is enabled anywhere
            if self.interaction_enabled:
                # Process text query through voice AI
                query = message.content.replace(f'<@{self.bot.user.id}>', '').strip()
                if query:
                    await self._process_voice_interaction(message, query)

def setup(bot: discord.Bot) -> None:
    bot.add_cog(VoiceInteractionCog(bot))
