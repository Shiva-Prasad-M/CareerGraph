// CareerGraph - Database Constraints

CREATE CONSTRAINT skill_name_unique IF NOT EXISTS
FOR (s:Skill)
REQUIRE s.name IS UNIQUE;

CREATE CONSTRAINT role_name_unique IF NOT EXISTS
FOR (r:Role)
REQUIRE r.name IS UNIQUE;

CREATE CONSTRAINT company_name_unique IF NOT EXISTS
FOR (c:Company)
REQUIRE c.name IS UNIQUE;

CREATE CONSTRAINT course_name_unique IF NOT EXISTS
FOR (c:Course)
REQUIRE c.name IS UNIQUE;

CREATE CONSTRAINT category_name_unique IF NOT EXISTS
FOR (c:Category)
REQUIRE c.name IS UNIQUE;