from __future__ import annotations

from .point import Point


class Operation():

    type: str
    params: list[float]

    def __init__(
            self,
            _type: str,
            _params: list[float],
        ) -> None:
        self.type = _type
        self.params = _params
    
    @staticmethod
    def from_dict(_dict: dict) -> Operation:
        return Operation(
            _dict["type"],
            _dict["params"],
        )


class Neuron():

    neuron_id: str
    max_inputs: int
    input_ids: list[str]
    operations: list[Operation]

    def __init__(
            self,
            _neuron_id: str,
            _max_inputs: int,
            _input_ids: list[str],
            _operations: list[Operation],
        ) -> None:
        self.neuron_id = _neuron_id
        self.max_inputs = _max_inputs
        self.input_ids = _input_ids
        self.operations = _operations
    
    @staticmethod
    def from_dict(_dict: dict) -> Neuron:
        return Neuron(
            _dict["neuron_id"],
            _dict["max_inputs"],
            _dict["input_ids"],
            [Operation.from_dict(op) for op in _dict["operations"]],
        )
    
    def generate_hover_text(self) -> str:
        text: str = f"<b>{self.neuron_id}</b>"
        if len(self.operations) > 0:
            for i, w in enumerate(self.operations[0].params):
                if i == 0:
                    text += f"<br>b: {w:+.2f}"
                else:
                    text +=f"<br>{self.input_ids[i-1]}: {w:+.2f}"
        return text


class Brain():

    neurons: list[Neuron]
    current_id: int

    layers: list[list[Neuron]]

    def __init__(
            self,
            _neurons: list[Neuron],
            _current_id: int,
        ) -> None:
        self.neurons = _neurons
        self.current_id = _current_id

        self.layers = []
        self.build_layers()
    
    @staticmethod
    def from_dict(_dict: dict) -> Brain:
        return Brain(
            [Neuron.from_dict(n) for n in _dict["neurons"]],
            _dict["current_id"],
        )
    
    def get_neuron(self, neuron_id: str) -> Neuron|None:
        for n in self.neurons:
            if n.neuron_id == neuron_id:
                return n
        return None
    
    def build_layers(self) -> None:
        for n in self.neurons:
            if n.neuron_id.startswith("t"):
                self.place_neuron(n, 0)
        input_layer: int = len(self.layers)
        for n in self.neurons:
            if n.neuron_id.startswith("s") or n.neuron_id.startswith("v"):
                self.place_neuron(n, input_layer)
        if len(self.layers[-2]) == 0:
            self.layers.pop(-2)
                
    def create_layer(self, i: int) -> None:
        while len(self.layers) < i+1:
            self.layers.append([])
    
    def place_neuron(self, neuron: Neuron, desired_layer: int) -> None:
        current_layer: int = self.get_neuron_coords(neuron)[0]
        if current_layer == -1 or current_layer < desired_layer:
            self.add_neuron_to_layer(neuron, desired_layer)
            for n_id in neuron.input_ids:
                input_n: Neuron|None = self.get_neuron(n_id)
                if input_n is not None:
                    self.place_neuron(input_n, desired_layer+1)

    def get_neuron_coords(self, neuron: Neuron) -> tuple[int, int]:
        coords: tuple[int, int] = (-1, -1)
        for i, l in enumerate(self.layers):
            for j, n in enumerate(l):
                if neuron == n:
                    coords = (i, j)
                    break
            if coords != (-1, -1):
                break
        return coords
        
    def add_neuron_to_layer(self, neuron: Neuron, i: int) -> None:
        current_layer: int = self.get_neuron_coords(neuron)[0]
        if current_layer != -1 and current_layer != i:
            self.remove_neuron_from_layer(neuron)
        self.create_layer(i)
        self.layers[i].append(neuron)
    
    def remove_neuron_from_layer(self, neuron: Neuron) -> None:
        for l in self.layers:
            for n in l:
                if n == neuron:
                    l.remove(neuron)
    
    def convert_plot_coords(self, layer: int, position: int) -> tuple[float, float]:
        h_spacing: float = 50.
        x: float = layer * h_spacing
        v_spacing: float = 20.
        max_h: float = max(len(l) for l in self.layers) * v_spacing
        delta_h: float = max_h - len(self.layers[layer]) * v_spacing
        y: float = delta_h / 2. + position * v_spacing
        return (x, y)

    def generate_traces_and_annotations(self) -> tuple[list[dict], list[dict]]:

        neuron_xs: list[float] = []
        neuron_ys: list[float] = []
        neuron_txt: list[str] = []
        conn_xs: list[float|None] = []
        conn_ys: list[float|None] = []
        annotations: list[dict] = []

        for i, l in enumerate(self.layers):
            for j, n in enumerate(l):
                n_x, n_y = self.convert_plot_coords(i, j)
                neuron_xs.append(n_x)
                neuron_ys.append(n_y)
                neuron_txt.append(n.generate_hover_text())
                annotations.append({
                    "x": n_x,
                    "y": n_y,
                    "text": n.neuron_id,
                    "showarrow": False,
                    "xshift": -10,
                    "yshift": 10,
                })
                for input_id in n.input_ids:
                    input_n: Neuron|None = self.get_neuron(input_id)
                    if input_n is not None:
                        input_x, input_y = self.convert_plot_coords(
                            *self.get_neuron_coords(input_n)
                        )
                        conn_xs.extend([input_x, n_x, None])
                        conn_ys.extend([input_y, n_y, None])

        traces: list[dict] = [
            {
                "type": "scatter",
                "mode": "lines",
                "x": conn_xs,
                "y": conn_ys,
                "line": {
                    "width": 1.,
                },
                "hoverinfo": "none",
            },
            {
                "type": "scatter",
                "mode": "markers",
                "x": neuron_xs,
                "y": neuron_ys,
                "text": neuron_txt,
                "marker": {
                    "size": 10,
                },
                "hoverinfo": "text",
                "textposition": "middle left",
            },
            
        ]
        return traces, annotations