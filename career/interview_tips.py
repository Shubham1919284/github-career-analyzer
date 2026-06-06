# career/interview_tips.py

INTERVIEW_TIPS = {

    "Frontend Developer": {
        "common_questions": [
            "Explain the difference between var, let, and const",
            "What is the Virtual DOM in React?",
            "How does CSS specificity work?",
            "What are React hooks and why were they introduced?",
            "Explain event bubbling and capturing",
            "What is TypeScript and why use it over JavaScript?",
            "How do you optimize React app performance?",
            "What is SSR vs CSR vs SSG?",
            "Explain CORS and how to handle it",
            "What are Web Vitals and why do they matter?",
        ],
        "what_companies_look_for_2026": [
            "TypeScript proficiency — JavaScript alone is not enough",
            "AI tool experience — GitHub Copilot, Cursor, V0",
            "Next.js knowledge — React alone is becoming outdated",
            "Testing skills — Jest, Cypress, or Playwright",
            "Performance optimization knowledge",
            "Ability to integrate LLM APIs into UI",
        ],
        "common_mistakes": [
            "Only knowing React without understanding JavaScript deeply",
            "No TypeScript experience",
            "Zero testing in projects",
            "Not knowing how browsers work",
            "Ignoring accessibility (a11y)",
        ],
        "portfolio_tips": [
            "Deploy ALL projects — undeployed projects are invisible",
            "Add live demo links in every README",
            "Include a project that uses an AI API",
            "Show responsive design in every project",
            "Write clean, commented code — interviewers check source code",
        ],
        "resources": [
            {"title": "Frontend Interview Questions", "url": "https://github.com/sudheerj/reactjs-interview-questions"},
            {"title": "JavaScript Interview Prep", "url": "https://www.greatfrontend.com"},
            {"title": "roadmap.sh/frontend", "url": "https://roadmap.sh/frontend"},
        ]
    },

    "Backend Developer": {
        "common_questions": [
            "What is REST vs GraphQL vs gRPC?",
            "Explain database indexing and when to use it",
            "What is the difference between SQL and NoSQL?",
            "How does authentication work with JWT?",
            "What are microservices and when to use them?",
            "Explain CAP theorem",
            "What is Redis and when do you use caching?",
            "How do you handle race conditions?",
            "What is database sharding?",
            "Explain ACID properties",
        ],
        "what_companies_look_for_2026": [
            "LLM/AI API integration experience",
            "RAG system knowledge",
            "Vector database understanding",
            "Microservices architecture",
            "Docker + Kubernetes basics",
            "System design skills",
        ],
        "common_mistakes": [
            "No understanding of database optimization",
            "Not knowing how to handle async operations",
            "Missing security knowledge (SQL injection, XSS)",
            "No Docker knowledge",
            "Cannot explain their own system design",
        ],
        "portfolio_tips": [
            "Include a project with proper authentication",
            "Show API documentation (Swagger/OpenAPI)",
            "Add a project with database migrations",
            "Include at least 1 AI-integrated API",
            "Write tests for your APIs",
        ],
        "resources": [
            {"title": "System Design Primer", "url": "https://github.com/donnemartin/system-design-primer"},
            {"title": "Backend Roadmap", "url": "https://roadmap.sh/backend"},
            {"title": "Backend Interview Questions", "url": "https://github.com/arialdomartini/Back-End-Developer-Interview-Questions"},
        ]
    },

    "Full Stack Developer": {
        "common_questions": [
            "How do you structure a full stack application?",
            "Explain the difference between monorepo and polyrepo",
            "How do you handle authentication across frontend and backend?",
            "What is tRPC and when would you use it?",
            "How do you manage state in a large React application?",
            "Explain the concept of API design and versioning",
            "What is server-side rendering and when should you use it?",
            "How do you handle database migrations in production?",
            "What is the difference between WebSockets and HTTP?",
            "How do you approach debugging a full stack issue?",
        ],
        "what_companies_look_for_2026": [
            "Next.js + FastAPI or Node.js full stack proficiency",
            "AI feature integration across the full stack",
            "TypeScript everywhere — frontend and backend",
            "Docker containerization and basic cloud deployment",
            "Database design skills (SQL + NoSQL)",
            "Real-time features (WebSockets, SSE)",
        ],
        "common_mistakes": [
            "Only knowing one side well (only frontend or only backend)",
            "No deployment experience — can't get to production",
            "Ignoring security across the full stack",
            "No database design knowledge",
            "Cannot explain their architecture choices",
        ],
        "portfolio_tips": [
            "Build complete apps — not just frontend or just backend",
            "Deploy with a real domain, not just localhost",
            "Show the architecture diagram in your README",
            "Include an AI-powered feature in your full stack project",
            "Show your API documentation alongside the UI",
        ],
        "resources": [
            {"title": "Full Stack Open", "url": "https://fullstackopen.com"},
            {"title": "roadmap.sh/full-stack", "url": "https://roadmap.sh/full-stack"},
            {"title": "The Odin Project", "url": "https://www.theodinproject.com"},
        ]
    },

    "ML/AI Engineer": {
        "common_questions": [
            "Explain bias-variance tradeoff",
            "What is overfitting and how do you prevent it?",
            "Difference between supervised and unsupervised learning",
            "What is a transformer architecture?",
            "Explain RAG (Retrieval Augmented Generation)",
            "What are embeddings and vector databases?",
            "How do you fine-tune an LLM?",
            "What is prompt engineering?",
            "Explain gradient descent",
            "What metrics do you use for classification problems?",
        ],
        "what_companies_look_for_2026": [
            "LLM fine-tuning experience",
            "RAG system implementation",
            "AI agent building (LangChain/LangGraph)",
            "MLOps knowledge (MLflow, DVC)",
            "Vector database experience",
            "Production ML deployment",
        ],
        "common_mistakes": [
            "Only theoretical knowledge, no deployed projects",
            "Not knowing how transformers work",
            "No MLOps or deployment knowledge",
            "Cannot explain model choices",
            "No knowledge of LLMs and prompt engineering",
        ],
        "portfolio_tips": [
            "Include a deployed ML model with UI",
            "Show a RAG-based project",
            "Add an AI agent project",
            "Include experiment tracking (MLflow)",
            "Show your Kaggle/HuggingFace profile",
        ],
        "resources": [
            {"title": "ML Interview Questions", "url": "https://github.com/khangich/machine-learning-interview"},
            {"title": "Andrej Karpathy YouTube", "url": "https://www.youtube.com/@AndrejKarpathy"},
            {"title": "HuggingFace Course", "url": "https://huggingface.co/learn/nlp-course"},
        ]
    },

    "Data Scientist": {
        "common_questions": [
            "What is the difference between correlation and causation?",
            "Explain p-value and statistical significance",
            "How do you handle missing data?",
            "What is cross-validation and why use it?",
            "Explain the difference between bagging and boosting",
            "How do you choose the right ML algorithm for a problem?",
            "What is feature engineering and why is it important?",
            "Explain dimensionality reduction (PCA, t-SNE)",
            "How do you evaluate a classification model?",
            "What is A/B testing and how do you design one?",
        ],
        "what_companies_look_for_2026": [
            "LLM-powered analytics and NLP skills",
            "AutoML and AI-assisted data analysis",
            "Real-time data processing and streaming",
            "Strong SQL + Python fundamentals",
            "Data storytelling and visualization skills",
            "Cloud data platform experience (Snowflake, BigQuery)",
        ],
        "common_mistakes": [
            "Cannot clean and prepare messy real-world data",
            "Only knows theory, no hands-on Kaggle/project experience",
            "Cannot communicate findings to non-technical stakeholders",
            "Ignores statistical assumptions when applying models",
            "No SQL knowledge — mandatory for data access",
        ],
        "portfolio_tips": [
            "Show end-to-end projects: data → insight → action",
            "Include visualizations and storytelling, not just code",
            "Add at least one Kaggle competition notebook",
            "Include a project with real business impact",
            "Use Streamlit or Gradio to demo your models",
        ],
        "resources": [
            {"title": "Kaggle Learn", "url": "https://www.kaggle.com/learn"},
            {"title": "roadmap.sh/data-scientist", "url": "https://roadmap.sh/data-scientist"},
            {"title": "StatQuest YouTube", "url": "https://www.youtube.com/@statquest"},
        ]
    },

    "DevOps Engineer": {
        "common_questions": [
            "Explain CI/CD pipeline from scratch",
            "What is Docker and how does it differ from a VM?",
            "Explain Kubernetes architecture",
            "What is Infrastructure as Code?",
            "How do you handle secrets management?",
            "What is GitOps?",
            "Explain blue-green deployment",
            "What monitoring tools have you used?",
            "How do you handle a production incident?",
            "What is service mesh?",
        ],
        "what_companies_look_for_2026": [
            "Kubernetes + Helm proficiency",
            "GitOps with ArgoCD/Flux",
            "IaC with Terraform or Pulumi",
            "Platform engineering mindset",
            "AIOps awareness",
            "FinOps basics",
        ],
        "common_mistakes": [
            "Only knowing Docker without Kubernetes",
            "No IaC experience",
            "Cannot explain CI/CD from scratch",
            "No monitoring/observability knowledge",
            "Ignoring security in pipelines",
        ],
        "portfolio_tips": [
            "Show a complete CI/CD pipeline in GitHub",
            "Include Terraform code for infrastructure",
            "Add monitoring dashboards (Grafana screenshots)",
            "Document your architecture decisions",
            "Show a Kubernetes deployment config",
        ],
        "resources": [
            {"title": "DevOps Roadmap", "url": "https://roadmap.sh/devops"},
            {"title": "TechWorld with Nana YouTube", "url": "https://www.youtube.com/@TechWorldwithNana"},
            {"title": "Kubernetes Docs", "url": "https://kubernetes.io/docs/home"},
        ]
    },

    "Android Developer": {
        "common_questions": [
            "What is the Android Activity lifecycle?",
            "Explain the difference between Fragment and Activity",
            "What is Jetpack Compose and how does it differ from XML layouts?",
            "How does ViewModel work in Android architecture?",
            "Explain the difference between LiveData, StateFlow, and SharedFlow",
            "What is Dependency Injection and how does Hilt implement it?",
            "How do you handle background tasks in Android?",
            "What is Room database and when to use it vs SQLite?",
            "Explain Kotlin coroutines and how they improve async code",
            "How do you optimize Android app performance and battery usage?",
        ],
        "what_companies_look_for_2026": [
            "Jetpack Compose — XML is being phased out",
            "Kotlin Multiplatform (KMM) for cross-platform",
            "On-device AI with ML Kit and Gemini Nano",
            "Modern Android architecture (MVVM + Clean Architecture)",
            "Kotlin coroutines and Flow for async",
            "Material 3 design system",
        ],
        "common_mistakes": [
            "Using Java instead of Kotlin in new projects",
            "Ignoring Activity/Fragment lifecycle — causes memory leaks",
            "No understanding of Android architecture components",
            "Doing heavy work on the main thread",
            "Not testing on multiple screen sizes and API levels",
        ],
        "portfolio_tips": [
            "Publish at least one app on Google Play Store",
            "Build with Jetpack Compose — not XML",
            "Include an app with an AI/ML feature (ML Kit)",
            "Show your architecture: MVVM, Clean Architecture",
            "Add proper app screenshots and demo video in README",
        ],
        "resources": [
            {"title": "Android Developer Docs", "url": "https://developer.android.com/docs"},
            {"title": "roadmap.sh/android", "url": "https://roadmap.sh/android"},
            {"title": "Philipp Lackner YouTube", "url": "https://www.youtube.com/@PhilippLackner"},
        ]
    },

    "iOS Developer": {
        "common_questions": [
            "Explain the iOS app lifecycle",
            "What is the difference between SwiftUI and UIKit?",
            "How does Auto Layout work?",
            "Explain Automatic Reference Counting (ARC)",
            "What is the difference between struct and class in Swift?",
            "How do you handle concurrency in Swift (async/await, actors)?",
            "What is Core Data and when would you use it?",
            "Explain the MVVM pattern in Swift",
            "How do you implement push notifications in iOS?",
            "What are Swift Protocols and how do they differ from classes?",
        ],
        "what_companies_look_for_2026": [
            "SwiftUI proficiency — UIKit knowledge still needed but SwiftUI is primary",
            "Swift Concurrency (async/await, actors)",
            "Core ML and Apple Intelligence API integration",
            "On-device AI and privacy-preserving ML",
            "App Store submission and distribution experience",
            "Vision Framework and ARKit for advanced features",
        ],
        "common_mistakes": [
            "Only knowing UIKit without learning SwiftUI",
            "Memory management issues — retain cycles and leaks",
            "No App Store published app",
            "Ignoring human interface guidelines",
            "Cannot handle different iPhone/iPad screen sizes",
        ],
        "portfolio_tips": [
            "Publish at least one app on the App Store",
            "Build with SwiftUI — it's the future",
            "Include an app with Core ML or Vision Framework",
            "Show clean Swift code — avoid Objective-C in new projects",
            "Record a demo video of your app working",
        ],
        "resources": [
            {"title": "Apple Developer Documentation", "url": "https://developer.apple.com/documentation"},
            {"title": "Hacking with Swift", "url": "https://www.hackingwithswift.com"},
            {"title": "Sean Allen YouTube", "url": "https://www.youtube.com/@seanallen"},
        ]
    },

    "Cloud Engineer": {
        "common_questions": [
            "What is the difference between IaaS, PaaS, and SaaS?",
            "Explain VPC, subnets, and security groups",
            "What is the difference between horizontal and vertical scaling?",
            "How does auto-scaling work in AWS/GCP/Azure?",
            "What is serverless computing and when should you use it?",
            "Explain the CAP theorem for distributed systems",
            "What is a CDN and why is it important?",
            "How do you handle cloud cost optimization (FinOps)?",
            "What is the difference between S3, EBS, and EFS in AWS?",
            "How do you design a highly available architecture?",
        ],
        "what_companies_look_for_2026": [
            "Multi-cloud or at least two cloud providers (AWS + GCP/Azure)",
            "AI cloud services (SageMaker, Vertex AI, Azure ML)",
            "Infrastructure as Code with Terraform or Pulumi",
            "Kubernetes and container orchestration",
            "FinOps — cost monitoring and optimization",
            "Security: IAM, encryption, compliance (SOC2, HIPAA)",
        ],
        "common_mistakes": [
            "Only theoretical knowledge — cloud requires hands-on practice",
            "No IaC experience — clicking through console is not enough",
            "Ignoring cost management — expensive mistakes happen",
            "No security knowledge — IAM, least-privilege ignored",
            "Cannot explain the tradeoffs between cloud services",
        ],
        "portfolio_tips": [
            "Get AWS Solutions Architect or GCP Associate certification",
            "Show Terraform code that provisions real infrastructure",
            "Include a project deployed on a cloud provider",
            "Document your architecture with diagrams (draw.io)",
            "Show cost analysis in your project READMEs",
        ],
        "resources": [
            {"title": "AWS Free Tier", "url": "https://aws.amazon.com/free"},
            {"title": "roadmap.sh/aws", "url": "https://roadmap.sh/aws"},
            {"title": "TechWorld with Nana YouTube", "url": "https://www.youtube.com/@TechWorldwithNana"},
        ]
    },

    "Blockchain Developer": {
        "common_questions": [
            "Explain how the Ethereum blockchain works",
            "What is a smart contract and how is it deployed?",
            "What is the difference between Solidity and Rust for blockchain?",
            "Explain gas fees and how to optimize gas usage",
            "What is a reentrancy attack and how do you prevent it?",
            "What is DeFi and how does it work?",
            "Explain ERC-20 vs ERC-721 vs ERC-1155 tokens",
            "What is a decentralized oracle and why are they needed?",
            "How does Proof of Stake differ from Proof of Work?",
            "What is account abstraction and why does it matter?",
        ],
        "what_companies_look_for_2026": [
            "Solidity smart contract development and security auditing",
            "Cross-chain development (Ethereum, Solana, L2s)",
            "Zero-knowledge proof knowledge (zkSNARKs, zkSTARKs)",
            "DeFi protocol understanding",
            "Web3.js/Ethers.js for frontend integration",
            "AI + Blockchain hybrid applications",
        ],
        "common_mistakes": [
            "No smart contract security knowledge — reentrancy, overflow",
            "Only knowing theory without any deployed contracts",
            "Ignoring gas optimization — expensive contracts won't be used",
            "No testing of smart contracts (Hardhat/Foundry tests)",
            "Cannot explain the protocols they work with",
        ],
        "portfolio_tips": [
            "Deploy contracts to a testnet (Sepolia, Mumbai)",
            "Get your contracts security-audited or use Slither",
            "Build a DeFi protocol or NFT marketplace",
            "Show your contract test coverage",
            "Link your deployed contracts on Etherscan",
        ],
        "resources": [
            {"title": "CryptoZombies", "url": "https://cryptozombies.io"},
            {"title": "Ethereum Developer Docs", "url": "https://ethereum.org/developers"},
            {"title": "Patrick Collins YouTube", "url": "https://www.youtube.com/@PatrickAlphaC"},
        ]
    },

    "Cybersecurity Engineer": {
        "common_questions": [
            "What is the CIA triad in security?",
            "Explain SQL injection and how to prevent it",
            "What is a man-in-the-middle attack?",
            "How does TLS/SSL work?",
            "What is the OWASP Top 10?",
            "Explain the difference between symmetric and asymmetric encryption",
            "What is penetration testing and how do you approach it?",
            "How does a buffer overflow attack work?",
            "What is zero-trust security architecture?",
            "How do you perform a threat model for an application?",
        ],
        "what_companies_look_for_2026": [
            "AI-powered threat detection and response",
            "Cloud security (AWS/Azure/GCP security services)",
            "Zero trust architecture implementation",
            "LLM security — prompt injection, jailbreaking defenses",
            "DevSecOps — security integrated into CI/CD",
            "SIEM tools and incident response",
        ],
        "common_mistakes": [
            "Only offensive security knowledge — defense is equally important",
            "No cloud security experience",
            "Cannot explain security concepts to non-technical teams",
            "No CTF experience or bug bounty participation",
            "Ignoring compliance and regulatory requirements",
        ],
        "portfolio_tips": [
            "Participate in CTF competitions and publish writeups",
            "Set up a home lab with vulnerable VMs (HackTheBox, TryHackMe)",
            "Earn a security certification (CEH, OSCP, CompTIA Security+)",
            "Build security tools and scripts on GitHub",
            "Document your penetration testing methodology",
        ],
        "resources": [
            {"title": "TryHackMe", "url": "https://tryhackme.com"},
            {"title": "HackTheBox", "url": "https://www.hackthebox.com"},
            {"title": "OWASP", "url": "https://owasp.org"},
        ]
    },

    "QA Engineer": {
        "common_questions": [
            "What is the difference between functional and non-functional testing?",
            "Explain the testing pyramid",
            "What is the difference between black-box and white-box testing?",
            "How do you write a good test case?",
            "What is regression testing and when do you run it?",
            "Explain end-to-end testing vs unit testing",
            "What is shift-left testing?",
            "How do you perform load testing?",
            "What is a test plan and what does it contain?",
            "How do you prioritize bugs and test cases?",
        ],
        "what_companies_look_for_2026": [
            "AI-assisted test generation (Testim, Applitools)",
            "Playwright or Cypress for E2E automation",
            "API testing with Postman or k6",
            "Performance and load testing skills",
            "Shift-left mindset — testing from day one",
            "Contract testing (Pact) for microservices",
        ],
        "common_mistakes": [
            "Only manual testing experience — automation is mandatory",
            "Cannot write test automation code",
            "No API testing knowledge",
            "Ignoring flaky tests rather than fixing root causes",
            "No performance or load testing experience",
        ],
        "portfolio_tips": [
            "Show automated test suites in your GitHub",
            "Include a CI/CD pipeline with tests running on every commit",
            "Build an automation framework from scratch",
            "Show test coverage reports in your projects",
            "Document your testing strategy in README",
        ],
        "resources": [
            {"title": "Playwright Docs", "url": "https://playwright.dev/docs/intro"},
            {"title": "roadmap.sh/qa", "url": "https://roadmap.sh/qa"},
            {"title": "Ministry of Testing", "url": "https://www.ministryoftesting.com"},
        ]
    },

    "Data Engineer": {
        "common_questions": [
            "What is the difference between a data warehouse and a data lake?",
            "Explain ETL vs ELT",
            "How does Apache Spark handle distributed data processing?",
            "What is Apache Kafka and when would you use it?",
            "Explain the star schema vs snowflake schema",
            "What is dbt and how does it fit into the data stack?",
            "How do you ensure data quality in a pipeline?",
            "What is data lineage and why does it matter?",
            "Explain partitioning and bucketing in Spark",
            "How do you handle late-arriving data in streaming pipelines?",
        ],
        "what_companies_look_for_2026": [
            "LLM pipeline construction — processing AI/text data at scale",
            "Vector database integration (Pinecone, Weaviate)",
            "Modern data stack: dbt + Airflow/Prefect + Snowflake",
            "Real-time streaming with Kafka or Flink",
            "Data quality automation (Great Expectations, dbt tests)",
            "Cloud data platforms (Snowflake, BigQuery, Databricks)",
        ],
        "common_mistakes": [
            "No streaming experience — batch-only is insufficient",
            "Cannot write efficient SQL queries",
            "No understanding of data modeling principles",
            "Ignoring data quality and validation",
            "Cannot scale solutions — only works with small datasets",
        ],
        "portfolio_tips": [
            "Build an end-to-end pipeline: ingestion → transform → serve",
            "Include a real-time streaming pipeline with Kafka",
            "Show dbt models with tests and documentation",
            "Add a data quality monitoring layer",
            "Deploy on a cloud platform (GCP, AWS, or Azure)",
        ],
        "resources": [
            {"title": "Data Engineering Zoomcamp", "url": "https://github.com/DataTalksClub/data-engineering-zoomcamp"},
            {"title": "roadmap.sh/data-engineer", "url": "https://roadmap.sh/data-engineer"},
            {"title": "Seattle Data Guy YouTube", "url": "https://www.youtube.com/@SeattleDataGuy"},
        ]
    },

    "Game Developer": {
        "common_questions": [
            "What is the game loop and how does it work?",
            "Explain the difference between Update() and FixedUpdate() in Unity",
            "What are design patterns used in game development? (e.g., Observer, State)",
            "How does collision detection work?",
            "What is the Entity Component System (ECS) pattern?",
            "How do you optimize game performance (FPS)?",
            "Explain the difference between 2D and 3D game engines",
            "What is shader programming and what is HLSL/GLSL?",
            "How do you implement pathfinding (A* algorithm)?",
            "What is procedural generation and when would you use it?",
        ],
        "what_companies_look_for_2026": [
            "AI-powered NPC behavior and procedural content generation",
            "Unity or Unreal Engine proficiency (one deeply)",
            "Multiplayer and networking knowledge",
            "Performance optimization — target frame rates matter",
            "Platform-specific experience (mobile, console, PC)",
            "Generative AI for game assets and testing",
        ],
        "common_mistakes": [
            "Game is never finished — scope control is critical",
            "No optimization — game runs fine on developer machine only",
            "Cannot explain game architecture and design decisions",
            "No version control for game assets (Git LFS)",
            "No multiplayer or networking knowledge",
        ],
        "portfolio_tips": [
            "Publish games on itch.io or Google Play/App Store",
            "Show your GitHub with game code (not just Unity scenes)",
            "Include a postmortem for each game — what you learned",
            "Build a game jam entry — shows you can ship fast",
            "Document your architecture and pattern choices",
        ],
        "resources": [
            {"title": "Unity Learn", "url": "https://learn.unity.com"},
            {"title": "Godot Docs", "url": "https://docs.godotengine.org"},
            {"title": "Brackeys YouTube", "url": "https://www.youtube.com/@Brackeys"},
        ]
    },

    "Embedded Systems Engineer": {
        "common_questions": [
            "What is the difference between a microcontroller and a microprocessor?",
            "Explain interrupts and interrupt service routines (ISR)",
            "What is the difference between UART, SPI, and I2C?",
            "How does RTOS task scheduling work?",
            "What are common causes of embedded system bugs? (race conditions, stack overflow)",
            "Explain DMA (Direct Memory Access) and when to use it",
            "What is a bootloader and how does it work?",
            "How do you debug embedded systems without a debugger?",
            "What is memory-mapped I/O?",
            "How do you reduce power consumption in embedded systems?",
        ],
        "what_companies_look_for_2026": [
            "TinyML and Edge AI (TensorFlow Lite, Edge Impulse)",
            "RTOS experience (FreeRTOS, Zephyr)",
            "IoT connectivity (MQTT, BLE, WiFi, LoRa)",
            "Rust for embedded — replacing C in safety-critical systems",
            "Low-power design for battery-operated devices",
            "Security: secure boot, encrypted firmware",
        ],
        "common_mistakes": [
            "Only software background without electronics fundamentals",
            "Ignoring timing constraints and real-time requirements",
            "No oscilloscope or logic analyzer experience",
            "Cannot read schematics or datasheets",
            "Ignoring power consumption — critical for IoT devices",
        ],
        "portfolio_tips": [
            "Show hardware projects with photos and circuit diagrams",
            "Include a project with an RTOS (FreeRTOS)",
            "Add a TinyML project — edge AI is booming",
            "Document your hardware setup clearly in README",
            "Show PCB design if possible (KiCad/EasyEDA)",
        ],
        "resources": [
            {"title": "FreeRTOS Docs", "url": "https://www.freertos.org/Documentation/RTOS_book.html"},
            {"title": "Embedded.fm Podcast", "url": "https://embedded.fm"},
            {"title": "Phil's Lab YouTube", "url": "https://www.youtube.com/@PhilsLab"},
        ]
    },
}

GENERIC_TIPS = {
    "common_questions": [
        "Tell me about yourself",
        "Why do you want this role?",
        "What is your biggest technical challenge?",
        "Describe a project you are proud of",
        "Where do you see yourself in 5 years?",
    ],
    "what_companies_look_for_2026": [
        "AI tool proficiency",
        "Problem-solving ability",
        "Communication skills",
        "Team collaboration",
        "Continuous learning mindset",
    ],
    "common_mistakes": [
        "Not researching the company",
        "Cannot explain projects clearly",
        "No questions for the interviewer",
        "Lying about skills",
        "Poor GitHub profile",
    ],
    "portfolio_tips": [
        "Deploy all projects",
        "Add README to every repo",
        "Include at least 1 AI project",
        "Keep GitHub active",
        "Link portfolio on resume",
    ],
    "resources": [
        {"title": "roadmap.sh", "url": "https://roadmap.sh"},
        {"title": "LeetCode", "url": "https://leetcode.com"},
        {"title": "GitHub Explore", "url": "https://github.com/explore"},
    ]
}


def get_interview_tips(role_name):
    return INTERVIEW_TIPS.get(role_name, GENERIC_TIPS)


# Test
if __name__ == "__main__":
    from career.job_roles import get_all_roles
    roles = get_all_roles()
    print(f"Total roles: {len(roles)}")
    covered = [r for r in roles if r in INTERVIEW_TIPS]
    missing = [r for r in roles if r not in INTERVIEW_TIPS]
    print(f"Covered: {len(covered)}/15")
    print(f"Missing: {missing}")
    tips = get_interview_tips("ML/AI Engineer")
    print("\nCommon Questions:")
    for q in tips["common_questions"][:5]:
        print(f"  - {q}")