from flask import Blueprint, flash, render_template, request

from dsa.graph import RailwayGraph

routes_bp = Blueprint("routes", __name__)


@routes_bp.route("/route-finder", methods=["GET", "POST"])
def route_finder():
    if request.method == "POST":
        source = (request.form.get("source") or "").strip()
        destination = (request.form.get("destination") or "").strip()
        if not source or not destination:
            flash("Source and destination are required.", "danger")
            return render_template("routes.html")
        graph = RailwayGraph()
        connections = [
            ("Bareilly", "Delhi"), ("Delhi", "Agra"), ("Agra", "Jaipur"), ("Delhi", "Lucknow"),
            ("Lucknow", "Kanpur"), ("Jaipur", "Jodhpur"), ("Bareilly", "Lucknow"), ("Chandigarh", "Delhi")
        ]
        for station_a, station_b in connections:
            graph.add_edge(station_a, station_b)
        bfs_path, _ = graph.bfs(source, destination)
        dfs_path = graph.dfs(source)
        return render_template("routes.html", source=source, destination=destination, bfs_path=bfs_path, dfs_path=dfs_path)
    return render_template("routes.html")


@routes_bp.route("/api/routes")
def api_routes():
    graph = RailwayGraph()
    connections = [
        ("Bareilly", "Delhi"), ("Delhi", "Agra"), ("Agra", "Jaipur"), ("Delhi", "Lucknow"),
        ("Lucknow", "Kanpur"), ("Jaipur", "Jodhpur"), ("Bareilly", "Lucknow"), ("Chandigarh", "Delhi")
    ]
    for station_a, station_b in connections:
        graph.add_edge(station_a, station_b)
    return {"success": True, "stations": list(graph.graph.keys())}


@routes_bp.route("/api/routes/find", methods=["POST"]) 
def api_routes_find():
    data = request.get_json(silent=True) or request.form
    source = (data.get("source") or "").strip()
    destination = (data.get("destination") or "").strip()
    if not source or not destination:
        return {"success": False, "message": "Source and destination are required."}, 400
    graph = RailwayGraph()
    connections = [
        ("Bareilly", "Delhi"), ("Delhi", "Agra"), ("Agra", "Jaipur"), ("Delhi", "Lucknow"),
        ("Lucknow", "Kanpur"), ("Jaipur", "Jodhpur"), ("Bareilly", "Lucknow"), ("Chandigarh", "Delhi")
    ]
    for station_a, station_b in connections:
        graph.add_edge(station_a, station_b)
    bfs_path, explored = graph.bfs(source, destination)
    return {"success": True, "source": source, "destination": destination, "bfs": bfs_path, "explored": sorted(explored)}
