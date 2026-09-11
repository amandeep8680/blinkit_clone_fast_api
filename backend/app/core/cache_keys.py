def active_categories_cache_key(
    skip: int,
    limit: int,
):
    return (
        f"cache:categories:active:"
        f"skip:{skip}:limit:{limit}"
    )

ACTIVE_CATEGORIES_CACHE_PATTERN = (
    "cache:categories:active:*"
)



