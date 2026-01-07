import time

from gh_wrapper.core.cache import ResponseCache


def test_cache_set_get() -> None:
    cache = ResponseCache(ttl=1)
    cache.set("key", "value")
    assert cache.get("key") == "value"


def test_cache_expiration() -> None:
    cache = ResponseCache(ttl=0.1)
    cache.set("key", "value")
    time.sleep(0.2)
    assert cache.get("key") is None


def test_cache_missing() -> None:
    cache = ResponseCache()
    assert cache.get("nonexistent") is None


def test_cache_cleanup_on_get() -> None:
    cache = ResponseCache(ttl=0.1)
    cache.set("key", "value")
    time.sleep(0.2)
    # This call should trigger deletion
    assert cache.get("key") is None
    assert "key" not in cache._cache
