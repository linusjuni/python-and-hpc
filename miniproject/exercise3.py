from src.data import load_building_ids, load_data
from src.jacobi import jacobi
from src.utils.logger import get_logger
from src.utils.settings import settings
from src.visualization import plot_simulation_results

logger = get_logger(__name__)

N = 3  # number of buildings to visualize
MAX_ITER = 20_000 # maximum number of iterations for the Jacobi method
ABS_TOL = 1e-4 # absolute tolerance for convergence in the Jacobi method

building_ids = load_building_ids()[:N]

for bid in building_ids:
    u, interior_mask = load_data(bid)
    u_after = jacobi(u, interior_mask, max_iter=MAX_ITER, atol=ABS_TOL)
    plot_simulation_results(u_after, interior_mask, bid, save_dir=settings.RESULTS_DIR)
    logger.info(f"Saved simulation plot for building {bid}")

