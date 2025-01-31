from telethon import TelegramClient, events
import os
import csv
import logging
from dotenv import load_dotenv

# Load environment variables
load_dotenv('.env')
api_id = os.getenv('API_ID')
api_hash = os.getenv('API_HASH')

# Set up logging
log_file = "scraper.log"
logging.basicConfig(
    filename=log_file,
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger()

# Directory for media files
media_dir = 'photos_'
os.makedirs(media_dir, exist_ok=True)

# Initialize Telegram client
client = TelegramClient('scraping_session', api_id, api_hash)

# Function to save messages to CSV
def save_message_to_csv(writer, channel_title, channel_username, message, media_path=None):
    try:
        writer.writerow([
            channel_title,
            channel_username,
            message.id,
            message.message,
            message.date,
            media_path
        ])
        logger.info(f"Saved message {message.id} from {channel_username}")
    except Exception as e:
        logger.error(f"Error saving message {message.id} from {channel_username}: {e}")

# Function to scrape past data from a single channel
async def scrape_channel(client, channel_username, writer, media_dir):
    try:
        entity = await client.get_entity(channel_username)
        channel_title = entity.title  # Extract the channel's title
        logger.info(f"Scraping past messages from {channel_username}")

        async for message in client.iter_messages(entity, limit=10000):
            media_path = None
            if message.media and hasattr(message.media, 'photo'):
                # Create a unique filename for the photo
                filename = f"{channel_username}_{message.id}.jpg"
                media_path = os.path.join(media_dir, filename)
                await client.download_media(message.media, media_path)
            
            # Save message to CSV
            save_message_to_csv(writer, channel_title, channel_username, message, media_path)
        
        logger.info(f"Completed scraping {channel_username}")
    except Exception as e:
        logger.error(f"Error scraping {channel_username}: {e}")

# Function to handle real-time message ingestion
@client.on(events.NewMessage(chats=['@meneshayeofficial']))
async def handle_new_message(event):
    try:
        channel = await event.get_chat()
        channel_title = channel.title
        channel_username = f"@{channel.username}" if channel.username else "Unknown"

        # Prepare the media path
        media_path = None
        if event.message.media and hasattr(event.message.media, 'photo'):
            filename = f"{channel_username}_{event.message.id}.jpg"
            media_path = os.path.join(media_dir, filename)
            await client.download_media(event.message.media, media_path)

        # Open the CSV in append mode to save real-time data
        with open('telegram_datas.csv', 'a', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            save_message_to_csv(writer, channel_title, channel_username, event.message, media_path)
        
        logger.info(f"New message saved from {channel_username}: {event.message.text[:50]}...")  # Log first 50 chars
    except Exception as e:
        logger.error(f"Error handling new message from {channel_username}: {e}")

# Main function
async def main():
    try:
        await client.start()
        
        # Open the CSV file and prepare the writer for initial data scraping
        with open('telegram_data.csv', 'w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(['Channel Title', 'Channel Username', 'ID', 'Message', 'Date', 'Media Path'])  # Header
            
            # List of channels to scrape
            channels = [
                '@DoctorsET',
                '@CheMed123',
                '@lobelia4cosmetics',
                '@yetenaweg',
                '@EAHCI'
            ]
            
            # Scrape past data from each channel
            for channel in channels:
                await scrape_channel(client, channel, writer, media_dir)
                logger.info(f"Scraped past data from {channel}")

        logger.info("Real-time ingestion has started. Listening for new messages...")
    except Exception as e:
        logger.error(f"Error in main function: {e}")

# Run the client with error handling
try:
    with client:
        client.loop.run_until_complete(main())
except Exception as e:
    logger.critical(f"Critical error: {e}")


