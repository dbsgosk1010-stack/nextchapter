import streamlit.components.v1 as components
from pyvis.network import Network
import json

def draw_book_map(books: list[str], result: dict):
    net = Network(height="600px", width="100%", bgcolor="#0e1117", font_color="white")
    net.barnes_hut(spring_length=180, spring_strength=0.04, gravity=-3000)

    # 드래그 후 고정되도록 옵션 설정
    net.set_options(json.dumps({
        "physics": {
            "barnesHut": {
                "springLength": 180,
                "springConstant": 0.04,
                "gravitationalConstant": -3000
            },
            "stabilization": {"iterations": 150}
        },
        "interaction": {
            "dragNodes": True,
            "hover": True
        },
        "nodes": {
            "fixed": {"x": False, "y": False}
        }
    }))

    b0, b1, b2 = books[0], books[1], books[2]

    for book in books:
        net.add_node(book, label=book, color="#e76f51", size=40,
                     title=f"<b>{book}</b>", font={"size": 16, "color": "white"})

    added_nodes = set(books)
    blue_nodes = []  # 나중에 노란 연결 체크용

    def make_popup(title, author, reason):
        return f"<b>📖 추천 도서</b><br><b>{title}</b><br>✍️ {author}<br><br><b>추천 이유:</b><br>{reason}"

    def add_blue(title, author, reason):
        if title not in added_nodes:
            net.add_node(title, label=title, color="#2a9d8f", size=28,
                         title=make_popup(title, author, reason),
                         font={"size": 13, "color": "white"})
            added_nodes.add(title)
            blue_nodes.append({"title": title, "author": author, "reason": reason})

    # 개별 추천
    individual = result.get("individual", {})
    for book in books:
        for rec in individual.get(book, []):
            add_blue(rec["title"], rec["author"], rec["reason"])
            if rec["title"] in added_nodes:
                net.add_edge(book, rec["title"], color="#2a9d8f", width=2,
                             title=rec["reason"], label=rec["reason"][:12]+"...")

    # 쌍/조합 추천
    pairs = result.get("pairs", {})
    pair_keys = [f"{b0}+{b1}", f"{b1}+{b2}", f"{b0}+{b2}", f"{b0}+{b1}+{b2}"]
    pair_sources = {
        f"{b0}+{b1}": b0, f"{b1}+{b2}": b1,
        f"{b0}+{b2}": b0, f"{b0}+{b1}+{b2}": b0
    }

    for key in pair_keys:
        pair = pairs.get(key, {})
        src = pair_sources[key]
        for rec in pair.get("books", []):
            add_blue(rec["title"], rec["author"], rec["reason"])
            if rec["title"] in added_nodes:
                net.add_edge(src, rec["title"], color="#2a9d8f", width=1,
                             title=rec["reason"], label=rec["reason"][:12]+"...")

    # 입력책 간 연결선 (키워드)
    net.add_edge(b0, b1, color="#888888", width=2,
                 label=pairs.get(f"{b0}+{b1}", {}).get("label", ""),
                 title=pairs.get(f"{b0}+{b1}", {}).get("label", ""))
    net.add_edge(b1, b2, color="#888888", width=2,
                 label=pairs.get(f"{b1}+{b2}", {}).get("label", ""),
                 title=pairs.get(f"{b1}+{b2}", {}).get("label", ""))
    net.add_edge(b0, b2, color="#888888", width=2,
                 label=pairs.get(f"{b0}+{b2}", {}).get("label", ""),
                 title=pairs.get(f"{b0}+{b2}", {}).get("label", ""))

    # 노란 노드: 파란 노드 간 주제 연결이 있을 때만
    yellow_connections = result.get("yellow_connections", [])
    for yc in yellow_connections:
        ytitle = yc.get("title", "")
        if ytitle and ytitle not in added_nodes:
            net.add_node(ytitle, label=ytitle, color="#e9c46a", size=20,
                         title=f"<b>🔗 연결 추천</b><br><b>{ytitle}</b><br>✍️ {yc.get('author','')}<br><br>{yc.get('reason','')}",
                         font={"size": 12, "color": "white"})
            added_nodes.add(ytitle)
        for conn in yc.get("connects", []):
            if conn in added_nodes:
                net.add_edge(ytitle, conn, color="#e9c46a", width=1, dashes=True)

    # 드래그 고정 JS 삽입
    html = net.generate_html()
    fix_js = """
    <script>
    document.addEventListener('DOMContentLoaded', function() {
        setTimeout(function() {
            if (typeof network !== 'undefined') {
                network.on("dragEnd", function(params) {
                    if (params.nodes.length > 0) {
                        params.nodes.forEach(function(nodeId) {
                            network.body.nodes[nodeId].options.fixed.x = true;
                            network.body.nodes[nodeId].options.fixed.y = true;
                        });
                    }
                });
            }
        }, 1000);
    });
    </script>
    """
    html = html.replace("</body>", fix_js + "</body>")
    components.html(html, height=620)
