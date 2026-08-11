from neo4j import GraphDatabase

from app.config import settings


driver = GraphDatabase.driver(
    settings.cognodb_uri,
    auth=(
        settings.cognodb_username,
        settings.cognodb_password
    )
)


def run_query(session, query, **parameters):
    result = session.run(query, parameters)
    result.consume()


def seed_database():
    with driver.session() as session:

        # -------------------------
        # Categories
        # -------------------------

        categories = [
            "Software Development",
            "Data",
            "Cloud & DevOps"
        ]

        for category in categories:
            run_query(
                session,
                """
                MERGE (c:Category {name: $name})
                """,
                name=category
            )

        # -------------------------
        # Skills
        # -------------------------

        skills = [
            ("Python", "Programming", "Intermediate"),
            ("Java", "Programming", "Intermediate"),
            ("JavaScript", "Programming", "Intermediate"),
            ("React", "Frontend", "Intermediate"),
            ("Node.js", "Backend", "Intermediate"),
            ("FastAPI", "Backend", "Intermediate"),
            ("SQL", "Database", "Intermediate"),
            ("PostgreSQL", "Database", "Intermediate"),
            ("MongoDB", "Database", "Intermediate"),
            ("REST APIs", "Backend", "Intermediate"),
            ("Docker", "DevOps", "Beginner"),
            ("Git", "Tools", "Intermediate"),
            ("AWS", "Cloud", "Beginner"),
            ("Pandas", "Data", "Intermediate"),
            ("NumPy", "Data", "Intermediate")
        ]

        for name, category, level in skills:
            run_query(
                session,
                """
                MERGE (s:Skill {name: $name})
                SET s.category = $category,
                    s.level = $level
                """,
                name=name,
                category=category,
                level=level
            )

        # -------------------------
        # Roles
        # -------------------------

        roles = [
            (
                "Backend Developer",
                "Builds server-side applications and APIs",
                "High"
            ),
            (
                "Frontend Developer",
                "Builds web interfaces and user experiences",
                "High"
            ),
            (
                "Full Stack Developer",
                "Works across frontend and backend systems",
                "High"
            ),
            (
                "Data Engineer",
                "Builds data pipelines and data infrastructure",
                "High"
            ),
            (
                "Python Developer",
                "Builds applications and services using Python",
                "High"
            )
        ]

        for name, description, demand in roles:
            run_query(
                session,
                """
                MERGE (r:Role {name: $name})
                SET r.description = $description,
                    r.demand = $demand
                """,
                name=name,
                description=description,
                demand=demand
            )

        # -------------------------
        # Companies
        # -------------------------

        companies = [
            ("TechNova", "Software", "Hyderabad"),
            ("CloudSphere", "Cloud Computing", "Bangalore"),
            ("DataForge", "Data Engineering", "Hyderabad"),
            ("CodeCraft", "Software", "Pune"),
            ("Vertex Labs", "Technology", "Chennai")
        ]

        for name, industry, location in companies:
            run_query(
                session,
                """
                MERGE (c:Company {name: $name})
                SET c.industry = $industry,
                    c.location = $location
                """,
                name=name,
                industry=industry,
                location=location
            )

        # -------------------------
        # Courses
        # -------------------------

        courses = [
            (
                "FastAPI Fundamentals",
                "LearningHub",
                "Intermediate"
            ),
            (
                "Advanced SQL",
                "LearningHub",
                "Intermediate"
            ),
            (
                "Docker for Developers",
                "CodeAcademy",
                "Beginner"
            ),
            (
                "React Development",
                "CodeAcademy",
                "Intermediate"
            ),
            (
                "Python Backend Development",
                "DevSchool",
                "Intermediate"
            )
        ]

        for name, provider, difficulty in courses:
            run_query(
                session,
                """
                MERGE (c:Course {name: $name})
                SET c.provider = $provider,
                    c.difficulty = $difficulty
                """,
                name=name,
                provider=provider,
                difficulty=difficulty
            )

        # -------------------------
        # Skill -> Role
        # -------------------------

        role_skills = {
            "Backend Developer": [
                "Python",
                "FastAPI",
                "SQL",
                "REST APIs",
                "Docker",
                "Git"
            ],
            "Frontend Developer": [
                "JavaScript",
                "React",
                "REST APIs",
                "Git"
            ],
            "Full Stack Developer": [
                "JavaScript",
                "React",
                "Node.js",
                "SQL",
                "REST APIs",
                "Git"
            ],
            "Data Engineer": [
                "Python",
                "SQL",
                "PostgreSQL",
                "Docker",
                "Git"
            ],
            "Python Developer": [
                "Python",
                "SQL",
                "REST APIs",
                "Git"
            ]
        }

        for role, skill_list in role_skills.items():
            for skill in skill_list:
                run_query(
                    session,
                    """
                    MATCH (s:Skill {name: $skill})
                    MATCH (r:Role {name: $role})
                    MERGE (s)-[:REQUIRED_FOR]->(r)
                    """,
                    skill=skill,
                    role=role
                )

        # -------------------------
        # Role -> Company
        # -------------------------

        role_companies = {
            "Backend Developer": [
                "TechNova",
                "CloudSphere"
            ],
            "Frontend Developer": [
                "CodeCraft",
                "TechNova"
            ],
            "Full Stack Developer": [
                "TechNova",
                "Vertex Labs"
            ],
            "Data Engineer": [
                "DataForge",
                "CloudSphere"
            ],
            "Python Developer": [
                "DataForge",
                "CodeCraft"
            ]
        }

        for role, company_list in role_companies.items():
            for company in company_list:
                run_query(
                    session,
                    """
                    MATCH (r:Role {name: $role})
                    MATCH (c:Company {name: $company})
                    MERGE (r)-[:OFFERED_BY]->(c)
                    """,
                    role=role,
                    company=company
                )

        # -------------------------
        # Course -> Skill
        # -------------------------

        course_skills = {
            "FastAPI Fundamentals": [
                "FastAPI",
                "REST APIs"
            ],
            "Advanced SQL": [
                "SQL",
                "PostgreSQL"
            ],
            "Docker for Developers": [
                "Docker"
            ],
            "React Development": [
                "React",
                "JavaScript"
            ],
            "Python Backend Development": [
                "Python",
                "REST APIs"
            ]
        }

        for course, skill_list in course_skills.items():
            for skill in skill_list:
                run_query(
                    session,
                    """
                    MATCH (c:Course {name: $course})
                    MATCH (s:Skill {name: $skill})
                    MERGE (c)-[:TEACHES]->(s)
                    """,
                    course=course,
                    skill=skill
                )

        # -------------------------
        # Skill relationships
        # -------------------------

        related_skills = [
            ("Python", "FastAPI"),
            ("Python", "Pandas"),
            ("Python", "NumPy"),
            ("JavaScript", "React"),
            ("SQL", "PostgreSQL"),
            ("Node.js", "REST APIs"),
            ("Docker", "AWS")
        ]

        for first, second in related_skills:
            run_query(
                session,
                """
                MATCH (a:Skill {name: $first})
                MATCH (b:Skill {name: $second})
                MERGE (a)-[:RELATED_TO]->(b)
                """,
                first=first,
                second=second
            )

        # -------------------------
        # Similar roles
        # -------------------------

        similar_roles = [
            ("Backend Developer", "Python Developer"),
            ("Backend Developer", "Full Stack Developer"),
            ("Frontend Developer", "Full Stack Developer"),
            ("Data Engineer", "Python Developer")
        ]

        for first, second in similar_roles:
            run_query(
                session,
                """
                MATCH (a:Role {name: $first})
                MATCH (b:Role {name: $second})
                MERGE (a)-[:SIMILAR_TO]->(b)
                """,
                first=first,
                second=second
            )


def main():
    try:
        seed_database()
        print("Database seeded successfully.")

    except Exception as error:
        print(f"Seed failed: {error}")

    finally:
        driver.close()


if __name__ == "__main__":
    main()