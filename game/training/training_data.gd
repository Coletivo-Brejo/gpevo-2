extends Resource
class_name TrainingData

@export var training_id: String
@export var run_data: RunData
@export var track_id: String
@export var racer_id: String
@export var n_neighbors: int
@export var initial_temperature: float
@export var cooling_rate: float
@export var convergence_threshold: float
@export var convergence_iterations: int
@export var n_iterations: int
var run_history: Array[RunData]
var racer_history: Array[RunStats]
var elapsed_time: float
var end_reason: String