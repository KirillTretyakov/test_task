from app.schemas import YearMetrics


REGIONAL_NEEDS: dict[str, dict[str, YearMetrics]] = {
    "Москва": {
        "2025": YearMetrics(total=1500, replacement=600, additional=900),
        "2026": YearMetrics(total=1800, replacement=700, additional=1100),
    },
    "Санкт-Петербург": {
        "2025": YearMetrics(total=920, replacement=370, additional=550),
        "2026": YearMetrics(total=1080, replacement=430, additional=650),
    },
    "Республика Татарстан": {
        "2025": YearMetrics(total=640, replacement=260, additional=380),
        "2026": YearMetrics(total=760, replacement=300, additional=460),
    },
}


def get_needs(region: str) -> dict[str, YearMetrics] | None:
    return REGIONAL_NEEDS.get(region)
