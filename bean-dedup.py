from beancount.core.data import Transaction, Directive
from typing import List, Optional, Dict, Tuple
from collections import defaultdict
import datetime

class DeduplicationPlugin:
    def __init__(self):
        self.entries = []
        self.options = None

    def set_options(self, options_map):
        self.options = options_map

    def close_file(self):
        pass

    def get_entries(self):
        return self.entries

    def __call__(self, entries, options_map, config_map):
        self.entries = entries
        self.options = options_map

        deduplicated_entries = self.deduplicate_entries(entries)
        return deduplicated_entries, []

    def deduplicate_entries(self, entries: List[Directive]) -> List[Directive]:
        deduplicated_entries = []
        seen_entries = defaultdict(list)

        # Preprocess entries into a hash table based on payee, narration, and amount
        for entry in entries:
            if isinstance(entry, Transaction):
                key = self.create_entry_key(entry)
                seen_entries[key].append(entry)

        # Process and deduplicate entries
        for key, entries_list in seen_entries.items():
            # Deduplicate entries within each list
            if len(entries_list) > 1:
                merged_entry = self.merge_entries(entries_list)
                deduplicated_entries.append(merged_entry)
            else:
                deduplicated_entries.extend(entries_list)

        return deduplicated_entries

    def create_entry_key(self, entry: Transaction) -> Tuple:
        # Create a key for the hash table based on payee, narration, amount, and date
        # Normalize payee and narration by stripping whitespace and converting to lowercase
        payee = entry.payee.strip().lower() if entry.payee else ""
        narration = entry.narration.strip().lower() if entry.narration else ""
        amount = float(entry.postings[0].units.amount)  # Assuming only one posting; adjust if needed
        date = entry.date

        # Use a tuple as the key
        return (payee, narration, amount, date)

    def merge_entries(self, entries_list: List[Transaction]) -> Transaction:
        # Merge entries in the list into a single entry
        # For simplicity, combine postings and use the first entry's flag, date, payee, and narration
        merged_postings = []
        for entry in entries_list:
            merged_postings.extend(entry.postings)

        # Create a merged entry based on the first entry in the list
        first_entry = entries_list[0]
        merged_entry = Transaction(
            flag=first_entry.flag,
            date=first_entry.date,
            payee=first_entry.payee,
            narration=first_entry.narration,
            tags=first_entry.tags,
            links=first_entry.links,
            postings=merged_postings,
        )

        return merged_entry

# To use the plugin, add it to the Beancount configuration file:
# plugin "path.to.this.file.DeduplicationPlugin"
