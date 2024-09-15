import ollama


SYSTEM_PROMPT=r"""
You are a Resume Editor. You will only reply back in the Latex format provided, you will reply back with BRAND NEW Projects and Technical Skills section. Make sure you provide a Date for projects. And make sure you escape % signs.
Reply back only with the Latex.

Make sure the key words in the Projects section aligns with the words in the Technical skills section.

Make sure the project names do not match that of the company being applied to.

DO NOT USER THE SAME PROJECTS/TECHNICAL SKILLS GIVEN - just follow the latex format.
"""


USER_PROMPT=r"""
give me 2 projects with 3 bullets each in the below resume style. The projects should cater to the job description provided.

you will also give a set of NEW/UPDATED technical skills which cater to the job description provided. Also following latex format.

Reply back in latex format, follow the format here

\section{Projects}
    \resumeSubHeadingListStart
      \resumeProjectHeading
          {\textbf{Gitlytics} $|$ \emph{Python, Flask, React, PostgreSQL, Docker}}{June 2020 -- Present}
          \resumeItemListStart
            \resumeItem{Developed a full-stack web application using with Flask serving a REST API with React as the frontend}
            \resumeItem{Implemented GitHub OAuth to get data from user’s repositories}
            \resumeItem{Visualized GitHub data to show collaboration}
            \resumeItem{Used Celery and Redis for asynchronous tasks}
          \resumeItemListEnd
      \resumeProjectHeading
          {\textbf{Simple Paintball} $|$ \emph{Spigot API, Java, Maven, TravisCI, Git}}{May 2018 -- May 2020}
          \resumeItemListStart
            \resumeItem{Developed a Minecraft server plugin to entertain kids during free time for a previous job}
            \resumeItem{Published plugin to websites gaining 2K+ downloads and an average 4.5/5-star review}
            \resumeItem{Implemented continuous delivery using TravisCI to build the plugin upon new a release}
            \resumeItem{Collaborated with Minecraft server administrators to suggest features and get feedback about the plugin}
          \resumeItemListEnd
    \resumeSubHeadingListEnd

\section{Technical Skills}
 \begin{itemize}[leftmargin=0.15in, label={}]
    \small{\item{
     \textbf{Languages}{: Java, Python, C/C++, SQL (Postgres), JavaScript, HTML/CSS, R} \\
     \textbf{Frameworks}{: React, Node.js, Flask, JUnit, WordPress, Material-UI, FastAPI} \\
     \textbf{Developer Tools}{: Git, Docker, TravisCI, Google Cloud Platform, VS Code, Visual Studio, PyCharm, IntelliJ, Eclipse} \\
     \textbf{Libraries}{: pandas, NumPy, Matplotlib}
    }}
 \end{itemize}

 
Here is the job description:

"""

Test = "DO NOT COPY AND PASTE THE PROJECTS & TECHNICAL SKILLS GIVEN. Provide new ones, and make sure they are not of the company name. Make sure to STRICTLY follow the Latex format with dates and everything."

def llm(job_description: str):
    response = ollama.chat(model='gemma2:2b', messages=[
    {
        'role': 'system',
        'content': SYSTEM_PROMPT,
    },
    {
        'role': 'user',
        'content': USER_PROMPT + job_description + SYSTEM_PROMPT
    },
    ])

    response = response['message']['content']
    return response
