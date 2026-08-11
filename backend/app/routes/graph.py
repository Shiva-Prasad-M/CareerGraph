from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from app.database.connection import database
from app.database.queries import RELATED_SKILLS_GRAPH

from app.services.career_service import (
    match_roles,
    get_missing_skills,
    get_learning_path,
)


router = APIRouter(
    prefix="/api/graph",
    tags=["Graph"]
)


class SkillRequest(BaseModel):
    skills: list[str]


class CareerRequest(BaseModel):
    role: str
    skills: list[str]


@router.get("/stats")
def graph_stats():
    try:
        with database.driver.session() as session:

            nodes = session.run(
                "MATCH (n) RETURN count(n) AS total"
            ).single()["total"]

            relationships = session.run(
                "MATCH ()-[r]->() RETURN count(r) AS total"
            ).single()["total"]

            return {
                "nodes": nodes,
                "relationships": relationships
            }

    except Exception as e:
        print("GRAPH QUERY ERROR:", repr(e))

        raise HTTPException(
            status_code=503,
            detail="Unable to load graph statistics"
        )


@router.post("/match")
def career_match(request: SkillRequest):
    try:
        return match_roles(request.skills)

    except Exception as e:
        print("CAREER MATCH ERROR:", repr(e))

        raise HTTPException(
            status_code=503,
            detail="Unable to calculate career matches"
        )


@router.post("/missing-skills")
def missing_skills(request: CareerRequest):
    try:
        return get_missing_skills(
            request.role,
            request.skills
        )

    except Exception as e:
        print("MISSING SKILLS ERROR:", repr(e))

        raise HTTPException(
            status_code=503,
            detail="Unable to calculate missing skills"
        )


@router.post("/learning-path")
def learning_path(request: CareerRequest):
    try:
        return get_learning_path(
            request.role,
            request.skills
        )

    except Exception as e:
        print("LEARNING PATH ERROR:", repr(e))

        raise HTTPException(
            status_code=503,
            detail="Unable to build learning path"
        )


@router.post("/explore")
def explore_graph(request: SkillRequest):

    query = """
    MATCH (s:Skill)-[:REQUIRED_FOR]->(r:Role)-[:OFFERED_BY]->(c:Company)
    WHERE s.name IN $skills
    RETURN
        s.name AS skill,
        r.name AS role,
        c.name AS company
    ORDER BY r.name, c.name
    """

    try:
        with database.driver.session() as session:

            result = session.run(
                query,
                skills=request.skills
            )

            return [record.data() for record in result]

    except Exception as e:
        print("EXPLORE GRAPH ERROR:", repr(e))

        raise HTTPException(
            status_code=503,
            detail="Unable to explore career graph"
        )


@router.post("/explore-related")
def explore_related(request: SkillRequest):

    try:
        with database.driver.session() as session:

            result = session.run(
                RELATED_SKILLS_GRAPH,
                skills=request.skills
            )

            return [record.data() for record in result]

    except Exception as e:
        print("EXPLORE RELATED ERROR:", repr(e))

        raise HTTPException(
            status_code=503,
            detail="Unable to explore related skills"
        )