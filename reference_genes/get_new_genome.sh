#!/bin/bash


##### THIS WILL ONLY DOWNLOAD LAST VERSION AS BIOMART DOES NOT ALLOW DIRECT DOWNLOAD OF ARCHIVED GENOMES ####
# Here the idea is that for a new version, user will add to BioMart_version.tsv the new version for the species supported.
# Running dvc repro will then get the proper biomart version
#  It is user responsability to check that the added version is the one matching at time t what will be doenloaded
# If a new species need to be supported, edit the bottom loop and create the appropriate function.
################################################################################################################
run_human (){
wget -O tmp 'http://www.ensembl.org/biomart/martservice?query=<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE Query>
<Query  virtualSchemaName = "default" formatter = "TSV" header = "0" uniqueRows = "0" count = "" datasetConfigVersion = "0.6" >
			
	<Dataset name = "hsapiens_gene_ensembl" interface = "default" >
		<Attribute name = "ensembl_gene_id" />
		<Attribute name = "ensembl_gene_id_version" />
		<Attribute name = "hgnc_id" />
		<Attribute name = "hgnc_symbol" />
		<Attribute name = "external_gene_name" />
		<Attribute name = "description" />
		<Attribute name = "external_synonym" />
	</Dataset>
</Query>'


 (echo -e "ensembl_gene_id\tensembl_gene_id_version\thgnc_id\thgnc_symbol\texternal_gene_name\tdescription\texternal_synonym" && 
            cat tmp) > $FILE
rm tmp
}


run_mouse (){
wget -O tmp 'http://www.ensembl.org/biomart/martservice?query=<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE Query>
<Query  virtualSchemaName = "default" formatter = "TSV" header = "0" uniqueRows = "0" count = "" datasetConfigVersion = "0.6" >
	<Dataset name = "mmusculus_gene_ensembl" interface = "default" >
		<Attribute name = "ensembl_gene_id" />
		<Attribute name = "ensembl_gene_id_version" />
		<Attribute name = "description" />
		<Attribute name = "external_gene_name" />
		<Attribute name = "external_synonym" />
		<Attribute name = "mgi_symbol" />
		<Attribute name = "genedb" />
	</Dataset>
</Query>' 
 (echo -e "ensembl_gene_id\tensembl_gene_id_version\tdescription\texternal_gene_name\texternal_synonym\tmgi_symbol" && 
            cat tmp) > $FILE

rm tmp

}

while IFS=$',' read -r Species Version ; do
    # Get version without parenthisis. Could be nicer
    vv=`echo $Version | sed 's/.*(\(.*\)).*/\1/'`
    FILE="${Species}_${vv}_alias.txt"
    if test -f "$FILE"; then
        echo "$FILE exists."
    else
        echo "$FILE does not exist"
        if [ "$Species" = "Human" ] ; then
            run_human
        elif [ "$Species" = "Mouse" ] ; then
            run_mouse
        else 
            echo "$Species not encoded"
        fi
    fi
done < <(grep -v '#' BioMart_version.tsv) 
#< "BioMart_version.tsv"