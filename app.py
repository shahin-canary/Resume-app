from flask import Flask, render_template, request, redirect, url_for
import os
from werkzeug.utils import secure_filename
import PyPDF2
import docx

from main import process_resume, input_prompt_template
from main import get_scores

# Flask app setup
app = Flask(__name__)

# Configure upload folder and allowed extensions
UPLOAD_FOLDER = 'resume_uploads'
ALLOWED_EXTENSIONS = {'pdf', 'doc', 'docx'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def allowed_file(filename): 
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def extract_text_from_pdf(pdf_file): 
    try:
        with open(pdf_file, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            text = ""
            for page in reader.pages:
                text += page.extract_text()
            return text
    except Exception:
        return "Error extracting text from PDF."

def extract_text_from_docx(docx_file): 
    try:
        doc = docx.Document(docx_file)
        text = ""
        for para in doc.paragraphs:
            text += para.text + "\n"
        return text
    except Exception:
        return "Error extracting text from DOCX."

@app.route('/', methods=['GET', 'POST'])
def index(): 
    extracted_data = "" 
    if request.method == 'POST':
        if 'file' not in request.files:
            return redirect(request.url) 
        file = request.files['file'] 
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath) 
            if filename.endswith('.pdf'):
                extracted_resume_text = extract_text_from_pdf(filepath)
            elif filename.endswith('.docx'):
                extracted_resume_text = extract_text_from_docx(filepath)
            else:
                extracted_resume_text = "Unsupported file type for extraction." 
            return redirect(url_for('score_results', extracted_resume_text=extracted_resume_text)) 
    return render_template('index.html')
 

@app.route('/score_results')
def score_results():
    # extracted_resume_text = request.args.get('extracted_resume_text', '') 
    # gemini_responses_lst = process_resume(input_prompt_template, extracted_resume_text) 
  
  


    gemini_responses_lst22222 = [
        {
            "personal_details": {
                "name": "Jaya Chandra",
                "email": "jaichandraios@gmail.com",
                "phone": "+918886916516",
                "address": 'null',#
                "gitHub": 'null',#
                "linked_in": "null",#
                "stack_overflow": "null",#
                "leetcode": "null"#
            },
            "total_work_experience": "4.2",
            "current_designation": "Software Engineer",
            "work_experience": [
                {
                    "company": "Innominds",
                    "role": "Software Engineer",
                    "job_description": "Fixed UI bugs which were reported by the Testing team.\nCollaborate with back-end developers for the REST API Integration.\nCreating and modifying React components.\nEnvironment / Technologies:\nHTML, CSS, TypeScript, React js,Redux and Fluent UI",
                    "duration": "January 2022 \u2013 till date"
                },
                {
                    "company": "Innominds",
                    "role": "Software Engineer",
                    "job_description": "Developed components for accessing PDF File using Fluent UI.\nFixed bugs for the already developed UI Components.\nResolving the PR comments and making changes as per Microsoft standards.\nEnvironment / Technologies:\nHTML, CSS, TypeScript and Fluent UI",
                    "duration": "Designation:"
                }
            ],
            "education": [
                {
                    "degree": "B.Tech",
                    "institution": "Hasvita Institute of Engineering and Technology Hyderabad IN",
                    "duration": "May 2016"
                },
                {
                    "degree": "BCA",
                    "institution": "Hasvita Institute of Engineering and Technology Hyderabad IN",
                    "duration": "May 2016"
                }
            ],
            "skills": [
                "HTML5",
                "CSS3",
                "SCSS",
                "Material UI",
                "Fluent UI",
                "JavaScript",
                "TypeScript",
                "React JS",
                "Redux",
                "RESTful APIs",
                "Version Control tools like GIT Gitlab and GitHub",
                "Bug tracking tools like JIRA and Redmine",
                "Responsive & Interactive websites",
                "Pixel Perfect documentation"
            ],
            "companies_worked": [
                "Innominds",
                "MIHY Innovations",
                "WalkingTree Technologies Pvt. Ltd"
            ],
            "languages_known": ["English", "Hindi"],
            "projects": [
                {
                    "project_name": "SigmaPlot NG",
                    "description": "SigmaPlot NG Cloudification is a proprietary software package for scientific graphing and data analysis. It runs on a web browser. The software can read multiple formats, such as Microsoft Excel spreadsheets, and can also perform mathematical transforms and statistical analyses.",
                    "role": "Software Engineer",
                    "duration": "null",#
                    "link": "null"#
                },
                {
                    "project_name": "SigmaPlot NG",
                    "description": "SigmaPlot NG Cloudification is a proprietary software package for scientific graphing and data analysis. It runs on a web browser. The software can read multiple formats, such as Microsoft Excel spreadsheets, and can also perform mathematical transforms and statistical analyses.",
                    "role": "Software Engineer",
                    "duration": "null",#
                    "link": "null"#
                }
            ],
            "certifications": ["Udemy"],
            "scores" : {
                        'education_scores_dict': 
                            {
                            'PhD in Computer Science': 65,
                            'MTech. in Computer Science': 12,
                            'BTech. in Computer Science': 96
                            },  
                        'skills_scores_dict': 
                            {
                            'HTML5': 63,
                            'CSS3': 13,
                            'JavaScript': 43
                            }, 
                        'language_scores_dict':
                            {
                            "English":11,
                            "Hindi":32 
                            },
                        'experience_scores_dict':
                            {
                            "3 to 5 years of experience": 10,
                            "5 to 7 years of experience": 10,
                            "7 to 10 years of experience": 10 
                            },
                        'skills_final_score': "43.0",
                        'language_final_score': "23.0",
                        'experience_final_score': "53.0",
                        'education_final_score': "12.0",
                        'total_score': "46"
                        },
            "final_score" : "46"
        }]
    



    # print("gemini_responses_lst : ", gemini_responses_lst)
    # scores_results_lst = get_scores(gemini_responses_lst)
    # print("scores_results :  ",scores_results_lst) 

    return render_template('score_results.html',  scores_results_lst = gemini_responses_lst22222)


if __name__ == '__main__':
    app.run(debug=True)
    # app.run()
