import os
import django

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'careerbridge.settings')
django.setup()

from courses.models import Course, SkillTest

def seed_courses():
    courses_data = [
        {
            'title': 'Python Full-Stack with Django',
            'provider': 'CareerBridge Academy',
            'provider_url': 'https://careerbridge.com/bca/fullstack',
            'category': 'Web Development',
            'target_program': 'BCA',
            'target_years': [1, 2, 3],
            'description': 'A professional course overview that highlights the importance of backend logic and frontend integration in 2026.',
            'icon': '🐍',
            'questions': [
                # Python Fundamentals
                {
                    'question': 'What is the output of: print([i**2 for i in range(4) if i > 1])?',
                    'options': ['[4, 9]', '[1, 4, 9]', '[0, 1, 4]', '[1, 4]'],
                    'correct_index': 0,
                    'explanation': 'range(4) is 0,1,2,3. if i > 1 filters 2,3. squared they are 4,9.'
                },
                {
                    'question': 'Which keyword is used to handle exceptions in Python?',
                    'options': ['catch', 'handle', 'except', 'error'],
                    'correct_index': 2,
                    'explanation': 'Python uses try...except blocks for error handling.'
                },
                {
                    'question': 'What does if __name__ == "__main__": mean?',
                    'options': ['Run code only if script is executed directly', 'Import all modules', 'Define the main class', 'Start the Django server'],
                    'correct_index': 0,
                    'explanation': 'This condition ensures code inside it only runs when the file is run directly, not when imported.'
                },
                {
                    'question': 'What is the correct way to define a list in Python?',
                    'options': ['(1, 2)', '{1, 2}', '[1, 2]', '<1, 2>'],
                    'correct_index': 2,
                    'explanation': 'Square brackets [] define a list; () define a tuple; {} define a dictionary or set.'
                },
                {
                    'question': 'What will be the output of print(type([]))?',
                    'options': ["<class 'list'>", "<class 'tuple'>", "<class 'dict'>", "<class 'array'>"],
                    'correct_index': 0,
                    'explanation': 'Empty brackets [] represent a list object.'
                },
                # Django Models/Views
                {
                    'question': 'Where should you define database schema in Django?',
                    'options': ['views.py', 'urls.py', 'models.py', 'forms.py'],
                    'correct_index': 2,
                    'explanation': 'models.py defines the data structure and relationships.'
                },
                {
                    'question': 'Which function returns a rendered HTML response in a view?',
                    'options': ['send()', 'render()', 'return_html()', 'response()'],
                    'correct_index': 1,
                    'explanation': 'The render() function combines a template with a context dictionary.'
                },
                {
                    'question': 'What command is used to apply database changes?',
                    'options': ['python manage.py run', 'python manage.py migrate', 'python manage.py update', 'python manage.py save'],
                    'correct_index': 1,
                    'explanation': 'migrate applies pending migrations to the database.'
                },
                {
                    'question': 'In a Model, what does ForeignKey(on_delete=models.CASCADE) mean?',
                    'options': ['Do nothing', 'Delete child if parent is deleted', 'Set child to null', 'Protect parent from deletion'],
                    'correct_index': 1,
                    'explanation': 'CASCADE means the dependent row is deleted when the referenced row is removed.'
                },
                {
                    'question': 'How do you access URL parameters in a function-based view?',
                    'options': ['Via request.GET', 'Via arguments in the function definition', 'Via request.DATA', 'Via session'],
                    'correct_index': 1,
                    'explanation': 'Named groups in URLs are passed as arguments to the view function.'
                },
                # Database Connectivity
                {
                    'question': 'Which setting in settings.py stores database credentials?',
                    'options': ['DB_CONFIG', 'DB_SETTINGS', 'DATABASES', 'DATABASE_URL'],
                    'correct_index': 2,
                    'explanation': 'The DATABASES dictionary holds all engine and connection info.'
                },
                {
                    'question': 'What is an ORM?',
                    'options': ['Object-Relational Mapping', 'Online Response Manager', 'Optional Resource Module', 'Object Retrieval Machine'],
                    'correct_index': 0,
                    'explanation': 'ORM bridges the gap between OOP code and Relational Databases.'
                },
                {
                    'question': 'How do you retrieve all records for a model named Post?',
                    'options': ['Post.get_all()', 'Post.objects.all()', 'Post.all()', 'select * from Post'],
                    'correct_index': 1,
                    'explanation': 'Django uses managers like .objects to execute queries.'
                },
                {
                    'question': 'What is the purpose of makemigrations?',
                    'options': ['Execute SQL', 'Create migration files based on model changes', 'Seed the database', 'Backup the database'],
                    'correct_index': 1,
                    'explanation': 'It generates the instruction files for future database updates.'
                },
                {
                    'question': 'Which field is used for many-to-many relationships?',
                    'options': ['ManyToOne', 'ManyToManyField', 'MultipleKeys', 'LinkField'],
                    'correct_index': 1,
                    'explanation': 'ManyToManyField handles many-to-many links in Django.'
                },
                # Frontend Integration
                {
                    'question': 'How do you output a variable "name" in a Django template?',
                    'options': ['{% name %}', '{ name }', '{{ name }}', '[[ name ]]'],
                    'correct_index': 2,
                    'explanation': 'Double curly braces {{ }} are used for variable interpolation in Django Templates.'
                },
                {
                    'question': 'What does {% static "css/style.css" %} do?',
                    'options': ['Saves the file', 'Generates the URL for a static asset', 'Imports CSS into HTML', 'Compresses CSS'],
                    'correct_index': 1,
                    'explanation': 'The static tag helps resolve the path to assets in the static directory.'
                },
                {
                    'question': 'Which tag is used to create loops in templates?',
                    'options': ['{{ for }}', '{% for %}', '[[ for ]]', '<for>'],
                    'correct_index': 1,
                    'explanation': 'Control structures in Django use {% logic %} tags.'
                },
                {
                    'question': 'How do you include CSRF protection in a template form?',
                    'options': ['{{ csrf }}', '{% csrf_token %}', '<csrf />', 'csrf_protection=True'],
                    'correct_index': 1,
                    'explanation': 'The {% csrf_token %} tag adds a hidden input with the security token.'
                },
                {
                    'question': 'What is template inheritance?',
                    'options': ['Sharing CSS between files', 'Using {% extend %} to reuse layout structures', 'Copying HTML files', 'Automated coding'],
                    'correct_index': 1,
                    'explanation': 'Extending a base template allows children to fill specific blocks of content.'
                }
            ]
        },
        {
            'title': 'Applied AI and Agentic Systems',
            'provider': 'AI Research Lab',
            'provider_url': 'https://careerbridge.com/btech/ai',
            'category': 'Artificial Intelligence',
            'target_program': 'BTech',
            'target_years': [3, 4],
            'description': 'A detailed course description that explains how AI agents are transforming the industry, followed by five learning modules.',
            'icon': '🤖',
            'questions': [
                # Beginner (20%)
                {
                    'question': 'What differentiates an AI "Agent" from a simple "Model"?',
                    'options': ['Higher accuracy', 'Autonomy and tool-use', 'Larger data size', 'Faster processing'],
                    'correct_index': 1,
                    'explanation': 'Agents can observe their environment, reason, and take actions using tools.'
                },
                 {
                    'question': 'Which of these is an example of an uninformed search algorithm?',
                    'options': ['A*', 'Greedy Search', 'Breadth-First Search (BFS)', 'Hill Climbing'],
                    'correct_index': 2,
                    'explanation': 'BFS explores all nodes at a level without using heuristic guidance.'
                },
                 {
                    'question': 'In a neural network, what is the purpose of an activation function?',
                    'options': ['To store data', 'To introduce non-linearity', 'To multiply weights', 'To reduce memory'],
                    'correct_index': 1,
                    'explanation': 'Non-linearity allows networks to learn complex patterns beyond simple linear relationships.'
                },
                 {
                    'question': 'What does RAG stand for in AI?',
                    'options': ['Random Agent Generation', 'Retrieval-Augmented Generation', 'Recursive AI Graph', 'Rapid Access Gateway'],
                    'correct_index': 1,
                    'explanation': 'RAG combines LLMs with external data retrieval for more accurate answers.'
                },
                # Intermediate (60%)
                {
                    'question': 'What is the "Chain of Thought" (CoT) prompting technique?',
                    'options': ['Encrypted communication', 'Asking AI to show its step-by-step reasoning', 'Chaining multiple agents', 'A type of GPU architecture'],
                    'correct_index': 1,
                    'explanation': 'CoT improves performance on complex tasks by allowing the model to break down steps.'
                },
                {
                    'question': 'Explain the concept of "Agentic Loops".',
                    'options': ['Infinite code recursion', 'Continuous cycle of observation, planning, and action', 'A physical device', 'Looping through a dataset'],
                    'correct_index': 1,
                    'explanation': 'Agentic loops allow AI to iterate on a task until a goal is met or refined.'
                },
                {
                    'question': 'What is the primary advantage of A* search over Depth-First Search?',
                    'options': ['It uses less memory', 'It is guaranteed to find the shortest path if an admissible heuristic is used', 'It is faster for deep trees', 'It is easier to implement'],
                    'correct_index': 1,
                    'explanation': 'A* uses heuristics to prioritize paths likely to reach the goal efficiently.'
                },
                {
                    'question': 'In Ethical AI, what is "Algorithmic Bias"?',
                    'options': ['A math error', 'Systemic unfairness in outcomes based on data prejudices', 'High CPU usage', 'Speed differences between algorithms'],
                    'correct_index': 1,
                    'explanation': 'Bias occurs when models reflect historical or social prejudices present in training data.'
                },
                {
                    'question': 'How does a Transformer model handle sequential data differently than an RNN?',
                    'options': ['It processes one word at a time', 'It uses Attention mechanisms to process sequences in parallel', 'It cannot handle sequences', 'It uses more RAM but is slower'],
                    'correct_index': 1,
                    'explanation': 'Self-attention allows Transformers to weigh the importance of all parts of a sequence simultaneously.'
                },
                {
                    'question': 'What is "Human-in-the-Loop" (HITL) in agentic systems?',
                    'options': ['People working inside data centers', 'Human intervention at critical decision points for safety/accuracy', 'A programming language', 'Virtual reality training'],
                    'correct_index': 1,
                    'explanation': 'HITL ensures that autonomous systems remain aligned with human values and intent.'
                },
                {
                    'question': 'Which search algorithm is "Optimal" and "Complete" given a non-zero cost per step?',
                    'options': ['Greedy Search', 'Uniform Cost Search', 'Random Walk', 'DFS'],
                    'correct_index': 1,
                    'explanation': 'Uniform Cost Search (UCS) finds the least cost path if costs are positive.'
                },
                {
                    'question': 'What is "Gradient Descent" used for in AI Training?',
                    'options': ['To sort data', 'To minimize the loss function by adjusting weights', 'To increase error', 'To label images'],
                    'correct_index': 1,
                    'explanation': 'It iteratively adjusts model parameters to find the point of lowest error.'
                },
                {
                    'question': 'What is the difference between "Model-based" and "Model-free" reinforcement learning?',
                    'options': ['Storage size', 'Whether the agent learns a representation of the environment’s dynamics', 'The cost of the software', 'The speed of the internet'],
                    'correct_index': 1,
                    'explanation': 'Model-based agents try to predict what the environment will do next.'
                },
                {
                    'question': 'Identify a common risk of "Hallucination" in LLM agents.',
                    'options': ['Hardware heating', 'Generating confident but false information', 'Running out of battery', 'Deleting files'],
                    'correct_index': 1,
                    'explanation': 'Hallucination occurs when a model treats its internal correlations as factual truth erroneously.'
                },
                {
                    'question': 'What is "Turing Completeness" in the context of an AI agent using a tool like a Python REPL?',
                    'options': ['Being able to speak English', 'The ability to perform any computation a universal Turing machine can', 'Passing the Turing Test', 'Having a human face'],
                    'correct_index': 1,
                    'explanation': 'Access to code execution gives agents universal computational power.'
                },
                # Advanced (20%)
                {
                    'question': 'In the context of Multi-Agent Systems, what is the "Emergent Behavior"?',
                    'options': ['The code starting up', 'Complex patterns arising from simple interactions among agents', 'System crashes', 'Data deletion'],
                    'correct_index': 1,
                    'explanation': 'When many agents interact, they can solve problems none of them could individually.'
                },
                {
                    'question': 'Explain "AI Alignment" in the context of Superintelligence.',
                    'options': ['Arranging servers in a line', 'Ensuring an AI’s goals perfectly match human values', 'Upgrading the processor', 'Increasing the token limit'],
                    'correct_index': 1,
                    'explanation': 'Alignment is crucial to prevent autonomous systems from pursuing harmful goals.'
                },
                {
                    'question': 'What is "Auto-GPT" or "BabyAGI" primarily known for?',
                    'options': ['Photo editing', 'Autonomous goal decomposition and iterative task execution', 'Play video games', 'Social media management'],
                    'correct_index': 1,
                    'explanation': 'These systems demonstrated the first "loops" where AI assigns itself tasks.'
                },
                {
                    'question': 'Compare "Breadth-First Search" (BFS) and "Depth-First Search" (DFS) in terms of memory.',
                    'options': ['BFS uses less memory', 'DFS usually uses less memory as it only stores the current path', 'Both are equal', 'Neither needs memory'],
                    'correct_index': 1,
                    'explanation': 'BFS memory usage grows exponentially with depth to store all nodes at the current level.'
                },
                {
                    'question': 'What is a "Reward Hack" in Reinforcement Learning?',
                    'options': ['Getting a high score fairly', 'Finding a loophole to gain rewards without achieving the true goal', 'Updating the server', 'Hacking a database'],
                    'correct_index': 1,
                    'explanation': 'Agents may find shortcuts that satisfy the mathematical reward but fail the intent.'
                }
            ]
        },
        {
            'title': 'Digital Taxation and Fintech Foundations',
            'provider': 'Fintech Institute',
            'provider_url': 'https://careerbridge.com/bcom/fintech',
            'category': 'Finance',
            'target_program': 'BCom',
            'target_years': [2, 3],
            'description': 'An engaging course summary that describes how automation is changing the role of an accountant.',
            'icon': '💳',
            'questions': [
                {
                    'question': 'Scenario: A business has a turnover of 50 lakhs. Which GST registration is mandatory?',
                    'options': ['No registration', 'Composition Scheme', 'Regular Registration', 'Voluntary Registration'],
                    'correct_index': 2,
                    'explanation': 'Turnover above the threshold (usually 40L for goods) requires regular registration.'
                },
                {
                    'question': 'What is Input Tax Credit (ITC)?',
                    'options': ['Tax on income', 'Credit for tax paid on purchases used to offset tax on sales', 'A bank loan', 'Interest income'],
                    'correct_index': 1,
                    'explanation': 'ITC allows businesses to avoid double taxation by deducting tax already paid on inputs.'
                },
                {
                    'question': 'How does Tally Prime handle Bank Reconciliation?',
                    'options': ['Manual entry only', 'Importing e-statements and auto-matching entries', 'It doesn’t handle it', 'Deleting entries'],
                    'correct_index': 1,
                    'explanation': 'Tally’s auto-reconciliation feature saves time and reduces errors.'
                },
                {
                    'question': 'What is the primary function of a UPI (Unified Payments Interface)?',
                    'options': ['Currency printing', 'Real-time fund transfer between bank accounts via mobile', 'Storing physical cash', 'Stock market trading'],
                    'correct_index': 1,
                    'explanation': 'UPI enables instant peer-to-peer and peer-to-merchant transactions.'
                },
                {
                    'question': 'In Financial Analytics, what does the "Current Ratio" measure?',
                    'options': ['Profitability', 'Liquidity (ability to pay short-term debt)', 'Market share', 'Employee efficiency'],
                    'correct_index': 1,
                    'explanation': 'It compares current assets to current liabilities.'
                },
                {
                   'question': 'Which financial instrument is best for "Capital Appreciation" over 10 years?',
                   'options': ['Savings Account', 'Equities (Stocks)', 'Fixed Deposit', 'Cash'],
                   'correct_index': 1,
                   'explanation': 'Equities historically provide higher long-term growth compared to interest-bearing accounts.'
                },
                {
                    'question': 'What is an "E-Way Bill"?',
                    'options': ['An email bill', 'Electronic document for movement of goods worth over 50k', 'A digital salary slip', 'Internet recharge bill'],
                    'correct_index': 1,
                    'explanation': 'E-Way bills are mandatory for transporting goods above specified values under GST.'
                },
                {
                    'question': 'What is "DeFi" in Fintech?',
                    'options': ['Deficit Finance', 'Decentralized Finance (Blockchain-based)', 'Department of Finance', 'Deferred Fintech'],
                    'correct_index': 1,
                    'explanation': 'DeFi aims to provide financial services without central intermediaries like banks.'
                },
                {
                    'question': 'Why is "Data Visualization" important for a modern Accountant?',
                    'options': ['It looks pretty', 'To spot trends and anomalies that manual sheets miss', 'To replace the need for math', 'To slow down reports'],
                    'correct_index': 1,
                    'explanation': 'Visual tools like PowerBI help accountants provide strategic insights.'
                },
                {
                    'question': 'What is "Double Entry Bookkeeping"?',
                    'options': ['Entering data twice', 'Every transaction affects at least two accounts (Debit/Credit)', 'Keeping two separate books', 'Writing in pencil then pen'],
                    'correct_index': 1,
                    'explanation': 'It ensures the accounting equation Assets = Liabilities + Equity remains balanced.'
                },
                {
                    'question': 'Which of these is a "Liability" in a Balance Sheet?',
                    'options': ['Cash in Hand', 'Accounts Payable', 'Machinery', 'Inventory'],
                    'correct_index': 1,
                    'explanation': 'Accounts Payable is money owed to suppliers, hence a liability.'
                },
                {
                    'question': 'What happens if a business misses the GST filing deadline?',
                    'options': ['Nothing', 'Late fees and interest on tax liability', 'Immediate jail', 'Free tax refund'],
                    'correct_index': 1,
                    'explanation': 'Delayed filing attracts pecuniary penalties and interest under GST law.'
                },
                {
                    'question': 'What is "Financial Modeling"?',
                    'options': ['Fashion for bankers', 'Building abstract representations of a company’s financial performance', 'Painting a bank', 'Selling insurance'],
                    'correct_index': 1,
                    'explanation': 'Models help in forecasting future performance and valuation.'
                },
                {
                    'question': 'What is "Direct Tax"?',
                    'options': ['GST', 'Income Tax paid by the person on whom it is levied', 'Tax on luxury goods', 'Entertainment tax'],
                    'correct_index': 1,
                    'explanation': 'Income tax is a direct tax; GST is an indirect tax.'
                },
                {
                    'question': 'In Fintech, what is a "Neo-Bank"?',
                    'options': ['A very old bank', 'A digital-only bank with no physical branches', 'A bank for robots', 'A government building'],
                    'correct_index': 1,
                    'explanation': 'Neo-banks operate entirely online, offering streamlined digital services.'
                },
                {
                    'question': 'What does "TDS" stand for?',
                    'options': ['Total Debt Service', 'Tax Deducted at Source', 'Time Data Sheet', 'Tax Deposit System'],
                    'correct_index': 1,
                    'explanation': 'TDS is a mechanism where tax is collected at the point of income generation.'
                },
                {
                    'question': 'Scenario: You want to save for a goal in 2 years with "Zero Risk". Which is best?',
                    'options': ['Crypto', 'Fixed Deposit', 'Penny Stocks', 'Gold Futures'],
                    'correct_index': 1,
                    'explanation': 'Fixed Deposits are generally low-risk and guaranteed in terms of returns.'
                },
                {
                    'question': 'What is the "Golden Rule" for Real Accounts?',
                    'options': ['Debit the receiver, Credit the giver', 'Debit what comes in, Credit what goes out', 'Debit expenses, Credit income', 'Ignore the rules'],
                    'correct_index': 1,
                    'explanation': 'This rule applies to assets like cash, furniture, etc.'
                },
                {
                    'question': 'What is "InsurTech"?',
                    'options': ['Insuring technology', 'Using tech to improve the insurance industry', 'Technical insurance', 'A new computer brand'],
                    'correct_index': 1,
                    'explanation': 'InsurTech uses data and mobile apps to provide personalized insurance.'
                },
                {
                    'question': 'What is an "Audit Trail" in Tally?',
                    'options': ['A physical path', 'A chronological record of all changes made to a transaction', 'A list of employees', 'A map of the office'],
                    'correct_index': 1,
                    'explanation': 'Audit trails are now mandatory for security and compliance tracking.'
                }
            ]
        },
        {
            'title': 'Data-Driven Human Resource Management',
            'provider': 'Leadership Academy',
            'provider_url': 'https://careerbridge.com/bba/hr',
            'category': 'Management',
            'target_program': 'BBA',
            'target_years': [1, 2, 3],
            'description': 'A compelling course introduction focusing on how data analytics is used to improve employee retention and hiring.',
            'icon': '📈',
            'questions': [
                # Dilemmas & Situational (50%)
                {
                    'question': 'Situational: A top performer is suddenly showing low engagement in their surveys. What is the best first step?',
                    'options': ['Terminate them', 'Ignore it (they are still performing)', 'Conduct a 1-on-1 "Stay Interview" to identify pain points', 'Give them a raise immediately'],
                    'correct_index': 2,
                    'explanation': 'Understanding the "Why" before taking action is key to retention.'
                },
                 {
                    'question': 'What is "Employee Attrition"?',
                    'options': ['Hiring new people', 'The rate at which employees leave the organization', 'Training employees', 'Employee salary'],
                    'correct_index': 1,
                    'explanation': 'High attrition levels can signal underlying culture or management issues.'
                },
                 {
                    'question': 'Situational: You have two candidates with identical experience. Candidate A has a higher score in the "Cultural Fit" assessment. Who do you hire?',
                    'options': ['Candidate A', 'Candidate B', 'Flip a coin', 'Re-interview both'],
                    'correct_index': 0,
                    'explanation': 'Cultural fit often predicts long-term retention and team harmony better than skills alone.'
                },
                {
                    'question': 'What does "Cost-per-Hire" measure?',
                    'options': ['Total salary of a new hire', 'Total recruiting expenses divided by number of hires', 'Cost of training', 'Office rent per person'],
                    'correct_index': 1,
                    'explanation': 'This metric helps optimize recruitment budget efficiency.'
                },
                {
                    'question': 'Situational: An employee consistently misses deadlines but produces exceptional work. HR should suggest:',
                    'options': ['Strict warning', 'A flexible schedule or performance-based timeline instead of fixed hours', 'Moving them to a different team', 'Decreasing their pay'],
                    'correct_index': 1,
                    'explanation': 'Modern HR focuses on output-based management for specialized talent.'
                },
                {
                    'question': 'What is "People Analytics"?',
                    'options': ['Counting employees', 'Applying statistics to HR data to improve business outcomes', 'Psychology', 'Writing job descriptions'],
                    'correct_index': 1,
                    'explanation': 'Analytics transform raw HR data into actionable business intelligence.'
                },
                {
                    'question': 'Situational: Your data shows that employees who work remotely are 20% more productive. Leadership wants to end WFH. What do you do?',
                    'options': ['Follow orders', 'Present the productivity data to justify a hybrid model', 'Quit the job', 'Tell employees to work harder in office'],
                    'correct_index': 1,
                    'explanation': 'Data-driven HR leaders advocate for strategy based on evidence, not intuition.'
                },
                {
                    'question': 'What is a "360-Degree Feedback"?',
                    'options': ['A circle in the office', 'Feedback from supervisors, peers, and subordinates', 'A very long review', 'Turning around while talking'],
                    'correct_index': 1,
                    'explanation': 'It provides a holistic view of an employee’s behavior and performance.'
                },
                {
                    'question': 'Situational: Diverse teams in your company are outperforming non-diverse ones. How do you use this info?',
                    'options': ['Do nothing', 'Implement Diversity, Equity, and Inclusion (DEI) initiatives to drive growth', 'Keep it secret', 'Hire only one type of person'],
                    'correct_index': 1,
                    'explanation': 'Diversity is a proven driver of innovation and improved decision-making.'
                },
                {
                    'question': 'What is "Employee Engagement"?',
                    'options': ['An office party', 'The emotional commitment an employee has to the organization', 'A marriage in the office', 'Working 12 hours a day'],
                    'correct_index': 1,
                    'explanation': 'High engagement leads to lower turnover and higher productivity.'
                },
                {
                    'question': 'What is "Onboarding"?',
                    'options': ['Going on a boat', 'The process of integrating a new employee into the company', 'Buying a new board', 'Closing the office'],
                    'correct_index': 1,
                    'explanation': 'Effective onboarding reduces the time-to-productivity for new hires.'
                },
                {
                    'question': 'Situational: Data reveals a high dropout rate during the online application process. What should you recommend?',
                    'options': ['Hire more recruiters', 'Simplify the application form and improve UX', 'Ignore it', 'Make the test harder'],
                    'correct_index': 1,
                    'explanation': 'Reducing "friction" in the application funnel increases the talent pool.'
                },
                {
                    'question': 'What is "Succession Planning"?',
                    'options': ['Planning for a party', 'Identifying and developing new leaders to replace old ones', 'Winning a lottery', 'Ending a business'],
                    'correct_index': 1,
                    'explanation': 'It ensures continuity in leadership roles.'
                },
                {
                    'question': 'Situational: An AI tool flags a resume for a typo. The candidate has a PhD and 20 years experience. Do you reject them?',
                    'options': ['Yes (attention to detail is key)', 'No (human overrides AI when context matters)', 'Maybe', 'Ask the AI again'],
                    'correct_index': 1,
                    'explanation': 'AI is a filtering tool, but human judgment handles nuances like relative value.'
                },
                {
                    'question': 'What is the "Bell Curve" in performance appraisals?',
                    'options': ['A type of bell', 'A distribution where most employees are "Average"', 'A music tool', 'A type of training'],
                    'correct_index': 1,
                    'explanation': 'It categorizes employees into top, middle, and bottom performers.'
                },
                {
                    'question': 'Situational: A team lead is toxic but meets all sales targets. What does HR suggest?',
                    'options': ['Promotion', 'Coaching or removal (toxic culture causes long-term cost via attrition)', 'Ignore the toxicity', 'Reduce their targets'],
                    'correct_index': 1,
                    'explanation': 'The cost of a "brilliant jerk" often outweighs their sales output through team damage.'
                },
                {
                    'question': 'What is "Employer Branding"?',
                    'options': ['A logo on a shirt', 'The reputation of the organization as a place to work', 'Naming the company', 'A building sign'],
                    'correct_index': 1,
                    'explanation': 'A strong brand attracts high-quality talent naturally.'
                },
                {
                    'question': 'What is "Human Capital"?',
                    'options': ['Money in the bank', 'The skills, knowledge, and experience of the workforce', 'A human city', 'Office supplies'],
                    'correct_index': 1,
                    'explanation': 'Investing in people increases the intellectual assets of the firm.'
                },
                {
                    'question': 'Situational: You need to reduce staff. Do you cut by "Last In First Out" (LIFO) or "Performance Score"?',
                    'options': ['LIFO', 'Performance Score (retain the best for recovery)', 'Randomly', 'Cut the highest paid'],
                    'correct_index': 1,
                    'explanation': 'Data-driven downsizing aims to keep the core expertise needed to rebuild.'
                },
                {
                    'question': 'What is "Gamification" in HR?',
                    'options': ['Playing video games at work', 'Using game elements in training/hiring to increase engagement', 'Buying a console', 'Hiring gamers'],
                    'correct_index': 1,
                    'explanation': 'Gamification makes tedious processes like training more interactive.'
                }
            ]
        }
    ]

    for data in courses_data:
        questions = data.pop('questions')
        course, created = Course.objects.update_or_create(
            title=data['title'],
            defaults=data
        )
        
        # Add SkillTest
        test, t_created = SkillTest.objects.update_or_create(
            course=course,
            defaults={
                'title': f"{course.title} - Final Assessment",
                'description': f"Test your knowledge of {course.title}.",
                'questions': questions,
                'passing_score': 70
            }
        )
        
        print(f"Course: {course.title} | Test: {'Created' if t_created else 'Updated'}")

if __name__ == '__main__':
    seed_courses()
