# career/job_roles.py

JOB_ROLES = {

    # ════════════════════════════════
    # 1. FRONTEND DEVELOPER
    # ════════════════════════════════
    "Frontend Developer": {
        "emoji": "🎨",
        "description": "Build beautiful, responsive web interfaces",
        "foundation_skills": {
            "languages": ["JavaScript", "HTML", "CSS", "TypeScript"],
            "frameworks": ["React", "Vue", "Angular"],
            "tools": ["Git", "npm", "Webpack", "Vite"]
        },
        "modern_2026_skills": {
            "ai_tools": ["GitHub Copilot", "V0", "Cursor"],
            "frameworks": ["Next.js", "Remix", "Astro"],
            "skills": ["AI Integration", "LLM APIs", "Web Components"],
            "testing": ["Jest", "Cypress", "Playwright"]
        },
        "repo_keywords": ["react", "vue", "angular", "frontend", "ui", "web", "portfolio", "nextjs"],
        "min_repos": 3,
        "min_stars": 5,
    },

    # ════════════════════════════════
    # 2. BACKEND DEVELOPER
    # ════════════════════════════════
    "Backend Developer": {
        "emoji": "⚙️",
        "description": "Build powerful APIs and server-side systems",
        "foundation_skills": {
            "languages": ["Python", "Java", "Go", "Node.js", "PHP", "Ruby"],
            "frameworks": ["Django", "FastAPI", "Spring", "Express"],
            "tools": ["Git", "Docker", "PostgreSQL", "MySQL", "Redis"]
        },
        "modern_2026_skills": {
            "ai_tools": ["GitHub Copilot", "Cursor"],
            "frameworks": ["FastAPI", "tRPC"],
            "skills": ["RAG Systems", "Vector Databases", "LLM Integration", "Microservices"],
            "testing": ["pytest", "JUnit", "Postman"]
        },
        "repo_keywords": ["api", "backend", "server", "django", "fastapi", "express", "rest"],
        "min_repos": 3,
        "min_stars": 5,
    },

    # ════════════════════════════════
    # 3. FULL STACK DEVELOPER
    # ════════════════════════════════
    "Full Stack Developer": {
        "emoji": "🌐",
        "description": "Master both frontend and backend development",
        "foundation_skills": {
            "languages": ["JavaScript", "TypeScript", "Python", "HTML", "CSS"],
            "frameworks": ["React", "Node.js", "Express", "Django"],
            "tools": ["Git", "Docker", "PostgreSQL", "MongoDB"]
        },
        "modern_2026_skills": {
            "ai_tools": ["GitHub Copilot", "V0", "Cursor"],
            "frameworks": ["Next.js", "FastAPI", "tRPC"],
            "skills": ["AI Integration", "RAG", "Vector DBs", "Serverless"],
            "testing": ["Jest", "pytest", "Cypress"]
        },
        "repo_keywords": ["fullstack", "full-stack", "mern", "mean", "nextjs", "webapp"],
        "min_repos": 4,
        "min_stars": 8,
    },

    # ════════════════════════════════
    # 4. ML/AI ENGINEER
    # ════════════════════════════════
    "ML/AI Engineer": {
        "emoji": "🤖",
        "description": "Build intelligent ML models and AI systems",
        "foundation_skills": {
            "languages": ["Python", "R", "Julia"],
            "frameworks": ["Scikit-learn", "TensorFlow", "PyTorch", "Keras"],
            "tools": ["Jupyter", "Git", "NumPy", "Pandas", "Matplotlib"]
        },
        "modern_2026_skills": {
            "ai_tools": ["GitHub Copilot", "Cursor"],
            "frameworks": ["LangChain", "LlamaIndex", "Hugging Face"],
            "skills": ["LLM Fine-tuning", "RAG", "AI Agents", "Prompt Engineering", "MLOps"],
            "testing": ["MLflow", "Weights & Biases"]
        },
        "repo_keywords": ["machine-learning", "deep-learning", "ai", "nlp", "computer-vision", "llm", "pytorch"],
        "min_repos": 3,
        "min_stars": 5,
    },

    # ════════════════════════════════
    # 5. DATA SCIENTIST
    # ════════════════════════════════
    "Data Scientist": {
        "emoji": "📊",
        "description": "Extract insights from data using statistics and ML",
        "foundation_skills": {
            "languages": ["Python", "R", "SQL"],
            "frameworks": ["Pandas", "NumPy", "Scikit-learn", "Matplotlib", "Seaborn"],
            "tools": ["Jupyter", "Tableau", "Power BI", "Excel"]
        },
        "modern_2026_skills": {
            "ai_tools": ["GitHub Copilot", "Julius AI"],
            "frameworks": ["LangChain", "Hugging Face", "Streamlit"],
            "skills": ["LLM-powered Analytics", "AutoML", "AI Dashboards", "Real-time Analytics"],
            "testing": ["Great Expectations", "dbt"]
        },
        "repo_keywords": ["data-science", "analysis", "visualization", "statistics", "pandas", "jupyter"],
        "min_repos": 3,
        "min_stars": 5,
    },

    # ════════════════════════════════
    # 6. DEVOPS ENGINEER
    # ════════════════════════════════
    "DevOps Engineer": {
        "emoji": "🛠️",
        "description": "Automate infrastructure and deployment pipelines",
        "foundation_skills": {
            "languages": ["Shell", "Python", "YAML", "Go"],
            "frameworks": ["Docker", "Kubernetes", "Terraform", "Ansible"],
            "tools": ["Git", "Jenkins", "GitHub Actions", "Linux"]
        },
        "modern_2026_skills": {
            "ai_tools": ["GitHub Copilot", "Cursor"],
            "frameworks": ["ArgoCD", "Flux", "Pulumi"],
            "skills": ["LLMOps", "AI-assisted CI/CD", "FinOps", "Platform Engineering"],
            "testing": ["Terratest", "k6"]
        },
        "repo_keywords": ["devops", "docker", "kubernetes", "ci-cd", "terraform", "ansible", "infrastructure"],
        "min_repos": 3,
        "min_stars": 5,
    },

    # ════════════════════════════════
    # 7. ANDROID DEVELOPER
    # ════════════════════════════════
    "Android Developer": {
        "emoji": "📱",
        "description": "Build native Android mobile applications",
        "foundation_skills": {
            "languages": ["Kotlin", "Java"],
            "frameworks": ["Android SDK", "Jetpack Compose", "Room", "Retrofit"],
            "tools": ["Android Studio", "Git", "Gradle", "Firebase"]
        },
        "modern_2026_skills": {
            "ai_tools": ["GitHub Copilot", "Android Studio AI"],
            "frameworks": ["Jetpack Compose", "KMM"],
            "skills": ["On-device AI", "ML Kit", "Gemini API", "AI Features Integration"],
            "testing": ["JUnit", "Espresso", "Mockito"]
        },
        "repo_keywords": ["android", "kotlin", "jetpack", "compose", "mobile", "app"],
        "min_repos": 2,
        "min_stars": 3,
    },

    # ════════════════════════════════
    # 8. IOS DEVELOPER
    # ════════════════════════════════
    "iOS Developer": {
        "emoji": "🍎",
        "description": "Build native iOS applications for Apple ecosystem",
        "foundation_skills": {
            "languages": ["Swift", "Objective-C"],
            "frameworks": ["UIKit", "SwiftUI", "CoreData", "AVFoundation"],
            "tools": ["Xcode", "Git", "CocoaPods", "TestFlight"]
        },
        "modern_2026_skills": {
            "ai_tools": ["GitHub Copilot", "Xcode AI"],
            "frameworks": ["SwiftUI", "CreateML"],
            "skills": ["On-device AI", "Core ML", "Vision Framework", "Apple Intelligence APIs"],
            "testing": ["XCTest", "XCUITest"]
        },
        "repo_keywords": ["ios", "swift", "swiftui", "apple", "iphone", "xcode"],
        "min_repos": 2,
        "min_stars": 3,
    },

    # ════════════════════════════════
    # 9. CLOUD ENGINEER
    # ════════════════════════════════
    "Cloud Engineer": {
        "emoji": "☁️",
        "description": "Design and manage cloud infrastructure at scale",
        "foundation_skills": {
            "languages": ["Python", "Shell", "YAML", "Go"],
            "frameworks": ["AWS", "Azure", "GCP", "Terraform"],
            "tools": ["Docker", "Kubernetes", "Git", "Linux"]
        },
        "modern_2026_skills": {
            "ai_tools": ["GitHub Copilot", "AWS CodeWhisperer"],
            "frameworks": ["Pulumi", "CDK"],
            "skills": ["AI Cloud Services", "LLMOps", "FinOps", "Multi-cloud", "Serverless AI"],
            "testing": ["Terratest", "CloudFormation Guard"]
        },
        "repo_keywords": ["cloud", "aws", "azure", "gcp", "terraform", "serverless", "infrastructure"],
        "min_repos": 3,
        "min_stars": 5,
    },

    # ════════════════════════════════
    # 10. BLOCKCHAIN DEVELOPER
    # ════════════════════════════════
    "Blockchain Developer": {
        "emoji": "⛓️",
        "description": "Build decentralized applications and smart contracts",
        "foundation_skills": {
            "languages": ["Solidity", "JavaScript", "Python", "Rust"],
            "frameworks": ["Ethereum", "Web3.js", "Ethers.js", "Hardhat"],
            "tools": ["MetaMask", "Truffle", "Git", "IPFS"]
        },
        "modern_2026_skills": {
            "ai_tools": ["GitHub Copilot"],
            "frameworks": ["Foundry", "Anchor (Solana)"],
            "skills": ["AI + Blockchain", "ZK Proofs", "DeFi 2.0", "Cross-chain", "Account Abstraction"],
            "testing": ["Hardhat Tests", "Foundry Tests", "Slither"]
        },
        "repo_keywords": ["blockchain", "solidity", "web3", "defi", "nft", "ethereum", "smart-contract"],
        "min_repos": 2,
        "min_stars": 3,
    },

    # ════════════════════════════════
    # 11. CYBERSECURITY ENGINEER
    # ════════════════════════════════
    "Cybersecurity Engineer": {
        "emoji": "🔐",
        "description": "Protect systems and networks from cyber threats",
        "foundation_skills": {
            "languages": ["Python", "Shell", "C", "PowerShell"],
            "frameworks": ["Metasploit", "Burp Suite", "Wireshark", "Nmap"],
            "tools": ["Kali Linux", "Git", "OWASP", "Nessus"]
        },
        "modern_2026_skills": {
            "ai_tools": ["GitHub Copilot"],
            "frameworks": ["AI-powered SIEM"],
            "skills": ["AI Threat Detection", "LLM Security", "Zero Trust", "Prompt Injection Defense"],
            "testing": ["OWASP ZAP", "Nuclei", "Semgrep"]
        },
        "repo_keywords": ["security", "cybersecurity", "pentesting", "ctf", "malware", "forensics", "hacking"],
        "min_repos": 2,
        "min_stars": 3,
    },

    # ════════════════════════════════
    # 12. QA ENGINEER
    # ════════════════════════════════
    "QA Engineer": {
        "emoji": "🧪",
        "description": "Ensure software quality through testing and automation",
        "foundation_skills": {
            "languages": ["Python", "JavaScript", "Java"],
            "frameworks": ["Selenium", "Cypress", "JUnit", "TestNG"],
            "tools": ["Git", "Jira", "Postman", "Jenkins"]
        },
        "modern_2026_skills": {
            "ai_tools": ["GitHub Copilot", "Testim AI"],
            "frameworks": ["Playwright", "k6"],
            "skills": ["AI Test Generation", "Self-healing Tests", "LLM Testing", "Chaos Engineering"],
            "testing": ["Playwright", "k6", "Pact"]
        },
        "repo_keywords": ["testing", "automation", "qa", "selenium", "cypress", "playwright", "jest"],
        "min_repos": 2,
        "min_stars": 3,
    },

    # ════════════════════════════════
    # 13. DATA ENGINEER
    # ════════════════════════════════
    "Data Engineer": {
        "emoji": "🔧",
        "description": "Build data pipelines and infrastructure at scale",
        "foundation_skills": {
            "languages": ["Python", "SQL", "Scala", "Java"],
            "frameworks": ["Apache Spark", "Airflow", "Kafka", "dbt"],
            "tools": ["Git", "Docker", "PostgreSQL", "Snowflake"]
        },
        "modern_2026_skills": {
            "ai_tools": ["GitHub Copilot"],
            "frameworks": ["dbt", "Dagster", "Prefect"],
            "skills": ["LLM Pipelines", "Vector DBs", "Real-time AI", "Data Mesh", "AI Data Quality"],
            "testing": ["Great Expectations", "dbt tests", "Soda"]
        },
        "repo_keywords": ["data-engineering", "pipeline", "etl", "spark", "airflow", "kafka", "dbt"],
        "min_repos": 2,
        "min_stars": 3,
    },

    # ════════════════════════════════
    # 14. GAME DEVELOPER
    # ════════════════════════════════
    "Game Developer": {
        "emoji": "🎮",
        "description": "Create engaging games for multiple platforms",
        "foundation_skills": {
            "languages": ["C#", "C++", "Python", "GDScript"],
            "frameworks": ["Unity", "Unreal Engine", "Godot"],
            "tools": ["Git", "Blender", "Photoshop", "FMOD"]
        },
        "modern_2026_skills": {
            "ai_tools": ["GitHub Copilot"],
            "frameworks": ["Unity AI", "Unreal MetaHuman"],
            "skills": ["Procedural AI", "NPC AI", "AI Game Assets", "Generative AI in Games"],
            "testing": ["Unity Test Framework", "Playmode Tests"]
        },
        "repo_keywords": ["game", "unity", "unreal", "godot", "pygame", "gamedev", "2d", "3d"],
        "min_repos": 2,
        "min_stars": 3,
    },

    # ════════════════════════════════
    # 15. EMBEDDED SYSTEMS ENGINEER
    # ════════════════════════════════
    "Embedded Systems Engineer": {
        "emoji": "🔌",
        "description": "Program microcontrollers and embedded hardware",
        "foundation_skills": {
            "languages": ["C", "C++", "Assembly", "Python"],
            "frameworks": ["FreeRTOS", "Zephyr", "Arduino", "ESP-IDF"],
            "tools": ["Git", "Keil", "STM32CubeIDE", "Oscilloscope"]
        },
        "modern_2026_skills": {
            "ai_tools": ["GitHub Copilot"],
            "frameworks": ["TensorFlow Lite", "Edge Impulse"],
            "skills": ["TinyML", "Edge AI", "RTOS AI", "IoT AI Integration"],
            "testing": ["Unity Test", "Ceedling", "Hardware-in-loop"]
        },
        "repo_keywords": ["embedded", "arduino", "raspberry-pi", "iot", "microcontroller", "firmware", "rtos"],
        "min_repos": 2,
        "min_stars": 3,
    },
}


# ✅ Helper Functions
def get_all_roles():
    return list(JOB_ROLES.keys())

def get_role_info(role_name):
    return JOB_ROLES.get(role_name, {})

def get_role_emojis():
    return {role: info["emoji"] for role, info in JOB_ROLES.items()}


# ✅ Test
if __name__ == "__main__":
    print(f"Total Job Roles: {len(JOB_ROLES)}")
    for role, info in JOB_ROLES.items():
        print(f"{info['emoji']} {role}")