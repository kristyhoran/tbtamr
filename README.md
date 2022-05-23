# tbTAMR

`tbTAMR` implements TB-profiler and custom logic developed at MDU to identify mutations linked to AMR mechanisms in _M. tuberculosis_ and generate reports suitable for public health in Victoria. It may also be suitable for use in research settings.

This is an alpha package - and is in the process of being validated for NATA accreditation.


**More details to com**

## tbTAMR DB

`tbTAMR` comes with a modified mutational database, defined by validation at MDU for the purposes of reporting mutations in a public health and clinical setting in Victoria.

This database was created using `tb-profiler create_db` (from MDU fork of pathogen-profiler)

The following files are required in order to generate a custom database

* `genome.fasta` the reference for mutations in the database
* `genome.fasta.fai`
* `genome.gff`
* `barcode.bed` 
* a `csv` file
    * header ```Gene,Mutation,Drug,Confers,Interaction```

Creation can be done by navigating to a storage directory and running

```
conda activate tb-profile-env
tb-profiler create_db -p <db_prefix> -c <path_to_csv> --custom --db_name <name_of_db> --db_commit <some_unique_string> --db_author <name_of_author> --db_date <date_created>
```

