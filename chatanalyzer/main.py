#!/usr/bin/env python3

import sys
import re
import matplotlib
matplotlib.use('Agg')
from collections import defaultdict, Counter
from datetime import datetime
import matplotlib.pyplot as plt
import pandas as pd
from dateutil.parser import parse as date_parse

def print_metrics(counters, metrics):
    """Print the main chat statistics metrics with dynamic user names"""
    users = [u for u in counters['messages'] if u != 'Total']
    header = f"| {'METRIC':<20} | " + " | ".join([f"{u.upper():<8}" for u in users]) + " | {'TOTAL':<8} |"
    separator = "|----------------------|" + "|".join(["-"*10 for _ in users]) + "|----------|"
    
    print("\nCHAT STATISTICS")
    print("=" * len(header))
    print(header)
    print(separator)
    
    # Total Messages
    msg_line = f"| {'Total Messages':<20} | " + " | ".join([f"{counters['messages'][u]:>8}" for u in users]) + f" | {counters['messages']['Total']:>8} |"
    print(msg_line)
    
    # Total Words
    words_line = f"| {'Total Words':<20} | " + " | ".join([f"{counters['words'][u]:>8}" for u in users]) + f" | {sum(counters['words'].values()):>8} |"
    print(words_line)
    
    # Words per Message
    wpm_line = f"| {'Words/Message':<20} | " + " | ".join([f"{metrics['words_per_message'][u]:>8.2f}" for u in users]) + f" | {metrics['words_per_message']['Total']:>8.2f} |"
    print(wpm_line)

def print_emoji_metrics(counters):
    """Print emoji statistics with dynamic user names"""
    def print_emojis(title, total_counter, messages_counter):
        print(f"\n{title}")
        print("-"*60)
        for rank, (emoji, total_count) in enumerate(total_counter.most_common(40), 1):
            message_count = messages_counter.get(emoji, 0)
            print(f"{rank:2}. {emoji} - {total_count:>6} times (in {message_count} messages)")

    users = [u for u in counters['emojis'] if u != 'Both']
    print_emojis("TOP EMOJIS (BOTH)", counters['emojis']['Both']['total'], counters['emojis']['Both']['messages'])
    for user in users:
        print_emojis(f"TOP EMOJIS ({user.upper()})", counters['emojis'][user]['total'], counters['emojis'][user]['messages'])

def plot_message_timeline(counters):
    """Plot message frequency over time with dynamic users"""
    if not counters['dates']:
        print("No date data available for plotting")
        return

    df = pd.DataFrame(counters['dates'], columns=['user', 'date'])
    df.set_index('date', inplace=True)
    
    plt.figure(figsize=(14, 7))
    users = list(set(u for u, _ in counters['dates']))
    
    # Plot total messages
    total = df.resample('ME').size()
    if not total.empty:
        total.plot(label='Total Messages', color='#2c3e50', linewidth=2, marker='o')
    
    # Plot individual users
    colors = ['#3498db', '#e74c3c', '#2ecc71', '#9b59b6'][:len(users)]
    for user, color in zip(users, colors):
        user_data = df[df['user'] == user].resample('ME').size()
        if not user_data.empty:
            user_data.plot(label=user, color=color, linestyle='--', alpha=0.8)
    
    if not df.empty:
        plt.title('Message Frequency Over Time', fontsize=14)
        plt.xlabel('Date', fontsize=12)
        plt.ylabel('Number of Messages', fontsize=12)
        plt.grid(True, alpha=0.3)
        plt.legend()
        plt.tight_layout()
        output_file = 'message_timeline.png'
        plt.savefig(output_file)
        print(f"\nPlot saved as {output_file}")
    else:
        print("No valid data for plotting timeline")

def process_chat_data(file_path):
    """Process WhatsApp chat data with dynamic user detection"""
    message_pattern = re.compile(
        r'^(\d{1,2}[\/\-\.]\d{1,2}[\/\-\.]\d{2,4},?\s+\d{1,2}:\d{2}(?::\d{2})?(?:\s[APap][Mm])?)\s+-\s+([^:]+):\s+(.+)'
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
        "]+", flags=re.UNICODE
    )

    def normalize_emojis(emojis):
        modifiers = [
            '\U0001F3FB', '\U0001F3FC', '\U0001F3FD', '\U0001F3FE', '\U0001F3FF',
            '\u2640', '\u2642', '\u200d', '\ufe0f'
        ]
        return [char for emoji in emojis for char in emoji if char not in modifiers]

    counters = {
        'messages': defaultdict(int),
        'words': defaultdict(int),
        'emojis': defaultdict(lambda: {'total': Counter(), 'messages': Counter()}),
        'dates': []
    }

    with open(file_path, "r", encoding="utf-8") as file:
        for line in file:
            match = message_pattern.match(line)
            if not match:
                continue

            try:
                date_str, user, message = match.groups()
                user = user.strip().title()
                
                # Skip system messages
                if user.lower() in ['system', 'whatsapp'] or 'changed' in user.lower():
                    continue

                date = date_parse(date_str, dayfirst=True)
                
                # Update counters
                counters['messages'][user] += 1
                counters['messages']['Total'] += 1
                counters['words'][user] += len(message.split())
                counters['dates'].append((user, date))
                
                # Process emojis
                found_emojis = emoji_pattern.findall(message)
                cleaned_emojis = normalize_emojis(found_emojis)
                unique_emojis = set(cleaned_emojis)

                counters['emojis'][user]['total'].update(cleaned_emojis)
                counters['emojis'][user]['messages'].update(unique_emojis)
                counters['emojis']['Both']['total'].update(cleaned_emojis)
                counters['emojis']['Both']['messages'].update(unique_emojis)

            except Exception as e:
                continue

    return counters

def calculate_metrics(counters):
    """Calculate metrics with dynamic users"""
    def safe_divide(a, b):
        return a / b if b > 0 else 0.0

    users = [u for u in counters['messages'] if u != 'Total']
    metrics = {'words_per_message': {'Total': 0.0}}
    total_words = sum(counters['words'].values())
    
    for user in users:
        metrics['words_per_message'][user] = safe_divide(
            counters['words'][user], counters['messages'][user]
        )
    
    metrics['words_per_message']['Total'] = safe_divide(
        total_words, counters['messages']['Total']
    )

    return metrics

def main():
    if len(sys.argv) < 2:
        print("Usage: python chat_analyzer.py <chat_file>")
        sys.exit(1)

    CHAT_FILE_PATH = sys.argv[1]
    counters = process_chat_data(CHAT_FILE_PATH)
    metrics = calculate_metrics(counters)
    
    print_metrics(counters, metrics)
    print_emoji_metrics(counters)
    plot_message_timeline(counters)
    
    # Debug info
    print("\nDEBUG INFO:")
    if counters['dates']:
        print(f"Processed {len(counters['dates'])} messages")
        start = min(d for _, d in counters['dates']).strftime('%Y-%m-%d')
        end = max(d for _, d in counters['dates']).strftime('%Y-%m-%d')
        print(f"Date range: {start} to {end}")
    else:
        print("No valid messages found")
        
    print("User distribution:")
    for user, count in sorted(counters['messages'].items()):
        if user != 'Total':
            print(f"- {user}: {count} messages")

if __name__ == "__main__":
    main()