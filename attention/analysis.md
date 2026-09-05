# Analysis

## Layer 9, Head 11

The attention table for Layer 9 Head 11 shows that words referencing the same entity pay attention to each other. Subject and reflexive pronouns like 'it' and 'itself' attended to each other and the subject noun of the sentence. This means that the Layer 9 Head 11 of BERT understands co-references between nouns. BERT can recognize co-reference when the main subject noun of the sentence comes before or after another co-referencing noun.

Example Sentences:
- The cat licked itself as it [MASK] in the sunlight.
- If it is hungry, the cat will begin to [MASK].

## Layer 4, Head 10

The attention table of Layer 4 Head 10 shows that auxiliary verbs like 'will' or 'has' pay attention to the main verbs of the sentence. The BERT Model also recognizes when verbs that are normally action verbs, such as 'go', are being used as auxiliary verbs by paying attention to the main verb of the verb phrase. Additionally, subject pronouns like 'I' and 'he' pay attention to the other parts of the verb phrase, indicating that BERT could have learned about verb conjugation and uses that in its association.

Example Sentences:
- I will wear my favorite red [MASK] when I go shopping later.
- He has done [MASK] of his homework.