from __future__ import annotations
from copy import deepcopy
from numpy import ndarray
from numpy.random import choice, normal, rand
from pydantic import BaseModel


class Operation(BaseModel):
    type: str
    params: list[float]


class Neuron(BaseModel):
    neuron_id: str
    max_inputs: int
    input_ids: list[str]
    operations: list[Operation]


class MutationSetup(BaseModel):
    n_clones: int
    prob_create_neuron: float
    prob_delete_neuron: float
    prob_create_connection: float
    prob_delete_connection: float
    max_hidden_layers: int
    max_hidden_neurons: int
    max_connections: int


class Brain(BaseModel):
    
    neurons: list[Neuron]
    current_id: int
    layers: list[list[str]]|None = None

    def clone(self) -> Brain:
        return deepcopy(self)
    
    def get_next_id(self) -> str:
        next_id: str = f"n{self.current_id}"
        self.current_id += 1
        return next_id

    def get_neuron(
            self,
            neuron_id: str,
        ) -> Neuron|None:
        for n in self.neurons:
            if n.neuron_id == neuron_id:
                return n
        return None
    
    def get_hidden_neurons(self) -> list[Neuron]:
        hidden_neurons: list[Neuron] = []
        for n in self.neurons:
            if n.neuron_id.startswith("n"):
                hidden_neurons.append(n)
        return hidden_neurons
    
    def get_neuron_layer(self, neuron: Neuron) -> int:
        if self.layers is None:
            self.build_layers()
        if self.layers is not None:
            for i, l in enumerate(self.layers):
                for n in l:
                    if n == neuron.neuron_id:
                        return i
        return -1
    
    def count_connections(self) -> int:
        connections: int = 0
        for n in self.neurons:
            connections += len(n.input_ids)
        return connections
    
    def build_layers(self) -> None:
        self.layers = []
        for n in self.neurons:
            if n.neuron_id.startswith("t"):
                self.place_neuron(n, 0)
        if self.layers is not None:
            input_layer: int = len(self.layers)
            for n in self.neurons:
                if n.neuron_id.startswith("s") or n.neuron_id.startswith("v"):
                    self.place_neuron(n, input_layer)
            if len(self.layers[-2]) == 0:
                self.layers.pop(-2)
                
    def create_layer(self, i: int) -> None:
        if self.layers is None:
            self.layers = []
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
        if self.layers is not None:
            for i, l in enumerate(self.layers):
                for j, n in enumerate(l):
                    if neuron.neuron_id == n:
                        coords = (i, j)
                        break
                if coords != (-1, -1):
                    break
        return coords
        
    def add_neuron_to_layer(self, neuron: Neuron, layer: int) -> None:
        current_layer: int = self.get_neuron_coords(neuron)[0]
        if current_layer != -1 and current_layer != layer:
            self.remove_neuron_from_layer(neuron)
        self.create_layer(layer)
        if self.layers is not None:
            self.layers[layer].append(neuron.neuron_id)
    
    def remove_neuron_from_layer(self, neuron: Neuron) -> None:
        if self.layers is not None:
            for l in self.layers:
                for n in l:
                    if n == neuron.neuron_id:
                        l.remove(n)
    
    def create_hidden_neuron(
            self,
            b: float = 0.,
            leakage: float = .01
        ) -> Neuron:
        neuron_id: str = self.get_next_id()
        operations: list[Operation] = []
        operations.append(
            Operation(
                type = "linear_combination",
                params = [b])
        )
        operations.append(
            Operation(
                type = "relu",
                params = [leakage],
            )
        )
        neuron: Neuron = Neuron(
            neuron_id = neuron_id,
            max_inputs = -1,
            input_ids = [],
            operations = operations,
        )
        self.neurons.append(neuron)
        return neuron
    
    def mutate(
            self,
            setup: MutationSetup,
        ) -> list[Brain]:
        self.build_layers()
        if setup.max_hidden_neurons > 0:
            if len(self.get_hidden_neurons()) > setup.max_hidden_neurons:
                setup.prob_create_neuron = 0.
        if len(self.get_hidden_neurons()) == 0:
            setup.prob_delete_neuron = 0.
        if setup.max_connections > 0:
            if self.count_connections() > setup.max_connections:
                setup.prob_create_connection = 0.
        if self.count_connections() == 0:
            setup.prob_delete_connection = 0.
        clones: list[Brain] = []
        for _ in range(setup.n_clones):
            clone: Brain = self.clone()
            rng: float = rand()
            accum_prob_create_neuron: float = setup.prob_create_neuron
            accum_prob_delete_neuron: float = setup.prob_delete_neuron + accum_prob_create_neuron
            accum_prob_create_connection: float = setup.prob_create_connection + accum_prob_delete_neuron
            accum_prob_delete_connection: float = setup.prob_delete_connection + accum_prob_create_connection
            print(f"RNG: {rng:.2f}")
            print(f"Probs: {accum_prob_create_neuron:.2f}, {accum_prob_delete_neuron:.2f}, {accum_prob_create_connection:.2f}, {accum_prob_delete_connection:.2f}")
            if accum_prob_create_neuron > rng:
                clone.mutate_creating_neuron(setup.max_hidden_layers)
            elif accum_prob_delete_neuron > rng:
                clone.mutate_deleting_neuron()
            elif accum_prob_create_connection > rng:
                clone.mutate_creating_connection(setup.max_hidden_layers)
            elif accum_prob_delete_connection > rng:
                clone.mutate_removing_connection()
            else:
                clone.mutate_weights()
            clone.build_layers()
            clones.append(clone)
        return clones
    
    def mutate_weights(
            self,
            amount: int = 1,
            std: float = 1.,
            weight_amount: int = 1,
        ) -> None:
        neurons_with_weights: list[Neuron] = []
        for n in self.neurons:
            if len(n.operations) > 0 and n.operations[0].type == "linear_combination":
                neurons_with_weights.append(n)
        if amount == -1:
            amount = len(neurons_with_weights)
        neuron_idx: ndarray = choice(
            range(len(neurons_with_weights)),
            size = amount,
            replace = False,
        )
        for i in neuron_idx:
            self.mutate_weights_from_neuron(
                neurons_with_weights[i],
                std,
                weight_amount,
            )

    def mutate_weights_from_neuron(
            self,
            neuron: Neuron,
            std: float = 1.,
            amount: int = 1,
        ) -> None:
        lin_op: Operation|None = None
        for op in neuron.operations:
            if op.type == "linear_combination":
                lin_op = op
        if lin_op is not None:
            if amount == -1:
                amount = len(lin_op.params)
            w_idx: ndarray = choice(
                range(len(lin_op.params)),
                size = amount,
                replace = False,
            )
            for i in w_idx:
                lin_op.params[i] += normal(0., std)
    
    def mutate_removing_connection(
            self,
            amount: int = 1,
        ) -> None:
        for _ in range(amount):
            neurons_with_input: list[Neuron] = []
            for n in self.neurons:
                if len(n.input_ids) > 0:
                    neurons_with_input.append(n)
            if len(neurons_with_input) > 0:
                idx: int = choice(range(len(neurons_with_input)))
                neuron: Neuron = neurons_with_input[idx]
                self.remove_random_input_from_neuron(neuron)
            else:
                return

    def remove_random_input_from_neuron(
            self,
            neuron: Neuron,
            amount: int = 1,
        ) -> None:
        amount = min(amount, len(neuron.input_ids))
        input_idx: ndarray = choice(
            range(len(neuron.input_ids)),
            size = amount,
            replace = False,
        )
        input_idx[::-1].sort() # ordena decrescente para evitar IndexError
        for i in input_idx:
            self.remove_input_from_neuron(neuron, i)

    def remove_input_from_neuron(
            self,
            neuron: Neuron,
            input_idx: int,
        ) -> None:
        if input_idx in range(len(neuron.input_ids)):
            del neuron.input_ids[input_idx]
            del neuron.operations[0].params[input_idx+1]

    def mutate_creating_connection(
            self,
            max_hidden_layers: int,
            amount: int = 1,
            std: float = 1.,
        ) -> None:
        for _ in range(amount):
            full_layers: bool = max_hidden_layers > 0 and self.layers is not None and (len(self.layers)-2) >= max_hidden_layers
            possible_inputs: list[Neuron] = []
            for n in self.neurons:
                if len(self.get_possible_connections_from_input(n, full_layers)) > 0:
                    possible_inputs.append(n)
            if len(possible_inputs) > 0:
                input_idx: int = choice(range(len(possible_inputs)))
                input_n: Neuron = possible_inputs[input_idx]
                possible_outputs: list[Neuron] = self.get_possible_connections_from_input(input_n, full_layers)
                output_idx: int = choice(range(len(possible_outputs)))
                output_n: Neuron = possible_outputs[output_idx]
                self.connect_neurons(output_n, input_n, std)
            else:
                return
    
    def get_possible_connections_from_input(
            self,
            input_n: Neuron,
            only_forward_layers: bool = False,
        ) -> list[Neuron]:
        input_layer: int = self.get_neuron_layer(input_n)
        possible_connections: list[Neuron] = []
        if not input_n.neuron_id.startswith("t"):
            for n in self.neurons:
                if n == input_n:
                    continue
                elif input_n.neuron_id in n.input_ids:
                    continue
                elif n.max_inputs != -1 and len(n.input_ids) >= n.max_inputs:
                    continue
                elif n in self.get_recursive_inputs(input_n): # impede conexões cíclicas
                    continue
                elif only_forward_layers and input_layer <= self.get_neuron_layer(n):
                    continue
                possible_connections.append(n)
        return possible_connections
    
    def get_recursive_inputs(
            self,
            neuron: Neuron,
        ) -> list[Neuron]:
        all_inputs: list[Neuron] = []
        for input_id in neuron.input_ids:
            if input_id not in all_inputs:
                input_n: Neuron|None = self.get_neuron(input_id)
                if input_n is not None:
                    all_inputs.append(input_n)
                    for rec_input_n in self.get_recursive_inputs(input_n):
                        if rec_input_n not in all_inputs:
                            all_inputs.append(rec_input_n)
        return all_inputs
    
    def connect_neurons(
            self,
            output_n: Neuron,
            input_n: Neuron,
            std: float = 1.,
        ) -> None:
        output_n.input_ids.append(input_n.neuron_id)
        output_n.operations[0].params.append(normal(scale = std))

    def mutate_deleting_neuron(
            self,
            amount: int = 1,
        ) -> None:
        deletable_neurons: list[Neuron] = []
        for n in self.neurons:
            if n.neuron_id.startswith("n"):
                deletable_neurons.append(n)
        amount = min(amount, len(deletable_neurons))
        delete_idx: ndarray = choice(
            range(len(deletable_neurons)),
            size = amount,
            replace = False,
        )
        for i in delete_idx:
            self.delete_neuron(deletable_neurons[i])

    def delete_neuron(self, neuron: Neuron) -> None:
        if neuron in self.neurons:
            for n in self.neurons:
                if neuron.neuron_id in n.input_ids:
                    input_idx: int = n.input_ids.index(neuron.neuron_id)
                    self.remove_input_from_neuron(n, input_idx)
            self.neurons.remove(neuron)

    def mutate_creating_neuron(
            self,
            max_hidden_layers: int,
            amount: int = 1,
            n_inputs: int = 1,
            n_outputs: int = 1,
        ) -> None:
        for _ in range(amount):
            full_layers: bool = max_hidden_layers > 0 and self.layers is not None and (len(self.layers)-2) >= max_hidden_layers
            new_neuron: Neuron = self.create_hidden_neuron()
            possible_inputs: list[Neuron] = []
            for n in self.neurons:
                if n.neuron_id != new_neuron.neuron_id and not n.neuron_id.startswith("t"):
                    if not full_layers or self.get_neuron_layer(n) > 1:
                        possible_inputs.append(n)
            for _ in range(n_inputs):
                if len(possible_inputs) > 0:
                    input_idx: int = choice(range(len(possible_inputs)))
                    input_n: Neuron = possible_inputs[input_idx]
                    self.connect_neurons(new_neuron, input_n)
                    possible_inputs.remove(input_n)
                else:
                    break
            for _ in range(n_outputs):
                possible_outputs: list[Neuron] = self.get_possible_connections_from_input(new_neuron, full_layers)
                if len(possible_outputs) > 0:
                    output_idx: int = choice(range(len(possible_outputs)))
                    output_n: Neuron = possible_outputs[output_idx]
                    self.connect_neurons(output_n, new_neuron)
                else:
                    break