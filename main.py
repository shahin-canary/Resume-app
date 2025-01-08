
input_prompt_template = """

resume:{resume}
current_date= January 2025

Extract the following information from the resume:

1. Personal Details: Candidate name, email, phone, location, address, GitHub, LinkedIn, Leetcode, StackOverflow.
2. Total years of work experience (numerical format), considering even implicit mentions such as "X years and months", "X-Y years", etc.
3. List of work experience (companies, roles, job descriptions, and duration in month and year - month and year format).
4. List of education/qualification details (degree, institution, and duration in "Month Year - Month Year" format).
5. List of skills mentioned in the resume (separate by commas).
6. List of companies worked for (separate by commas).
7. Languages known (separate by commas).
8. List of projects (project name, project description, role, and duration in "Month Year - Month Year" format, Link).
9. List of certifications (certification name, institution, and date, Link).

Provide the response in the following JSON structure:

{{
    "Personal Details": {{
        "Name": "<Name>",
        "Email": "<Email>",
        "Phone": "<Phone>",
        "Address": "<Address>",
        "Location": "<Location>",
        "GitHub": "<GitHub>",
        "LinkedIn": "<LinkedIn>",
        "Leetcode": "<Leetcode>",
        "StackOverflow": "<StackOverflow>"
    }},
    "Total Experience (in years)": "<numerical_value>",
    "Work Experience": [
        {{
            "Company": "<Company Name>",
            "Role": "<Role>",
            "Job Description": "<Job Description>",
            "Duration": "<Duration in Month Year - Month Year format>",
            "Total Years (in numerical format)": "<total_years with months format>"
        }}
    ],
    "Education": [
        {{
            "Degree": "<Degree>",
            "Institution": "<Institution>",
            "Duration": "<Duration in Month Year - Month Year format>",
            "Total Years (in numerical format)": "<total_years with months format>"
        }}
    ],
    "Skills": ["<Skill 1>", "<Skill 2>", "<Skill 3>", ...],
    "Companies Worked": ["<Company 1>", "<Company 2>", "<Company 3>", ...],
    "Languages Known": ["<Language 1>", "<Language 2>", "<Language 3>", ...],
    "Projects": [
        {{
            "Project Name": "<Project Name>",
            "Description": "<Project Description>",
            "Role": "<Role>",
            "Duration": "<Duration>",
            "Link": "<Project Link>"
        }}
    ],
    "Certifications": [
        {{
            "Certification Name": "<Certification Name>",
            "Institution": "<Institution>",
            "Date": "<Date>",
            "Link": "<Certification Link>"
        }}
    ]
}}"""

import json
import PyPDF2 as pdf 
import google.generativeai as genai 
def get_gemini_response(resume_text, input_prompt_template):
    input_prompt = input_prompt_template.format(resume=resume_text)
    genai.configure(api_key="AIzaSyCyh0yprRa2hbiuVTOkQMQgjxkW1J0OrTc")
    model = genai.GenerativeModel("gemini-pro")
    response = model.generate_content(input_prompt)
    return response.text

# def extract_text_from_pdf(uploaded_file):
#     reader = pdf.PdfReader(uploaded_file)
#     resume_text = ""
#     for page in range(len(reader.pages)):
#         resume_text += str(reader.pages[page].extract_text())
#     return resume_text

def process_resume(input_prompt_template, resume_text):  
    import json 
    attempt_count = 0
    max_retries = 5  # You can set the max retries to any value you prefer
    # Initialize gemini_response variable
    gemini_response = None

    while attempt_count < max_retries:
        gemini_response = get_gemini_response(resume_text, input_prompt_template)
        print("Attempt", attempt_count + 1, "gemini_response: ", gemini_response)
        
        try:
            # Try to parse the response as JSON
            gemini_response_json = json.loads(gemini_response)
            print("new:::: ", gemini_response_json)
            break  # If the response is valid, break out of the loop
        except json.JSONDecodeError:
            # If the response is invalid, retry
            print("Error: The response is not valid JSON.")
            attempt_count += 1
            if attempt_count >= max_retries:
                print("Max retries reached. Could not get a valid response.")
                break


    # gemini_response = get_gemini_response(resume_text, input_prompt_template)  
    # print("gemini_response:            :",gemini_response)
    # gemini_response_json = json.loads(gemini_response) 
    # print("new:::: ",gemini_response_json)
    # print([gemini_response_json])
    print(type(gemini_response_json))
    return [gemini_response_json]

    
  
# response = process_resume(input_prompt_template)
# print(response)











from sentence_transformers import SentenceTransformer 
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
# def calculate_similarity(jd_text, applicant_text):  
#     model = SentenceTransformer('all-MiniLM-L6-v2')
#     jd_embedding = model.encode([jd_text])
#     applicant_embedding = model.encode([applicant_text])
#     similarity_score = cosine_similarity([np.mean(jd_embedding, axis=0)], [np.mean(applicant_embedding, axis=0)])[0][0]
#     return similarity_score
  
# jd_text = "Insert job description text here."
# applicant_text = "Insert applicant's profile text here." 

# similarity = calculate_similarity(jd_text, applicant_text)
# print(f"Similarity between job description and applicant: {similarity}")


 
# def get_scores(gemini_responses_lst):

#     def calculate_similarity(jd_text, applicant_text):  
#         model = SentenceTransformer('all-MiniLM-L6-v2')
#         jd_embedding = model.encode([jd_text])
#         applicant_embedding = model.encode([applicant_text])
#         similarity_score = cosine_similarity([np.mean(jd_embedding, axis=0)], [np.mean(applicant_embedding, axis=0)])[0][0]
#         return similarity_score

#     for gemini_response in gemini_responses_lst:
#         # Extracted data from resume
#         skills = gemini_response["Skills"]
#         languages = gemini_response["Languages Known"]
#         education = gemini_response["Education"]
#         resume_experience = gemini_response["Total Experience (in years)"]

#         # Job description data
#         jd_skills = ["AI", "Machine Learning", "Deep Learning", "NLP", "HTML5", "React.js", "Redux", "Context API", "Next.js", "CSS3"]
#         jd_languages = ["English", "Hindi", "Malayalam"]
#         jd_education = " | ".join(["B.Tech in IT", "B.Tech in Computer Science", "MCA", "BCA", "M.Tech in Computer Science", "M.Tech in IT"])
#         jd_experience = "3 to 5 years of experience"

#         # Calculate skills similarity
#         skills_str = " | ".join(skills)
#         jd_skills_str = " | ".join(jd_skills)
#         skills_similarity = calculate_similarity(skills_str, jd_skills_str)

#         # Calculate language similarity if resume has languages
#         if languages:
#             languages_str = " | ".join(languages)
#             jd_languages_str = " | ".join(jd_languages)
#             language_similarity = calculate_similarity(languages_str, jd_languages_str)
#         else:
#             language_similarity = 0

#         # Calculate education similarity
#         education_list = [edu["Degree"] for edu in education if edu["Degree"]]
#         education_similarity_scores = [calculate_similarity(jd_education, edu) for edu in education_list]
#         average_education_similarity = sum(education_similarity_scores) / len(education_similarity_scores) if education_similarity_scores else 0

#         # Calculate experience similarity
#         experience_similarity = calculate_similarity(jd_experience, resume_experience)

#         # Combine all the scores into a dictionary with two digits after the decimal point
#         scores = {
#             "skills_score": round(skills_similarity * 100, 2),
#             "language_score": round(language_similarity * 100, 2),
#             "education_score": round(average_education_similarity * 100, 2),
#             "experience_score": round(experience_similarity * 100, 2)
#         }

#         gemini_response["scores"] = scores     
#         gemini_response["Total Score"] = "51" 

#     scores_results = gemini_responses_lst
#     return scores_results



def get_scores(gemini_responses_lst):

    def calculate_similarity(jd_text, applicant_text):  
        model = SentenceTransformer('all-MiniLM-L6-v2')
        jd_embedding = model.encode([jd_text])
        applicant_embedding = model.encode([applicant_text])
        similarity_score = cosine_similarity([np.mean(jd_embedding, axis=0)], [np.mean(applicant_embedding, axis=0)])[0][0]
        return similarity_score  

    for gemini_response in gemini_responses_lst:
        # Extracted data from resume
        skills = gemini_response["Skills"]
        languages = gemini_response["Languages Known"]
        education = gemini_response["Education"]
        resume_experience = gemini_response["Total Experience (in years)"]

        # Convert experience to string if it's an integer
        resume_experience_str = str(resume_experience)  # Ensure it's a string

        # Job description data
        jd_skills = ["AI", "Machine Learning", "Deep Learning", "NLP", "HTML5", "React.js", "Redux", "Context API", "Next.js", "CSS3"]
        jd_languages = ["English", "Hindi", "Malayalam"]
        jd_education = " | ".join(["B.Tech in IT", "B.Tech in Computer Science", "MCA", "BCA", "M.Tech in Computer Science", "M.Tech in IT"])
        jd_experience = "3 to 5 years of experience"

        # Calculate skills similarity
        skills_str = " | ".join(skills)
        jd_skills_str = " | ".join(jd_skills)
        skills_similarity = calculate_similarity(skills_str, jd_skills_str)

        # Calculate language similarity if resume has languages
        if languages:
            languages_str = " | ".join(languages)
            jd_languages_str = " | ".join(jd_languages)
            language_similarity = calculate_similarity(languages_str, jd_languages_str)
        else:
            language_similarity = 0

        # Calculate education similarity
        education_list = [edu["Degree"] for edu in education if edu["Degree"]]
        education_similarity_scores = [calculate_similarity(jd_education, edu) for edu in education_list]
        average_education_similarity = sum(education_similarity_scores) / len(education_similarity_scores) if education_similarity_scores else 0

        # Calculate experience similarity
        experience_similarity = calculate_similarity(jd_experience, resume_experience_str)  # Use string here

        # Combine all the scores into a dictionary with two digits after the decimal point
        scores = {
            "skills_score": round(skills_similarity * 100, 2),
            "language_score": round(language_similarity * 100, 2),
            "education_score": round(average_education_similarity * 100, 2),
            "experience_score": round(experience_similarity * 100, 2)
        }

        gemini_response["scores"] = scores     
        gemini_response["Total Score"] = round(sum(scores.values()) / len(scores), 2) 

    scores_results = gemini_responses_lst
    return scores_results





# gemini_response = {
#     "Personal Details": {
#         "Name": "Jaya Chandra",
#         "Email": "jaichandraios@gmail.com",
#         "Phone": "+918886916516",
#         "Address": 'null',
#         "GitHub": 'null',
#         "LinkedIn": "null",
#         "StackOverflow": "null",
#         "Leetcode": "null"
#     },
#     "Total Experience (in years)": "4+",
#     "Work Experience": [
#         {
#             "Company": "Innominds",
#             "Role": "Software Engineer",
#             "Job Description": "Fixed UI bugs which were reported by the Testing team.\nCollaborate with back-end developers for the REST API Integration.\nCreating and modifying React components.\nEnvironment / Technologies:\nHTML, CSS, TypeScript, React js,Redux and Fluent UI",
#             "Duration": "January 2022 \u2013 till date"
#         },
#         {
#             "Company": "Innominds",
#             "Role": "Software Engineer",
#             "Job Description": "Developed components for accessing PDF File using Fluent UI.\nFixed bugs for the already developed UI Components.\nResolving the PR comments and making changes as per Microsoft standards.\nEnvironment / Technologies:\nHTML, CSS, TypeScript and Fluent UI",
#             "Duration": "Designation:"
#         },
#         {
#             "Company": "MIHY Innovations",
#             "Role": "Software Engineer",
#             "Job Description": "Developed UI React Screens as per UX renders well across multiple devices like web, tab and mobile devices.\nFixed UI Bugs for the developed screens.\nCollaborate with back-end developers for the REST API Integration.\nCreating and Modifying Material UI Components as per application requirements.\nCreating and modifying React components and making reusable components.\nTaking care of build and deployment issues.\nEnvironment / Technologies:\nHTML, CSS, JavaScript, React, Redux, REST API Integration, Material UI",
#             "Duration": "null"
#         },
#         {
#             "Company": "MIHY Innovations",
#             "Role": "Software Engineer",
#             "Job Description": "Developed UI React Screens as per UX renders well across multiple devices like web, tab and mobile devices.\nFixed UI Bugs for the developed screens.\nCollaborate with back-end developers for the REST API Integration.\nCreating and Modifying Material UI Components as per application requirements.\nEnvironment / Technologies:\nHTML, CSS, JavaScript, React, Redux, REST API Integration, Material UI.",
#             "Duration": "null"
#         },
#         {
#             "Company": "WalkingTree Technologies Pvt. Ltd",
#             "Role": "Associate Software Engineer",
#             "Job Description": "Developing and maintaining the UI Screens renders well across multiple devices.\nFixing UI bugs which were reported by the Testing team and Modifying React components.\nCollaborate with back-end developers for the REST API Integration.\nEnvironment / Technologies:\nHTML, CSS, JavaScript, React JS, Redux, Material UI, REST API Integration.",
#             "Duration": "null"
#         }
#     ],
#     "Education": [
#         {
#             "Degree": "B.Tech",
#             "Institution": "Hasvita Institute of Engineering and Technology Hyderabad IN",
#             "Duration": "May 2016"
#         }
#     ],
#     "Skills": [
#         "HTML5",
#         "CSS3",
#         "SCSS",
#         "Material UI",
#         "Fluent UI",
#         "JavaScript",
#         "TypeScript",
#         "React JS",
#         "Redux",
#         "RESTful APIs",
#         "Version Control tools like GIT Gitlab and GitHub",
#         "Bug tracking tools like JIRA and Redmine",
#         "Responsive & Interactive websites",
#         "Pixel Perfect documentation"
#     ],
#     "Companies Worked": [
#         "Innominds",
#         "MIHY Innovations",
#         "WalkingTree Technologies Pvt. Ltd"
#     ],
#     "Languages Known": [],
#     "Projects": [
#         {
#             "Project Name": "SigmaPlot NG",
#             "Description": "SigmaPlot NG Cloudification is a proprietary software package for scientific graphing and data analysis. It runs on a web browser. The software can read multiple formats, such as Microsoft Excel spreadsheets, and can also perform mathematical transforms and statistical analyses.",
#             "Role": "Software Engineer",
#             "Duration": "null",
#             "Link": "null"
#         },
#         {
#             "Project Name": "Microsoft Edge Browser -PDF Team",
#             "Description": "Worked on Edge Browser with PDF ToolBar, Developed UI components Zoom Component, Pageview flout and upsell flout component using Fluent UI for accessing the pdf file.",
#             "Role": "Software Engineer",
#             "Duration": "null",
#             "Link": "null"
#         },
#         {
#             "Project Name": "BULLFORCE",
#             "Description": "Bullforce is a web-based trading application used by Indian clients to trade and invest in stock investment using high technology machine learning and artificial intelligence.",
#             "Role": "Software Engineer",
#             "Duration": "null",
#             "Link": "null"
#         },
#         {
#             "Project Name": "FXEQUITY",
#             "Description": "FXEQUITY is a world class trading platform for people who wants to trade and invest in stock markets. Providing round the clock assistance. Offering experiences of different trading platforms like CTrader and MT5.",
#             "Role": "Software Engineer",
#             "Duration": "null",
#             "Link": "null"
#         },
#         {
#             "Project Name": "eGovernments",
#             "Description": "eGovernments is a web-based application intended for citizens in the state, apply to the government for their new construction buildings to get the fire no objection certificate from the nearest fire station.",
#             "Role": "Associate Software Engineer",
#             "Duration": "null",
#             "Link": "null"
#         }
#     ],
#     "Certifications": []
# }


# scores_results = get_scores(gemini_responses_lst)
# print(scores_results)
    








# # "Personal Details" 
# # "Total Experience (in years)" 
# # "Work Experience" 
# # "Education" 
# # "Skills" 
# # "Companies Worked" 
# # "Languages Known" 
# # "Projects" 
# # "Certifications"

# # "Total Experience (in years)_score" 
# # "Work Experience_score" 
# # "Education_score" 
# # "Skills_score" 
# # "Companies Worked _score" 
# # "Languages_score" 
# # "Projects_score" 
# # "Certifications_score"