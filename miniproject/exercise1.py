from src.data import load_building_ids, load_data
from src.utils.logger import get_logger
from src.utils.settings import settings
from src.visualization import plot_initial_domain_conditions_and_mask

logger = get_logger(__name__)

N = 3  # number of buildings to visualize

building_ids = load_building_ids()[:N]

for bid in building_ids:
    u, interior_mask = load_data(bid)
    plot_initial_domain_conditions_and_mask(u, interior_mask, bid, save_dir=settings.RESULTS_DIR)
    logger.info(f"Saved plot for building {bid}")
