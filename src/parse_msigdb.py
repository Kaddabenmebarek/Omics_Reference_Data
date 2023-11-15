import xml.sax
import copy
from genesets_declaration import Signature


class MSigDBHandler(xml.sax.ContentHandler):
    def __init__(self):
        """ 
        This script uses sax XML processing to parse the xml representation of the msigdb,
        a public database of gene signatures.  It exports a subset of this database (for supported organisms)
        and gene set families to a json lines format compatible with the default json serializer in AWS Athena


        The GeneSet tag contained the following attributes at the time of this file's creation. 
        "AUTHORS", "CATEGORY_CODE", "CHIP", "CONTRIBUTOR", "CONTRIBUTOR_ORG", "DESCRIPTION_BRIEF", 
        "DESCRIPTION_FULL", "EXACT_SOURCE", "EXTERNAL_DETAILS_URL", "FILTERED_BY_SIMILARITY", "FOUNDER_NAMES", 
        "GENESET_LISTING_URL", "GEOID", "HISTORICAL_NAME", "MEMBERS", "MEMBERS_EZID", "MEMBERS_MAPPING", 
        "MEMBERS_SYMBOLIZED", "ORGANISM", "PMID", "REFINEMENT_DATASETS", "STANDARD_NAME", "SUB_CATEGORY_CODE", 
        "SYSTEMATIC_NAME", "TAGS", "VALIDATION_DATASETS"
        """
        self.sets = {
            "H":  {"desc": "hallmark", "set": []},
            "C1": {"desc": "positional", "set": []},
            "C2": {"desc": "pathways", "set": []},
            "C3": {"desc": "regulatory", "set": []},
            "C4": {"desc": "computational_oncology", "set": []},
            "C5": {"desc": "ontology", "set": []},
            "C6": {"desc": "oncogenic", "set": []},
            "C7": {"desc": "immunologic", "set": []},
            "C8": {"desc": "cell_types", "set": []}
        }
        self.species_map = {
            "Homo sapiens": "human",
            "Mus musculus": "mouse",
            "Rattus norvegicus": "rat"
        }

    # Call when an element starts
    def startElement(self, tag, attributes):
        d = vars(attributes)["_attrs"]
        if (tag == "GENESET"):
            organism = d.pop("ORGANISM")
            code = d.pop("CATEGORY_CODE")
            #d.pop("MEMBERS")
            #d.pop("MEMBERS_EZID")
            #d.pop("MEMBERS_MAPPING")
            if organism in self.species_map:
                if code in self.sets:
                    signature = Signature(
                        name=d.pop("STANDARD_NAME"),
                        description=d.pop("DESCRIPTION_BRIEF"),
                        genes=d.pop("MEMBERS_SYMBOLIZED").split(","),
                        species=self.species_map[organism],
                        production="External",
                        source=f"MSigDB-{code}",
                        meta=copy.deepcopy(d),
                    )
                    self.sets[code]["set"] += [signature]

    def export_json_lines(self, out_dir):
        for key in self.sets.keys():
            description = self.sets[key]["desc"]
            filename = f"{out_dir}/{key}.{description}.json"
            signatures = self.sets[key]["set"]
            if len(signatures) > 0:
                with open(filename, "w") as file:
                    file.write("\n".join([sig.export_as_json()
                               for sig in signatures]))
                    print(f"{filename} written")


def parse_MSigDB(msig_xml, out_dir):
    parser = xml.sax.make_parser()
    # turn off namepsaces
    parser.setFeature(xml.sax.handler.feature_namespaces, 0)
    # override the default ContextHandler
    handler = MSigDBHandler()
    parser.setContentHandler(handler)
    parser.parse(msig_xml)
    handler.export_json_lines(out_dir)


if (__name__ == "__main__"):
    msig_xml = "/home/hartaa1/git/genesets/public_data/msigdb/msigdb_v2022.1.Hs.xml"
    out_dir = "/home/hartaa1/git/genesets/formated_genesets"
    parse_MSigDB(msig_xml, out_dir)
