import { useEffect, useState } from "react";

import GraphStats from "../components/GraphStats";
import GraphView from "../components/GraphView";
import RoleCard from "../components/RoleCard";
import SkillGap from "../components/SkillGap";
import SkillSelector from "../components/SkillSelector";
import {
  getSkills,
  matchRoles,
  getMissingSkills,
  getLearningPath,
  exploreGraph,
  exploreRelatedGraph,
  getGraphStats,
} from "../services/api";


function Dashboard() {
  const [skills, setSkills] = useState([]);
  const [selectedSkills, setSelectedSkills] = useState([]);

  const [roles, setRoles] = useState([]);
  const [selectedRole, setSelectedRole] = useState(null);

  const [missingSkills, setMissingSkills] = useState([]);
  const [courses, setCourses] = useState([]);

  const [graphData, setGraphData] = useState([]);

const [stats, setStats] = useState(null);

const [loading, setLoading] = useState(true);
  const [searching, setSearching] = useState(false);
  const [error, setError] = useState("");

useEffect(() => {
  async function loadDashboard() {
    try {
      const [skillsData, statsData] = await Promise.all([
        getSkills(),
        getGraphStats(),
      ]);

      setSkills(skillsData);
      setStats(statsData);
    } catch (error) {
      setError(
        "Unable to connect to the CareerGraph backend."
      );
    } finally {
      setLoading(false);
    }
  }

  loadDashboard();
}, []);


  async function exploreCareers() {
  if (selectedSkills.length === 0) {
    return;
  }

  setSearching(true);
  setError("");
  setRoles([]);
  setSelectedRole(null);
  setMissingSkills([]);
  setCourses([]);
  setGraphData([]);

  try {
    const results = await matchRoles(selectedSkills);

    setRoles(results);

    if (results.length > 0) {
      const firstRole = results[0];

      setSelectedRole(firstRole);

      const [missing, learning, graph] =
        await Promise.all([
          getMissingSkills(
            firstRole.role,
            selectedSkills
          ),
          getLearningPath(
            firstRole.role,
            selectedSkills
          ),
          exploreRelatedGraph(selectedSkills),
        ]);

      setMissingSkills(missing);
      setCourses(learning);
      setGraphData(graph);
    }
  } catch (error) {
    setError(
      "Something went wrong while exploring your career paths."
    );
  } finally {
    setSearching(false);
  }
}


  async function selectRole(role) {
    setSelectedRole(role);

    try {
      const [missing, learning] =
        await Promise.all([
          getMissingSkills(
            role.role,
            selectedSkills
          ),
          getLearningPath(
            role.role,
            selectedSkills
          ),
        ]);

      setMissingSkills(missing);
      setCourses(learning);
    } catch {
      setError(
        "Unable to load the selected role."
      );
    }
  }


  if (loading) {
    return (
      <div className="center-state">
        Loading CareerGraph...
      </div>
    );
  }


  return (
    <main>

      <section className="hero">
        <span className="eyebrow">
          CAREER INTELLIGENCE
        </span>

        <h1>
          Find the career path
          <br />
          hidden in your skills.
        </h1>

        <p>
          Connect your skills to roles, companies,
          and learning opportunities through a
          relationship-driven career graph.
        </p>
      </section>
      {stats && <GraphStats stats={stats} />}


      {error && (
        <div className="error">
          {error}
        </div>
      )}


      <section className="panel">
        <div className="section-heading">
          <div>
            <span className="eyebrow">
              STEP 01
            </span>

            <h2>
              What can you do?
            </h2>
          </div>

          <span className="selection-count">
            {selectedSkills.length} selected
          </span>
        </div>


        <SkillSelector
          skills={skills}
          selectedSkills={selectedSkills}
          onChange={setSelectedSkills}
        />


        <button
          className="primary-button"
          onClick={exploreCareers}
          disabled={
            selectedSkills.length === 0 ||
            searching
          }
        >
          {searching
            ? "Exploring..."
            : "Explore career paths"}
        </button>
      </section>

{roles.length > 0 && (
  <section className="panel">
    <div className="section-heading">
      <div>
        <span className="eyebrow">
          STEP 02
        </span>

        <h2>
          Your strongest matches
        </h2>
      </div>
    </div>

    <div className="role-grid">
      {roles.map((role) => (
        <RoleCard
          key={role.role}
          role={role}
          selected={
            selectedRole?.role === role.role
          }
          onClick={() => selectRole(role)}
        />
      ))}
    </div>
  </section>
)}

{roles.length === 0 &&
  selectedSkills.length > 0 &&
  !searching &&
  !error && (
    <section className="panel empty-state">
      <span className="eyebrow">
        STEP 02
      </span>

      <h2>
        No matching roles found
      </h2>

      <p>
        We couldn't find a career role matching
        the selected skills. Try selecting a
        different combination of skills.
      </p>
    </section>
)}


      {selectedRole && (
        <SkillGap
          missingSkills={missingSkills}
          courses={courses}
        />
      )}


      {graphData.length > 0 && (
        <section className="panel">
          <div className="section-heading">
            <div>
              <span className="eyebrow">
                GRAPH EXPLORER
              </span>

              <h2>
                See how the connections lead there
              </h2>
            </div>
          </div>

          <GraphView data={graphData} />
        </section>
      )}

    </main>
  );
}

export default Dashboard;