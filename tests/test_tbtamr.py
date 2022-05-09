import sys, pathlib, pandas, pytest, numpy, logging, collections

from unittest.mock import patch, PropertyMock

from tbtamr.AmrSetup import AmrSetup
from tbtamr.RunProfiler import RunProfiler

test_folder = pathlib.Path(__file__).parent

def test_file_present():
    """
    assert true when the input file is true
    """
    with patch.object(AmrSetup, "__init__", lambda x: None):
        amr_obj = AmrSetup()
        amr_obj.logger = logging.getLogger(__name__)
        p = test_folder / "dummy_R1.fq.gz"
    
        assert amr_obj._file_present(p)

def test_file_not_present():
    """
    assert true when the input file is true
    """
    with patch.object(AmrSetup, "__init__", lambda x: None):
        amr_obj = AmrSetup()
        amr_obj.logger = logging.getLogger(__name__)
        p = test_folder / "dummy_R5.fq.gz"
    
        assert not amr_obj._file_present(p)


def test_resorces_maxjob_1():
    """
    assert true when the maxjob is returned as the number of tbprofiler because jobs is not provided
    """
    with patch.object(AmrSetup, "__init__", lambda x: None):
        amr_obj = AmrSetup()
        amr_obj.logger = logging.getLogger(__name__)
        amr_obj.one = 16
        amr_obj.five = 24
        amr_obj.fifteen = 32
        amr_obj.total_cores = 64
        val = 0

        assert amr_obj._set_threads(jobs=val) == amr_obj.fifteen/2

def test_resorces_maxjob_2():
    """
    assert true when the maxjob is returned as the number of tbprofiler because jobs is greater than available resources
    """
    with patch.object(AmrSetup, "__init__", lambda x: None):
        amr_obj = AmrSetup()
        amr_obj.logger = logging.getLogger(__name__)
        amr_obj.one = 16
        amr_obj.five = 24
        amr_obj.fifteen = 32
        amr_obj.total_cores = 64
        val = 8

        assert amr_obj._set_threads(jobs=val) == int(val/2)

def test_resorces_job():
    """
    assert true when the job is returned as the number of tbprofiler because jobs is less than available resources
    """
    with patch.object(AmrSetup, "__init__", lambda x: None):
        amr_obj = AmrSetup()
        amr_obj.logger = logging.getLogger(__name__)
        amr_obj.one = 16
        amr_obj.five = 24
        amr_obj.fifteen = 32
        amr_obj.total_cores = 64
        val = 3

        assert amr_obj._set_threads(jobs=val) == int(val/2)

def test_run_cmd_success():
    """
    assert true when the run cmd has exitcode == 0
    """
    with patch.object(AmrSetup, "__init__", lambda x: None):
        amr_obj = AmrSetup()
        amr_obj.logger = logging.getLogger(__name__)
        cmd = "echo Hello World"

        assert amr_obj._run_cmd(cmd = cmd)

def test_run_cmd_failure():
    """
    assert true when the run cmd has exitcode != 0
    """
    with patch.object(AmrSetup, "__init__", lambda x: None):
        amr_obj = AmrSetup()
        amr_obj.logger = logging.getLogger(__name__)
        cmd = "ks"

        with pytest.raises(SystemExit):
            amr_obj._run_cmd(cmd = cmd)

def test_check_prefix_success():
    """
    assert true when the prefix is provided
    """
    with patch.object(AmrSetup, "__init__", lambda x: None):
        amr_obj = AmrSetup()
        amr_obj.logger = logging.getLogger(__name__)
        amr_obj.prefix = 'some_prefix'
        assert amr_obj._check_prefix()

def test_check_prefix_success():
    """
    raise system exit the prefix is not
    """
    with patch.object(AmrSetup, "__init__", lambda x: None):
        amr_obj = AmrSetup()
        amr_obj.logger = logging.getLogger(__name__)
        amr_obj.prefix = ''
        with pytest.raises(SystemExit):
            amr_obj._check_prefix()

def test_reads_exist_success():
    """
    assert true when reads in input file are present
    """
    with patch.object(AmrSetup, "__init__", lambda x: None):
        amr_obj = AmrSetup()
        amr_obj.logger = logging.getLogger(__name__)
        read = test_folder / "dummy_R1.fq.gz"

        
        assert amr_obj._check_reads(read=read)

def test_reads_exist_fail():
    """
    assert true when reads in input file are present
    """
    with patch.object(AmrSetup, "__init__", lambda x: None):
        amr_obj = AmrSetup()
        amr_obj.logger = logging.getLogger(__name__)
        read = test_folder / "dummy_R5.fq.gz"

        with pytest.raises(SystemExit):
            amr_obj._check_reads(read=read)
     

# # Test SetupMDU
DATA = collections.namedtuple('Data', ['input_file', 'jobs', 'db', 'keep', 'keep_bam'])


def test_generate_cmd_batch_success():
    """
    assert True when non-empty string is given
    """
    with patch.object(AmrSetup, "__init__", lambda x: None):
        args = DATA(f"{test_folder / 'isolates.tab'}", 3, 'tbdb',False,False)
        # print(args)
        amr_obj = RunProfiler(args)
        amr_obj.logger = logging.getLogger(__name__)

        assert amr_obj._batch_cmd() == f"parallel --colsep '\\t' -j {args.jobs} 'tb-profiler profile --read1 {{2}} --read2 {{3}} --db {args.db} --prefix {{1}} --dir {{1}} --no_trim --call_whole_genome --threads 1 >> {{1}}/tbprofiler.log 2>&1' :::: {args.input_file}"
