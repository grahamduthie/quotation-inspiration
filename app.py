from flask import Flask, render_template
import requests
import random

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/get_quote')
def get_quote():
    try:
        # Fetch a random quote
        response = requests.get('https://zenquotes.io/api/random', timeout=5)
        if response.status_code == 200:
            data = response.json()[0]
            quote = data['q']
            author = data['a']
            
            # Translate to Spanish
            spanish_response = requests.get(
                'https://api.mymemory.translated.net/get',
                params={
                    'q': quote,
                    'langpair': 'en|es'
                }
            )
            
            # Translate to French
            french_response = requests.get(
                'https://api.mymemory.translated.net/get',
                params={
                    'q': quote,
                    'langpair': 'en|fr'
                }
            )
            
            # Translate to German
            german_response = requests.get(
                'https://api.mymemory.translated.net/get',
                params={
                    'q': quote,
                    'langpair': 'en|de'
                }
            )
            
            if (spanish_response.status_code == 200 and 
                french_response.status_code == 200 and 
                german_response.status_code == 200):
                
                spanish_data = spanish_response.json()
                french_data = french_response.json()
                german_data = german_response.json()
                
                spanish_quote = spanish_data['responseData']['translatedText']
                french_quote = french_data['responseData']['translatedText']
                german_quote = german_data['responseData']['translatedText']
                
                # Return all four versions separated by double newlines
                output = f'"{quote}" - {author}\r\n\r\n'
                output += f'"{spanish_quote}" - {author}\r\n\r\n'
                output += f'"{french_quote}" - {author}\r\n\r\n'
                output += f'"{german_quote}" - {author}'
                return output
            else:
                return "Failed to translate quotes"
        else:
            return f"Failed to fetch quote. Status code: {response.status_code}"
    except Exception as e:
        return f"An error occurred: {str(e)}"

if __name__ == '__main__':
    app.run(debug=True) 