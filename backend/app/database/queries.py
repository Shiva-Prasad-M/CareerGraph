GET_SKILLS = """
MATCH (s:Skill)
RETURN s.name AS name,
       s.category AS category,
       s.level AS level
ORDER BY s.name
"""


GET_ROLES = """
MATCH (r:Role)
OPTIONAL MATCH (s:Skill)-[:REQUIRED_FOR]->(r)
WITH r, collect(s.name) AS skills
RETURN r.name AS name,
       r.description AS description,
       r.demand AS demand,
       skills
ORDER BY r.name
"""


GET_COMPANIES = """
MATCH (c:Company)
OPTIONAL MATCH (r:Role)-[:OFFERED_BY]->(c)
WITH c, collect(r.name) AS roles
RETURN c.name AS name,
       c.industry AS industry,
       c.location AS location,
       roles
ORDER BY c.name
"""


MATCH_ROLES = """
MATCH (s:Skill)-[:REQUIRED_FOR]->(r:Role)
WHERE s.name IN $skills

WITH r,
     count(DISTINCT s) AS matchedSkills

MATCH (required:Skill)-[:REQUIRED_FOR]->(r)

WITH r,
     matchedSkills,
     count(DISTINCT required) AS totalSkills

RETURN
    r.name AS role,
    r.description AS description,
    matchedSkills,
    totalSkills,
    round(
        (toFloat(matchedSkills) / totalSkills) * 100
    ) AS matchPercentage
ORDER BY matchPercentage DESC
"""


MISSING_SKILLS = """
MATCH (r:Role {name: $role})
MATCH (s:Skill)-[:REQUIRED_FOR]->(r)
WHERE NOT s.name IN $skills

RETURN
    s.name AS skill,
    s.category AS category,
    s.level AS level
ORDER BY s.name
"""


LEARNING_PATH = """
MATCH (r:Role {name: $role})
MATCH (s:Skill)-[:REQUIRED_FOR]->(r)
WHERE NOT s.name IN $skills

MATCH (c:Course)-[:TEACHES]->(s)

RETURN
    s.name AS skill,
    c.name AS course,
    c.provider AS provider,
    c.difficulty AS difficulty
ORDER BY s.name
"""


CAREER_GRAPH = """
MATCH (start:Skill)
WHERE start.name IN $skills

MATCH (start)-[:RELATED_TO*1..2]->(related:Skill)
MATCH (related)-[:REQUIRED_FOR]->(role:Role)
MATCH (role)-[:OFFERED_BY]->(company:Company)

RETURN
    role.name AS role,
    company.name AS company,
    collect(DISTINCT related.name) AS relatedSkills
ORDER BY role, company
LIMIT 20
"""
RELATED_SKILLS_GRAPH = """
MATCH (s:Skill)-[:RELATED_TO]->(related:Skill)
WHERE s.name IN $skills
OPTIONAL MATCH (related)-[:REQUIRED_FOR]->(r:Role)
OPTIONAL MATCH (r)-[:OFFERED_BY]->(c:Company)

RETURN
    s.name AS skill,
    related.name AS relatedSkill,
    r.name AS role,
    c.name AS company
ORDER BY s.name, related.name
"""