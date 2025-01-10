from flask import Flask, render_template, request, redirect, url_for
import os
from werkzeug.utils import secure_filename
import PyPDF2
import docx

from main import get_gemini_response, input_prompt_template
from main import get_scores, validate_and_clean


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

    # # JD INPUTS 
    jd_educations_lst = ["B.Tech in IT", "B.Tech in Computer Science", "MCA", "BCA", "M.Tech in Computer Science", "M.Tech in IT"]  
    # jd_skills_lst = ["AI", "Machine Learning", "Deep Learning", "React.js"] 
    jd_skills_lst = ["Python Django",
            "CSS",
            "MySQL",
            "HTML",
            "Inter Personality Skills",
            "Time management",
            "Hard Working",
            "Quick Learner"]
    
    jd_designation = "AI Developer"  
    jd_Languages_lst = ["English", "Hindi", "Malayalam"] 
    jd_data = {"jd_designation":jd_designation, "jd_educations_lst": jd_educations_lst, "jd_skills_lst": jd_skills_lst, "jd_Languages_lst": jd_Languages_lst }
  

 
    import json
    extracted_resume_text = request.args.get('extracted_resume_text', '')   
    # gemini_responses = get_gemini_response(extracted_resume_text, input_prompt_template) 
     
      
    # import time 
    # def get_valid_json_response(extracted_resume_text, input_prompt_template, max_retries=5, delay=2):
    #     attempts = 0
    #     while attempts < max_retries:
    #         gemini_responses = get_gemini_response(extracted_resume_text, input_prompt_template)
    #         print(f"Attempt {attempts + 1} - gemini_responses: {gemini_responses}")
            
    #         # Check if the response is non-empty and looks like JSON
    #         if gemini_responses.strip() and gemini_responses.strip().startswith("{"):
    #             try:
    #                 # Attempt to parse the response
    #                 gemini_responses_lst = json.loads(gemini_responses)
    #                 print("Valid JSON received.")
    #                 return gemini_responses_lst
    #             except json.JSONDecodeError as e:
    #                 print(f"Error decoding JSON on attempt {attempts + 1}: {e}")
    #         else:
    #             print(f"Attempt {attempts + 1}: Invalid or empty response.")
            
    #         attempts += 1
    #         time.sleep(delay)

    #     print("Max retries reached. No valid JSON response.")
    #     return None


    # # Now call the function to get a valid JSON response
    # gemini_responses_lst = get_valid_json_response(extracted_resume_text, input_prompt_template)

    # if gemini_responses_lst is not None:
    #     print("gemini_responses_lst: ", gemini_responses_lst)
    # else:
    #     print("Failed to get a valid JSON response after multiple attempts.")



    null ="null"
    gemini_responses_lst = [{
        "personal_details": {
            "name": "ABHIJITH A",
            "designation": null,
            "email": "abhijith02003@gmail.com",
            "phone": "+91 9847038539",
            "address": "Anilnivas, Pambra colony, Pambra, Pulikkamally P.O Ernakulam",
            "location": null,
            "gitHub": null,
            "linkedin": null,
            "stackoverflow": null,
            "leetcode": null
        },
        "total_work_experience": null,
        "current_designation": "web developer",
        "work_experience": [
            {
                "company": "Nosce Techno Solution",
                "role": null,
                "job_description": "Internship in PHP",
                "duration": null,
                "total_work_years": null
            }, 
        ],
        "education": [
            {
                "degree": "BCA",
                "institution": "Nirmala Arts and Science College, Mulanthuruthy",
                "duration": "2020-2023",
                "total_completion_years": 3
            }
        ],
        "skills": [
            "Python Django",
            "CSS",
        ],
        "companies_worked": [
            "Nosce Techno Solution",
            "Zion IT Company Software and Networking",
            "Luminar Technolub"
        ],
        "languages_known": [
            "English",
            "Malayalam"
        ],
        "projects": [
            {
                "project_name": "Smart attendance System Using Face Recognition",
                "description": null,
                "role": null,
                "duration": null,
                "link": null
            },
            {
                "project_name": "Job Placement System",
                "description": null,
                "role": null,
                "duration": null,
                "link": null
            },
            {
                "project_name": "Flight Management System For Indian Coast Guard",
                "description": null,
                "role": null,
                "duration": null,
                "link": null
            }
        ],
        "certifications": []
    },
    {
        "personal_details": {
            "name": "ABHIJITH C",
            "designation": null,
            "email": "abhijith02003@gmail.com",
            "phone": "+91 9847038539",
            "address": "Anilnivas, Pambra colony, Pambra, Pulikkamally P.O Ernakulam",
            "location": null,
            "gitHub": null,
            "linkedin": null,
            "stackoverflow": null,
            "leetcode": null
        },
        "total_work_experience": null,
        "current_designation": "web developer",
        "work_experience": [
            {
                "company": "Nosce Techno Solution",
                "role": null,
                "job_description": "Internship in PHP",
                "duration": null,
                "total_work_years": null
            }, 
        ],
        "education": [
            {
                "degree": "BCA",
                "institution": "Nirmala Arts and Science College, Mulanthuruthy",
                "duration": "2020-2023",
                "total_completion_years": 3
            }, 
            {
                "degree": "SSLC",
                "institution": "St Jude E M HSS Karnakodam",
                "duration": null,
                "total_completion_years": null
            }
        ],
        "skills": [
            "Python Django",
            "CSS",
            "MySQL",
            "HTML", 
        ],
        "companies_worked": [
            "Nosce Techno Solution",
            "Zion IT Company Software and Networking",
            "Luminar Technolub"
        ],
        "languages_known": [
            "English",
            "Malayalam"
        ],
        "projects": [
            {
                "project_name": "Smart attendance System Using Face Recognition",
                "description": null,
                "role": null,
                "duration": null,
                "link": null
            },
            {
                "project_name": "Job Placement System",
                "description": null,
                "role": null,
                "duration": null,
                "link": null
            },
            {
                "project_name": "Flight Management System For Indian Coast Guard",
                "description": null,
                "role": null,
                "duration": null,
                "link": null
            }
        ],
        "certifications": []
    },
    {
        "personal_details": {
            "name": "ABHIJITH B",
            "designation": null,
            "email": "abhijith02003@gmail.com",
            "phone": "+91 9847038539",
            "address": "Anilnivas, Pambra colony, Pambra, Pulikkamally P.O Ernakulam",
            "location": null,
            "gitHub": null,
            "linkedin": null,
            "stackoverflow": null,
            "leetcode": null
        },
        "total_work_experience": null,
        "current_designation": null,
        "work_experience": [
            {
                "company": "Nosce Techno Solution",
                "role": null,
                "job_description": "Internship in PHP",
                "duration": null,
                "total_work_years": null
            },
            {
                "company": "Zion IT Company Software and Networking",
                "role": null,
                "job_description": "Internship in Python",
                "duration": null,
                "total_work_years": null
            },
            {
                "company": "Luminar Technolub",
                "role": null,
                "job_description": "Internship Course in Python Django",
                "duration": null,
                "total_work_years": null
            }
        ],
        "education": [
            {
                "degree": "BCA",
                "institution": "Nirmala Arts and Science College, Mulanthuruthy",
                "duration": "2020-2023",
                "total_completion_years": 3
            },
            {
                "degree": "PLUS TWO",
                "institution": "Darul Uloom HSS, Pullepady",
                "duration": null,
                "total_completion_years": null
            },
            {
                "degree": "SSLC",
                "institution": "St Jude E M HSS Karnakodam",
                "duration": null,
                "total_completion_years": null
            }
        ],
        "skills": [
            "Python Django",
            "CSS",
            "MySQL",
            "HTML",
            "Inter Personality Skills",
            "Time management",
            "Hard Working",
            "Quick Learner"
        ],
        "companies_worked": [
            "Nosce Techno Solution",
            "Zion IT Company Software and Networking",
            "Luminar Technolub"
        ],
        "languages_known": [
            "English",
            "Malayalam"
        ],
        "projects": [
            {
                "project_name": "Smart attendance System Using Face Recognition",
                "description": null,
                "role": null,
                "duration": null,
                "link": null
            },
            {
                "project_name": "Job Placement System",
                "description": null,
                "role": null,
                "duration": null,
                "link": null
            },
            {
                "project_name": "Flight Management System For Indian Coast Guard",
                "description": null,
                "role": null,
                "duration": null,
                "link": null
            }
        ],
        "certifications": []
    }]

    final_json = get_scores(gemini_responses_lst, jd_data) 
    cleaned_json = validate_and_clean(final_json) 
    final_json_lst = cleaned_json
    print("final_json_lst  : ", final_json_lst)
 
    for final_json in final_json_lst:
        if isinstance(final_json["final_score"], str):
            final_json["final_score"] = int(final_json["final_score"]) 
    final_json_lst.sort(key=lambda x: x["final_score"], reverse=True) 
    for final_json in final_json_lst:
        print(f'{final_json["personal_details"]["name"]} : {final_json["final_score"]}')
                
    return render_template('score_results.html',  final_json_lst = final_json_lst)

if __name__ == '__main__':
    app.run(debug=True) 
