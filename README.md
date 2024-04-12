# beancount-dedup

Deduplicate Plugin for Beancount

This is mostly for myself, dipping my toes into plugin creation for Beancount.

---

## Role

This plugin seeks to deduplicate transactional entries by a fast (for python) method of sanitizing transactions by date, payee, narration, and amount and seeing what seems suspiciously similar.

### Porcelain and Plumbing

Date sanitization is not implemented yet, but could be done by a binning strategy. I suspect two days would be a good window to account for closing differences. Note that all other fields would have to be identical as well to count as a "duplicate" so there shouldn't be any false-positives with a large date window.

Amount uses the first posting. Technically I'd want to use the "total", meaning the sum of all positive (or negative) postings (the sum of which is zero, duh, but the 'total' of one side of the equation would be a rather unique identifier for a given transaction).

## Installation

See script ending comment.

## Usage

**Back up your ledger using `git`. This makes diffing the result of this script much easier.**
Call the plugin class (`DeduplicationPlugin`) and it'll spit out a list of deduplicated transaction entries (and an empty list? IDK why)

---

## GPT Disclosure

This was written using GPT. I used two prompts to construct it. While versed enough to read python and know what most stuff does, I am in no way a python expert so I condole for any bugs.
