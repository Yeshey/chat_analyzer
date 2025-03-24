#!/usr/bin/env python3

import sys
import re
import matplotlib  # Import matplotlib first
matplotlib.use('Agg')  # Set the backend before importing pyplot
from collections import Counter
from datetime import datetime
import matplotlib.pyplot as plt
import pandas as pd
from dateutil.parser import parse as date_parse


def print_metrics(counters, metrics):
    """Print the main chat statistics metrics"""
    print("\nCHAT STATISTICS")
    print("="*40)
    print(f"| {'METRIC':<20} | {'JONNAS':<8} | {'VICTOR':<8} | {'TOTAL':<8} |")
    print("|----------------------|----------|----------|----------|")
    print(f"| {'Total Messages':<20} | {counters['messages']['Jonnas']:>8} | {counters['messages']['Victor']:>8} | {counters['messages']['Total']:>8} |")
    print(f"| {'Total Words':<20} | {counters['words']['Jonnas']:>8} | {counters['words']['Victor']:>8} | {counters['words']['Jonnas'] + counters['words']['Victor']:>8} |")
    print(f"| {'Words/Message':<20} | {metrics['words_per_message']['Jonnas']:>8} | {metrics['words_per_message']['Victor']:>8} | {metrics['words_per_message']['Total']:>8} |")

def print_emoji_metrics(counters):
    """Print emoji statistics using the counters"""
    def print_emojis(title, total_counter, messages_counter):
        """Helper function to print individual emoji tables"""
        print(f"\n{title}")
        print("-"*60)
        for rank, (emoji, total_count) in enumerate(total_counter.most_common(40), 1):
            message_count = messages_counter.get(emoji, 0)
            print(f"{rank:2}. {emoji} - {total_count:>6} times (in {message_count} separate messages)")

    print_emojis("TOP EMOJIS (BOTH)", counters['emojis']['Both']['total'], counters['emojis']['Both']['messages'])
    print_emojis("TOP EMOJIS (JONNAS)", counters['emojis']['Jonnas']['total'], counters['emojis']['Jonnas']['messages'])
    print_emojis("TOP EMOJIS (VICTOR)", counters['emojis']['Victor']['total'], counters['emojis']['Victor']['messages'])

def plot_message_timeline(counters):
    """Plot message frequency over time using matplotlib"""
    if not counters['dates']:
        print("No date data available for plotting")
        return
    
    # Create DataFrame from date records
    df = pd.DataFrame(counters['dates'], columns=['user', 'date'])
    df.set_index('date', inplace=True)
    
    # Resample to monthly frequency
    plt.figure(figsize=(14, 7))
    
    # Plot total messages
    df.resample('ME').size().plot(
        label='Total Messages', 
        color='#2c3e50',
        linewidth=2,
        marker='o'
    )
    
    # Plot individual users
    df[df['user'] == 'Jonnas'].resample('ME').size().plot(
        label='Jonnas', 
        color='#3498db',
        linestyle='--',
        alpha=0.8
    )
    
    df[df['user'] == 'Victor'].resample('ME').size().plot(
        label='Victor', 
        color='#e74c3c',
        linestyle='--',
        alpha=0.8
    )
    
    plt.title('Message Frequency Over Time', fontsize=14)
    plt.xlabel('Date', fontsize=12)
    plt.ylabel('Number of Messages', fontsize=12)
    plt.grid(True, alpha=0.3)
    plt.legend()
    plt.tight_layout()

    plt.show() # if this fails its fine, the image is also saved in current directory
    
    # Save the plot instead of showing it
    output_file = 'message_timeline.png'
    plt.savefig(output_file)
    print(f"\nPlot saved as {output_file}")

def process_chat_data(file_path):
    """Process WhatsApp chat data and return statistics counters"""
    message_pattern = re.compile(
        r'^(\[)?(\d{1,2}[\/\-\.]\d{1,2}[\/\-\.]\d{2,4}),?\s+\d{1,2}:\d{2}(?::\d{2})?(?:\s[AP]M)?(?(1)\])?\s+([^:]+):\s+'
    )

    emoji_pattern = re.compile(
        "["
        u"\U0001F600-\U0001F64F"  # Emoticons
        u"\U0001F300-\U0001F5FF"  # Symbols & pictographs
        u"\U0001F680-\U0001F6FF"  # Transport & map
        u"\U0001F1E0-\U0001F1FF"  # Flags
        u"\U00002500-\U00002BEF"  # Misc symbols
        u"\U00002702-\U000027B0"  # Dingbats
        u"\U000024C2-\U0001F251"  # Enclosed chars
        u"\U0001F900-\U0001F9FF"  # Supplemental symbols
        u"\U0001FA70-\U0001FAFF"  # Chess symbols
        "]+", 
        flags=re.UNICODE
    )

    def normalize_emojis(emojis):
        modifiers = [
            '\U0001F3FB', '\U0001F3FC', '\U0001F3FD', '\U0001F3FE', '\U0001F3FF',
            '\u2640', '\u2642', '\u200d', '\ufe0f'
        ]
        normalized = []
        for emoji in emojis:
            for mod in modifiers:
                emoji = emoji.replace(mod, '')
            for char in emoji:
                if char.strip() and emoji_pattern.match(char):
                    normalized.append(char)
        return normalized

    counters = {
        'messages': {'Victor': 0, 'Jonnas': 0, 'Total': 0},
        'words': {'Victor': 0, 'Jonnas': 0},
        'emojis': {
            'Victor': {'total': Counter(), 'messages': Counter()},
            'Jonnas': {'total': Counter(), 'messages': Counter()},
            'Both': {'total': Counter(), 'messages': Counter()}
        },
        'dates': []
    }

    with open(file_path, "r", encoding="utf-8") as file:
        for line in file:
            match = message_pattern.match(line)
            if not match:
                continue
            
            try:
                # Extract message metadata
                date_str = match.group(2).strip()
                user = match.group(3).strip().lower()
                message = line.split(': ', 2)[-1].strip()
                
                # Parse date
                date = date_parse(date_str, dayfirst=True)
                
                # Determine user
                if 'victor' in user:
                    user_key = 'Victor'
                elif 'jonnas' in user or 'jonas' in user:
                    user_key = 'Jonnas'
                else:
                    continue
                
                # Update counters
                counters['messages'][user_key] += 1
                counters['messages']['Total'] += 1
                counters['words'][user_key] += len(message.split()) if message else 0
                counters['dates'].append((user_key, date))
                
                # Process emojis
                found_emojis = emoji_pattern.findall(message)
                cleaned_emojis = normalize_emojis(found_emojis)
                unique_emojis = set(cleaned_emojis)

                counters['emojis'][user_key]['total'].update(cleaned_emojis)
                counters['emojis'][user_key]['messages'].update(unique_emojis)
                counters['emojis']['Both']['total'].update(cleaned_emojis)
                counters['emojis']['Both']['messages'].update(unique_emojis)
                
            except Exception as e:
                continue

    return counters

def calculate_metrics(counters):
    """Calculate derived metrics from raw counters"""
    def safe_divide(a, b):
        return round(a/b, 2) if b > 0 else 0.0

    return {
        'words_per_message': {
            'Victor': safe_divide(counters['words']['Victor'], counters['messages']['Victor']),
            'Jonnas': safe_divide(counters['words']['Jonnas'], counters['messages']['Jonnas']),
            'Total': safe_divide(
                counters['words']['Victor'] + counters['words']['Jonnas'],
                counters['messages']['Total']
            )
        }
    }

def main():
    if len(sys.argv) < 2:
        print("Usage: python chat_analyzer.py <chat_file>")
        sys.exit(1)

    CHAT_FILE_PATH = sys.argv[1]
    
    # Process data
    counters = process_chat_data(CHAT_FILE_PATH)
    metrics = calculate_metrics(counters)
    
    # Print text reports
    print_metrics(counters, metrics)
    print_emoji_metrics(counters)
    
    # Show timeline plot
    plot_message_timeline(counters)
    
    # Debug info
    print("\nDEBUG INFO:")
    if counters['dates']:
        print(f"Processed {len(counters['dates'])} messages with date information")
        print(f"Date range: {counters['dates'][0][1].date()} to {counters['dates'][-1][1].date()}")
    else:
        print("No date data found")
    print(f"Victor/Jonnas ratio: {counters['messages']['Victor']}/{counters['messages']['Jonnas']}")

if __name__ == "__main__":
    main()