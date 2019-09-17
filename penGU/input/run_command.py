import sys

from penGU.db.penguDB import check_or_create_db

from penGU.isolate.db_record import update_isolate_database

from penGU.sequencing.db_record import update_sequencing_database

from penGU.mlst.update_refdb import generate_mlst_refdb
from penGU.mlst.db_record import update_mlst_database

from penGU.distance.update_refdb import update_distance_refdb
from penGU.distance.db_record import update_distance_database

from penGU.snpaddress.clustercode_isolate import get_snpaddresses_from_snapperdb, update_isolate_clustercode_db
from penGU.snpaddress.clustercode_database import update_clustercode_database
from penGU.snpaddress.clustercode_history import update_clustercode_history

from penGU.input.utils import check_config
from penGU.output.utils import write_updated_records_to_csv, write_all_records_to_csv


def run_commmand(config_dict, args):
    if args.command is None:
        print("Please use a subcommand. Subcommand options can be viewed with " + sys.argv[0] + " --help\n")

    elif 'create_db' in args.command:
        check_or_create_db(config_dict, args.sql_scriptfile)
        
    elif 'add_isolates' in args.command:
        update_isolate_database(config_dict, args.isolate_csv)
    
    elif 'add_sequencing_metadata' in args.command:
        update_sequencing_database(config_dict, args.sequencing_csv)

    elif 'update_mlst_db' in args.command:
        generate_mlst_refdb(config_dict, args.mlst_scheme_name, args.pubmlst_url)
        update_mlst_database(config_dict, args.mlst_csv)

    elif 'update_distance_refdb' in args.command:
        update_distance_refdb(config_dict, args.dist_ref_csv)
    
    elif 'update_distance_db' in args.command:
        update_distance_database(config_dict, args.dist_csv)

    elif 'update_clustercode_db' in args.command:
        snapperdb_config = check_config(args.snapperdb_conf, config_type="snapperdb")
        all_snapperdb_snpaddresses = get_snpaddresses_from_snapperdb(snapperdb_config, config_dict, args.snapperdb_refgenome)
        update_clustercode_database(config_dict, all_snapperdb_snpaddresses)

        if args.output_all:
            write_all_records_to_csv(all_snapperdb_snpaddresses, args.output_all)

        updated_records = update_isolate_clustercode_db(config_dict, args.snapperdb_refgenome, args.isolate_file, all_snapperdb_snpaddresses)
        if updated_records:
        #    update_clustercode_history(config_dict, updated_records)
            write_updated_records_to_csv(updated_records, args.output_csv)

        #
        #    snapperdb_config = check_config(args.snapperdb_conf, config_type="snapperdb")
        #    all_snapperdb_snpaddresses = get_snpaddresses_from_snapperdb(snapperdb_config, config_dict, args.snapperdb_refgenome)
        #   