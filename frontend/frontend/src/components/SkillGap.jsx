function SkillGap({ missingSkills, courses }) {
  return (
    <section className="panel">
      <div className="section-heading">
        <div>
          <span className="eyebrow">DEVELOPMENT PLAN</span>
          <h2>Close your skill gaps</h2>
        </div>
      </div>

      {missingSkills.length === 0 ? (
        <div className="empty-state">
          You already have all the skills required for this role.
        </div>
      ) : (
        <>
          <div className="gap-list">
            {missingSkills.map((skill) => (
              <div className="gap-item" key={skill.skill}>
                <div>
                  <strong>{skill.skill}</strong>
                  <span>{skill.category}</span>
                </div>

                <span className="level">
                  {skill.level}
                </span>
              </div>
            ))}
          </div>

          <h3 className="subheading">
            Recommended learning
          </h3>

          <div className="course-list">
            {courses.map((course, index) => (
              <div className="course" key={`${course.course}-${index}`}>
                <div>
                  <strong>{course.course}</strong>
                  <span>{course.provider}</span>
                </div>

                <span>{course.difficulty}</span>
              </div>
            ))}
          </div>
        </>
      )}
    </section>
  );
}

export default SkillGap;