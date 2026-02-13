# WordClock 2024 (Home Assistant Integration)

Custom integration for AWSW WordClock 2024.

## Features

- RGB control for Time text
- RGB control for Background
- Global brightness control
- 12 synchronized Extra Word switches
- Reset buttons (midnight reset, reactivate, refresh)
- Availability detection
- Polling via DataUpdateCoordinator
- Fully UI-configurable
- HACS ready

## Installation (HACS)

1. Go to HACS → Integrations → Custom repositories
2. Add your GitHub repo URL
3. Select category: Integration
4. Install “WordClock 2024”
5. Restart Home Assistant
6. Add Integration via Settings → Devices & Services

## Installation (Manual)

Copy:

```
custom_components/wordclock
```

into:

```
/config/custom_components/
```

Restart Home Assistant.

## Configuration

When adding the integration:

- Host (IP of WordClock)
- Port (default 2023)
- Scan interval (recommended: 10 seconds)

## Entities Created

### Lights
- WordClock Color Time
- WordClock Color Background

 max power to LED is software limited to 50% (100% on slider = 50% brightness)

### Switches
- EW1 – EW12

### Buttons
- Reset Extra Words Until Midnight
- Reactivate Extra Words
- Refresh Status

## API Used

Uses native WordClock HTTP API:

- `/status`
- `/config`
- `/ew`
- `/resetew1`
- `/resetew0`

## License

MIT
