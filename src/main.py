from operator import truediv
from json_processing import read_json_MSIGDB, dump_all_as_we_want
from read_internal_dump import read_all_signature
from parse_msigdb import parse_MSigDB
import sys, getopt
import os

def main(argv):
    
    if len(argv) < 3:
        sys.stderr.write("Arguments error. Usage:\n")
        sys.stderr.write("\tmain.py  <inputfile>  <outputfile> <type> <group> (optional) \n")
        sys.exit(1)

    inputfile = argv[0]
    outputfile = argv[1]        
    type_db = argv[2]
    if (len(argv))==4:
        group=argv[3]
    if not type_db in ["msigdb", "stockcare"]:
        print("msigdb, stockcare db only for now")
        sys.exit(1)
    all_signatures = []
    if type_db == "msigdb":
        #all_signatures = read_json_MSIGDB(file=inputfile)
        all_signatures = parse_MSigDB(file=inputfile, group=group)
    if type_db == "stockcare":
        ## Specific structure of file, see dvc 
        genesets_repo =  os.path.join(os.path.dirname("inhouse_data/Geneset_inventory_20220513.csv"), "data")
        all_signatures = read_all_signature(directory = genesets_repo,description_f=inputfile, symbol_check= True)
    dump_all_as_we_want(all_signatures, file_to_write=outputfile)


if __name__ == "__main__":
    main(sys.argv[1:])
