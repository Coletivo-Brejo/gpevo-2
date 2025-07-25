from pydantic import BaseModel


class Point(BaseModel):
    x: float
    y: float

class TrackSegment(BaseModel):
    length: float
    curvature: float
    l_wall_dist: float
    l_wall_curv: float
    r_wall_dist: float
    r_wall_curv: float

class Track(BaseModel):
    track_id: str
    name: str
    segments: list[TrackSegment]
    loops: bool
    core: list[Point]
    l_wall: list[Point]
    r_wall: list[Point]
    length: float

class Thruster(BaseModel):
    power: float
    texture: str
    position: Point
    rotation: float

class SensorSet(BaseModel):
    amount: int
    aperture: float
    reach: float
    texture: str
    position: Point
    rotation: float

class Ship(BaseModel):
    ship_id: str
    name: str
    mass: float
    chassis_texture: str
    chassis_collision: list[Point]
    thrusters: list[Thruster]
    sensors: list[SensorSet]

class Operation(BaseModel):
    type: str
    params: list[float]

class Neuron(BaseModel):
    neuron_id: str
    max_inputs: int
    input_ids: list[str]
    operations: list[Operation]

class Brain(BaseModel):
    neurons: list[Neuron]
    current_id: int

class Racer(BaseModel):
    racer_id: str
    name: str
    brain: Brain
    ship: Ship

class RunStats(BaseModel):
    racer_id: str
    track_id: str
    lap: int
    time: float
    max_progress: float
    finished: bool
    stuck: bool
    time_history: list[float]
    progress_history: list[float]
    position_history: list[Point]

class RunSetup(BaseModel):
    begin_countdown: float
    end_countdown: float
    stuck_timeout: float
    run_timeout: float
    follow_first: bool
    end_on_first_finish: bool
    stat_collection_frequency: float
    mirrored: bool
    laps: int

class Run(BaseModel):
    run_id: str
    track_id: str
    racer_ids: list[str]
    setup: RunSetup
    elapsed_time: float
    end_reason: str
    stats: list[RunStats]

class TrainingRunSetup(BaseModel):
    track_id: str
    run_setup: RunSetup

class Training(BaseModel):
    training_id: str
    racer_id: str
    setups: list[TrainingRunSetup]
    save_results: bool
    n_neighbors: int
    initial_temperature: float
    cooling_rate: float
    convergence_threshold: float
    convergence_iterations: int
    n_iterations: int
    progress_objective: float
    time_objective: float
    max_training_time: float
    greedy: bool
    prob_create_neuron: float
    prob_delete_neuron: float
    prob_create_connection: float
    prob_delete_connection: float
    run_history: list[list[Run]]
    clone_history: list[str]
    elapsed_time: float
    end_reason: str