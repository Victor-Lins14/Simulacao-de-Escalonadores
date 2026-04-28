from services.registry import get_algorithm_info
from views.main_window import MainWindow
from controllers.simulation_controller import SimulationController

if __name__ == "__main__":
    window = MainWindow(get_algorithm_info())
    SimulationController(window)
    window.mainloop()
