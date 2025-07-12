@tool
extends Node2D

@onready var report_lb: Label = $Report
@export var neurons: Array[NeuronData]
@export_group("Actions")
@export_tool_button("Compile brain") var compile_bt: Callable = compile_brain
@export var neuron_to_activate: String
@export var manual_activation: bool
@export var manual_value: float
@export_tool_button("Activate neuron") var activate_bt: Callable = activate_neuron
@export_tool_button("Refresh brain") var refresh_bt: Callable = refresh_brain
var brain: BrainData


func compile_brain() -> void:
    brain = BrainData.create(neurons, 0)
    brain.refresh()
    write_report()

func activate_neuron() -> void:
    if brain != null and neuron_to_activate in brain.neurons:
        if manual_activation:
            brain.neurons[neuron_to_activate].activate_manually(manual_value)
        else:
            brain.neurons[neuron_to_activate].activate()
        write_report()

func refresh_brain() -> void:
    if brain != null:
        brain.refresh()
        write_report()

func write_report() -> void:
    var report: String = ""
    if brain != null:
        for n in brain.neurons:
            var neuron: NeuronData = brain.neurons[n]
            report += """
            ---
            id: %s
            activated: %s
            activation: %.2f
            """ % [neuron.neuron_id, neuron.activated, neuron.activation]
    report_lb.set_text(report)