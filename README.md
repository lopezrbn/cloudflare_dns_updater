
# Cloudflare DNS Updater

This script automatically updates your Cloudflare DNS records with your current public IP address. It's particularly useful for users with a dynamic IP address who want to ensure that their domain points to the correct IP.

## Features

- **Automatic IP detection**: The script detects your current public IP address.
- **Cloudflare DNS update**: It updates the DNS records for the specified domains in your Cloudflare account.
- **Logging**: Changes are logged with timestamps in a single log file (`update.log`).
- **Efficient**: It only updates the DNS records if the IP address has changed.

## Setup

### 1. Clone the repository

First, clone the repository to your local machine or server:

```bash
git clone https://github.com/lopezrbn/cloudflare_dns_updater.git
cd cloudflare_dns_updater
```

### 2. Create the `config.json` file

**Important**: The `config.json` file, which contains sensitive information such as your Cloudflare API token and zone ID, is not included in the repository for security reasons. You need to create this file yourself.

Copy the provided `config_example.json` and rename it to `config.json`:

```bash
cp config_example.json config.json
```

Then, edit the `config.json` file with your Cloudflare API token, zone ID, and domains. Example structure:

```json
{
  "CLOUDFLARE_API_TOKEN": "your-cloudflare-api-token",
  "ZONE_ID": "your-cloudflare-zone-id",
  "DOMINIOS": {
    "your-domain.com": {
      "proxied": false
    },
    "app1.your-domain.com": {
      "proxied": true
    }
  }
}
```

### 3. Obtain Cloudflare API Token and Zone ID

To use this script, you'll need a Cloudflare API token and your Cloudflare zone ID. Here's how to get them:

#### Cloudflare API Token:

1. Go to the [Cloudflare dashboard](https://dash.cloudflare.com/).
2. In the left sidebar, click on **"My Profile"**.
3. Under **API Tokens**, click **"Create Token"**.
4. Use the **"Edit zone DNS"** template or create a custom token with permissions to edit DNS records.
5. Copy the token generated and paste it into the `CLOUDFLARE_API_TOKEN` field in the `config.json` file.

#### Cloudflare Zone ID:

1. Go to the [Cloudflare dashboard](https://dash.cloudflare.com/).
2. Select the website/domain for which you want to update the DNS.
3. In the **Overview** section, find your **Zone ID**.
4. Copy the Zone ID and paste it into the `ZONE_ID` field in the `config.json` file.

### 4. Install dependencies

This script requires the `requests` library to make HTTP requests to the Cloudflare API. Install it using the requirements.txt file:

```bash
pip install -r requirements.txt
```

### 5. Running the script

To run the script manually, simply execute:

```bash
python3 main.py
```

The script will check your current public IP and update your DNS records in Cloudflare if the IP has changed. Logs will be written to `update.log`.

### 6. Automate with Cron (Optional)

To automate the script to run at regular intervals, you can use **cron**. For example, to run the script every 5 minutes, open your crontab configuration:

```bash
crontab -e
```

Then, add the following line to run the script:

```bash
*/5 * * * * /usr/bin/python3 /path/to/cloudflare_dns_updater/main.py
```

This will execute the script every 5 minutes.

## Security Note

For security reasons, the `config.json` file, which contains your Cloudflare API token and other sensitive information, is not included in the repository. You must create this file yourself by copying the example `config_example.json` and filling in the necessary details.

## Log File

- All changes (IP updates) are logged in the `update.log` file.
- Each entry in the log contains a timestamp and a summary of the change.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
