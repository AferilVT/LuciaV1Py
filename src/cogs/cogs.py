def setup_cogs(bot):
    cogs_list = [
        'music',
        'reboot',
        'example',
        'speech_to_text',
        'simple_voice',
        'rvc_voice_enhanced',
        'voice_interaction',
    ]

    for cog in cogs_list:
        bot.load_extension(f"cogs.{cog}")
