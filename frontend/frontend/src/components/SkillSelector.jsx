function SkillSelector({ skills, selectedSkills, onChange }) {
  function toggleSkill(skill) {
    if (selectedSkills.includes(skill)) {
      onChange(
        selectedSkills.filter((item) => item !== skill)
      );
    } else {
      onChange([...selectedSkills, skill]);
    }
  }

  return (
    <div className="skill-selector">
      <div className="skill-grid">
        {skills.map((skill) => (
          <button
            key={skill.name}
            className={
              selectedSkills.includes(skill.name)
                ? "skill active"
                : "skill"
            }
            onClick={() => toggleSkill(skill.name)}
          >
            {skill.name}
          </button>
        ))}
      </div>
    </div>
  );
}

export default SkillSelector;