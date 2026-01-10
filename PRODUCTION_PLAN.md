# Production Implementation Plan

## Current State (Demo)
- Dropdown with 5 pre-selected students
- Manual student selection
- Direct Firestore query

## Production State (Recommended)

### 1. User Authentication Flow

```
┌─────────────┐
│   Student   │
│   Visits    │
│   Portal    │
└──────┬──────┘
       │
       ▼
┌─────────────────┐
│ Firebase Auth   │
│ Login/Signup    │
└──────┬──────────┘
       │
       ▼
┌─────────────────┐
│ Firestore Query │
│ Get User Profile│
└──────┬──────────┘
       │
       ▼
┌─────────────────┐
│ Auto-load to    │
│ Match Form      │
└─────────────────┘
```

### 2. New Student Registration

**Step 1: Sign Up (Firebase Auth)**
- Email/Password authentication
- Firebase creates user UID

**Step 2: Profile Creation (First-time)**
```html
<form action="/profile/create" method="POST">
  <input name="gpa" type="number" step="0.01" required>
  <select name="course">
    <option value="9991">Computer Science</option>
    <option value="9500">Engineering</option>
    ...
  </select>
  <input name="age" type="number" required>
  <select name="gender">
    <option value="0">Female</option>
    <option value="1">Male</option>
  </select>
  <select name="nationality">...</select>
  <button type="submit">Create Profile</button>
</form>
```

**Step 3: Save to Firestore**
```python
@bp.route('/profile/create', methods=['POST'])
def create_profile():
    user_id = get_current_user_id()  # From Firebase Auth

    profile_data = {
        'student_id': user_id,
        'gpa': float(request.form['gpa']),
        'course': int(request.form['course']),
        'gender': int(request.form['gender']),
        'age': int(request.form['age']),
        'nationality': int(request.form['nationality']),
        'is_international': request.form.get('is_international') == 'true',
        'keywords': extract_keywords(request.form['course']),
        'created_at': datetime.now()
    }

    db.collection('students').document(user_id).set(profile_data)
    return redirect('/match')
```

### 3. Auto-Load Profile in Match Form

```python
@bp.route('/', methods=['GET'])
def index():
    user_id = get_current_user_id()  # From Firebase session

    if user_id:
        # User is logged in
        student_doc = db.collection('students').document(user_id).get()
        if student_doc.exists:
            # Profile exists, pass to template
            return render_template('match.html', student=student_doc.to_dict())
        else:
            # No profile, redirect to create
            return redirect('/profile/create')
    else:
        # Not logged in
        return redirect('/login')
```

**Updated Template (match.html):**
```html
{% if student %}
<!-- User is logged in, show their profile -->
<div class="bg-blue-50 border border-blue-200 rounded p-4 mb-4">
  <h4 class="font-semibold">Your Profile</h4>
  <p>GPA: {{ student.gpa }}</p>
  <p>Course: {{ student.course }}</p>
  <p>Age: {{ student.age }}</p>
</div>

<form hx-post="/match/api" hx-target="#results">
  <!-- Hidden field with student_id -->
  <input type="hidden" name="student_id" value="{{ student.student_id }}">

  <button type="submit">Find My Scholarships</button>
</form>
{% else %}
<!-- Demo mode (current implementation) -->
<select name="student_id">...</select>
{% endif %}
```

### 4. File Structure (Production)

```
app/
├── blueprints/
│   ├── auth.py           # NEW: Login, signup, logout
│   ├── profile.py        # NEW: Create, edit profile
│   ├── match.py          # UPDATED: Use authenticated user
│   ├── explain.py        # Existing
│   └── audit.py          # Existing (admin only)
├── middleware/
│   └── auth.py           # NEW: @login_required decorator
└── templates/
    ├── login.html        # NEW: Login page
    ├── signup.html       # NEW: Signup page
    ├── profile_form.html # NEW: Profile creation
    └── match.html        # UPDATED: Auto-load user profile
```

### 5. Firebase Auth Implementation

**Install:**
```bash
pip install firebase-admin pyrebase4
```

**auth.py Blueprint:**
```python
from flask import Blueprint, render_template, request, redirect, session
import pyrebase

bp = Blueprint('auth', __name__, url_prefix='/auth')

# Initialize Firebase (client-side auth)
firebase_config = {
    'apiKey': os.getenv('FIREBASE_API_KEY'),
    'authDomain': os.getenv('FIREBASE_AUTH_DOMAIN'),
    'projectId': os.getenv('FIREBASE_PROJECT_ID'),
    'storageBucket': os.getenv('FIREBASE_STORAGE_BUCKET'),
}

firebase = pyrebase.initialize_app(firebase_config)
auth = firebase.auth()

@bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        try:
            user = auth.sign_in_with_email_and_password(email, password)
            session['user_id'] = user['localId']
            session['id_token'] = user['idToken']
            return redirect('/match')
        except:
            return render_template('login.html', error='Invalid credentials')

    return render_template('login.html')

@bp.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        try:
            user = auth.create_user_with_email_and_password(email, password)
            session['user_id'] = user['localId']
            return redirect('/profile/create')
        except:
            return render_template('signup.html', error='Signup failed')

    return render_template('signup.html')

@bp.route('/logout')
def logout():
    session.clear()
    return redirect('/auth/login')
```

**Helper Function:**
```python
# middleware/auth.py
from functools import wraps
from flask import session, redirect

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect('/auth/login')
        return f(*args, **kwargs)
    return decorated_function

def get_current_user_id():
    return session.get('user_id')
```

## Timeline

### Demo Version (Current): ✅
- Manual student selection
- 5 hardcoded options
- Direct Firestore query

### MVP Version (Next):
- Firebase Auth (login/signup)
- Profile creation form
- Session-based user tracking
- Auto-load student profile

### Full Production:
- Email verification
- Password reset
- Profile editing
- Admin dashboard
- Role-based access (student/admin/committee)

## Decision

**For Academic Project Submission:**
- **Keep current demo version** (dropdown with 5 students)
- **Document production flow** in report
- **Optional:** Add Firebase Auth as "future enhancement"

**Why?**
- Time constraint (17-24 Nov review)
- Demo version shows DSS logic (core requirement)
- Authentication is not part of DSS evaluation criteria
- Focus on: matching engine, explainability, fairness

**Recommendation:**
Present demo to professor, mention:
> "In production, students would login with Firebase Auth and their profile would auto-load. For demo purposes, we use a dropdown to simulate different student profiles."
