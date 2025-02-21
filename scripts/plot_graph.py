from pathlib import Path

from app.agent.graph import graph

root_dir = Path(__file__).parents[1]
image_dir = root_dir / "images"
graph_path = image_dir / "graph.png"


graph_path.write_bytes(graph.get_graph().draw_mermaid_png())
