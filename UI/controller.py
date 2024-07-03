import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model
        self.minimo = None
        self.massimo = None

    def handle_graph(self, e):
        self._model.creaGrafo()
        self.minimo, self.massimo = self._model.getMinMaxArco()
        self._view.txt_result.controls.clear()
        self._view.txt_result.controls.append(ft.Text(f"nodi: {self._model.dettagliGrafo()[0]}, archi: {self._model.dettagliGrafo()[1]}"))
        self._view.txt_result.controls.append(ft.Text(f"minimo: {self.minimo}, massimo: {self.massimo}"))
        self._view.update_page()

    def handle_countedges(self, e):
        if int(self._view.txt_soglia.value) < self.minimo or int(self._view.txt_soglia.value) > self.massimo:
            self._view.txt_result2.controls.clear()
            self._view.txt_result2.controls.append(ft.Text("Soglia balorda"))
        else:
            minori, maggiori = self._model.getArchiSoglia(int(self._view.txt_soglia.value))
            self._view.txt_result2.controls.clear()
            self._view.txt_result2.controls.append(ft.Text(f"Archi sotto la soglia: {minori}"))
            self._view.txt_result2.controls.append(ft.Text(f"Archi sopra la soglia: {maggiori}"))
            self._view.update_page()

    def handle_search(self, e):
        cammino, lun = self._model.trovaCammino(int(self._view.txt_soglia.value))
        self._view.txt_result3.controls.clear()
        self._view.txt_result3.controls.append(ft.Text(f"Peso cammino massimo: {lun}"))
        self._view.txt_result3.controls.append(ft.Text(f"Cammino: {cammino}"))
        self._view.update_page()