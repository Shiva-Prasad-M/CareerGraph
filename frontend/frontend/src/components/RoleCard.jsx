function RoleCard({ role, selected, onClick }) {
  return (
    <button
      className={`role-card ${selected ? "selected" : ""}`}
      onClick={onClick}
    >
      <span className="role-label">
        CAREER MATCH
      </span>

      <h3>{role.role}</h3>

      <div className="match-score">
        {role.match_percentage ?? role.score ?? 0}%
      </div>

      <span className="role-action">
        View skill gap →
      </span>
    </button>
  );
}

export default RoleCard;