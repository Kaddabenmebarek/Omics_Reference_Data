## This file is intended to read internal stock care format used in the shiny App.
## It is internal format intended once for now.
import pandas as pd
from os import listdir, path
import sys
from genesets_declaration import Signature


def _get_genesets_header(
    file_name: str,
):  # = "../inhouse_data/Geneset_inventory_20220513.csv"):
    # Reading and skipping empty first column /
    description = pd.read_table(file_name, sep=";").iloc[:, 1:]
    return description


def _parse_species_(geneset_species: str):
    get_all_species = geneset_species.split(" ")
    return [k for k in get_all_species if k != "and"]


def read_all_signature(directory: str, description_f: str, symbol_check: bool = False):  # = "../inhouse_data/"):
    ## Put together list of genesets dumps from stock care with all information with list of genes pre-curated by Gabin.
    ## The whole dump from stock has an chaotic format to parse for later with precaution.
    genesets = []
    description = _get_genesets_header(description_f)
    genesets_files = listdir(directory)
    for fileg in genesets_files:
        name_id = fileg.split("_")[0]
        mask = description.Geneset == name_id
        geneset_info = description[mask].iloc[0]
        if True not in mask.value_counts().index:
            print("Do not find " + name_id)
            sys.exit(2)
        ff = open(path.join(directory, fileg), "r")
        gene_list = ff.read().splitlines()
        ff.close()
        ## Handling Mulitples species entry -> for now, one geneset per species *so multiples genesets*
        all_species = _parse_species_(geneset_info.get("Species"))
        for specie in all_species:
            genesets += [
                Signature(
                    name=geneset_info.get("Name"),
                    description=geneset_info.get("Description"),
                    genes=gene_list,
                    species=specie,  # human geneSYmbok
                    production=geneset_info.get("Production"),
                    source="StockCare",
                    meta={
                        "Curation"  : geneset_info.get("Curation"),
                        "GenesetID" : geneset_info.get("Geneset"),
                        "Source"    : geneset_info.get("Source"),
                        "Comments"  : geneset_info.get("Comments") if geneset_info.get("Comments") == geneset_info.get("Comments") else None, #Raw values contain NaN not None
                        "CreatedBy" : geneset_info.get("CreatedBy"),
                        "date"      : geneset_info.get("date"),
                    },
                    symbol_check = symbol_check
                )
            ]
    return genesets
