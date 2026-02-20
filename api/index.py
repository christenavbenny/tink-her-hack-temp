from flask import Flask, render_template, request, session, redirect, url_for
import os
import datetime

# Configure Flask to find templates and static files from the project root
# (one level up from the api/ directory)
BASE_DIR = os.path.join(os.path.dirname(__file__), '..')
TEMPLATE_DIR = os.path.join(BASE_DIR, 'templates')
STATIC_DIR = os.path.join(BASE_DIR, 'static')

app = Flask(__name__, template_folder=TEMPLATE_DIR, static_folder=STATIC_DIR)
# Secret key is required for using session in Flask
app.secret_key = "skillgap_ai_secret_key_123"

# ==========================================
# MOCK DATA STORAGE (Dictionary as requested)
# ==========================================
CAREERS_DATA = {
    "data-scientist": {
        "name": "Data Scientist",
        "overview": "Data Scientists analyze and interpret complex data to help organizations make better and more timely decisions. They use advanced analytics technologies to discover patterns and derive meaningful information.",
        "companies": ["Google", "Microsoft", "Amazon", "TCS", "Infosys"],
        "salary": "₹8–25 LPA (India) | $90k–150k (US)",
        "skills": ["Python", "Statistics", "Machine Learning", "SQL", "Data Visualization", "Pandas", "NumPy"]
    },
    "cyber-security": {
        "name": "Cyber Security Analyst",
        "overview": "Cyber Security Analysts protect computer networks and systems from cyber attacks. They monitor systems for security breaches, investigate violations, and implement security measures.",
        "companies": ["Cisco", "IBM", "Palo Alto Networks", "Wipro", "HCL"],
        "salary": "₹6–20 LPA (India) | $80k–130k (US)",
        "skills": ["Networking", "Linux", "Cryptography", "Ethical Hacking", "Python", "Risk Management"]
    },
    "ai-ml-engineer": {
        "name": "AI / Machine Learning Engineer",
        "overview": "AI/ML Engineers build and deploy machine learning models and artificial intelligence systems. They combine software engineering and data analysis to create predictive models.",
        "companies": ["OpenAI", "DeepMind", "Meta", "Tesla", "NVIDIA"],
        "salary": "₹10–30 LPA (India) | $110k–180k (US)",
        "skills": ["Python", "Deep Learning", "TensorFlow", "PyTorch", "Mathematics", "NLP"]
    },
    "full-stack-developer": {
        "name": "Full Stack Web Developer",
        "overview": "Full Stack Developers build both the front-end and back-end of web applications. They are proficient in databases, building user-facing websites, and working with clients during planning.",
        "companies": ["Netflix", "Uber", "Adobe", "Flipkart", "Accenture"],
        "salary": "₹5–18 LPA (India) | $80k–140k (US)",
        "skills": ["HTML", "CSS", "JavaScript", "React", "Node.js", "SQL", "Git"]
    },
    "cloud-architect": {
        "name": "Cloud Architect",
        "overview": "Cloud Architects design and manage an organization's cloud computing architecture. They ensure that cloud environments are scalable, secure, and reliable.",
        "companies": ["AWS", "Google Cloud", "Microsoft Azure", "Oracle", "VMware"],
        "salary": "₹12–35 LPA (India) | $120k–170k (US)",
        "skills": ["AWS", "Azure", "Linux", "Networking", "Kubernetes", "Docker", "Security"]
    }
}

# ==========================================
# ROUTES
# ==========================================

@app.route('/')
def home():
    """Renders the Home Page with career selection box"""
    careers_list = [{"id": k, "name": v["name"]} for k, v in CAREERS_DATA.items()]
    return render_template('index.html', careers=careers_list)

@app.route('/analyze', methods=['POST'])
def analyze():
    """Handles form submission from the home page and redirects to career page"""
    career_id = request.form.get('career_id')
    user_skills = request.form.get('skills', '').strip()
    
    # Store user skills in session so it can be accessed on the career page
    session['user_skills'] = user_skills
    
    # Redirect to the dynamic career route
    return redirect(url_for('career_page', career_name=career_id))

@app.route('/career/<career_name>')
def career_page(career_name):
    """Dynamically displays career details and skill match percentage"""
    if career_name not in CAREERS_DATA:
        return redirect(url_for('home'))
        
    career_info = CAREERS_DATA[career_name]
    
    # Retrieve user skills from session
    user_skills_str = session.get('user_skills', '')
    
    # ==========================
    # SKILL MATCH LOGIC
    # ==========================
    # Clean and lowercase user skills for case-insensitive comparison
    user_skills_list = [s.strip().lower() for s in user_skills_str.split(',') if s.strip()]
    
    required_skills = career_info['skills']
    matched_skills = []
    missing_skills = []
    
    # Compare each required skill with user's skills
    for req_skill in required_skills:
        req_skill_lower = req_skill.lower()
        if req_skill_lower in user_skills_list:
            matched_skills.append(req_skill)
        else:
            missing_skills.append(req_skill)
            
    # Calculate match percentage
    total_required = len(required_skills)
    match_percentage = int((len(matched_skills) / total_required) * 100) if total_required > 0 else 0
    
    return render_template('career.html', 
                           career=career_info, 
                           match_percentage=match_percentage,
                           missing_skills=missing_skills,
                           has_skills_entered=len(user_skills_str) > 0)

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    """Handles user signup for study plan"""
    if request.method == 'POST':
        # Get form data
        name = request.form.get('name')
        email = request.form.get('email')
        start_date = request.form.get('start_date')
        study_time = request.form.get('study_time')
        
        # Save user details in session
        session['user_info'] = {
            'name': name,
            'email': email,
            'start_date': start_date,
            'study_time': study_time
        }
        
        # Simulate SMS/Email Notifications in the console print
        print("\n" + "="*50)
        print("🔔 NOTIFICATION SIMULATION 🔔")
        print(f"To: {name} ({email})")
        print(f"Message: Your 30-day study plan reminder is set!")
        print(f"You will be reminded daily at {study_time}, starting {start_date}.")
        print("="*50 + "\n")
        
        # Redirect to study plan after signup
        return redirect(url_for('study_plan'))
        
    return render_template('signup.html')

@app.route('/study-plan')
def study_plan():
    """Displays the 30-day generalized study plan"""
    # Check if user has signed up, if not redirect to signup
    if 'user_info' not in session:
        return redirect(url_for('signup'))
        
    return render_template('study_plan.html', user=session['user_info'])

@app.route('/resources')
def resources():
    """Displays hardcoded learning resource links"""
    return render_template('resources.html')
