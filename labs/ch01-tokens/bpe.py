from collections import Counter
import re

PRE_TOKENIZE = re.compile(r"\d+|[A-Za-z]+|\s+|[^\sA-Za-z\d]", re.UNICODE)

class BPE:
    """Byte-level BPE: base alphabet is the 256 byte values; merges learned by pair frequency."""
    def __init__(self):
        self.merges = []                      # ordered list of (a, b) byte-tuple pairs
        self.vocab = {bytes([i]): i for i in range(256)}

    def _words(self, text):
        return [tuple(bytes([b]) for b in w.encode("utf-8")) for w in PRE_TOKENIZE.findall(text)]

    def train(self, text, vocab_size):
        words = Counter(self._words(text))
        while len(self.vocab) < vocab_size:
            pairs = Counter()
            for w, n in words.items():
                for a, b in zip(w, w[1:]): pairs[(a, b)] += n
            if not pairs: break
            (a, b), _ = pairs.most_common(1)[0]
            self.merges.append((a, b)); self.vocab[a + b] = len(self.vocab)
            words = Counter({self._merge(w, a, b): n for w, n in words.items()})
        return self

    @staticmethod
    def _merge(word, a, b):
        out, i = [], 0
        while i < len(word):
            if i < len(word) - 1 and word[i] == a and word[i + 1] == b: out.append(a + b); i += 2
            else: out.append(word[i]); i += 1
        return tuple(out)

    def encode(self, text):
        ids = []
        for w in self._words(text):
            for a, b in self.merges: w = self._merge(w, a, b)
            ids.extend(self.vocab[t] for t in w)
        return ids

    def tokens(self, text):
        out = []
        for w in self._words(text):
            for a, b in self.merges: w = self._merge(w, a, b)
            out.extend(t.decode("utf-8", errors="replace") for t in w)
        return out
