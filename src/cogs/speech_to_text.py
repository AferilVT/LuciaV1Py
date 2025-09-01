import discord
from discord.ext import commands
import asyncio
import os
import tempfile
import logging
import speech_recognition as sr
import whisper
import io

from cogs.defaults import default_params

class SpeechToTextCog(commands.Cog):
    '''
    Add speech-to-text functionality to the bot
    '''

    def __init__(self, bot: discord.Bot) -> None:
        self.bot = bot
        self.recognizer = sr.Recognizer()
        self.whisper_model = None
        self.voice_channels = {}  # Track voice channels for real-time transcription
        self.auto_transcribe = {}  # Track servers with auto-transcription enabled
        
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

    @discord.slash_command(name="auto_transcribe", description="Enable automatic transcription for voice channels", **default_params)
    async def enable_auto_transcribe(self, ctx):
        """Enable automatic transcription for all voice channels in this server"""
        try:
            guild_id = ctx.guild.id
            self.auto_transcribe[guild_id] = True
            await ctx.respond("✅ **Auto-transcription enabled!**\n\nI'll automatically start transcribing when someone joins a voice channel and send transcriptions to the general chat.")
        except Exception as e:
            logging.error(f"Error enabling auto-transcribe: {e}")
            await ctx.respond(f"Error enabling auto-transcribe: {str(e)}")

    @discord.slash_command(name="disable_auto_transcribe", description="Disable automatic transcription", **default_params)
    async def disable_auto_transcribe(self, ctx):
        """Disable automatic transcription for this server"""
        try:
            guild_id = ctx.guild.id
            if guild_id in self.auto_transcribe:
                del self.auto_transcribe[guild_id]
            await ctx.respond("🛑 **Auto-transcription disabled!**\n\nI'll no longer automatically transcribe voice channels.")
        except Exception as e:
            logging.error(f"Error disabling auto-transcribe: {e}")
            await ctx.respond(f"Error disabling auto-transcribe: {str(e)}")

    @discord.slash_command(name="transcribe_status", description="Check transcription status", **default_params)
    async def transcribe_status(self, ctx):
        """Check the current transcription status"""
        try:
            guild_id = ctx.guild.id
            auto_enabled = guild_id in self.auto_transcribe
            
            # Check if currently transcribing any voice channels
            active_channels = []
            for channel_id, data in self.voice_channels.items():
                if data.get('ctx', {}).guild.id == ctx.guild.id:
                    channel = ctx.guild.get_channel(channel_id)
                    if channel:
                        active_channels.append(channel.name)
            
            status_msg = f"📊 **Transcription Status**\n\n"
            status_msg += f"**Auto-transcription:** {'✅ Enabled' if auto_enabled else '❌ Disabled'}\n"
            
            if active_channels:
                status_msg += f"**Active transcriptions:** {', '.join(active_channels)}\n"
            else:
                status_msg += "**Active transcriptions:** None\n"
            
            status_msg += f"\n**Commands:**\n"
            status_msg += "• `/transcribe_live` - Start manual transcription\n"
            status_msg += "• `/auto_transcribe` - Enable auto-transcription\n"
            status_msg += "• `/transcribe_stop` - Stop transcription\n"
            
            await ctx.respond(status_msg)
            
        except Exception as e:
            logging.error(f"Error checking transcribe status: {e}")
            await ctx.respond(f"Error checking status: {str(e)}")

    @discord.slash_command(name="transcribe", description="Transcribe an audio file or voice message", **default_params)
    @discord.option("file", description="Audio file to transcribe", required=False)
    async def transcribe_audio(self, ctx, file: discord.Attachment = None):
        """Transcribe an audio file or voice message"""
        try:
            # Check if there's a file attachment or if we should use the last recording
            if file:
                audio_file = file
            else:
                # Check if there are any recent recordings
                recordings_dir = "recordings"
                if not os.path.exists(recordings_dir):
                    await ctx.respond("No audio file provided and no recordings found. Please attach an audio file or use /record_start first.")
                    return
                
                # Get the most recent recording
                recordings = [f for f in os.listdir(recordings_dir) if f.endswith('.mp3')]
                if not recordings:
                    await ctx.respond("No audio file provided and no recordings found. Please attach an audio file or use /record_start first.")
                    return
                
                # Use the most recent recording
                latest_recording = max(recordings, key=lambda x: os.path.getctime(os.path.join(recordings_dir, x)))
                audio_file = discord.Attachment(
                    filename=latest_recording,
                    url=f"file://{os.path.join(recordings_dir, latest_recording)}"
                )
            
            await ctx.respond("Processing audio transcription...")
            
            # Download the audio file
            audio_data = await audio_file.read()
            
            # Save to temporary file
            with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as temp_file:
                temp_file.write(audio_data)
                temp_file_path = temp_file.name
            
            try:
                # Try using Whisper for transcription
                await self._load_whisper_model()
                if self.whisper_model:
                    transcription = await self._transcribe_with_whisper(temp_file_path)
                else:
                    # Fallback to Google Speech Recognition
                    transcription = await self._transcribe_with_google(temp_file_path)
                
                if transcription:
                    # Split long transcriptions
                    if len(transcription) > 2000:
                        chunks = [transcription[i:i+1990] for i in range(0, len(transcription), 1990)]
                        for i, chunk in enumerate(chunks):
                            if i == 0:
                                await ctx.followup.send(f"**Transcription:**\n{chunk}\n[1/{len(chunks)}]")
                            else:
                                await ctx.followup.send(f"{chunk}\n[{i+1}/{len(chunks)}]")
                    else:
                        await ctx.followup.send(f"**Transcription:**\n{transcription}")
                else:
                    await ctx.followup.send("Could not transcribe the audio. Please try again with clearer audio.")
                    
            finally:
                # Clean up temporary file
                if os.path.exists(temp_file_path):
                    os.unlink(temp_file_path)
                    
        except Exception as e:
            logging.error(f"Error in transcribe_audio: {e}")
            await ctx.followup.send(f"Error transcribing audio: {str(e)}")

    async def _transcribe_with_whisper(self, audio_file_path: str):
        """Transcribe audio using Whisper"""
        try:
            result = self.whisper_model.transcribe(audio_file_path)
            return result["text"].strip()
        except Exception as e:
            logging.error(f"Whisper transcription error: {e}")
            return None

    async def _transcribe_with_google(self, audio_file_path: str):
        """Transcribe audio using Google Speech Recognition"""
        try:
            with sr.AudioFile(audio_file_path) as source:
                audio = self.recognizer.record(source)
                text = self.recognizer.recognize_google(audio)
                return text
        except sr.UnknownValueError:
            logging.warning("Google Speech Recognition could not understand audio")
            return None
        except sr.RequestError as e:
            logging.error(f"Google Speech Recognition error: {e}")
            return None
        except Exception as e:
            logging.error(f"Error in Google transcription: {e}")
            return None

    @discord.slash_command(name="transcribe_live", description="Start real-time transcription in voice channel", **default_params)
    async def start_live_transcription(self, ctx):
        """Start real-time transcription in the current voice channel"""
        try:
            # Check if user is in a voice channel
            if not ctx.author.voice:
                await ctx.respond("You need to be in a voice channel to use this command!")
                return
            
            voice_channel = ctx.author.voice.channel
            
            # Check if bot is already transcribing this channel
            if voice_channel.id in self.voice_channels:
                await ctx.respond("Already transcribing this voice channel!")
                return
            
            # Join the voice channel if not already connected
            voice_client = ctx.guild.voice_client
            if not voice_client or voice_client.channel != voice_channel:
                voice_client = await voice_channel.connect()
            
            # Start recording for transcription
            sink = discord.sinks.MP3Sink()
            voice_client.start_recording(sink, self._live_transcription_callback, ctx)
            
            self.voice_channels[voice_channel.id] = {
                'sink': sink,
                'voice_client': voice_client,
                'ctx': ctx,
                'text_channel': ctx.channel  # Store the text channel to send transcriptions to
            }
            
            await ctx.respond(f"🎤 **Live transcription started in {voice_channel.name}!**\n\nI'll now transcribe everything said in voice chat and send it to this text channel.\n\nUse `/transcribe_stop` to stop the transcription.")
            
        except Exception as e:
            logging.error(f"Error starting live transcription: {e}")
            await ctx.respond(f"Error starting live transcription: {str(e)}")

    async def _live_transcription_callback(self, sink: discord.sinks.Sink, ctx):
        """Handle live transcription callback - sends transcriptions to text chat"""
        try:
            # Process each user's audio
            for user_id, audio in sink.audio_data.items():
                # Save audio to temporary file
                with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as temp_file:
                    temp_file.write(audio.file.read())
                    temp_file_path = temp_file.name
                
                try:
                    # Transcribe the audio
                    await self._load_whisper_model()
                    if self.whisper_model:
                        transcription = await self._transcribe_with_whisper(temp_file_path)
                    else:
                        transcription = await self._transcribe_with_google(temp_file_path)
                    
                    if transcription and transcription.strip():
                        # Get user info
                        user = await self.bot.fetch_user(int(user_id))
                        user_name = user.display_name if user else f"User {user_id}"
                        
                        # Send transcription to the text channel
                        # Find the correct text channel from the stored data
                        text_channel = ctx.channel  # Default to the context channel
                        for channel_id, data in self.voice_channels.items():
                            if data.get('ctx') == ctx:
                                text_channel = data.get('text_channel', ctx.channel)
                                break
                        
                        await text_channel.send(f"**{user_name}:** {transcription}")
                        
                finally:
                    # Clean up temporary file
                    if os.path.exists(temp_file_path):
                        os.unlink(temp_file_path)
            
            # Remove from tracking
            voice_channel = ctx.author.voice.channel if ctx.author.voice else None
            if voice_channel and voice_channel.id in self.voice_channels:
                del self.voice_channels[voice_channel.id]
                
        except Exception as e:
            logging.error(f"Error in live transcription callback: {e}")

    @discord.slash_command(name="transcribe_stop", description="Stop real-time transcription", **default_params)
    async def stop_live_transcription(self, ctx):
        """Stop real-time transcription"""
        try:
            # Check if user is in a voice channel
            if not ctx.author.voice:
                await ctx.respond("You need to be in a voice channel to use this command!")
                return
            
            voice_channel = ctx.author.voice.channel
            
            # Check if we're transcribing this channel
            if voice_channel.id not in self.voice_channels:
                await ctx.respond("Not currently transcribing this voice channel!")
                return
            
            # Stop recording
            voice_client = self.voice_channels[voice_channel.id]['voice_client']
            voice_client.stop_recording()
            
            await ctx.respond("🛑 **Live transcription stopped!**\n\nI'm no longer transcribing voice chat to text.")
            
        except Exception as e:
            logging.error(f"Error stopping live transcription: {e}")
            await ctx.respond(f"Error stopping live transcription: {str(e)}")

    @discord.slash_command(name="transcribe_voice_message", description="Transcribe a voice message", **default_params)
    async def transcribe_voice_message(self, ctx):
        """Transcribe the most recent voice message in the channel"""
        try:
            # Get the last 10 messages to find voice messages
            messages = await ctx.channel.history(limit=10).flatten()
            
            voice_message = None
            for message in messages:
                if message.attachments:
                    for attachment in message.attachments:
                        if attachment.content_type and 'audio' in attachment.content_type:
                            voice_message = attachment
                            break
                    if voice_message:
                        break
            
            if not voice_message:
                await ctx.respond("No voice message found in the recent messages. Please send a voice message first.")
                return
            
            await ctx.respond("Processing voice message transcription...")
            
            # Download and transcribe
            audio_data = await voice_message.read()
            
            with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as temp_file:
                temp_file.write(audio_data)
                temp_file_path = temp_file.name
            
            try:
                await self._load_whisper_model()
                if self.whisper_model:
                    transcription = await self._transcribe_with_whisper(temp_file_path)
                else:
                    transcription = await self._transcribe_with_google(temp_file_path)
                
                if transcription:
                    await ctx.followup.send(f"**Voice Message Transcription:**\n{transcription}")
                else:
                    await ctx.followup.send("Could not transcribe the voice message. Please try again.")
                    
            finally:
                if os.path.exists(temp_file_path):
                    os.unlink(temp_file_path)
                    
        except Exception as e:
            logging.error(f"Error transcribing voice message: {e}")
            await ctx.respond(f"Error transcribing voice message: {str(e)}")

    @discord.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        """Automatically start transcription when someone joins a voice channel"""
        try:
            # Check if auto-transcription is enabled for this server
            guild_id = member.guild.id
            if guild_id not in self.auto_transcribe:
                return
            
            # Only start transcription when someone joins (not when they leave)
            if before.channel is None and after.channel is not None:
                voice_channel = after.channel
                
                # Don't start if already transcribing this channel
                if voice_channel.id in self.voice_channels:
                    return
                
                # Find the general text channel to send transcriptions to
                text_channel = None
                for channel in member.guild.text_channels:
                    if channel.name.lower() in ['general', 'chat', 'main']:
                        text_channel = channel
                        break
                
                if not text_channel:
                    # Use the first text channel if no general channel found
                    text_channels = [c for c in member.guild.text_channels if c.permissions_for(member.guild.me).send_messages]
                    if text_channels:
                        text_channel = text_channels[0]
                
                if text_channel:
                    try:
                        # Join the voice channel
                        voice_client = await voice_channel.connect()
                        
                        # Start recording for transcription
                        sink = discord.sinks.MP3Sink()
                        voice_client.start_recording(sink, self._auto_transcription_callback, text_channel)
                        
                        self.voice_channels[voice_channel.id] = {
                            'sink': sink,
                            'voice_client': voice_client,
                            'ctx': None,  # No context for auto-transcription
                            'text_channel': text_channel
                        }
                        
                        # Send notification to text channel
                        await text_channel.send(f"🎤 **Auto-transcription started in {voice_channel.name}!**\n\nI'm now transcribing everything said in voice chat and sending it here.")
                        
                    except Exception as e:
                        logging.error(f"Error starting auto-transcription: {e}")
                        
        except Exception as e:
            logging.error(f"Error in voice state update: {e}")

    async def _auto_transcription_callback(self, sink: discord.sinks.Sink, text_channel):
        """Handle auto-transcription callback"""
        try:
            # Process each user's audio
            for user_id, audio in sink.audio_data.items():
                # Save audio to temporary file
                with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as temp_file:
                    temp_file.write(audio.file.read())
                    temp_file_path = temp_file.name
                
                try:
                    # Transcribe the audio
                    await self._load_whisper_model()
                    if self.whisper_model:
                        transcription = await self._transcribe_with_whisper(temp_file_path)
                    else:
                        transcription = await self._transcribe_with_google(temp_file_path)
                    
                    if transcription and transcription.strip():
                        # Get user info
                        user = await self.bot.fetch_user(int(user_id))
                        user_name = user.display_name if user else f"User {user_id}"
                        
                        # Send transcription to the text channel
                        await text_channel.send(f"**{user_name}:** {transcription}")
                        
                finally:
                    # Clean up temporary file
                    if os.path.exists(temp_file_path):
                        os.unlink(temp_file_path)
            
            # Remove from tracking
            for channel_id, data in list(self.voice_channels.items()):
                if data.get('text_channel') == text_channel:
                    del self.voice_channels[channel_id]
                    break
                    
        except Exception as e:
            logging.error(f"Error in auto-transcription callback: {e}")

def setup(bot: discord.Bot) -> None:
    bot.add_cog(SpeechToTextCog(bot)) 