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
    extracted_resume_text = request.args.get('extracted_resume_text', '') 
    gemini_responses_lst = process_resume(input_prompt_template, extracted_resume_text) 
  
    print("gemini_responses_lst : ", gemini_responses_lst)
    scores_results_lst = get_scores(gemini_responses_lst)
    print("scores_results :  ",scores_results_lst)

    return render_template('score_results.html',  scores_results_lst = scores_results_lst)


if __name__ == '__main__':
    app.run(debug=True)
    # app.run()
