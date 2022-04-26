import pathlib, pandas, datetime, subprocess, os, logging,subprocess,collections, re

from tbtamr.CustomLog import CustomFormatter
from tbtamr.TbTamr import Tbtamr


class RunProfiler(Tbtamr):
    """
    A class to run tbprofiler
    """
    def __init__(self, args):
        
        super().__init__(args)
        self.database = args.db
        self.run_type = args.run_type
        self.jobs = args.jobs
        self.datafile = args.datafile
        self.prefix = args.prefix
        self.read1 = args.read1
        self.read2 = args.read2

    def _single_cmd(self, input_data):
        cmd = f"tb-profiler profile --read1 {input_data.read1} --read2 {input_data.read2} --db {input_data.db} --prefix {input_data.prefix} --dir {input_data.prefix} --csv --call_whole_genome --no_trim --threads {input_data.jobs} > {input_data.prefix}/tbprofiler.log 2>&1"
        return cmd
    
    def _batch_cmd(self, input_data):

        cmd = f"parallel --colsep '\t' -n {input_data.jobs} 'tb-profiler profile --read1 {{2}} --read2 {{3}} --db {input_data.db} --prefix {{1}} --dir {{1}} --csv --call_whole_genome --no_trim --threads {input_data.jobs} > {{1}}/tbprofiler.log 2>&1' :::: {input_data.datafile}"
        return cmd

    def _check_tbprofiler(self):

        version_pat_3 = re.compile(r'\bv?(?P<major>[0-9]+)\.(?P<minor>[0-9]+)(?:\.(?P<release>[0-9]+)*)?(?:\.(?P<build>[0-9]+)*)?\b')
        p = subprocess.run(f"tb-profiler --version", capture_output=True, encoding = "utf-8", shell = True)
        p = p.stdout
        v = version_pat_3.search(p.strip())
        if v:
            v = v.group(0)
            self.logger.info(f"TB Profiler version {v} detected.")    
        else:
            self.logger.critical(f"It seems something is not quite right with your TB profiler installation. Please check your installation and try again.")
            raise SystemExit


    def _generate_cmd(self):
        """
        Generate a command to run amrfinder
        """
        cmd = self._batch_cmd() if self.running_type == 'batch' else self._single_cmd()
        return cmd
        
    
    # def _check_output_file(self, path):
    #     """
    #     check that tb-profiler outputs are present
    #     """
    #     if not pathlib.Path(path).exists():
    #         self.logger.critical(f"The amrfinder output : {path} is missing. Something has gone wrong with AMRfinder plus. Please check all inputs and try again.")
    #         raise SystemExit
    #     else:
    #         return True

    # def _check_outputs(self):
    #     """
    #     use inputs to check if files made
    #     """
    #     if self.run_type != 'batch':
    #         self._check_output_file(f"{self.prefix}/amrfinder.out")
    #     else:
    #         tab = pandas.read_csv(self.input, sep = '\t', header = None)
    #         for row in tab.iterrows():
    #             self._check_output_file(f"{row[1][0]}/amrfinder.out")
    #     return True

    def run(self):
        """
        run tbprofiler
        """
        if self._check_tbprofiler():
            self.logger.info(f"All check complete now running TB-profiler")
        else:
            self.logger.critical(f"TB-profiler does not seem to be installed correctly. Please try again.")
            raise SystemExit
        cmd = self._generate_cmd()
        self.logger.info(f"You are running abritamr in {self.running_type} mode. Now executing : {cmd}")
        self._run_cmd(cmd)
        # self._check_outputs()
        # Data = collections.namedtuple('Data', ['running_type', 'input', 'prefix'])
        # amr_data = Data(self.run_type, self.input, self.prefix)

        return amr_data
