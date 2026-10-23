"""Progressive disclosure for the research-status page, preserving its records."""
import re


def organize_review(html):
    # The publication synchronizer replaces these two blocks. Reorganize only
    # blocks that do not yet contain our disclosure, making refreshes idempotent.
    def outcome(match):
        body = match[1]
        if 'review-outcome-details' in body:
            return match[0]
        heading, rest = body.split('</h2>', 1)
        return ('<div class="review-panel" id="review-outcome">' + heading + '</h2>'
                '<p><a href="./unresolved.html">Open the current case directory →</a></p>'
                '<details class="review-details" id="review-outcome-details">'
                '<summary>Classification counts and historical scope</summary>' + rest + '</details></div>')
    html = re.sub(r'<div class="review-panel" id="review-outcome">(.*?)</div>', outcome, html, flags=re.S)
    for identifier, title in [('rank-seven-m5', 'Rank seven · census and verification'),
                               ('rank-eight-m3', 'Rank eight · current results and research history')]:
        pattern = r'(<section id="' + identifier + r'">)(.*?)(</section>)'
        def fold(match, title=title):
            if match[2].lstrip().startswith('<details class="review-details"'):
                return match[0]
            return match[1] + '<details class="review-details"><summary>' + title + '</summary>' + match[2] + '</details>' + match[3]
        html = re.sub(pattern, fold, html, flags=re.S)
    return html
