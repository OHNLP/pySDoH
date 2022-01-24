import spacy
from spacy.lang.en import English
from spacy.pipeline import EntityRuler

nlp = spacy.load("en_core_web_sm")

def set_custom_boundaries(doc):
    for token in doc[:-1]:
        if token.text == "\n":
            doc[token.i+1].is_sent_start = True
        if token.text == ":":
            doc[token.i+1].is_sent_start = False            
    return doc

nlp.add_pipe(set_custom_boundaries, before="parser")

ruler = EntityRuler(nlp, overwrite_ents=True)

ruler.from_disk("homelessness_patterns.jsonl")  # loads patterns only

nlp.add_pipe(ruler)

SDH = ["HOMELESSNESS"]

with open("input-file.txt", 'r') as FileObj:  #one note per line

	for line in FileObj:
		note = line.replace("\n","")
		doc = nlp(note)

		for entity in list(doc.ents):
			if entity.label_ in SDH:
				elements = [
				entity.label_,
				entity.ent_id_,
				entity.text,
				str(entity.sent).replace("\n",""),
				entity.lemma_,
				str(entity.start),
				str(entity.end),
				]
				print('	'.join(elements))

