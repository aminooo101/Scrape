import requests, time
from bs4 import BeautifulSoup



HEADERS = {"User-Agent": "Mozilla/5.0 job-scraper/1.0"}

def is_junior_level(title: str) -> bool:
    title_lower = title.lower()
    exclude = ["senior", "sr.", "lead", "principal", "staff",
               "head of", "manager", "director", "architect", "vp", "2+ years", "3+ years", "5+ years", "10+ years"]
    if any(word in title_lower for word in exclude):
        return False
    return True

def get_pythonorg(keywords):
    r = requests.get("https://www.python.org/jobs/",
        headers=HEADERS)
    soup = BeautifulSoup(r.text, "html.parser")

    results = []
    for job in soup.find_all("li", class_="list-recent-jobs"):
        a       = job.find("a")
        title   = a.text.strip() if a else ""
        url     = "https://www.python.org" + a["href"] if a else ""
        company = job.find("span", class_="listing-company-name")
        company = company.text.strip() if company else "Unknown"

        if matches(title, keywords) and is_junior_level(title):
            results.append({
                "id":      f"pyorg-{url.split('/')[-2]}",
                "title":   title,
                "company": company,
                "url":     url,
                "source":  "Python.org"
            })
    return results




def get_remoteok(keywords):
    r = requests.get("https://remoteok.com/api", headers=HEADERS)
    jobs = [j for j in r.json() if isinstance(j, dict) and "position" in j]
    return [
        {"id": f"rok-{j['id']}", "title": j["position"],
         "company": j.get("company", ""), "url": j.get("url", ""),
         "url": j.get("apply_url") or j.get("url", ""),
         "source": "RemoteOK"}
        for j in jobs
        if matches(j.get("position", ""), keywords)
        and is_junior_level(j.get("position", ""))
    ]

def get_remotive(keywords):
    r = requests.get("https://remotive.com/api/remote-jobs", headers=HEADERS)
    jobs = r.json().get("jobs", [])  # FIX: era r.json() directo, faltaba ["jobs"]
    return [
        {"id": f"rem-{j['id']}", "title": j["title"],
            "company": j["company_name"],
            "url": j["url"],
            "source": "Remotive"}
        for j in jobs
        if matches(j.get("title", ""), keywords)  # FIX: "title" no "position"
        and is_junior_level(j.get("title", ""))   # FIX: "title" no "position"
    ]

def get_arbeitnow(keywords):
    r = requests.get("https://www.arbeitnow.com/api/job-board-api", headers=HEADERS)
    jobs = r.json().get("data", [])
    return [
        {"id": f"arb-{j['slug']}", "title": j["title"],
         "company": j["company_name"], "url": j["url"],
         "source": "Arbeitnow"}
        for j in jobs
        if matches(j.get("title", ""), keywords)  # FIX: "title" no "position"
        and is_junior_level(j.get("title", ""))   # FIX: "title" no "position"
    ]

def get_himalayas(keywords):
    results = []
    for kw in keywords:
        r = requests.get("https://himalayas.app/jobs/api/search",
            params={"q": kw, "limit": 20}, headers=HEADERS)
        for j in r.json().get("jobs", []):
            url = (j.get("applicationLink") or   # FIX: campo correcto
                   j.get("guid") or "")           # fallback
            if not is_junior_level(j.get("title", "")):
                continue
            results.append({
                "id": f"him-{j.get('guid', kw+str(len(results))).split('/')[-1]}",
                "title": j.get("title", ""),
                "company": j.get("companyName", ""),
                "url": url,
                "source": "Himalayas"
            })
    return [j for j in results if matches(j["title"], keywords)]

def matches(text, keywords):
    return any(kw.lower() in text.lower() for kw in keywords)

def get_jobs(keywords):
    print(f"Searching for keywords: {keywords}")
    all_jobs = []
    sources = [get_remoteok, get_remotive, get_arbeitnow, get_himalayas]
    for fn in sources:
        try:
            found = fn(keywords)
            with_url    = [j for j in found if j.get("url")]
            without_url = [j for j in found if not j.get("url")]
            print(f"{fn.__name__}: {len(with_url)} con link, {len(without_url)} sin link")
              
            all_jobs += found
            time.sleep(1)
        except Exception as e:
            print(f"Error en {fn.__name__}: {e}")
    print(f"Total jobs matching keywords: {len(all_jobs)}")
    return all_jobs