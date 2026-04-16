"""
Run with: python seed_courses.py
Seeds course and skill test data into the DB.
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'careerbridge.settings')
django.setup()

from courses.models import Course, SkillTest

# Clear old data
SkillTest.objects.all().delete()
Course.objects.all().delete()
print("Cleared old courses and tests.")

COURSES = [
    {
        "id": 1,
        "title": "Python for Data Science & AI",
        "provider": "YouTube",
        "provider_url": "https://www.youtube.com/watch?v=LHBE6Q9XlzI",
        "category": "data",
        "target_program": "BTech",
        "target_years": [2, 3, 4],
        "is_free": True,
        "description": "Learn Python from scratch. Covers data manipulation, NumPy, Pandas, and intro to Machine Learning with real-world projects.",
        "duration": "12 hrs",
        "icon": "🐍",
    },
    {
        "id": 2,
        "title": "Full-Stack Web Development Bootcamp",
        "provider": "freeCodeCamp",
        "provider_url": "https://www.youtube.com/watch?v=nu_pCVPKzTk",
        "category": "web",
        "target_program": "BCA",
        "target_years": [1, 2, 3],
        "is_free": True,
        "description": "Build real-world projects with HTML, CSS, JavaScript, React, Node.js and MongoDB. Beginner to advanced coverage.",
        "duration": "15 hrs",
        "icon": "🌐",
    },
    {
        "id": 3,
        "title": "Business Management Fundamentals",
        "provider": "Coursera",
        "provider_url": "https://www.youtube.com/watch?v=yoEezZD71sc",
        "category": "BBA",
        "target_program": "BBA",
        "target_years": [1, 2, 3, 4],
        "is_free": True,
        "description": "Introduction to core business concepts including organizational behavior, strategic planning, and management principles.",
        "duration": "8 hrs",
        "icon": "📊",
    },
    {
        "id": 4,
        "title": "Accounting & Financial Statements",
        "provider": "NPTEL",
        "provider_url": "https://www.youtube.com/watch?v=yYX4bvQSqbo",
        "category": "BCom",
        "target_program": "BCom",
        "target_years": [1, 2, 3, 4],
        "is_free": True,
        "description": "Covers journal entries, ledger accounts, balance sheets, P&L statements and corporate taxation basics.",
        "duration": "10 hrs",
        "icon": "📒",
    },
    {
        "id": 5,
        "title": "Data Structures & Algorithms",
        "provider": "YouTube",
        "provider_url": "https://www.youtube.com/watch?v=8hly31xKli0",
        "category": "data",
        "target_program": "BTech",
        "target_years": [1, 2, 3],
        "is_free": True,
        "description": "Master arrays, linked lists, trees, graphs, sorting, dynamic programming — everything needed for placement interviews.",
        "duration": "20 hrs",
        "icon": "🔢",
    },
    {
        "id": 6,
        "title": "React.js — Complete Guide 2025",
        "provider": "YouTube",
        "provider_url": "https://www.youtube.com/watch?v=CgkZ7MvWUAA",
        "category": "web",
        "target_program": "Any",
        "target_years": [2, 3, 4],
        "is_free": True,
        "description": "Build modern SPAs with React hooks, Context API, Redux, React Router. Includes 3 project builds.",
        "duration": "11 hrs",
        "icon": "⚛️",
    },
    {
        "id": 7,
        "title": "Digital Marketing Masterclass",
        "provider": "Google",
        "provider_url": "https://www.youtube.com/watch?v=hiCjj55_zV0",
        "category": "BBA",
        "target_program": "BBA",
        "target_years": [2, 3, 4],
        "is_free": True,
        "description": "SEO, SEM, social media strategy, email marketing and analytics. Includes Google Analytics certification prep.",
        "duration": "6 hrs",
        "icon": "📱",
    },
    {
        "id": 8,
        "title": "Database Management with SQL",
        "provider": "freeCodeCamp",
        "provider_url": "https://www.youtube.com/watch?v=HXV3zeQKqGY",
        "category": "web",
        "target_program": "BCA",
        "target_years": [1, 2, 3, 4],
        "is_free": True,
        "description": "Master SQL from zero to advanced — SELECT, JOINs, subqueries, indexing, stored procedures and transactions.",
        "duration": "4 hrs",
        "icon": "🗄️",
    },
    {
        "id": 9,
        "title": "Corporate Finance & Investment",
        "provider": "edX",
        "provider_url": "https://www.youtube.com/watch?v=WEDIj9JBTC8",
        "category": "BCom",
        "target_program": "BCom",
        "target_years": [2, 3, 4],
        "is_free": True,
        "description": "Valuation, capital budgeting, risk & return, portfolio management and financial statement analysis.",
        "duration": "9 hrs",
        "icon": "💹",
    },
    {
        "id": 10,
        "title": "Machine Learning with TensorFlow",
        "provider": "YouTube",
        "provider_url": "https://www.youtube.com/watch?v=tPYj3fFJGjk",
        "category": "data",
        "target_program": "BTech",
        "target_years": [3, 4],
        "is_free": True,
        "description": "Build neural networks, CNNs, RNNs and NLP models. Includes image classification and sentiment analysis projects.",
        "duration": "14 hrs",
        "icon": "🤖",
    },
]

TESTS = {
    1: {
        "title": "Python & Data Science Test",
        "description": "Test your Python and data science fundamentals.",
        "passing_score": 70,
        "time_limit_minutes": 15,
        "questions": [
            {
                "question": "Which of the following creates a DataFrame in Pandas?",
                "options": ["pd.DataFrame()", "pd.Series()", "pd.Array()", "pd.Table()"],
                "correct_index": 0,
                "explanation": "pd.DataFrame() is the constructor for creating DataFrame objects."
            },
            {
                "question": "What does len() return for a list?",
                "options": ["The last element", "The sum of elements", "The number of elements", "The first element"],
                "correct_index": 2,
                "explanation": "len() returns the number of items in a list."
            },
            {
                "question": "Which library is used for numerical computing in Python?",
                "options": ["Matplotlib", "NumPy", "Scikit-learn", "Flask"],
                "correct_index": 1,
                "explanation": "NumPy provides fast array operations and mathematical functions."
            },
            {
                "question": "What is the output of print(type([]))?",
                "options": ["<class 'tuple'>", "<class 'dict'>", "<class 'list'>", "<class 'array'>"],
                "correct_index": 2,
                "explanation": "[] creates a list object, so type([]) returns <class 'list'>."
            },
            {
                "question": "Which keyword defines a function in Python?",
                "options": ["function", "define", "def", "func"],
                "correct_index": 2,
                "explanation": "The 'def' keyword is used to define a function in Python."
            },
        ],
    },
    2: {
        "title": "Web Development Fundamentals Test",
        "description": "Test your HTML, CSS, and JavaScript knowledge.",
        "passing_score": 70,
        "time_limit_minutes": 15,
        "questions": [
            {
                "question": "Which HTML tag links an external CSS file?",
                "options": ["<style>", "<link>", "<css>", "<script>"],
                "correct_index": 1,
                "explanation": "<link rel='stylesheet'> is used to import external CSS."
            },
            {
                "question": "What does CSS stand for?",
                "options": ["Creative Style Sheets", "Cascading Style Sheets", "Computer Style Scripts", "Coded Style System"],
                "correct_index": 1,
                "explanation": "CSS stands for Cascading Style Sheets."
            },
            {
                "question": "Which JS method selects an element by ID?",
                "options": ["document.getElement()", "document.querySelector()", "document.getElementById()", "document.findById()"],
                "correct_index": 2,
                "explanation": "getElementById() returns the element with matching ID."
            },
            {
                "question": "Correct arrow function syntax in JavaScript?",
                "options": ["function() =>", "() => {}", "=> function()", "() -> {}"],
                "correct_index": 1,
                "explanation": "Arrow functions use () => {} syntax from ES6."
            },
            {
                "question": "Which CSS property controls text size?",
                "options": ["font-weight", "text-size", "font-size", "text-style"],
                "correct_index": 2,
                "explanation": "font-size controls the size of the text."
            },
        ],
    },
    3: {
        "title": "Business Management Test",
        "description": "Test your knowledge of core management concepts.",
        "passing_score": 70,
        "time_limit_minutes": 15,
        "questions": [
            {
                "question": "Which management function involves setting organizational goals?",
                "options": ["Organizing", "Controlling", "Planning", "Directing"],
                "correct_index": 2,
                "explanation": "Planning defines goals and determines how to achieve them."
            },
            {
                "question": "SWOT stands for?",
                "options": ["Speed, Work, Output, Time", "Strengths, Weaknesses, Opportunities, Threats", "System, Work, Operations, Tasks", "Sales, Wages, Output, Targets"],
                "correct_index": 1,
                "explanation": "SWOT = Strengths, Weaknesses, Opportunities, Threats."
            },
            {
                "question": "Primary goal of Human Resource Management?",
                "options": ["Maximize profits", "Manage financial assets", "Optimize employee performance", "Control production costs"],
                "correct_index": 2,
                "explanation": "HRM focuses on recruiting, managing, and developing employees."
            },
            {
                "question": "Which leadership style gives employees maximum freedom?",
                "options": ["Autocratic", "Democratic", "Transactional", "Laissez-Faire"],
                "correct_index": 3,
                "explanation": "Laissez-Faire provides full autonomy — minimal direction from leader."
            },
            {
                "question": "The Marketing Mix (4 Ps) consists of?",
                "options": ["Price, Product, Process, People", "Product, Price, Place, Promotion", "Product, Profit, Place, Publicity", "Price, People, Position, Promotion"],
                "correct_index": 1,
                "explanation": "The 4 Ps: Product, Price, Place, and Promotion."
            },
        ],
    },
    4: {
        "title": "Accounting & Finance Test",
        "description": "Test your accounting and financial statement knowledge.",
        "passing_score": 70,
        "time_limit_minutes": 15,
        "questions": [
            {
                "question": "Which statement shows financial position at a specific point in time?",
                "options": ["Income Statement", "Cash Flow Statement", "Balance Sheet", "Statement of Equity"],
                "correct_index": 2,
                "explanation": "The Balance Sheet shows assets, liabilities and equity at a specific date."
            },
            {
                "question": "What is the accounting equation?",
                "options": ["Assets = Revenue - Expenses", "Assets = Liabilities + Equity", "Profit = Revenue + Expenses", "Assets - Equity = Revenue"],
                "correct_index": 1,
                "explanation": "Fundamental equation: Assets = Liabilities + Owner's Equity."
            },
            {
                "question": "Which of these is a current asset?",
                "options": ["Land", "Goodwill", "Accounts Receivable", "Patent"],
                "correct_index": 2,
                "explanation": "Accounts Receivable is short-term — converted to cash within a year."
            },
            {
                "question": "Depreciation is applied to?",
                "options": ["Current assets", "Fixed/Non-current assets", "Revenue", "Liabilities"],
                "correct_index": 1,
                "explanation": "Depreciation reduces the value of fixed assets over their useful life."
            },
            {
                "question": "When rent is paid in advance, it is recorded as?",
                "options": ["Rent Expense", "Accounts Payable", "Prepaid Expense", "Accrued Liability"],
                "correct_index": 2,
                "explanation": "Rent paid in advance = Prepaid Expense (a current asset)."
            },
        ],
    },
    5: {
        "title": "DSA Fundamentals Test",
        "description": "Test your data structures and algorithms knowledge.",
        "passing_score": 70,
        "time_limit_minutes": 20,
        "questions": [
            {
                "question": "Time complexity of Binary Search?",
                "options": ["O(n)", "O(n^2)", "O(log n)", "O(1)"],
                "correct_index": 2,
                "explanation": "Binary Search halves the search space each step — O(log n)."
            },
            {
                "question": "Which data structure uses LIFO order?",
                "options": ["Queue", "Stack", "Linked List", "Tree"],
                "correct_index": 1,
                "explanation": "Stack = LIFO (Last In, First Out)."
            },
            {
                "question": "Worst-case time complexity of QuickSort?",
                "options": ["O(n log n)", "O(log n)", "O(n^2)", "O(n)"],
                "correct_index": 2,
                "explanation": "QuickSort worst case O(n2) when pivot is always smallest/largest."
            },
            {
                "question": "Which traversal visits Left → Root → Right?",
                "options": ["Preorder", "Postorder", "Inorder", "Level-order"],
                "correct_index": 2,
                "explanation": "Inorder traversal: left subtree, root, right subtree."
            },
            {
                "question": "Average time complexity of hash table lookup?",
                "options": ["O(n)", "O(n log n)", "O(log n)", "O(1)"],
                "correct_index": 3,
                "explanation": "Hash tables provide O(1) average-case lookup."
            },
        ],
    },
    8: {
        "title": "SQL Database Test",
        "description": "Test your SQL and database fundamentals.",
        "passing_score": 70,
        "time_limit_minutes": 15,
        "questions": [
            {
                "question": "Which SQL clause filters records?",
                "options": ["ORDER BY", "GROUP BY", "WHERE", "HAVING"],
                "correct_index": 2,
                "explanation": "WHERE filters rows before any grouping occurs."
            },
            {
                "question": "What does JOIN do in SQL?",
                "options": ["Deletes duplicate rows", "Combines rows from two or more tables", "Creates a new table", "Updates multiple tables at once"],
                "correct_index": 1,
                "explanation": "JOIN combines rows from related tables based on a condition."
            },
            {
                "question": "Which aggregate function counts rows?",
                "options": ["SUM()", "AVG()", "COUNT()", "MAX()"],
                "correct_index": 2,
                "explanation": "COUNT() returns the number of rows matching the criteria."
            },
            {
                "question": "What is a PRIMARY KEY?",
                "options": ["A key that can have NULL values", "A column that uniquely identifies each row", "A foreign key reference", "An index on multiple columns"],
                "correct_index": 1,
                "explanation": "PRIMARY KEY uniquely identifies each record and cannot be NULL."
            },
            {
                "question": "Which command removes all rows without deleting the table?",
                "options": ["DROP TABLE", "DELETE FROM", "REMOVE ALL", "TRUNCATE"],
                "correct_index": 3,
                "explanation": "TRUNCATE removes all rows efficiently without logging individual deletions."
            },
        ],
    },
}

# Create courses
for c_data in COURSES:
    course = Course(
        id=c_data["id"],
        title=c_data["title"],
        provider=c_data["provider"],
        provider_url=c_data["provider_url"],
        category=c_data["category"],
        target_program=c_data["target_program"],
        target_years=c_data["target_years"],
        is_free=c_data["is_free"],
        description=c_data["description"],
        duration=c_data["duration"],
        icon=c_data["icon"],
    )
    course.save()
    print(f"  Created course: {course.title}")

# Create skill tests
for course_id, t_data in TESTS.items():
    try:
        course = Course.objects.get(id=course_id)
        test = SkillTest(
            course=course,
            title=t_data["title"],
            description=t_data["description"],
            passing_score=t_data["passing_score"],
            time_limit_minutes=t_data["time_limit_minutes"],
            questions=t_data["questions"],
        )
        test.save()
        print(f"  Created test: {test.title} ({len(t_data['questions'])} questions)")
    except Course.DoesNotExist:
        print(f"  Course {course_id} not found, skipping test.")

print("\nDone! Courses and skill tests seeded successfully.")
