from django.core.cache import cache


# Redis Cache Mixin 
class RedisCacheMixin:
    
    cache_timeout = 3 * 60 # cache for 3 hours 
    cache_prefix = "job_listing_cache"
    
    # get cache 
    def get_cache_key(self):
        return f"{self.cache_prefix}_{self.request.path}"
    
    # get queryset 
    def get_queryset(self):
        cache_key = self.get_cache_key()
        queryset = cache.get(cache_key)

        if queryset is None:
            queryset = super().get_queryset()
            cache.set(cache_key, queryset, timeout=self.cache_timeout)

        return queryset 
    
    # retrieve cache 
    def retrieve(self, request, *args, **kwargs):
        cache_key = self.get_cache_key()
        instance = cache.get(cache_key)

        if instance is None:
            instance = super().retrieve(request, *args, **kwargs)
            cache.set(cache_key, instance, timeout=self.cache_timeout)

        return instance 