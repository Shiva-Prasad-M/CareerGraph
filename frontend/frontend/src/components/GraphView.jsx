import {
  ReactFlow,
  Background,
  Controls,
  MiniMap,
} from "@xyflow/react";

import "@xyflow/react/dist/style.css";

function GraphView({ data }) {
  const nodesMap = new Map();
  const edges = [];

  data.forEach((item, index) => {
    const skillId = `skill-${item.skill}`;
    const relatedId = `related-${item.relatedSkill}`;
    const roleId = `role-${item.role}`;
    const companyId = `company-${item.company}`;

    // Selected skill
    if (!nodesMap.has(skillId)) {
      nodesMap.set(skillId, {
        id: skillId,
        position: { x: 0, y: index * 140 },
        className: "career-node skill-node",
        data: { label: item.skill },
      });
    }

    // Related skill
    if (!nodesMap.has(relatedId)) {
      nodesMap.set(relatedId, {
        id: relatedId,
        position: { x: 280, y: index * 140 },
        className: "career-node related-node",
        data: { label: item.relatedSkill },
      });
    }

    // Role
    if (!nodesMap.has(roleId)) {
      nodesMap.set(roleId, {
        id: roleId,
        position: { x: 560, y: index * 140 },
        className: "career-node role-node",
        data: { label: item.role },
      });
    }

    // Company
    if (!nodesMap.has(companyId)) {
      nodesMap.set(companyId, {
        id: companyId,
        position: { x: 840, y: index * 140 },
        className: "career-node company-node",
        data: { label: item.company },
      });
    }

    edges.push(
      {
        id: `${skillId}-${relatedId}`,
        source: skillId,
        target: relatedId,
        label: "RELATED_TO",
      },
      {
        id: `${relatedId}-${roleId}`,
        source: relatedId,
        target: roleId,
        label: "REQUIRED_FOR",
      },
      {
        id: `${roleId}-${companyId}`,
        source: roleId,
        target: companyId,
        label: "OFFERED_BY",
      }
    );
  });

  const uniqueEdges = Array.from(
    new Map(edges.map((edge) => [edge.id, edge])).values()
  );

  return (
    <div className="graph-container">
      <ReactFlow
        nodes={Array.from(nodesMap.values())}
        edges={uniqueEdges}
        fitView
      >
        <Background />
        <Controls />
        <MiniMap />
      </ReactFlow>
    </div>
  );
}

export default GraphView;