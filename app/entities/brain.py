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
    

class MutationSetup():

    n_clones: int
    prob_create_neuron: float
    prob_delete_neuron: float
    prob_create_connection: float
    prob_delete_connection: float
    max_hidden_layers: int
    max_hidden_neurons: int
    max_connections: int

    def __init__(
            self,
            _n_clones: int,
            _prob_create_neuron: float,
            _prob_delete_neuron: float,
            _prob_create_connection: float,
            _prob_delete_connection: float,
            _max_hidden_layers: int,
            _max_hidden_neurons: int,
            _max_connections: int,
        ) -> None:
        self.n_clones = _n_clones
        self.prob_create_neuron = _prob_create_neuron
        self.prob_delete_neuron = _prob_delete_neuron
        self.prob_create_connection = _prob_create_connection
        self.prob_delete_connection = _prob_delete_connection
        self.max_hidden_layers = _max_hidden_layers
        self.max_hidden_neurons = _max_hidden_neurons
        self.max_connections = _max_connections
    
    @staticmethod
    def from_dict(_dict: dict) -> MutationSetup:
        return MutationSetup(
            _dict["n_clones"],
            _dict["prob_create_neuron"],
            _dict["prob_delete_neuron"],
            _dict["prob_create_connection"],
            _dict["prob_delete_connection"],
            _dict["max_hidden_layers"],
            _dict["max_hidden_neurons"],
            _dict["max_connections"],
        )
    
    def to_dict(self) -> dict:
        return {
            "n_clones": self.n_clones,
            "prob_create_neuron": self.prob_create_neuron,
            "prob_delete_neuron": self.prob_delete_neuron,
            "prob_create_connection": self.prob_create_connection,
            "prob_delete_connection": self.prob_delete_connection,
            "max_hidden_layers": self.max_hidden_layers,
            "max_hidden_neurons": self.max_hidden_neurons,
            "max_connections": self.max_connections,
        }


class Brain():

    neurons: list[Neuron]
    current_id: int
    layers: list[list[str]]

    def __init__(
            self,
            _neurons: list[Neuron],
            _current_id: int,
            _layers: list[list[str]],
        ) -> None:
        self.neurons = _neurons
        self.current_id = _current_id
        self.layers = _layers
    
    @staticmethod
    def from_dict(_dict: dict) -> Brain:
        return Brain(
            [Neuron.from_dict(n) for n in _dict["neurons"]],
            _dict["current_id"],
            _dict["layers"],
        )
    
    def get_neuron(self, neuron_id: str) -> Neuron|None:
        for n in self.neurons:
            if n.neuron_id == neuron_id:
                return n
        return None

    def get_neuron_coords(self, neuron: Neuron) -> tuple[int, int]:
        coords: tuple[int, int] = (-1, -1)
        for i, l in enumerate(self.layers):
            for j, n in enumerate(l):
                if n == neuron.neuron_id:
                    coords = (i, j)
                    break
            if coords != (-1, -1):
                break
        return coords
    
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
                neuron: Neuron|None = self.get_neuron(n)
                if neuron is not None:
                    n_x, n_y = self.convert_plot_coords(i, j)
                    neuron_xs.append(n_x)
                    neuron_ys.append(n_y)
                    neuron_txt.append(neuron.generate_hover_text())
                    annotations.append({
                        "x": n_x,
                        "y": n_y,
                        "text": n,
                        "showarrow": False,
                        "xshift": -10,
                        "yshift": 10,
                    })
                    for input_id in neuron.input_ids:
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