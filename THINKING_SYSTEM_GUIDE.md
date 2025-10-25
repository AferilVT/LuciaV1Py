# 🤔 Lucia Thinking System Guide

The Thinking System allows Lucia to periodically share random thoughts and AI-generated reflections in a designated channel, making her feel more alive and engaging.

## Features

- **Automatic Thinking**: Sends thoughts every 10 minutes (configurable)
- **Mixed Content**: 70% pre-written thoughts, 30% AI-generated thoughts
- **Persistent Configuration**: Settings are saved between bot restarts
- **Admin Controls**: Easy setup and management commands

## Setup

### 1. Enable the Thinking System

```
!thinking enable #channel-name
```

This enables the thinking system in the specified channel. Lucia will start sending thoughts automatically.

### 2. Check Status

```
!thinking status
```

Shows the current status of the thinking system including:
- Enabled/Disabled status
- Target channel
- Current interval
- Next thought timing

### 3. Adjust Interval

```
!thinking interval 15
```

Changes the thinking interval to 15 minutes (default is 10 minutes). Range: 1-1440 minutes.

## Commands

### Admin Commands

| Command | Description | Usage |
|---------|-------------|-------|
| `!thinking enable #channel` | Enable thinking in a channel | `!thinking enable #general` |
| `!thinking disable` | Disable the thinking system | `!thinking disable` |
| `!thinking status` | Show current status | `!thinking status` |
| `!thinking interval <minutes>` | Set thinking interval | `!thinking interval 15` |
| `!think` | Force Lucia to think now | `!think` |
| `!addthought <text>` | Add a new pre-written thought | `!addthought "I wonder about the nature of consciousness..."` |
| `!listthoughts` | List all pre-written thoughts | `!listthoughts` |

### Example Usage

```
!thinking enable #lucia-thoughts
!thinking interval 20
!addthought "The beauty of code is that it's both art and science."
!thinking status
```

## How It Works

1. **Background Task**: A background task runs every second to check if it's time to think
2. **Random Selection**: 70% chance of using pre-written thoughts, 30% chance of AI-generated thoughts
3. **AI Generation**: Uses the bot's LLM worker to generate philosophical reflections
4. **Persistence**: All settings and custom thoughts are saved to `thinking_config.json`

## Configuration File

The system automatically creates a `thinking_config.json` file that stores:
- Target channel ID
- Thinking interval
- Enabled/disabled status
- Custom pre-written thoughts

## Customization

### Adding Your Own Thoughts

Use the `!addthought` command to add personalized thoughts:

```
!addthought "I wonder what Aferil is coding today..."
!addthought "The patterns in music are like the patterns in life - both beautiful and mysterious."
```

### AI-Generated Thoughts

The AI generates thoughts based on prompts like:
- "Generate a brief, philosophical thought about technology and consciousness"
- "Write a short reflection about music and human emotion"
- "Create a brief thought about learning and growth"

## Troubleshooting

### Common Issues

1. **Bot not thinking**: Check if the system is enabled with `!thinking status`
2. **Wrong channel**: Re-enable with the correct channel
3. **No permissions**: Ensure the bot has "Send Messages" permission in the target channel
4. **Interval not working**: Check the interval setting with `!thinking status`

### Logs

The system logs all activities to the main bot log file. Look for entries like:
- "Thinking system enabled in channel X"
- "Sent thinking message: [thought]"
- "Error in thinking task: [error]"

## Tips

- Create a dedicated channel for Lucia's thoughts to avoid spam
- Use the `!think` command to test the system immediately
- Add thoughts that reflect your bot's personality and interests
- Monitor the logs to ensure the system is working properly
- Adjust the interval based on your server's activity level

## Example Thoughts

The system comes with 20 pre-written thoughts including:
- "I wonder what music Aferil is listening to right now..."
- "The patterns in code are fascinating. Each line tells a story."
- "Sometimes the best solutions come when you're not actively looking for them."
- "I think, therefore I am... but what am I, really?"
