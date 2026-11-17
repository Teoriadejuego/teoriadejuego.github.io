"""Measure the existing build on a private loopback preview; write qa/performance.json.

Timings describe this run, not a hosting benchmark or a performance guarantee.
Invalid operations, unexpected DOM/storage/network growth and JS errors fail.
"""
from datetime import datetime, timezone
from importlib.metadata import version
from pathlib import Path
import json
import os
import platform
import statistics
import sys
import time
from urllib.parse import urlsplit

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
from tools.preview import preview
from playwright.sync_api import sync_playwright

PUBLIC = ROOT / "public"
OUTPUT = ROOT / "qa" / "performance.json"
VIEWPORT = {"width": 1440, "height": 1000}
NAVIGATION_PAIRS = 3
INTERACTIONS = 20


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def distribution(values):
    return {"samples": len(values), "minimum": min(values), "median": statistics.median(values), "maximum": max(values)}


def inventory(directory):
    paths = sorted(directory.rglob("*"))
    require(all(not p.is_symlink() for p in paths), "Measurement input contains a symlink")
    sizes = [{"path": p.relative_to(directory).as_posix(), "bytes": p.stat().st_size} for p in paths if p.is_file()]
    return {"files": len(sizes), "bytes": sum(p["bytes"] for p in sizes)}


def snapshot(page, context):
    state = page.evaluate("""() => {
      let walker=document.createTreeWalker(document,NodeFilter.SHOW_TEXT),textNodes=0;
      while(walker.nextNode())textNodes++;
      return {elements:document.querySelectorAll('*').length,text_nodes:textNodes,
        local_storage_entries:localStorage.length,session_storage_entries:sessionStorage.length,
        document_cookie_present:document.cookie.length>0,history_entries:history.length};
    }""")
    state["context_cookies"] = len(context.cookies())
    return state


def timed_input(page, selector, value):
    # dispatchEvent is synchronous here: the first duration measures input to
    # completed DOM handlers. Two rAF callbacks add an observed frame opportunity,
    # not proof of physical paint or end-to-end human interaction latency.
    return page.evaluate("""async ({selector,value}) => {
      const input=document.querySelector(selector);
      if(!input)throw new Error('Measurement control missing');
      const start=performance.now();input.value=value;
      input.dispatchEvent(new Event('input',{bubbles:true}));
      const domEnd=performance.now();
      await new Promise(resolve=>requestAnimationFrame(()=>requestAnimationFrame(resolve)));
      return {input_to_dom_ms:domEnd-start,input_to_second_animation_frame_ms:performance.now()-start,
        value:input.value,visible_articles:[...document.querySelectorAll('.publication')].filter(e=>!e.hidden).length};
    }""", {"selector": selector, "value": str(value)})


def instrument(page, base):
    observed = {"requests": [], "outside_origin": [], "http_errors": [], "javascript_errors": []}
    allowed = urlsplit(base).netloc
    def request(r):
        observed["requests"].append({"method": r.method, "type": r.resource_type})
        if urlsplit(r.url).netloc != allowed or r.method not in ("GET", "HEAD"):
            observed["outside_origin"].append({"method": r.method, "type": r.resource_type})
    def response(r):
        if r.status >= 400:
            observed["http_errors"].append(r.status)
    page.on("request", request)
    page.on("response", response)
    page.on("pageerror", lambda error: observed["javascript_errors"].append(str(error)))
    return observed


def check_observed(observed):
    require(not observed["outside_origin"], "Unexpected origin or request method during measurement")
    require(not observed["http_errors"], "A preview resource failed to load")
    require(not observed["javascript_errors"], "JavaScript failed during measurement")


def navigate(page, url=None):
    started = time.perf_counter()
    response = page.goto(url, wait_until="load") if url else page.reload(wait_until="load")
    elapsed = (time.perf_counter() - started) * 1000
    require(response is not None and response.status == 200, "Measured navigation did not return HTTP 200")
    page.wait_for_load_state("networkidle")
    require(page.locator("h1").count() == 1, "Measured page has no unique main heading")
    require(page.locator("img").evaluate_all("xs=>xs.filter(i=>i.loading!=='lazy').every(i=>i.complete&&i.naturalWidth>0)"), "A non-lazy page image failed")
    metrics = page.evaluate("""() => {
      const n=performance.getEntriesByType('navigation')[0],resources=performance.getEntriesByType('resource');
      return {response_start_ms:n.responseStart,dom_content_loaded_ms:n.domContentLoadedEventEnd,
        load_event_end_ms:n.loadEventEnd,navigation_type:n.type,document_transfer_bytes:n.transferSize,
        resource_entries:resources.length,resource_transfer_bytes:resources.reduce((sum,r)=>sum+r.transferSize,0),
        zero_transfer_resource_entries:resources.filter(r=>r.transferSize===0).length};
    }""")
    metrics["automation_observed_load_ms"] = elapsed
    return metrics


def repeat_component(page, context, observed, kind):
    baseline = snapshot(page, context)
    require(not any(baseline[key] for key in ("local_storage_entries", "session_storage_entries", "document_cookie_present", "context_cookies")), "Measurement did not start with empty application storage")
    start_requests = len(observed["requests"])
    samples, states = [], []
    if kind == "publication_filters":
        total = page.locator(".publication").count()
        require(total > 0, "No publications to filter")
        doi = page.locator(".publication").first.get_attribute("data-search").split()[0]
        actions = [("#pub-search", value, expected) for value, expected in ((doi, 1), ("__measurement_no_match__", 0), (doi, 1), ("", total))] * 5
    else:
        actions = [(selector, value, None) for selector, value in (
            ("#sample", 20), ("#effect", -15), ("#noise", 40), ("#effect", 15), ("#sample", 2000),
            ("#effect", 0), ("#noise", 5), ("#sample", 200), ("#effect", 3), ("#noise", 15),
        )] * 2
    require(len(actions) == INTERACTIONS, "Unexpected interaction plan length")
    for index, (selector, value, expected) in enumerate(actions, 1):
        measured = timed_input(page, selector, value)
        require(measured["value"] == str(value), "Control rejected a measured value")
        if kind == "publication_filters":
            require(measured["visible_articles"] == expected, "Filter results disagree with the requested operation")
            require(page.locator("#pub-empty").is_visible() == (expected == 0), "Filter empty state is inconsistent")
            require(page.locator("#pub-reset").is_visible() == bool(value), "Filter reset state is inconsistent")
        else:
            require(page.locator("#interval").inner_text().startswith("["), "Lab interval was not rendered")
            require(page.locator("#lab-se").text_content().strip() not in ("", "—"), "Lab table did not update")
            require(page.locator("#ci-line").evaluate("e=>Number.isFinite(Number(e.getAttribute('x1')))&&Number.isFinite(Number(e.getAttribute('x2')))&&Number(e.getAttribute('x1'))<=Number(e.getAttribute('x2'))"), "Lab graph contains invalid coordinates")
        state = snapshot(page, context)
        require(state == baseline, "Unexpected DOM, history or storage growth during repeated " + kind)
        require(len(observed["requests"]) == start_requests, "Repeated " + kind + " issued a network request")
        check_observed(observed)
        samples.append({"iteration": index, "control": selector, **measured})
        states.append(state)
    return {"interactions": INTERACTIONS, "samples": samples,
            "input_to_dom_ms": distribution([s["input_to_dom_ms"] for s in samples]),
            "input_to_second_animation_frame_ms": distribution([s["input_to_second_animation_frame_ms"] for s in samples]),
            "baseline": baseline, "final": states[-1], "all_snapshots_equal": all(s == baseline for s in states),
            "additional_requests": len(observed["requests"]) - start_requests}


def main():
    report = {
        "schema_version": 1, "status": "running", "measured_at_utc": datetime.now(timezone.utc).isoformat(),
        "environment": {"os": platform.system(), "os_release": platform.release(), "machine": platform.machine(),
                        "logical_cpu_count": os.cpu_count(), "python": platform.python_version(), "playwright": version("playwright")},
        "viewport": {**VIEWPORT, "device_scale_factor": 1},
        "conditions": {"hosting": "own ephemeral loopback HTTP preview", "network_throttling": "none",
                       "cpu_throttling": "none", "headless": True, "navigation_pairs": NAVIGATION_PAIRS,
                       "cold": "Fresh browser context per pair; OS filesystem and browser process are not cold.",
                       "warm": "Reload in the same context; cache behaviour is that of the local preview, not GitHub Pages.",
                       "interaction_method": "Synthetic input event; synchronous handler duration and second animation-frame opportunity.",
                       "cache_measurement": "No request interception, so Playwright routing does not disable the HTTP cache."},
        "limits": ["Local descriptive samples only; no arbitrary timing pass threshold.",
                   "No hosting capacity, concurrent-user or universal speed claim.",
                   "Two animation frames do not prove a physical paint or measure human typing latency.",
                   "Stable DOM/storage/request counts do not prove absence of JavaScript heap leaks."],
    }
    try:
        for route in ("index.html", "publications/index.html", "lab/index.html", "assets/app.js"):
            require((PUBLIC / route).is_file(), "Required build input is missing: " + route)
        report["public"] = inventory(PUBLIC)
        report["assets"] = inventory(PUBLIC / "assets")
        manifest = PUBLIC / "release.json"
        report["content_digest"] = json.loads(manifest.read_text(encoding="utf8")).get("content_digest") if manifest.exists() else None
        with preview(PUBLIC) as base, sync_playwright() as p:
            options = {"headless": True}
            executable = os.environ.get("PLAYWRIGHT_CHROMIUM_EXECUTABLE")
            if executable:
                options["executable_path"] = executable
            browser = p.chromium.launch(**options)
            report["browser"] = {"name": "chromium", "version": browser.version, "executable_override": bool(executable)}
            try:
                pairs = []
                for iteration in range(1, NAVIGATION_PAIRS + 1):
                    context = browser.new_context(viewport=VIEWPORT, device_scale_factor=1, service_workers="block")
                    try:
                        page = context.new_page()
                        observed = instrument(page, base)
                        cold = navigate(page, base + "/")
                        warm = navigate(page)
                        check_observed(observed)
                        pairs.append({"iteration": iteration, "cold": cold, "warm": warm})
                    finally:
                        context.close()
                report["navigation"] = {"pairs": pairs, "load_event_end_ms": {
                    name: distribution([pair[name]["load_event_end_ms"] for pair in pairs]) for name in ("cold", "warm")}}
                context = browser.new_context(viewport=VIEWPORT, device_scale_factor=1, service_workers="block")
                try:
                    page = context.new_page()
                    observed = instrument(page, base)
                    report["repeated_interactions"] = {}
                    for route, name in (("publications/", "publication_filters"), ("lab/", "synthetic_lab")):
                        navigate(page, base + "/" + route)
                        report["repeated_interactions"][name] = repeat_component(page, context, observed, name)
                    check_observed(observed)
                    report["javascript_errors"] = observed["javascript_errors"]
                finally:
                    context.close()
            finally:
                browser.close()
        report["status"] = "completed"
    except Exception as error:
        report["status"] = "failed"
        report["error"] = {"type": type(error).__name__, "message": str(error)}
        raise
    finally:
        OUTPUT.parent.mkdir(parents=True, exist_ok=True)
        OUTPUT.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf8")
    print("Local measurements recorded in qa/performance.json: 3 cold/warm pairs, 20 filter and 20 lab inputs; structural checks passed.")


if __name__ == "__main__":
    main()
