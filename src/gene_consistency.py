import pandas as pd

from typing import List


def get_genome_information(file_from_genome_construct: str):
    gene_info = pd.read_table(file_from_genome_construct, dtype=str).get("GeneSymbol").values
    # should get a table with header like [gene_id GeneSymbol Chromosome Class Strand]
    return gene_info


def get_genome_aliases(file_from_biomart: str, species: str) -> dict:
    """Will read file and get possible official gene symbol for aliases
    Args:
        file_from_biomart (_type_): file to reads
        species (_type_): specie : [huamn, mouse]. used to get name of column containing official gene symbol

    Returns:
        dict : key is a gene alias, value is official gene symbol
    """
    key_symbol_dict = {"human": "hgnc_symbol", "mouse": "mgi_symbol"}
    key_symbol = key_symbol_dict[species]
    alias_key = "external_synonym"
    tt = pd.read_table(file_from_biomart, header=0, index_col=False, dtype=str, sep="\t").drop_duplicates()
    alias_dict = {}
    ambiguous_alias = []
    for ii, row in tt.iterrows():
        ## IF ALIAS already found and assigned to other symbol. AKA ambiguous alias.
        ## THIS IS ANNOYING
        current_alias = row[alias_key]
        if not pd.isna(current_alias):
            if current_alias in alias_dict.keys():
                if row[key_symbol] != alias_dict[current_alias]:
                    ambiguous_alias += [current_alias]
                    pass
            alias_dict[current_alias] = row[key_symbol]
    # print( "Ambiguous alias: ", ",".join(set(ambiguous_alias)))
    return alias_dict


def _mapping_symbol(gene_to_map: str, dict_alias: dict = {}) -> str:
    """mapping_symbol

    Args:
        gene_to_map (str): symbol of the gene
        dict_alias (dict, optional): alias dictionary, key are possible symbol, gene official name is the value . Defaults to {}.
    Returns:
        str: a possible official symbol; if not found ; return the original for now.
    """ """"""
    if gene_to_map in dict_alias.keys():
        return dict_alias[gene_to_map]
    else:
        return gene_to_map


def validate_gene_list(gene_list: list, all_symbols, dict_alias: dict = {}) -> List[str]:
    """validate_gene_list

    Args:
        gene_list (_type_): gene array
        table_genome (_type_): Table containing supported genes values.
        dict_alias (dict): key is a gene alias, value is official gene symbol
    """
    if all_symbols is None:
        print("No genome to compare with")
        return gene_list
    else:
        is_valid_gene = [gene in all_symbols for gene in gene_list]
        gene_list_final = [b for a, b in zip(is_valid_gene, gene_list) if a]
        if not all(is_valid_gene):
            invalid =  [b for a, b in zip(is_valid_gene, gene_list) if not a]
            replacement = [_mapping_symbol(k, dict_alias) for k in invalid]
            gene_list_final += replacement
        return gene_list_final
