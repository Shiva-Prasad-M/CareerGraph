function GraphStats({ stats }) {
  if (!stats) {
    return null;
  }

  return (
    <div className="stats-grid">
      <div className="stat-card">
        <span>GRAPH NODES</span>
        <strong>{stats.nodes}</strong>
      </div>

      <div className="stat-card">
        <span>RELATIONSHIPS</span>
        <strong>{stats.relationships}</strong>
      </div>
    </div>
  );
}

export default GraphStats;