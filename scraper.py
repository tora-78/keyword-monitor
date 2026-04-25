import requests
import time

# ─── HackerNews ───────────────────────────────────────────

def fetch_hn(keyword):
    """搜索HackerNews上包含关键词的帖子"""
    url = "https://hn.algolia.com/api/v1/search_by_date"
    params = {
        "query": keyword,
        "tags": "story",
        "numericFilters": f"created_at_i>{int(time.time()) - 86400}"  # 过去24小时
    }
    try:
        res = requests.get(url, params=params, timeout=10)
        res.raise_for_status()
        hits = res.json().get("hits", [])
        results = []
        for h in hits:
            results.append({
                "source": "HackerNews",
                "title": h.get("title", ""),
                "url": f"https://news.ycombinator.com/item?id={h.get('objectID')}",
                "author": h.get("author", ""),
            })
        return results
    except Exception as e:
        print(f"[HN error] {e}")
        return []

# ─── Reddit ───────────────────────────────────────────────

def fetch_reddit(keyword):
    """用Reddit公开JSON接口搜索关键词（无需API key）"""
    url = f"https://www.reddit.com/search.json"
    params = {
        "q": keyword,
        "sort": "new",
        "limit": 10,
        "t": "day"
    }
    headers = {"User-Agent": "keyword-monitor/0.1"}
    try:
        res = requests.get(url, params=params, headers=headers, timeout=10)
        res.raise_for_status()
        posts = res.json()["data"]["children"]
        results = []
        for p in posts:
            d = p["data"]
            results.append({
                "source": "Reddit",
                "title": d.get("title", ""),
                "url": f"https://reddit.com{d.get('permalink', '')}",
                "author": d.get("author", ""),
            })
        return results
    except Exception as e:
        print(f"[Reddit error] {e}")
        return []
    
# ─── ProductHunt ───────────────────────────────────────────

def fetch_producthunt(keyword):
    """搜索ProductHunt上包含关键词的产品"""
    url = "https://api.producthunt.com/v2/api/graphql"
    headers = {
        "Authorization": f"Bearer i7okzzzoWiVuGQ9b9AhIvHXDH1oMKfn287YzD-rAWyY",
        "Content-Type": "application/json",
    }
    query = """
    {
      posts(query: "%s", first: 10, order: NEWEST) {
        edges {
          node {
            id
            name
            tagline
            url
            createdAt
          }
        }
      }
    }
    """ % keyword

    try:
        res = requests.post(url, json={"query": query}, headers=headers, timeout=10)
        res.raise_for_status()
        edges = res.json().get("data", {}).get("posts", {}).get("edges", [])
        results = []
        for edge in edges:
            node = edge["node"]
            results.append({
                "source": "ProductHunt",
                "title": f"{node['name']} — {node['tagline']}",
                "url": node["url"],
                "author": "",
            })
        return results
    except Exception as e:
        print(f"[ProductHunt error] {e}")
        return []

# ─── 统一入口 ──────────────────────────────────────────────

def search_all(keyword):
    print(f"\n🔍 搜索关键词: {keyword}")
    results = []
    results += fetch_hn(keyword)
    results += fetch_reddit(keyword)
    return results

# ─── 测试 ──────────────────────────────────────────────────

if __name__ == "__main__":
    keyword = "solopreneur"
    results = search_all(keyword)
    print(f"\n找到 {len(results)} 条结果：")
    for r in results:
        print(f"[{r['source']}] {r['title']}")
        print(f"  → {r['url']}\n")