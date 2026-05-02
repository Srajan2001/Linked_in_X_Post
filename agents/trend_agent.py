from ddgs import DDGS

def fetch_trend(topic_keyword="AI in Data Analytics", max_results=15):
    print(f"\nSearching the live web for the latest news on: {topic_keyword}...")
    try:
        with DDGS() as ddgs:
            # We fetch 15 upfront to support the "Refresh/Load More" UI efficiently
            results = list(ddgs.text(f"{topic_keyword} news", max_results=max_results))
        print(f"Fetched {len(results)} articles!")
        return results
    except Exception as e:
        print(f"Search failed: {e}")
        return []