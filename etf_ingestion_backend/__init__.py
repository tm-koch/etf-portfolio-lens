"""ETF ingestion backend."""

from .pipeline import IngestionPipeline
from .registry import ETFRegistry, load_registry
