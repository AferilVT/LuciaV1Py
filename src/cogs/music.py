import discord
from discord.ext import commands
import asyncio
import yt_dlp
import os
import tempfile
import logging
import time

from cogs.defaults import default_params

class NotInVCException(Exception):
    pass

class MusicCog(commands.Cog):
    '''
    Add music and voice functionality to the bot
    '''

    def __init__(self, bot: discord.Bot) -> None:
        self.bot = bot
        self.vc = None
        self.volume = 1.0  # Default volume (max)
        self.playlist = []  # Song queue
        self.is_playing = False
        self.recording = False  # Track recording state
        
    def _check_connected(self) -> bool:
        '''Return whether the bot is connected to a voice channel'''
        return self.vc is not None and self.vc.is_connected()
    
    async def _disconnect_client_if_connected(self) -> bool:
        '''Disconnect the bot from the voice channel if it is connected'''
        if self._check_connected():
            try:
                await self.vc.disconnect()
                self.vc = None
                return True
            except Exception as e:
                logging.error(f"Error disconnecting from voice: {e}")
                self.vc = None
                return False
        else:
            return False
        
    @discord.slash_command(name="join", description="Join a voice channel", **default_params)
    @discord.option("channel", type=discord.channel.VoiceChannel)
    async def join_vc(self, ctx, channel: discord.VoiceChannel) -> None:
        '''Join bot to specified VC'''
        try:
            await ctx.respond("🎤 Attempting to join voice channel...")
            
            # Check if bot is already in a voice channel
            if self._check_connected():
                await self.vc.disconnect()
                await asyncio.sleep(1)  # Small delay to ensure clean disconnect
            
            # Check bot permissions
            if not channel.permissions_for(ctx.guild.me).connect:
                await ctx.followup.send(f"❌ I don't have permission to connect to {channel.name}")
                return
            
            if not channel.permissions_for(ctx.guild.me).speak:
                await ctx.followup.send(f"❌ I don't have permission to speak in {channel.name}")
                return
            
            # Try to connect with timeout
            try:
                self.vc = await asyncio.wait_for(channel.connect(), timeout=30.0)
                await ctx.followup.send(f"✅ Successfully joined {channel.name}!")
            except asyncio.TimeoutError:
                await ctx.followup.send(f"❌ Connection to {channel.name} timed out. Please try again.")
                return
                
        except discord.ClientException as err:
            logging.error(f"ClientException when joining voice: {err}")
            await ctx.followup.send(f"❌ Failed to join {channel.name}. The bot may already be in a voice channel or there's a connection issue.")
            return
        except asyncio.TimeoutError as err:
            logging.error(f"Timeout when joining voice: {err}")
            await ctx.followup.send(f"❌ Request to join {channel.name} timed out. Please try again.")
            return
        except discord.ConnectionClosed as err:
            logging.error(f"Connection closed when joining voice: {err}")
            await ctx.followup.send(f"❌ Voice connection failed for {channel.name}. This might be due to missing voice dependencies or Discord rate limiting. Please try again in a few minutes.")
            return
        except Exception as err:
            logging.error(f"Unexpected error when joining voice: {err}")
            await ctx.followup.send(f"❌ Failed to join {channel.name}. Please check if the bot has the necessary permissions and voice dependencies are installed.")
            return

    @discord.slash_command(name="leave", description="Leave the voice channel", **default_params)
    async def leave_vc(self, ctx) -> None:
        '''Leave the voice channel'''
        try:
            if not await self._disconnect_client_if_connected():
                raise NotInVCException
            await ctx.respond("✅ Left the voice channel!")
        except NotInVCException:
            logging.warning("Attempted to leave voice channel when not connected")
            await ctx.respond("❌ I'm not in a voice channel!")
            return
        except Exception as err:
            logging.error(f"Error leaving voice channel: {err}")
            await ctx.respond("❌ Failed to leave voice channel...")
            return

    @discord.slash_command(name="play", description="Play a song", **default_params)
    async def play_sound(self, ctx) -> None:
        '''Play a song'''
        try:
            if not self._check_connected():
                raise NotInVCException
            if not self.is_playing and self.playlist:
                await self.play_next(ctx)
            elif not self.playlist:
                await ctx.respond("Playlist is empty. Add songs with /addsong.")
            else:
                await ctx.respond("Already playing.")
        except NotInVCException:
            print(err)
            await ctx.respond("I'm not in a voice channel!")
            return
        except Exception as err:
            print(err)
            await ctx.respond("Failed to play sound...")
            return

    @discord.slash_command(name="record_start", description="Start recording current voice channel audio", **default_params)
    async def record_start(self, ctx) -> None:
        '''Start recording current voice channel audio'''
        try:
            if not self._check_connected():
                raise NotInVCException
            
            if self.recording:
                await ctx.respond("❌ Already recording! Use /record_stop to stop first.")
                return
                
            # Check if we have permission to record
            if not ctx.guild.me.guild_permissions.attach_files:
                await ctx.respond("❌ I don't have permission to attach files (needed for recording).")
                return
            
            sink = discord.sinks.MP3Sink()
            self.vc.start_recording(sink, self._record_callback, ctx)
            self.recording = True
            
            await ctx.respond("🎤 **Recording started!**\n\nI'm now recording everything said in the voice channel. Use `/record_stop` to stop recording.")
            
        except NotInVCException:
            logging.warning("Attempted to start recording when not in voice channel")
            await ctx.respond("❌ I'm not in a voice channel! Use `/join` first.")
            return
        except discord.sinks.RecordingException as err:
            logging.error(f"RecordingException: {err}")
            await ctx.respond("❌ Already recording! Use `/record_stop` to stop first.")
            return
        except Exception as err:
            logging.error(f"Error starting recording: {err}")
            await ctx.respond("❌ Failed to start recording. Please try again.")
            return

    async def _record_callback(self, sink: discord.sinks.Sink, ctx) -> None:
        '''Store audio from sink into one audio file per user'''
        try:
            self.recording = False
            os.makedirs("recordings", exist_ok=True)
            
            if not sink.audio_data:
                await ctx.send("📝 **Recording finished!** (No audio was captured)")
                return
            
            for user_id, audio in sink.audio_data.items():
                try:
                    user = await self.bot.fetch_user(int(user_id))
                    user_name = user.display_name if user else f"User_{user_id}"
                    filename = f"recordings/{user_name}_{int(time.time())}.mp3"
                    
                    with open(filename, "wb") as f:
                        f.write(audio.file.read())
                    
                    await ctx.send(f"📝 **Recording saved:** `{filename}`")
                    
                except Exception as e:
                    logging.error(f"Error saving recording for user {user_id}: {e}")
                    await ctx.send(f"❌ Error saving recording for user {user_id}")
                    
        except Exception as e:
            logging.error(f"Error in record callback: {e}")
            await ctx.send("❌ Error processing recording")

    @discord.slash_command(name="record_stop", description="Stop recording current voice channel audio", **default_params)
    async def record_stop(self, ctx) -> None:
        '''Stop recording current voice channel audio'''
        try:
            if not self._check_connected():
                raise NotInVCException
            
            if not self.recording:
                await ctx.respond("❌ Not currently recording! Use `/record_start` to start recording.")
                return
            
            self.vc.stop_recording()
            self.recording = False
            
            await ctx.respond("🛑 **Recording stopped!**\n\nProcessing recordings...")
            
        except NotInVCException:
            logging.warning("Attempted to stop recording when not in voice channel")
            await ctx.respond("❌ I'm not in a voice channel!")
            return
        except discord.sinks.RecordingException as err:
            logging.error(f"RecordingException when stopping: {err}")
            await ctx.respond("❌ Was not recording!")
            return
        except Exception as err:
            logging.error(f"Error stopping recording: {err}")
            await ctx.respond("❌ Failed to stop recording!")
            return
        
    @discord.slash_command(name="volume", description="Set playback volume (1-10)", **default_params)
    @discord.option("level", type=int, min_value=1, max_value=10, description="Volume level (1-10)")
    async def set_volume(self, ctx, level: int):
        '''Set the playback volume for future plays.'''
        self.volume = level / 10.0
        await ctx.respond(f"Volume set to {level}/10")

    async def play_next(self, ctx=None):
        if not self.playlist:
            self.is_playing = False
            return
        self.is_playing = True
        entry = self.playlist.pop(0)
        try:
            if entry.startswith('http://') or entry.startswith('https://'):
                # Stream directly from URL using yt-dlp
                ydl_opts = {
                    'format': 'bestaudio/best',
                    'quiet': True,
                    'no_warnings': True,
                    'default_search': 'auto',
                    'extract_flat': False,
                }
                logging.info(f"[API] Fetching audio stream for: {entry}")
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    info = ydl.extract_info(entry, download=False)
                    title = info.get('title', entry)
                    url = info['url']
                logging.info(f"[API] Audio stream ready: {title}")
                source = discord.FFmpegPCMAudio(url)
            else:
                title = entry
                source = discord.FFmpegPCMAudio(entry)
            
            source = discord.PCMVolumeTransformer(source, volume=self.volume)
            def after_playing(error):
                fut = self.bot.loop.create_task(self.play_next())
            self.vc.play(source, after=after_playing)
            if ctx:
                await ctx.respond(f"Now playing: {title}")
        except Exception as err:
            logging.error(f"[API] Error playing entry: {entry} | {err}")
            if ctx:
                await ctx.respond(f"Failed to play: {entry}")
            self.is_playing = False
            await self.play_next()

    async def _extract_playlist_videos(self, url: str) -> list:
        '''Extract all video URLs from a YouTube playlist'''
        ydl_opts = {
            'quiet': True,
            'no_warnings': True,
            'extract_flat': True,
            'force_generic_extractor': False
        }
        try:
            logging.info(f"[API] Extracting playlist videos: {url}")
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=False)
                if 'entries' in info:
                    logging.info(f"[API] Extracted {len(info['entries'])} videos from playlist.")
                    return [f"https://www.youtube.com/watch?v={entry['id']}" for entry in info['entries']]
                return [url]
        except Exception as e:
            logging.error(f"[API] Error extracting playlist: {e}")
            return [url]

    @discord.slash_command(name="addsong", description="Add a song (file path or URL) to the playlist", **default_params)
    @discord.option("song", description="File path or URL")
    async def addsong(self, ctx, song: str):
        logging.info(f"[USER] {ctx.author} used /addsong: {song}")
        if song.startswith('http://') or song.startswith('https://'):
            if 'youtube.com/playlist' in song or 'youtu.be/playlist' in song:
                await ctx.respond("Processing playlist...")
                logging.info(f"[API] Fetching YouTube playlist: {song}")
                videos = await self._extract_playlist_videos(song)
                self.playlist.extend(videos)
                await ctx.respond(f"Added {len(videos)} songs from the playlist!")
            else:
                self.playlist.append(song)
                await ctx.respond(f"Added to playlist: {song}")
        else:
            self.playlist.append(song)
            await ctx.respond(f"Added to playlist: {song}")
        
        if not self.is_playing and self._check_connected():
            await self.play_next(ctx)

    @discord.slash_command(name="playlist", description="Show the current playlist", **default_params)
    async def show_playlist(self, ctx):
        if not self.playlist:
            await ctx.respond("The playlist is empty.")
        else:
            msg = "\n".join(f"{i+1}. {s}" for i, s in enumerate(self.playlist))
            await ctx.respond(f"Current playlist:\n{msg}")

    @discord.slash_command(name="skip", description="Skip the current song", **default_params)
    async def skip(self, ctx):
        if self.vc and self.vc.is_playing():
            self.vc.stop()
            await ctx.respond("Skipped!")
        else:
            await ctx.respond("Nothing is playing.")

    @discord.slash_command(name="voice_status", description="Check voice connection status", **default_params)
    async def voice_status(self, ctx):
        """Check the current voice connection status"""
        try:
            status_msg = "🎤 **Voice Status:**\n\n"
            
            # Check if connected
            if self._check_connected():
                status_msg += f"✅ **Connected to:** {self.vc.channel.name}\n"
                status_msg += f"🔊 **Playing:** {'Yes' if self.vc.is_playing() else 'No'}\n"
                status_msg += f"📝 **Recording:** {'Yes' if self.recording else 'No'}\n"
                status_msg += f"🎵 **Playlist:** {len(self.playlist)} songs\n"
            else:
                status_msg += "❌ **Not connected to any voice channel**\n"
            
            # Check permissions
            if ctx.guild.me.guild_permissions.connect:
                status_msg += "✅ **Can connect to voice channels**\n"
            else:
                status_msg += "❌ **Cannot connect to voice channels**\n"
                
            if ctx.guild.me.guild_permissions.speak:
                status_msg += "✅ **Can speak in voice channels**\n"
            else:
                status_msg += "❌ **Cannot speak in voice channels**\n"
                
            if ctx.guild.me.guild_permissions.attach_files:
                status_msg += "✅ **Can attach files (for recordings)**\n"
            else:
                status_msg += "❌ **Cannot attach files**\n"
            
            await ctx.respond(status_msg)
            
        except Exception as e:
            logging.error(f"Error checking voice status: {e}")
            await ctx.respond(f"❌ Error checking voice status: {str(e)}")

def setup(bot: discord.Bot) -> None:
    bot.add_cog(MusicCog(bot))
        
        
