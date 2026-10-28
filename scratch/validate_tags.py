import glob
from html.parser import HTMLParser

class Validator(HTMLParser):
    def __init__(self, filename):
        super().__init__()
        self.filename = filename
        self.stack = []
        self.errors = []
        self.void_tags = {'area', 'base', 'br', 'col', 'embed', 'hr', 'img', 'input', 'link', 'meta', 'param', 'source', 'track', 'wbr'}

    def handle_starttag(self, tag, attrs):
        if tag not in self.void_tags:
            self.stack.append((tag, self.getpos()))

    def handle_endtag(self, tag):
        if tag in self.void_tags:
            return
        if not self.stack:
            self.errors.append(f"Unexpected end tag </{tag}> at line {self.getpos()[0]} with empty stack")
            return
        last_tag, pos = self.stack.pop()
        if last_tag != tag:
            # Check if last_tag was unclosed or tag is misplaced
            # Search backwards
            found = False
            for idx in range(len(self.stack) - 1, -1, -1):
                if self.stack[idx][0] == tag:
                    found = True
                    break
            if found:
                self.errors.append(f"Unclosed tag <{last_tag}> from line {pos[0]} closed by </{tag}> at line {self.getpos()[0]}")
                # unwind to tag
                while self.stack and self.stack[-1][0] != tag:
                    self.stack.pop()
                if self.stack:
                    self.stack.pop()
            else:
                self.errors.append(f"Stray end tag </{tag}> at line {self.getpos()[0]} (expected </{last_tag}>)")

html_files = sorted(glob.glob("docs/**/*.html", recursive=True))
total_errors = 0
for h in html_files:
    content = open(h, encoding="utf-8").read()
    val = Validator(h)
    val.feed(content)
    if val.stack:
        for tag, pos in val.stack:
            val.errors.append(f"Unclosed tag <{tag}> opened at line {pos[0]}")
    if val.errors:
        print(f"=== {h} ({len(val.errors)} tag errors) ===")
        for e in val.errors[:10]:
            print(" ", e)
        total_errors += len(val.errors)
    else:
        print(f"{h}: All tags properly balanced and closed.")

print(f"Total HTML tag errors across all files: {total_errors}")

