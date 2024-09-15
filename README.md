# ai-linkedin-applier

The AI LinkedIn Applier which adjusts your Resume based on the job descripton provided -- updating the Projects & Technical Skills Section of your Resume 🔥

The AI scraper will:
1. Go through job postings one-by-one on LinkedIn.
2. Read the job description of the posting, and send it the LLM.
3. The LLM will output a new `Projects` & `Technical Skills` section for your Resume in Latex format.
4. The LLM output will get pasted on your Resume, on Overleaf -> and will recompile & save your new Resume as a PDF.
5. The scraper will go back to LinkedIn and apply to the job with your new Resume 💎
6. The scraper will give you 60 seconds (adjustable in the code), to fill out any additional questions on the LinkedIn
application. 
7. Once you click `Submit application` you don't need to do anything else, steps 1-6 will repeat on auto-pilot 😎.

Everything was built live on [stream](https://www.twitch.tv/joeknowscode) 🔥

## Simple Pre-requisites
1. [Ollama](https://ollama.com). For running the LLM locally on your machine. *Note:* I may make a separate branch which uses HuggingFace for the LLM call.
2. A Resume on Overleaf which follows the popular [Jake's Resume Format](https://www.overleaf.com/latex/templates/jakes-resume/syzfjbzwjncs).


## How to Run:

### 1. Run chrome in Debug mode:
```
/Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome --remote-debugging-port=9222
```
Adjust to the location of your Chrome.

### 2. Open your tabs:
1. Open LinkedIn -> go to Jobs -> go to the Easy Apply category.
2. Open Overleaf on your Resume.
* **Note:** The order in which you open your tabs is important. Open LinkedIn first, and Overleaf second.

### 3. Set your ENV variables:
Set the follow variables in your `.env` file.
* `DOWNLOAD_DIR`: the absolute path to your Downloads directory.
* `PHONE_NUMBER`: your phone number (Easy Apply applications usually ask for this).
* `CHROME_DRIVER_PATH`: the absolute path to your chrome webdriver.

### 4. Run the Scraper
```
pip install -r requirments.txt 
```
```
python scraper.py
```

Now go and secure those job offers 💪