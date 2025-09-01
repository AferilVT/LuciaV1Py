#!/usr/bin/env python3
"""
Voice Diagnostic Script for Lucia
"""

import discord
import asyncio
import logging
import os
from dotenv import load_dotenv

# Set up logging
logging.basicConfig(level=logging.DEBUG)

class VoiceDiagnosticBot(discord.Bot):
    def __init__(self):
        intents = discord.Intents.default()
        intents.message_content = True
        intents.voice_states = True
        intents.guilds = True
        super().__init__(intents=intents)

    async def on_ready(self):
        print(f"🔧 Voice Diagnostic Bot Ready: {self.user}")
        print("=" * 50)
        print("DIAGNOSTIC COMMANDS:")
        print("/test_voice - Test basic voice connection")
        print("/check_permissions - Check bot permissions")
        print("/voice_status - Check voice client status")
        print("=" * 50)

    @discord.slash_command(name="test_voice", description="Test voice connection")
    async def test_voice(self, ctx, channel: discord.VoiceChannel):
        """Test basic voice connection"""
        try:
            await ctx.respond("🔧 Testing voice connection...")
            
            # Check permissions
            permissions = channel.permissions_for(ctx.guild.me)
            await ctx.followup.send(f"📋 **Permission Check:**\n"
                                  f"Connect: {'✅' if permissions.connect else '❌'}\n"
                                  f"Speak: {'✅' if permissions.speak else '❌'}\n"
                                  f"View Channel: {'✅' if permissions.view_channel else '❌'}")
            
            if not permissions.connect:
                await ctx.followup.send("❌ **Missing Connect Permission!**")
                return
            
            # Try to connect
            try:
                voice_client = await channel.connect()
                await ctx.followup.send(f"✅ **Successfully connected to {channel.name}!**")
                
                # Test recording
                try:
                    sink = discord.sinks.MP3Sink()
                    voice_client.start_recording(sink, self._test_recording_callback, ctx)
                    await ctx.followup.send("🎤 **Recording test started!** (Will stop in 5 seconds)")
                    
                    # Stop recording after 5 seconds
                    await asyncio.sleep(5)
                    voice_client.stop_recording()
                    
                except Exception as e:
                    await ctx.followup.send(f"❌ **Recording test failed:** {e}")
                
                # Disconnect
                await voice_client.disconnect()
                await ctx.followup.send("✅ **Voice test completed successfully!**")
                
            except Exception as e:
                await ctx.followup.send(f"❌ **Connection failed:** {e}")
                
        except Exception as e:
            await ctx.followup.send(f"❌ **Test failed:** {e}")

    async def _test_recording_callback(self, sink, ctx):
        """Test recording callback"""
        try:
            await ctx.followup.send("🎤 **Recording test completed!**")
        except Exception as e:
            await ctx.followup.send(f"❌ **Recording callback error:** {e}")

    @discord.slash_command(name="check_permissions", description="Check bot permissions")
    async def check_permissions(self, ctx):
        """Check bot permissions in the server"""
        try:
            await ctx.respond("🔧 Checking bot permissions...")
            
            guild = ctx.guild
            bot_member = guild.me
            
            permissions = bot_member.guild_permissions
            
            perm_list = [
                ("Connect", permissions.connect),
                ("Speak", permissions.speak),
                ("Use Voice Activity", permissions.use_voice_activity),
                ("View Channels", permissions.view_channel),
                ("Send Messages", permissions.send_messages),
                ("Attach Files", permissions.attach_files),
                ("Use Slash Commands", permissions.use_slash_commands)
            ]
            
            status_msg = "📋 **Bot Permissions:**\n"
            for perm_name, has_perm in perm_list:
                status_msg += f"{perm_name}: {'✅' if has_perm else '❌'}\n"
            
            await ctx.followup.send(status_msg)
            
        except Exception as e:
            await ctx.followup.send(f"❌ **Permission check failed:** {e}")

    @discord.slash_command(name="voice_status", description="Check voice client status")
    async def voice_status(self, ctx):
        """Check current voice client status"""
        try:
            await ctx.respond("🔧 Checking voice status...")
            
            voice_client = ctx.guild.voice_client
            
            if voice_client:
                status_msg = f"🎤 **Voice Client Status:**\n"
                status_msg += f"Connected: {'✅' if voice_client.is_connected() else '❌'}\n"
                status_msg += f"Channel: {voice_client.channel.name if voice_client.channel else 'None'}\n"
                status_msg += f"Playing: {'✅' if voice_client.is_playing() else '❌'}\n"
                status_msg += f"Recording: {'✅' if voice_client.recording else '❌'}\n"
            else:
                status_msg = "🎤 **Voice Client Status:** Not connected"
            
            await ctx.followup.send(status_msg)
            
        except Exception as e:
            await ctx.followup.send(f"❌ **Status check failed:** {e}")

async def main():
    load_dotenv()
    token = os.getenv('TOKEN')
    
    if not token:
        print("❌ No token found in .env file!")
        return
    
    bot = VoiceDiagnosticBot()
    await bot.start(token)

if __name__ == "__main__":
    asyncio.run(main()) 