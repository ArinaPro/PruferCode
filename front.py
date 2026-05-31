import customtkinter
from functions import *
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import networkx as nx

class GraphWindow(customtkinter.CTkToplevel):
    def __init__(self, master, graph):
        super().__init__(master)

        self.bg_color = "#E4D3F5"
        self.configure(fg_color=self.bg_color)
        self.geometry("400x300")
        self.title("Graph Output")

        G = nx.Graph()
        for i in range(1, len(graph[0])+1):
            G.add_node(i)

        for edge in range(len(graph[0])-2):
            G.add_edge(int(graph[0][edge]), int(graph[1][edge]))
        G.add_edge(int(graph[0][-1]), int(graph[0][-2]))

        fig, ax = plt.subplots(figsize=(8, 6))
        pos = nx.spring_layout(G, seed=7, k=1)

        fig.set_facecolor(self.bg_color)
        ax.set_facecolor(self.bg_color)

        nx.draw_networkx_nodes(G, pos, node_color="lightyellow", node_size=800)
        nx.draw_networkx_edges(G, pos, edge_color="white", width=2)
        nx.draw_networkx_labels(G, pos, font_size=10, font_family="sans-serif", font_weight="bold")


        title_str = "Graph "+(''.join(list(graph[1])[:(len(graph[0]) - 2)]))
        ax.set_title(title_str)
        ax.axis("off")

        canvas = FigureCanvasTkAgg(fig, master=self)
        canvas.draw()
        canvas.get_tk_widget().configure(bg=self.bg_color)
        canvas.get_tk_widget().pack(pady=20)

        # label = customtkinter.CTkLabel(self, text=str(graph))
        # label.pack(pady=20)


class MainWindow(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        self.configure(fg_color="#E4D3F5")
        self.geometry("400x300")
        self.title("Encoder/Decoder")
        self.bg_color = "#E4D3F5"

        button_decoder = customtkinter.CTkButton(
            self,
            text="Decode",
            command=self.button_decoder_funk,
            fg_color=("#A066D1", "#6803A3"),
            width=200,
            height=40,
            corner_radius=10,
            text_color="#520366"
        )
        button_decoder.pack(padx=20, pady=20)

        self.toplevel_window = None

    def button_decoder_funk(self):
        dialog = customtkinter.CTkInputDialog(
            text="Input Prüfer Code",
            title="Decoder Input",
            fg_color=("#A066D1", "#6803A3"),
            button_fg_color="#520366",
            entry_fg_color=self.bg_color
        )

        input_value = dialog.get_input()

        if not input_value:
            return

        graph = decoder(input_value)

        if self.toplevel_window is None or not self.toplevel_window.winfo_exists():
            self.toplevel_window = GraphWindow(self, graph)
        else:
            self.toplevel_window.focus()


app = MainWindow()
app.mainloop()