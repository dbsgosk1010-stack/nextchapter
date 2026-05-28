import streamlit as st
import streamlit.components.v1 as components
from pyvis.network import Network

def draw_book_map(books: list[str], connections: list[dict], recommendations: list[dict] = None):
    net = Network(height="500px", width="100%", bgcolor="#0e1117", font_color="white")
    net.barnes_hut(spring_length=200, spring_strength=0.05)

    for book in books:
        net.add_node(book, label=book, color="#f4a261", size=35, font={"size": 16, "color": "white"})

    if recommendations:
        for rec in recommendations:
            net.add_node(rec["title"], label=rec["title"], color="#2a9d8f", size=25, font={"size": 14, "color": "white"})
            net.add_edge(books[0], rec["title"], title=rec["reason"], color="#2a9d8f", width=1)

    for conn in connections:
        net.add_edge(conn["from"], conn["to"], title=conn["label"], label=conn["label"], color="#888888", width=2, font={"size": 11, "color": "#aaaaaa"})

    html = net.generate_html()
    components.html(html, height=520)
