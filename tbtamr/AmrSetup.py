import pathlib, pandas,re, datetime, subprocess, os, logging,subprocess,collections, psutil
from tbtamr.CustomLog import CustomFormatter
from tbtamr.TbTamr import Tbtamr


class AmrSetup(Tbtamr):

    def __init__(self, args):
        super().__init__()
        self.jobs = args.jobs # number of tbprofilers to run at a time
        self.read1 = args.read1
        self.read2 = args.read2
        self.prefix = args.prefix
        self.datafile = args.data
        self.database = args.database

    def _check_prefix(self):
        """
        If running type is not batch, then check that prefix is present and a string
        """

        if self.prefix == '':
            self.logger.critical(f"You must supply a sample or sequence id.")
            raise SystemExit
        else:
            return True

    def _check_reads(self, read):

        if not self._file_present(read):
            self.logger.critical(f"{read} is not a valid file path. Please check your input and try again.")
            raise SystemExit
        return True

    def _input_files(self, jobs):
        """
        Ensure that the files (either contigs or amrfinder output) exist and return running type
        """
        
        running_type = 'batch' if self.datafile != '' else 'single'
        if running_type == 'batch':
            self.logger.info(f"Checking that the input data is present.")
            jobs = self._set_threads(jobs=jobs)
            try:

                with open(self.datafile, 'r') as c:
                    data = c.read().strip().split('\n')
                    for line in data:
                        row = line.split('\t')
                        if self._check_reads(row[1]) and self._check_reads(row[2]):
                            self.logger.info(f"Reads for {row[0]} have been found")
            except Exception as e:
                self.logger.critical(f"Something has gone wrong with your input file. Please try again {e}.")
                raise SystemExit
        elif running_type == 'single' and self._check_reads(self.read1) and self._check_reads(self.read2):
            self._check_prefix()
            jobs = self._set_threads(jobs=jobs)
            self.logger.info(f"Reads for {self.prefix} are present. tbtamr can proceed.")
        else:
            self.logger.critical(f"Something has gone wrong with your inputs. Please try again.")
            raise SystemExit

        return running_type,jobs
   

    def _setup(self):
        # check that inputs are correct and files are present
        running_type, jobs = self._input_files(jobs = self.jobs)
        # check that prefix is present (if needed)
        Data = collections.namedtuple('Data', ['run_type', 'datafile', 'prefix','read1','read2', 'jobs', 'db'])
        input_data = Data(running_type, self.datafile,self.prefix,self.read1,self.read2, jobs, self.database)
        
        return input_data
    

