import streamlit as st
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from langdetect import detect
from googletrans import Translator

# Initialize VADER sentiment analyzer
analyzer = SentimentIntensityAnalyzer()
translator = Translator()

def detect_language(text):
    try:
        return detect(text)
    except:
        return "en"  # Default to English if detection fails

def translate_to_english(text, src_lang):
    if src_lang != 'en':
        try:
            return translator.translate(text, src=src_lang, dest='en').text
        except:
            st.warning("Translation failed. Proceeding with original text.")
            return text
    return text

def analyze_sentiment(text):
    return analyzer.polarity_scores(text)

def interpret_sentiment(compound):
    if compound >= 0.05:
        return "Positive"
    elif compound <= -0.05:
        return "Negative"
    else:
        return "Neutral"

def get_emoji(sentiment):
    if sentiment == "Positive":
        return "😊"
    elif sentiment == "Negative":
        return "😔"
    else:
        return "😐"

def get_sentiment_description(sentiment):
    if sentiment['compound'] >= 0.5:
        return "Very Positive", "The text expresses strong positive emotions or opinions. It might include words of high praise, excitement, or strong agreement."
    elif 0.5 > sentiment['compound'] >= 0.05:
        return "Somewhat Positive", "The text leans towards positivity. It may express mild approval, satisfaction, or general optimism."
    elif 0.05 > sentiment['compound'] > -0.05:
        return "Neutral", "The text doesn't show a clear positive or negative bias. It might be stating facts, or balancing positive and negative aspects."
    elif -0.05 >= sentiment['compound'] > -0.5:
        return "Somewhat Negative", "The text leans towards negativity. It may express mild disapproval, dissatisfaction, or general pessimism."
    else:
        return "Very Negative", "The text expresses strong negative emotions or opinions. It might include words of criticism, disappointment, or strong disagreement."

def main():
    st.title("Multilingual Text Mood Analyzer")
    st.write("Discover the emotional tone of your text in any language!")

    text = st.text_area("Enter your text here:", height=150)

    if st.button("Analyze Mood"):
        if text:
            # Detect language
            detected_lang = detect_language(text)
            st.write(f"Detected language: {detected_lang}")

            # Translate to English if necessary
            english_text = translate_to_english(text, detected_lang)
            
            if detected_lang != 'en':
                st.write("Translated text (for analysis):")
                st.write(english_text)

            # Analyze sentiment
            sentiment = analyze_sentiment(english_text)
            overall = interpret_sentiment(sentiment['compound'])
            emoji = get_emoji(overall)
            mood, description = get_sentiment_description(sentiment)

            st.subheader(f"Overall Mood: {mood} {emoji}")
            st.write(f"**What this means:** {description}")

            st.write("#### Breaking it down further:")
            
            # Explaining the balance of sentiments
            positive_ratio = sentiment['pos'] / (sentiment['pos'] + sentiment['neg'] + 0.0001)
            if positive_ratio > 0.8:
                st.write("👍 The text is overwhelmingly positive.")
            elif positive_ratio > 0.6:
                st.write("👍 The text contains significantly more positive elements than negative ones.")
            elif positive_ratio > 0.4:
                st.write("⚖️ The text has a fairly balanced mix of positive and negative elements, with a slight positive edge.")
            elif positive_ratio > 0.2:
                st.write("👎 The text contains more negative elements than positive ones.")
            else:
                st.write("👎 The text is overwhelmingly negative.")

            # Explaining the strength of the sentiment
            strength = abs(sentiment['compound'])
            if strength > 0.75:
                st.write("💪 The emotional tone of this text is very strong.")
            elif strength > 0.5:
                st.write("🏋️ The text has a clear and noticeable emotional tone.")
            elif strength > 0.25:
                st.write("🤔 The emotional tone is present but moderate.")
            else:
                st.write("😐 The emotional tone is quite subtle or mixed.")

            st.write("#### Key takeaway:")
            if overall == "Positive":
                st.write("This text gives off good vibes! The writer seems to be expressing something favorable or feeling upbeat.")
            elif overall == "Negative":
                st.write("This text gives off not-so-good vibes. The writer might be expressing concerns, criticisms, or feeling down.")
            else:
                st.write("This text doesn't lean strongly positive or negative. The writer might be trying to be objective or is expressing mixed feelings.")

        else:
            st.warning("Please enter some text to analyze.")

    st.write("#### How it works")
    st.write("This app uses smart technology to understand the mood of your text in any language. It first detects the language, translates it to English if necessary, and then analyzes the emotional tone. It's like having a multilingual friend read your text and tell you how it feels!")

if __name__ == "__main__":
    main()

