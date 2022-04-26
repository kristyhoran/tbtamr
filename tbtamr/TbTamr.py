import pathlib, pandas,re, datetime, subprocess, os, logging,subprocess,collections, psutil
from tbtamr.CustomLog import CustomFormatter


class Tbtamr(object):
    """
    A base class for setting up tbtamr return a valid input object for subsequent steps
    """
    def __init__(self, args):
        

        self.logger =logging.getLogger(__name__) 
        self.logger.setLevel(logging.DEBUG)
        ch = logging.StreamHandler()
        ch.setLevel(logging.DEBUG)
        ch.setFormatter(CustomFormatter())
        fh = logging.FileHandler('tbtamr.log')
        fh.setLevel(logging.DEBUG)
        formatter = logging.Formatter('[%(levelname)s:%(asctime)s] %(message)s', datefmt='%Y%m-%d %I:%M:%S %p') 
        fh.setFormatter(formatter)
        self.logger.addHandler(ch) 
        self.logger.addHandler(fh)
        self.one,self.five,self.fifteen = psutil.getloadavg()
        self.total_cores = os.cpu_count()
        # self.jobs = args.jobs # number of tbprofilers to run at a time
        # self.read1 = args.read1
        # self.read2 = args.read2
        # self.prefix = args.prefix
        # self.datafile = args.data
        # self.database = args.database

    def _run_cmd(self, cmd):
        
        """
        Use subprocess to run the command for tb-profiler
        """

        p = subprocess.run(cmd, shell = True, capture_output = True, encoding = "utf-8")
        if p.returncode == 0:
            self.logger.info(f"TBProfiler completed successfully. Will now move on to phenotype inferrence.")
            return True
        else:
            self.logger.critical(f"There appears to have been a problem with running tb-profiler. The following error has been reported : \n {p.stderr}")
            raise SystemExit
    
    def _set_threads(self, jobs):
        
        self.logger.info(f"Detecting available resources")
        
        
        avail = self.total_cores - max(self.one,self.five,self.fifteen)
        self.logger.info(f"The available cores is : {avail}")
        max_tbjob = avail  / 8 # divide by 8 - this is the max length of pipes in tb-profiler - need to avoid killing resources
        
        if int(jobs) == 0:
            self.logger.info(f"Number of TB-profiler jobs to run {max_tbjob}")
            return max_tbjob
        elif int(jobs) <  max_tbjob:
            self.logger.info(f"Number of TB-profiler jobs to run {jobs}")
            return jobs
        else:
            self.logger.info(f"Number of TB-profiler jobs to run {max_tbjob}")
            return max_tbjob
            
    
    def _file_present(self, name):
        """
        check file is present
        :name is the path of the file to check
        """
        
        if name == "":
            return False
        elif pathlib.Path(name).exists():
            self.logger.info(f"Checking if file {name} exists")
            return True
        else:
            return False
