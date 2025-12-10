# Backend Optimization Plan

## Current Bottlenecks

### 1. Sequential Resource Fetching (MAJOR)

**Location**: `main.py` lines 360-376
**Issue**: The main loop processes resources one-by-one sequentially

```python
for idx, res in enumerate(request.resources):
    fetched = await fetcher.fetch_all(res.type, res.id, ...)
```

**Impact**: For 100 resources, this creates 100 sequential network round trips

### 2. Sequential Support File Processing (MODERATE)

**Location**: `main.py` lines 379-392
**Issue**: Scripts and config profiles are processed sequentially
**Impact**: Additional latency for each script/profile

### 3. No HTTP Connection Pooling (MODERATE)

**Location**: `jamf_client.py`
**Issue**: Each API call may create a new HTTP connection
**Impact**: TCP handshake overhead for each request

### 4. Token Refresh on Every Export (MINOR)

**Location**: `main.py` line 344
**Issue**: New token requested for each export
**Impact**: Additional ~200-500ms per export

## Optimization Strategy

### Phase 1: Parallel Resource Fetching (CRITICAL - 5-10x speedup)

**Change**: Use `asyncio.gather()` to fetch all root resources in parallel
**Expected Improvement**: ~80% reduction in fetch time
**Implementation**:

```python
# Current (Sequential)
for res in request.resources:
    fetched = await fetcher.fetch_all(...)

# Optimized (Parallel)
tasks = [fetcher.fetch_all(res.type, res.id, ...) for res in request.resources]
all_fetched = await asyncio.gather(*tasks, return_exceptions=True)
```

### Phase 2: Parallel Support File Processing (MODERATE - 2-3x speedup)

**Change**: Use `asyncio.gather()` to process scripts and profiles in parallel
**Expected Improvement**: ~50% reduction in support file processing time
**Implementation**:

```python
# Current (Sequential)
for r_type, r_data in resources:
    if r_type == 'scripts':
        await support_handler.process_script(...)

# Optimized (Parallel)
tasks = []
for r_type, r_data in resources:
    if r_type == 'scripts':
        tasks.append(support_handler.process_script(...))
await asyncio.gather(*tasks, return_exceptions=True)
```

### Phase 3: HTTP Connection Pooling (MODERATE - 20-30% speedup)

**Change**: Use `httpx.AsyncClient` with connection limits
**Expected Improvement**: ~20-30% reduction in network overhead
**Implementation**:

```python
# In JamfClient.__init__
self.client = httpx.AsyncClient(
    timeout=30.0,
    limits=httpx.Limits(max_connections=20, max_keepalive_connections=10)
)
```

### Phase 4: Token Caching (MINOR - saves ~500ms per export)

**Change**: Cache token in memory with expiration
**Expected Improvement**: Marginal but free optimization
**Implementation**: Cache token for 20 minutes (tokens are valid for 30 min)

## Expected Overall Improvement

- **Small instances** (10-20 resources): 2-3x faster (5s → 2s)
- **Medium instances** (50-100 resources): 5-8x faster (5min → 40-60s)
- **Large instances** (200+ resources): 8-10x faster (15min → 1.5-2min)

## Priority

1. ✅ **Phase 1**: Parallel resource fetching (MUST HAVE)
2. ✅ **Phase 2**: Parallel support file processing (SHOULD HAVE)
3. ⚠️ **Phase 3**: Connection pooling (NICE TO HAVE)
4. ⚠️ **Phase 4**: Token caching (NICE TO HAVE)

Let's implement Phase 1 and 2 first as they provide the biggest wins.
