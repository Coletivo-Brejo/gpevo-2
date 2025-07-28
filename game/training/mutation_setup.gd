extends Resource
class_name MutationSetup

@export var n_clones: int
@export var prob_create_neuron: float
@export var prob_delete_neuron: float
@export var prob_create_connection: float
@export var prob_delete_connection: float
@export var max_hidden_layers: int
@export var max_hidden_neurons: int
@export var max_connections: int


static func create(
        _n_clones: int,
        _prob_create_neuron: float,
        _prob_delete_neuron: float,
        _prob_create_connection: float,
        _prob_delete_connection: float,
        _max_hidden_layers: int,
        _max_hidden_neurons: int,
        _max_connections: int,
    ) -> MutationSetup:
    var setup = MutationSetup.new()
    setup.n_clones = _n_clones
    setup.prob_create_neuron = _prob_create_neuron
    setup.prob_delete_neuron = _prob_delete_neuron
    setup.prob_create_connection = _prob_create_connection
    setup.prob_delete_connection = _prob_delete_connection
    setup.max_hidden_layers = _max_hidden_layers
    setup.max_hidden_neurons = _max_hidden_neurons
    setup.max_connections = _max_connections
    return setup

static func from_dict(dict: Dictionary) -> MutationSetup:
    var setup = MutationSetup.create(
        dict["n_clones"],
        dict["prob_create_neuron"],
        dict["prob_delete_neuron"],
        dict["prob_create_connection"],
        dict["prob_delete_connection"],
        dict["max_hidden_layers"],
        dict["max_hidden_neurons"],
        dict["max_connections"],
    )
    return setup

func to_dict() -> Dictionary:
    return {
        "n_clones": n_clones,
        "prob_create_neuron": prob_create_neuron,
        "prob_delete_neuron": prob_delete_neuron,
        "prob_create_connection": prob_create_connection,
        "prob_delete_connection": prob_delete_connection,
        "max_hidden_layers": max_hidden_layers,
        "max_hidden_neurons": max_hidden_neurons,
        "max_connections": max_connections,
    }