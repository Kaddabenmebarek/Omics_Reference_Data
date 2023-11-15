# This is the start of processing json files for geneset curation;

import json
import re
from genesets_declaration import Signature

def read_json_MSIGDB(file, exclusion_pattern="^KEGG"):
    # File= json file to read
    # exclusion pattern one, or more pattern that will not preserved
    # exclusion pattern is based on the signature name
    # Opening JSON file
    full_signature = []
    f = open(file)
    data = json.load(f)
    # Iterating through the json
    for signature, values in data.items():
        if not bool(re.match(exclusion_pattern, signature)):
            full_signature += [
                Signature(
                    name=signature,
                    description=values["exactSource"],
                    genes=values["geneSymbols"],
                    species="human",  # human geneSYmbok
                    production="External",
                    source="MSigDB",
                    meta={
                        "systematicName": values["systematicName"],
                        "pmid": values["pmid"],
                        "msigdbURL": values["msigdbURL"],
                    },
                )
            ]
    # Closing file
    f.close()
    return full_signature


def dump_all_as_we_want(signature_table, file_to_write):
    with  open(file_to_write, "w") as file:
        file.write("\n".join( [signature.export_as_json() for signature in signature_table]))