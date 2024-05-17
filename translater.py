#!/usr/bin/env python3

from openai import OpenAI
import os

languages = {
    "en": "English",
    "fr": "French",
    "eu": "Euskera",
    "es": "Spanish",
    "ca": "Catalan",
}

def translate_text(api_key, text, lang_code, target_language):
    client = OpenAI(api_key=api_key)
    source_language = languages[lang_code]
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": f"You are a translator from {source_language} to {target_language}."},
            {"role": "system", "content": f"You must keep the data header, translating the values if necessary"},
            {"role": "system", "content": f"You must adapt the text to match the destination language and culture"},
            {"role": "user", "content": text}
        ],
        max_tokens=4096,
        n=1,
        stop=None,
        temperature=0.5
    )
    return response.choices[0].message.content.strip()

def translate_file(api_key, input_file_path, output_file_path, source_language, target_language):
    with open(input_file_path, 'r') as file:
        text = file.read()

    translated_text = translate_text(api_key, text, source_language, target_language)

    with open(output_file_path, 'w') as file:
        file.write(translated_text)

    print(f"Translation completed. Translated text saved to {output_file_path}")

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Translate text file using OpenAI API")
    parser.add_argument("input_file", help="Path to the input text file")
    parser.add_argument("output_file", help="Path to save the translated text file")
    parser.add_argument("--source_language", required=True, choices=["en", "fr", "eu", "es", "ca"], help="Source language code (one of: en, fr, eu, es, ca)")
    parser.add_argument("--target_language", required=True, choices=["en", "fr", "eu", "es", "ca"], help="Target language code (one of: en, fr, eu, es, ca)")

    args = parser.parse_args()

    api_key = os.getenv("OPENAI_API_KEY")
    translate_file(api_key, args.input_file, args.output_file, args.source_language, args.target_language)

