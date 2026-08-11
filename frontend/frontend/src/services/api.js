const API_URL = "https://career-graph-l8w2.onrender.com";

async function request(url, options = {}) {
  const response = await fetch(`${API_URL}${url}`, {
    headers: {
      "Content-Type": "application/json",
    },
    ...options,
  });

  if (!response.ok) {
    throw new Error("Unable to connect to CareerGraph API");
  }

  return response.json();
}

export function getSkills() {
  return request("/api/skills");
}

export function getRoles() {
  return request("/api/roles");
}

export function matchRoles(skills) {
  return request("/api/graph/match", {
    method: "POST",
    body: JSON.stringify({ skills }),
  });
}

export function getMissingSkills(role, skills) {
  return request("/api/graph/missing-skills", {
    method: "POST",
    body: JSON.stringify({
      role,
      skills,
    }),
  });
}

export function getLearningPath(role, skills) {
  return request("/api/graph/learning-path", {
    method: "POST",
    body: JSON.stringify({
      role,
      skills,
    }),
  });
}

export function exploreGraph(skills) {
  return request("/api/graph/explore", {
    method: "POST",
    body: JSON.stringify({ skills }),
  });
}

export function getGraphStats() {
  return request("/api/graph/stats");
}
export function exploreRelatedGraph(skills) {
  return request("/api/graph/explore-related", {
    method: "POST",
    body: JSON.stringify({ skills }),
  });
}
