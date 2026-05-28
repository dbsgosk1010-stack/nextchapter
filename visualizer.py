import streamlit as st
import streamlit.components.v1 as components
from pyvis.network import Network

def draw_book_map(books: list[str], connections: list[dict]):
    net = Network(height="400px", width="100%", bgcolor="#0e1117", font_color="white")
    net.barnes_hut()

    colors = ["#f4a261", "#2a9d8f", "#e76f51"]
    for i, book in enumerate(books):
        net.add_node(book, label=book, color=colors[i], size=30, font={"size": 14})

    for conn in connections:
        net.add_edge(conn["from"], conn["to"], title=conn["label"], color="#888888", width=2)

    html = net.generate_html()
    components.html(html, height=420)
