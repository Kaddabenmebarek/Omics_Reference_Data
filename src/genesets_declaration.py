from dataclasses import dataclass
import json
from gene_consistency import (
    get_genome_aliases,
    get_genome_information,
    validate_gene_list,
)
from abc import ABC, abstractmethod

###########


class Validator(ABC):
    def __set_name__(self, owner, name):
        self.private_name = "_" + name

    def __get__(self, obj, objtype=None):
        return getattr(obj, self.private_name)

    def __set__(self, obj, value):
        self.validate(value)
        setattr(obj, self.private_name, value)

    @abstractmethod
    def validate(self, value):
        pass


########### FOR NOW GENESET DECISION
# Validator Gene
file_genomes_genes = {
    "human": [
        "reference_genes/Homo_sapiens.GRCh38.98.csv",
        "reference_genes/Human_GRCh38.p13_alias.txt",
    ],
    "mouse": [
        "reference_genes/Mus_musculus.GRCm38.98.csv",
        "reference_genes/Mouse_GRCm39_alias.txt",
    ],
    "rat": "",
}
table_genomes_genes = {}
table_alias = {}
for key, value in file_genomes_genes.items():
    key = str.lower(key)
    if file_genomes_genes[key] == "":
        table_genomes_genes[key] = None
        table_alias[key] = {}
    else:
        table_genomes_genes[key] = get_genome_information(value[0])
        table_alias[key] = get_genome_aliases(value[1], key)
# print(table_genomes_genes)


# Decorator and integrity checks
# Subclass will be use for attribute checkin using decorator


class OneOf(Validator):
    def __init__(self, *options):
        self.options = set(options)

    def validate(self, value):
        if value not in self.options:
            raise ValueError(f"Expected {value!r} to be one of {self.options!r}")


# name
# description
# genes array
# Additional information inspired by StockCare
# Species
# Production -> internal / external
# Source : either if Internal: Group/ Team , if External :  DOI or DB expected
# Meta : dict free text


class Signature:
    """Signature class
    """ """"""

    species = OneOf("mouse", "human", "rat")
    production = OneOf("internal", "external")

    def __init__(
        self,
        name,
        description,
        genes,
        species,
        production,
        source,
        meta,
        symbol_check=False,
    ):
        self.name = name
        self.description = description
        self.species = str.lower(species)
        if symbol_check:
            self.genes = validate_gene_list(
                genes, table_genomes_genes[self.species], table_alias[self.species]
            )
        else:
            self.genes = genes
        self.production = str.lower(production)
        self.source = source
        self.meta = meta

    def __str__(self):
        main_info = "Signature %s ; %s  %s, %s" % (
            self.name,
            self.species,
            self.description,
            ",".join(self.genes),
        )
        return main_info

    def export_as_json(self):
        """Export Signature object as JSON

        Returns:
            string : full json dumps
        """
        d = {
            "name": self.name,
            "description": self.description,
            "genes": self.genes,
            "species": self.species,
            "production": self.production,
            "source": self.source,
            "meta": self.meta,
        }
        return json.dumps(d)
# SHOULD NOT WORK
# ppyt = Signature( "toto" ,"", [str(k) for k in range(10)], "hh" , production  = "", source = "internal" , meta = {})
# ppyt = Signature( "toto" ,"", [str(k) for k in range(10)], "human" , production  = "", source = "internal" , meta = {})
# SHOULD BE OK:
# ppyt = Signature( "toto" ,"", [str(k) for k in range(10)], "human" , production  = "internal", source = "internal" , meta = {})
# print( ppyt)