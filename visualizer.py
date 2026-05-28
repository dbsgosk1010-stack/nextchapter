import streamlit.components.v1 as components
from pyvis.network import Network

def draw_book_map(books: list[str], result: dict):
    net = Network(height="600px", width="100%", bgcolor="#0e1117", font_color="white")
    net.barnes_hut(spring_length=180, spring_strength=0.04, gravity=-3000)

    b0, b1, b2 = books[0], books[1], books[2]

    # 입력 책 3권 (빨강)
    for book in books:
        net.add_node(book, label=book, color="#e76f51", size=40,
                     title=f"<b>{book}</b>", font={"size": 16, "color": "white"})

    added_nodes = set(books)

    def add_blue_node(title, author, reason, deeper=None):
        if title not in added_nodes:
            popup = f"<b>📖 추천 도서</b><br>🔵 {title}<br>✍️ {author}<br><br><b>추천 이유:</b><br>{reason}"
            if deeper:
                popup += f"<br><br><b>더 읽어볼 책:</b><br>🟡 {deeper['title']} — {deeper['author']}<br>{deeper['reason']}"
            net.add_node(title, label=title, color="#2a9d8f", size=28,
                         title=popup, font={"size": 13, "color": "white"})
            added_nodes.add(title)

            # 노랑 노드 (deeper)
            if deeper and deeper["title"] not in added_nodes:
                d_popup = f"<b>📖 더 읽어볼 책</b><br>🟡 {deeper['title']}<br>✍️ {deeper['author']}<br><br>{deeper['reason']}"
                net.add_node(deeper["title"], label=deeper["title"], color="#e9c46a", size=20,
                             title=d_popup, font={"size": 12, "color": "white"})
                added_nodes.add(deeper["title"])
                net.add_edge(title, deeper["title"], color="#e9c46a", width=1, dashes=True)

    # 개별 추천
    individual = result.get("individual", {})
    for book in books:
        for rec in individual.get(book, []):
            add_blue_node(rec["title"], rec["author"], rec["reason"], rec.get("deeper"))
            if rec["title"] in added_nodes:
                net.add_edge(book, rec["title"], color="#2a9d8f", width=2,
                             title=rec["reason"], label=rec["reason"][:15]+"...")

    # 쌍/조합 추천
    pairs = result.get("pairs", {})
    pair_map = {
        f"{b0}+{b1}": (b0, b1),
        f"{b1}+{b2}": (b1, b2),
        f"{b0}+{b2}": (b0, b2),
        f"{b0}+{b1}+{b2}": (b0, b2),
    }

    # 입력책 간 연결선
    net.add_edge(b0, b1, color="#888888", width=2,
                 label=pairs.get(f"{b0}+{b1}", {}).get("label", ""),
                 title=pairs.get(f"{b0}+{b1}", {}).get("label", ""))
    net.add_edge(b1, b2, color="#888888", width=2,
                 label=pairs.get(f"{b1}+{b2}", {}).get("label", ""),
                 title=pairs.get(f"{b1}+{b2}", {}).get("label", ""))
    net.add_edge(b0, b2, color="#888888", width=2,
                 label=pairs.get(f"{b0}+{b2}", {}).get("label", ""),
                 title=pairs.get(f"{b0}+{b2}", {}).get("label", ""))

    for key, (src, _) in pair_map.items():
        pair = pairs.get(key, {})
        for rec in pair.get("books", []):
            add_blue_node(rec["title"], rec["author"], rec["reason"], rec.get("deeper"))
            if rec["title"] in added_nodes:
                net.add_edge(src, rec["title"], color="#2a9d8f", width=1,
                             title=rec["reason"], label=rec["reason"][:15]+"...")

    html = net.generate_html()
    components.html(html, height=620)
