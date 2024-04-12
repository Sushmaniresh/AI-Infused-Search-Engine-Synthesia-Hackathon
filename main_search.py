# The solution aims to create a comprehensive search platform with the following key components:

## User Interface:
##Develop an intuitive and responsive interface for Android or web platforms to enable seamless search query input.
##Utilize Google search or alternative search engines to fetch the top 10 search results for each query.

## AI-Driven Information Extraction:
##Employ AI and machine learning models, particularly NLP and deep learning, to analyze and distill data from the top 10 search result pages.
##Use advanced techniques for relevance assessment and content extraction, ensuring the retrieval of valuable insights.

## Content Refinement:
##Refine the extracted information to ensure coherence, accuracy, and relevance.
##Implement mechanisms to filter out noise and prioritize valuable insights, enhancing the overall quality of the extracted content.

## HTML Page Generation:
##Dynamically generate HTML pages enriched with AI-curated content based on the search results.
##Ensure comprehensive coverage of information to provide users with valuable insights on their queries.

## Shareable Output:
#Implement functionality to allow users to easily share the generated HTML page via Android or web apps, enabling seamless sharing of curated content.

## Tech Stack:
#Participants can choose any programming language, framework, or library to develop the solution.
#Integration of open-source AI models using APIs or libraries suitable for the chosen platform is encouraged to enhance the capabilities of the solution.

## Submission Format:
#Provide the Android app or web page URL where users can input their queries and receive a shareable HTML page with relevant information.
#Include the APK of the Android app or the URL of the webpage along with the source code of the Android app/webpage and the backend codebase.

## Resources:
#Access to the OpenAI API key can be provided if needed, enabling integration of AI models for content extraction and refinement.
#Infrastructure support on platforms like Azure can be provided for running open-source models to enhance the solution's capabilities.

from flask import Flask, render_template, request, redirect
import requests
from bs4 import BeautifulSoup
import openai
import json

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/process_query', methods=['POST'])
def process_query():
    query = request.form['query']

    GOOGLE_API_KEY = "GOOGLE API KEY"
    GOOGLE_CX = "GOOGLE CX"

    url = f"https://www.googleapis.com/customsearch/v1?key={GOOGLE_API_KEY}&cx={GOOGLE_CX}&q={query}"
    response = requests.get(url)
    search_results = []
    data_url = []
    if "items" in response.json():
        search_results = response.json()["items"]
        data_url = [item['link'] for item in search_results]

    content = ""
    for result in search_results:
        content += result["snippet"] + "\n"

    OPENAI_API_KEY = "OPEN AI KEY"

    openai.api_key = OPENAI_API_KEY
    response = openai.Completion.create(
            engine="gpt-3.5-turbo-instruct",
            prompt=f"Summarize the following information about {query}:\n\n{content}",
            max_tokens=1024,
            n=1,
            stop=None,
            temperature=0.5,
        )
    refined_content = response.choices[0].text.strip()

    return render_template('result.html', query=query, refined_content=refined_content, data_url=data_url)

@app.route('/refresh')
def refresh():
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)
