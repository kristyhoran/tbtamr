from cmath import log
import pathlib, pandas, datetime, subprocess, os, logging,subprocess,collections, re

from tbtamr.CustomLog import logger
from tbtamr.TbTamr import Tbtamr


class RunProfiler(Tbtamr):
    """
    A class to run tbprofiler
    """
    def __init__(self, args):
        
        # super().__init__()
        self.database = args.db
        self.input_file = args.input_file
        self.jobs = args.jobs
        self.keep = args.keep
        self.keep_bam = args.keep_bam
        # self.logger = self._get_logger()
        # self.input_data = args
        

    # def _single_cmd(self):
    #     cmd = f"mkdir -p {self.prefix} && tb-profiler profile --read1 {self.read1} --read2 {self.read2} --db {self.database} --prefix {self.prefix} --dir {self.prefix} --csv --call_whole_genome --no_trim --threads {self.jobs} > {self.prefix}/tbprofiler.log 2>&1"
    #     return cmd

    # def _single_collate(self):
    #     cmd = f"tb-profiler collate -d {self.prefix}/results/ --db {self.database} -p {self.prefix}/tb-profiler_report --full --all_variants --mark_missing"
    #     return cmd

    def _check_output(self, isolates, step = 'profile'):

        for iso in isolates:
            wldcrd = f"{iso}/results/{iso}.results.json" if step == 'profile' else f"{iso}/tb-profiler_report.json"
            p = sorted(pathlib.Path.cwd().glob(wldcrd))
            if p[0].exists():
                isolates[iso][step] = f"{p[0]}"
            else:
                logger.critical(f"There seems to be a serious problem - file {p[0]} was not created. Please check logs and try again.")
                raise SystemExit
        logger.info(f"All files for step : {step} have been created.")
        return isolates

    def _get_isolates(self):

        isolates = {}
        with open(self.input_file,'r') as i:

            lines = i.read().strip().split('\n')
            for line in lines:
                iso = line.split('\t')[0]
                if iso not in isolates:
                    isolates[iso] = {}
                
        return isolates
        
    def _remove(self, keep_bam = False, keep = False):

        if not keep:
            folders = ['vcf','bam'] if not keep_bam else ['vcf']
            for f in folders:
                p = pathlib.Path().resolve()
                cmd = self._clean_cmd(path = f"{p}/*/{f}")
                self._run_cmd(cmd=cmd)
        else:
            logger.info(f"Keeping all accessory data folders.")

    def _tidy_tbp(self):

        p = pathlib.Path().resolve()

        logger.info(f"Now tidying up")
        cmd = self._clean_cmd(path = f"{p}/*vcf*")

        self._run_cmd(cmd=cmd)

    def _batch_cmd(self):
        cmd = f"parallel --colsep '\\t' -j {self.jobs} 'tb-profiler profile --read1 {{2}} --read2 {{3}} --db {self.database} --prefix {{1}} --dir {{1}} --no_trim --call_whole_genome --threads 1 >> {{1}}/tbprofiler.log 2>&1' :::: {self.input_file}"
        return cmd

    def _batch_collate(self):
        cmd = f"parallel --colsep '\\t' -j {self.jobs} tb-profiler collate -d {{1}}/results/ --db {self.database} -p {{1}}/tb-profiler_report --full --all_variants --mark_missing :::: {self.input_file}"
        return cmd

    def _check_tbprofiler(self):
        version_pat_3 = re.compile(r'\bv?(?P<major>[0-9]+)\.(?P<minor>[0-9]+)(?:\.(?P<release>[0-9]+)*)?(?:\.(?P<build>[0-9]+)*)?\b')
        p = subprocess.run(f"tb-profiler --version", capture_output=True, encoding = "utf-8", shell = True)
        p = p.stdout
        v = version_pat_3.search(p.strip())
        if v:
            v = v.group(0)
            logger.info(f"TB Profiler version {v} detected.")    
        else:
            logger.critical(f"It seems something is not quite right with your TB profiler installation. Please check your installation and try again.")
            raise SystemExit
        return True

        
    def _run(self):
        """
        run tbprofiler
        """
        
        if self._check_tbprofiler():
            # print(self.read1)
            logger.info(f"All check complete now running TB-profiler")
        else:
            logger.critical(f"TB-profiler does not seem to be installed correctly. Please try again.")
            raise SystemExit
        # get list isolates
        isolates = self._get_isolates()
        # self._check_tbprofiler()
        cmd_profiler = self._batch_cmd()
        
        if self._run_cmd(cmd = cmd_profiler):
            isolates = self._check_output(isolates = isolates, step = 'profile')
            logger.info(f"Profiling was completed successfully, now collating results.")
            cmd_collate = self._batch_collate()
            if self._run_cmd(cmd = cmd_collate):
                isolates = self._check_output(isolates = isolates, step = 'collate')
        # clean up
                self._tidy_tbp()
                self._remove(keep_bam=self.keep_bam, keep = self.keep)
                return isolates
        
        logger.critical(f"Something seems to be wrong with your run of tbTAMR. Please try again.")


        
