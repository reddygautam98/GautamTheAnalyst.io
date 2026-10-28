import os
import re
import glob
import json
from html.parser import HTMLParser

DOCS_DIR = os.path.abspath("docs")

class DocInspector(HTMLParser):
    def __init__(self, filename):
        super().__init__()
        self.filename = filename
        self.ids = []
        self.hrefs = []
        self.srcs = []
        self.data_fulls = []
        self.images = []
        self.buttons = []
        self.inputs = []
        self.headings = []
        self.links = []
        self.tags_with_aria = []
        self.tab_index_tags = []
        self.current_tag = None
        self.current_attrs = {}
        self.text_buffer = ""
        self.scripts = []
        self.stylesheets = []

    def handle_starttag(self, tag, attrs):
        self.current_tag = tag
        attr_dict = dict(attrs)
        self.current_attrs = attr_dict
        
        # Check id
        if "id" in attr_dict:
            self.ids.append((attr_dict["id"], self.getpos()))
            
        # Check href
        if "href" in attr_dict:
            self.hrefs.append((attr_dict["href"], tag, attr_dict, self.getpos()))
            if tag == "a":
                self.links.append((attr_dict, self.getpos()))
            elif tag == "link" and attr_dict.get("rel") == "stylesheet":
                self.stylesheets.append(attr_dict.get("href"))
                
        # Check src
        if "src" in attr_dict:
            self.srcs.append((attr_dict["src"], tag, attr_dict, self.getpos()))
            if tag == "script":
                self.scripts.append(attr_dict.get("src"))
                
        # Check data-full
        if "data-full" in attr_dict:
            self.data_fulls.append((attr_dict["data-full"], tag, attr_dict, self.getpos()))
            
        # Check img
        if tag == "img":
            self.images.append((attr_dict, self.getpos()))
            
        # Check button
        if tag == "button":
            self.buttons.append((attr_dict, self.getpos()))
            
        # Check input / select / textarea
        if tag in ["input", "select", "textarea"]:
            self.inputs.append((tag, attr_dict, self.getpos()))
            
        # Check headings
        if tag in ["h1", "h2", "h3", "h4", "h5", "h6"]:
            self.headings.append((tag, attr_dict, self.getpos()))
            
        # Check ARIA
        aria_attrs = {k: v for k, v in attr_dict.items() if k.startswith("aria-") or k == "role"}
        if aria_attrs:
            self.tags_with_aria.append((tag, aria_attrs, self.getpos()))

def audit():
    html_files = glob.glob(os.path.join(DOCS_DIR, "**/*.html"), recursive=True)
    report = {
        "files_checked": len(html_files),
        "duplicate_ids": [],
        "broken_internal_links": [],
        "broken_anchors": [],
        "broken_assets": [],
        "images_without_alt": [],
        "buttons_without_name": [],
        "inputs_without_labels": [],
        "heading_hierarchy": {},
        "scripts": {},
        "stylesheets": {}
    }
    
    parsed = {}
    
    for f in html_files:
        rel = os.path.relpath(f, DOCS_DIR)
        with open(f, "r", encoding="utf-8") as fp:
            content = fp.read()
        parser = DocInspector(rel)
        parser.feed(content)
        parsed[rel] = parser
        
        # Check duplicate IDs in page
        id_counts = {}
        for id_val, pos in parser.ids:
            id_counts.setdefault(id_val, []).append(pos)
        for id_val, positions in id_counts.items():
            if len(positions) > 1:
                report["duplicate_ids"].append({
                    "file": rel,
                    "id": id_val,
                    "count": len(positions),
                    "positions": positions
                })
                
        # Check images without alt
        for img, pos in parser.images:
            if "alt" not in img:
                report["images_without_alt"].append({
                    "file": rel,
                    "src": img.get("src"),
                    "pos": pos
                })
                
        # Check headings hierarchy
        report["heading_hierarchy"][rel] = [h[0] for h in parser.headings]
        report["scripts"][rel] = parser.scripts
        report["stylesheets"][rel] = parser.stylesheets

    # Check internal links and anchors
    for rel, parser in parsed.items():
        page_dir = os.path.dirname(os.path.join(DOCS_DIR, rel))
        page_ids = set([x[0] for x in parser.ids])
        
        for href, tag, attrs, pos in parser.hrefs:
            if not href or href.startswith("http:") or href.startswith("https:") or href.startswith("mailto:") or href.startswith("tel:") or href.startswith("javascript:"):
                continue
            
            if href.startswith("#"):
                anchor = href[1:]
                if anchor and anchor not in page_ids:
                    report["broken_anchors"].append({
                        "file": rel,
                        "anchor": href,
                        "pos": pos,
                        "tag": tag
                    })
            else:
                parts = href.split("#")
                path_part = parts[0].split("?")[0]
                anchor_part = parts[1] if len(parts) > 1 else None
                
                target_file = os.path.normpath(os.path.join(page_dir, path_part))
                if not os.path.exists(target_file):
                    report["broken_internal_links"].append({
                        "file": rel,
                        "href": href,
                        "resolved": target_file,
                        "pos": pos
                    })
                elif anchor_part:
                    rel_target = os.path.relpath(target_file, DOCS_DIR)
                    if rel_target in parsed:
                        target_ids = set([x[0] for x in parsed[rel_target].ids])
                        if anchor_part not in target_ids:
                            report["broken_anchors"].append({
                                "file": rel,
                                "target_file": rel_target,
                                "anchor": anchor_part,
                                "href": href,
                                "pos": pos
                            })

        # Check srcs (images, scripts, etc.)
        for src, tag, attrs, pos in parser.srcs:
            if not src or src.startswith("http:") or src.startswith("https:") or src.startswith("data:"):
                continue
            clean_src = src.split("?")[0].split("#")[0]
            target_path = os.path.normpath(os.path.join(page_dir, clean_src))
            if not os.path.exists(target_path):
                report["broken_assets"].append({
                    "file": rel,
                    "tag": tag,
                    "src": src,
                    "resolved": target_path,
                    "pos": pos
                })

        # Check data-full
        for df, tag, attrs, pos in parser.data_fulls:
            if not df or df.startswith("http:") or df.startswith("https:") or df.startswith("data:"):
                continue
            clean_df = df.split("?")[0].split("#")[0]
            target_path = os.path.normpath(os.path.join(page_dir, clean_df))
            if not os.path.exists(target_path):
                report["broken_assets"].append({
                    "file": rel,
                    "tag": tag,
                    "data-full": df,
                    "resolved": target_path,
                    "pos": pos
                })

    with open("scratch/audit_report_static.json", "w", encoding="utf-8") as out:
        json.dump(report, out, indent=2)

    print("Static audit completed.")
    print("Files checked:", report["files_checked"])
    print("Duplicate IDs:", len(report["duplicate_ids"]))
    print("Broken internal links:", len(report["broken_internal_links"]))
    print("Broken anchors:", len(report["broken_anchors"]))
    print("Broken assets:", len(report["broken_assets"]))
    print("Images without alt:", len(report["images_without_alt"]))

if __name__ == "__main__":
    audit()

