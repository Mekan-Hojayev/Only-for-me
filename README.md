# Server Configuration Manager

This repository automatically fetches and validates server configurations on a daily basis. It maintains both current and archived server lists, with connectivity validation.

## Features

- Daily automatic server list updates at midnight UTC
- Server connectivity validation
- Historical data storage in SQLite database
- Archived configuration files with timestamps

## Setup

1. Clone the repository:
```bash
git clone https://github.com/yourusername/server-config-manager
```

2. Install dependencies:
```bash

pip install -r requirements.txt
```

3. Configure environment variables: Create a .env file with:

```
SUBSCRIPTION_URL=your_subscription_url
```