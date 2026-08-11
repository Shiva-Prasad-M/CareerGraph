from app.database.connection import database
from app.database import queries


def get_skills():
    with database.driver.session() as session:
        result = session.run(queries.GET_SKILLS)

        return [
            record.data()
            for record in result
        ]


def get_roles():
    with database.driver.session() as session:
        result = session.run(queries.GET_ROLES)

        return [
            record.data()
            for record in result
        ]


def get_companies():
    with database.driver.session() as session:
        result = session.run(queries.GET_COMPANIES)

        return [
            record.data()
            for record in result
        ]


def match_roles(skills):
    query = """
    MATCH (r:Role)<-[:REQUIRED_FOR]-(required:Skill)
    WITH r, collect(required.name) AS required_skills

    WITH
        r,
        required_skills,
        [skill IN required_skills
         WHERE toLower(skill) IN [x IN $skills | toLower(x)]
        ] AS matched_skills

    RETURN
        r.name AS role,
        required_skills,
        matched_skills,
        size(matched_skills) AS matched_count,
        size(required_skills) AS required_count,
        CASE
            WHEN size(required_skills) = 0 THEN 0
            ELSE round(
                100.0 * size(matched_skills) /
                size(required_skills)
            )
        END AS match_percentage

    ORDER BY match_percentage DESC
    """

    with database.driver.session() as session:
        result = session.run(
            query,
            skills=skills
        )

        return [record.data() for record in result]


def get_missing_skills(role, skills):
    with database.driver.session() as session:
        result = session.run(
            queries.MISSING_SKILLS,
            role=role,
            skills=skills
        )

        return [
            record.data()
            for record in result
        ]


def get_learning_path(role, skills):
    with database.driver.session() as session:
        result = session.run(
            queries.LEARNING_PATH,
            role=role,
            skills=skills
        )

        return [
            record.data()
            for record in result
        ]


def get_career_graph(skills):
    with database.driver.session() as session:
        result = session.run(
            queries.CAREER_GRAPH,
            skills=skills
        )

        return [
            record.data()
            for record in result
        ]