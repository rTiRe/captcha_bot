import re
import emoji

def count_emojis(text):
    # Используем emoji.emoji_list для поиска всех эмодзи
    return emoji.distinct_emoji_list(text)

# Пример использования
text = "Привет! 👋🏼👋🏼"
emoji_count = count_emojis(text)
print(f"Количество эмодзи в строке: {emoji_count}")