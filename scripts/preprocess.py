import pandas as pd
import os
import logging
import emoji
import re

class cleaning:
    #df=pd.read_csv('./telegram_data.csv')
    def __init__(self):
        # Ensure logs folder exists
        os.makedirs("../logs", exist_ok=True)

        # Configure logging
        logging.basicConfig(
            level=logging.INFO,
            format="%(asctime)s - %(levelname)s - %(message)s",
            handlers=[
                logging.FileHandler("../logs/data_cleaning.log"),
                logging.StreamHandler()
            ]
        )
    
    def load_csv(self,file_path):
        """ Load CSV file into a Pandas DataFrame. """
        try:
            df = pd.read_csv(file_path)
            logging.info(f"✅ CSV file '{file_path}' loaded successfully.")
            return df
        except Exception as e:
            logging.error(f"❌ Error loading CSV file: {e}")
            raise
    def extract_emojis(self,text):
        """ Extract emojis from text, return 'No emoji' if none found. """
        emojis = ''.join(c for c in text if c in emoji.EMOJI_DATA)
        return emojis if emojis else "No emoji"

    def remove_emojis(self,text):
        """ Remove emojis from the message text. """
        return ''.join(c for c in text if c not in emoji.EMOJI_DATA)

    def extract_youtube_links(self,text):
        """ Extract YouTube links from text, return 'No YouTube link' if none found. """
        youtube_pattern = r"(https?://(?:www\.)?(?:youtube\.com|youtu\.be)/[^\s]+)"
        links = re.findall(youtube_pattern, text)
        return ', '.join(links) if links else "No YouTube link"

    def remove_youtube_links(self,text):
        """ Remove YouTube links from the message text. """
        youtube_pattern = r"https?://(?:www\.)?(?:youtube\.com|youtu\.be)/[^\s]+"
        return re.sub(youtube_pattern, '', text).strip()

    def clean_text(self,text):
        """ Standardize text by removing newline characters and unnecessary spaces. """
        if pd.isna(text):
            return "No Message"
        return re.sub(r'\n+', ' ', text).strip()

    def preprocess(self,df,output_file):
    
        try:
            df = df.drop_duplicates(subset=["ID"]).copy()  # Ensure a new copy
            logging.info("✅ Duplicates removed from dataset.")

            # ✅ Convert Date to datetime format, replacing NaT with None
            df.loc[:, 'Date'] = pd.to_datetime(df['Date'], errors='coerce')
            df.loc[:, 'Date'] = df['Date'].where(df['Date'].notna(), None)
            logging.info("✅ Date column formatted to datetime.")

            # ✅ Convert 'ID' to integer for PostgreSQL BIGINT compatibility
            df.loc[:, 'ID'] = pd.to_numeric(df['ID'], errors="coerce").fillna(0).astype(int)

            # ✅ Fill missing values
            df.loc[:, 'Message'] = df['Message'].fillna("No Message")
            df.loc[:, 'Media Path'] = df['Media Path'].fillna("No Media")
            logging.info("✅ Missing values filled.")

            # ✅ Standardize text columns
            df.loc[:, 'Channel Title'] = df['Channel Title'].str.strip()
            df.loc[:, 'Channel Username'] = df['Channel Username'].str.strip()
            df.loc[:, 'Message'] = df['Message'].apply(self.clean_text)
            df.loc[:, 'Media Path'] = df['Media Path'].str.strip()
            logging.info("✅ Text columns standardized.")

            # ✅ Extract emojis and store them in a new column
            df.loc[:, 'emoji_used'] = df['Message'].apply(self.extract_emojis)
            logging.info("✅ Emojis extracted and stored in 'emoji_used' column.")
            
            # ✅ Remove emojis from message text
            df.loc[:, 'Message'] = df['Message'].apply(self.remove_emojis)

            # ✅ Extract YouTube links into a separate column
            df.loc[:, 'youtube_links'] = df['Message'].apply(self.extract_youtube_links)
            logging.info("✅ YouTube links extracted and stored in 'youtube_links' column.")

            # ✅ Remove YouTube links from message text
            df.loc[:, 'Message'] = df['Message'].apply(self.remove_youtube_links)

            # ✅ Rename columns to match PostgreSQL schema
            df = df.rename(columns={
                "Channel Title": "channel_title",
                "Channel Username": "channel_username",
                "ID": "message_id",
                "Message": "message",
                "Date": "message_date",
                "Media Path": "media_path",
                "emoji_used": "emoji_used",
                "youtube_links": "youtube_links"
            })

            logging.info("✅ Data cleaning completed successfully.")
            df=df.reset_index()
            df=df.drop(columns='index')
            df.to_csv(output_file,index=False)
            return df
        except Exception as e:
            logging.error(f"❌ Data cleaning error: {e}")
            raise
    #preprocess(df)