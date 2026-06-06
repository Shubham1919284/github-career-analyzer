# career/salary_insight.py


SALARY_DATA = {
    "Frontend Developer": {
        "Beginner":             {"india": "₹2-4 LPA",   "remote": "$8-15k/yr"},
        "Internship Seeker":    {"india": "₹8-15k/mo",  "remote": "$500-1k/mo"},
        "Fresher":              {"india": "₹4-7 LPA",   "remote": "$15-25k/yr"},
        "Working Professional": {"india": "₹8-18 LPA",  "remote": "$30-60k/yr"},
        "Senior":               {"india": "₹20-40 LPA", "remote": "$70-120k/yr"},
    },
    "Backend Developer": {
        "Beginner":             {"india": "₹2-4 LPA",   "remote": "$8-15k/yr"},
        "Internship Seeker":    {"india": "₹10-20k/mo", "remote": "$600-1.2k/mo"},
        "Fresher":              {"india": "₹5-9 LPA",   "remote": "$18-30k/yr"},
        "Working Professional": {"india": "₹10-22 LPA", "remote": "$35-70k/yr"},
        "Senior":               {"india": "₹25-50 LPA", "remote": "$80-140k/yr"},
    },
    "Full Stack Developer": {
        "Beginner":             {"india": "₹2-5 LPA",   "remote": "$10-18k/yr"},
        "Internship Seeker":    {"india": "₹10-20k/mo", "remote": "$600-1.2k/mo"},
        "Fresher":              {"india": "₹5-10 LPA",  "remote": "$20-35k/yr"},
        "Working Professional": {"india": "₹12-25 LPA", "remote": "$40-80k/yr"},
        "Senior":               {"india": "₹28-55 LPA", "remote": "$90-150k/yr"},
    },
    "ML/AI Engineer": {
        "Beginner":             {"india": "₹3-6 LPA",   "remote": "$12-20k/yr"},
        "Internship Seeker":    {"india": "₹12-25k/mo", "remote": "$800-1.5k/mo"},
        "Fresher":              {"india": "₹7-14 LPA",  "remote": "$25-45k/yr"},
        "Working Professional": {"india": "₹15-35 LPA", "remote": "$50-100k/yr"},
        "Senior":               {"india": "₹35-80 LPA", "remote": "$100-180k/yr"},
    },
    "Data Scientist": {
        "Beginner":             {"india": "₹3-5 LPA",   "remote": "$10-18k/yr"},
        "Internship Seeker":    {"india": "₹10-20k/mo", "remote": "$600-1.2k/mo"},
        "Fresher":              {"india": "₹6-12 LPA",  "remote": "$22-40k/yr"},
        "Working Professional": {"india": "₹12-28 LPA", "remote": "$45-85k/yr"},
        "Senior":               {"india": "₹30-60 LPA", "remote": "$90-160k/yr"},
    },
    "DevOps Engineer": {
        "Beginner":             {"india": "₹2-5 LPA",   "remote": "$10-18k/yr"},
        "Internship Seeker":    {"india": "₹10-18k/mo", "remote": "$600-1k/mo"},
        "Fresher":              {"india": "₹5-10 LPA",  "remote": "$20-38k/yr"},
        "Working Professional": {"india": "₹12-25 LPA", "remote": "$40-80k/yr"},
        "Senior":               {"india": "₹28-55 LPA", "remote": "$85-145k/yr"},
    },
    "Android Developer": {
        "Beginner":             {"india": "₹2-4 LPA",   "remote": "$8-15k/yr"},
        "Internship Seeker":    {"india": "₹8-15k/mo",  "remote": "$500-1k/mo"},
        "Fresher":              {"india": "₹4-8 LPA",   "remote": "$15-28k/yr"},
        "Working Professional": {"india": "₹9-20 LPA",  "remote": "$32-65k/yr"},
        "Senior":               {"india": "₹22-45 LPA", "remote": "$70-120k/yr"},
    },
    "iOS Developer": {
        "Beginner":             {"india": "₹2-4 LPA",   "remote": "$8-15k/yr"},
        "Internship Seeker":    {"india": "₹8-15k/mo",  "remote": "$500-1k/mo"},
        "Fresher":              {"india": "₹4-9 LPA",   "remote": "$18-30k/yr"},
        "Working Professional": {"india": "₹10-22 LPA", "remote": "$35-70k/yr"},
        "Senior":               {"india": "₹25-50 LPA", "remote": "$80-140k/yr"},
    },
    "Cloud Engineer": {
        "Beginner":             {"india": "₹3-5 LPA",   "remote": "$10-18k/yr"},
        "Internship Seeker":    {"india": "₹10-20k/mo", "remote": "$700-1.2k/mo"},
        "Fresher":              {"india": "₹5-10 LPA",  "remote": "$20-38k/yr"},
        "Working Professional": {"india": "₹12-28 LPA", "remote": "$45-90k/yr"},
        "Senior":               {"india": "₹30-60 LPA", "remote": "$90-160k/yr"},
    },
    "Blockchain Developer": {
        "Beginner":             {"india": "₹3-6 LPA",   "remote": "$12-20k/yr"},
        "Internship Seeker":    {"india": "₹12-25k/mo", "remote": "$800-1.5k/mo"},
        "Fresher":              {"india": "₹6-12 LPA",  "remote": "$25-45k/yr"},
        "Working Professional": {"india": "₹15-35 LPA", "remote": "$50-100k/yr"},
        "Senior":               {"india": "₹35-80 LPA", "remote": "$100-180k/yr"},
    },
    "Cybersecurity Engineer": {
        "Beginner":             {"india": "₹2-5 LPA",   "remote": "$10-18k/yr"},
        "Internship Seeker":    {"india": "₹10-18k/mo", "remote": "$600-1k/mo"},
        "Fresher":              {"india": "₹5-10 LPA",  "remote": "$20-38k/yr"},
        "Working Professional": {"india": "₹12-28 LPA", "remote": "$45-90k/yr"},
        "Senior":               {"india": "₹30-65 LPA", "remote": "$90-160k/yr"},
    },
    "QA Engineer": {
        "Beginner":             {"india": "₹2-4 LPA",   "remote": "$8-14k/yr"},
        "Internship Seeker":    {"india": "₹8-14k/mo",  "remote": "$500-900/mo"},
        "Fresher":              {"india": "₹4-7 LPA",   "remote": "$15-25k/yr"},
        "Working Professional": {"india": "₹8-18 LPA",  "remote": "$28-55k/yr"},
        "Senior":               {"india": "₹20-40 LPA", "remote": "$65-110k/yr"},
    },
    "Data Engineer": {
        "Beginner":             {"india": "₹3-5 LPA",   "remote": "$10-18k/yr"},
        "Internship Seeker":    {"india": "₹10-20k/mo", "remote": "$700-1.2k/mo"},
        "Fresher":              {"india": "₹6-11 LPA",  "remote": "$22-40k/yr"},
        "Working Professional": {"india": "₹13-28 LPA", "remote": "$45-85k/yr"},
        "Senior":               {"india": "₹30-60 LPA", "remote": "$90-150k/yr"},
    },
    "Game Developer": {
        "Beginner":             {"india": "₹2-4 LPA",   "remote": "$8-14k/yr"},
        "Internship Seeker":    {"india": "₹8-14k/mo",  "remote": "$500-900/mo"},
        "Fresher":              {"india": "₹4-7 LPA",   "remote": "$15-25k/yr"},
        "Working Professional": {"india": "₹8-18 LPA",  "remote": "$28-60k/yr"},
        "Senior":               {"india": "₹20-40 LPA", "remote": "$65-120k/yr"},
    },
    "Embedded Systems Engineer": {
        "Beginner":             {"india": "₹2-4 LPA",   "remote": "$8-14k/yr"},
        "Internship Seeker":    {"india": "₹8-15k/mo",  "remote": "$500-1k/mo"},
        "Fresher":              {"india": "₹4-8 LPA",   "remote": "$15-28k/yr"},
        "Working Professional": {"india": "₹9-20 LPA",  "remote": "$32-65k/yr"},
        "Senior":               {"india": "₹22-45 LPA", "remote": "$70-120k/yr"},
    },
}

# Next level mapping
NEXT_LEVEL = {
    "Beginner": "Internship Seeker",
    "Internship Seeker": "Fresher",
    "Fresher": "Working Professional",
    "Working Professional": "Senior",
    "Senior": None
}


def get_salary_insight(role_name, experience_level):
    role_data = SALARY_DATA.get(role_name)
    if not role_data:
        return None

    current = role_data.get(experience_level, {})
    next_level = NEXT_LEVEL.get(experience_level)
    next_salary = role_data.get(next_level, {}) if next_level else None

    return {
        "role": role_name,
        "current_level": experience_level,
        "current_salary": current,
        "next_level": next_level,
        "next_salary": next_salary,
        "insight": get_salary_insight_message(experience_level, next_level)
    }


def get_salary_insight_message(current_level, next_level):
    messages = {
        "Beginner": "Focus on building projects and learning consistently — internship is the next big step!",
        "Internship Seeker": "Land an internship and convert it — that's the fastest path to a full-time role!",
        "Fresher": "Your first job shapes your career — choose a company where you can learn fast!",
        "Working Professional": "Upskill with AI/ML tools and system design — Senior roles pay 2x more!",
        "Senior": "You're at the top! Consider open source contributions or building your own product!"
    }
    return messages.get(current_level, "")


# Test
if __name__ == "__main__":
    result = get_salary_insight("ML/AI Engineer", "Fresher")
    print(f"Role: {result['role']}")
    print(f"Level: {result['current_level']}")
    print(f"Current Salary (India): {result['current_salary']['india']}")
    print(f"Current Salary (Remote): {result['current_salary']['remote']}")
    print(f"Next Level: {result['next_level']}")
    if result['next_salary']:
        print(f"Next Level Salary (India): {result['next_salary']['india']}")
    print(f"Insight: {result['insight']}")