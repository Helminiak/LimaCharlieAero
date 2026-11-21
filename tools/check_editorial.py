"""Report overdue public reviews and planned drafts against the editorial clock."""
from datetime import date
from build_common import ROOT, json

def overdue(as_of):
    for name in ('updates', 'editorial-backlog'):
        records = json.loads((ROOT / 'content' / (name + '.json')).read_text())
        for record in records:
            due = record.get('next_review') or record.get('planned_review')
            if due and date.fromisoformat(due) < as_of:
                yield name, record.get('slug', record.get('title')), due

if __name__ == '__main__':
    today = date.today()
    for group, item, due in overdue(today):
        print(f'{today} | {group} | {due} | {item}')
