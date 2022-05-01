import sys, pathlib, pandas, pytest, numpy, logging, collections

from unittest.mock import patch, PropertyMock

from tbtamr.AmrSetup import AmrSetup
from tbtamr.RunProfiler import RunProfiler
# from abritamr.RunFinder import RunFinder
# from abritamr.Collate import Collate, MduCollate

test_folder = pathlib.Path(__file__).parent
# REFGENES = f"{pathlib.Path(__file__).parent.parent /'abritamr' /'db' / 'refgenes_latest.csv'}"

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

        assert amr_obj._set_threads(jobs=val) == amr_obj.fifteen/8

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

        assert amr_obj._set_threads(jobs=val) == amr_obj.fifteen/8

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

        assert amr_obj._set_threads(jobs=val) == val

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

# def test_check_input_batch_success():
#     """
#     assert true when batch is the running type
#     """
#     with patch.object(AmrSetup, "__init__", lambda x: None):
#         amr_obj = AmrSetup()
#         amr_obj.logger = logging.getLogger(__name__)
#         amr_obj.datafile = test_folder / "isolates.tab"
#         amr_obj.one = 16
#         amr_obj.five = 24
#         amr_obj.fifteen = 32
#         amr_obj.total_cores = 64
#         val = 3

#         assert amr_obj._input_files(jobs = val) == ('batch',val)

# def test_check_input_batch_fail():
#     """
#     assert true when batch is the running type
#     """
#     with patch.object(AmrSetup, "__init__", lambda x: None):
#         amr_obj = AmrSetup()
#         amr_obj.logger = logging.getLogger(__name__)
#         amr_obj.datafile = test_folder / "isolates.txt"
#         amr_obj.one = 16
#         amr_obj.five = 24
#         amr_obj.fifteen = 32
#         amr_obj.total_cores = 64
#         val = 3

#         with pytest.raises(SystemExit):
#             amr_obj._input_files(jobs=val)
        
# def test_check_input_single_success():
#     """
#     assert true when batch is the running type
#     """
#     with patch.object(AmrSetup, "__init__", lambda x: None):
#         amr_obj = AmrSetup()
#         amr_obj.logger = logging.getLogger(__name__)
#         amr_obj.read1 = test_folder / "dummy_R1.fq.gz"
#         amr_obj.read2 = test_folder / "dummy_R2.fq.gz"
#         amr_obj.datafile = ""
#         amr_obj.prefix = 'some_prefix'
#         amr_obj.one = 16
#         amr_obj.five = 24
#         amr_obj.fifteen = 32
#         amr_obj.total_cores = 64
#         val = 3

#         assert amr_obj._input_files(jobs = val) == ('single',val)

# def test_check_input_single_fail():
#     """
#     assert true when batch is the running type
#     """
#     with patch.object(AmrSetup, "__init__", lambda x: None):
#         amr_obj = AmrSetup()
#         amr_obj.logger = logging.getLogger(__name__)
#         amr_obj.read1 = test_folder / "dummy_R1.fq.gz"
#         amr_obj.read2 = test_folder / "dummy_R5.fq.gz"
#         amr_obj.datafile = ""
#         amr_obj.prefix = 'some_prefix'
#         amr_obj.one = 16
#         amr_obj.five = 24
#         amr_obj.fifteen = 32
#         amr_obj.total_cores = 64
#         val = 3

#         with pytest.raises(SystemExit):
#             amr_obj._input_files(jobs = val)
        

# # Test SetupMDU
DATA = collections.namedtuple('Data', ['input_file', 'jobs', 'db', 'keep', 'keep_bam'])

def test_batch_setup_success():
    """
    assert True when non-empty string is given
    """
    with patch.object(AmrSetup, "__init__", lambda x: None):
        args = DATA("batch", f"{test_folder / 'isolates.tab'}", '', '', '', 3, 'tbdb')
        # print(args)
        amr_obj = AmrSetup()
        amr_obj.logger = logging.getLogger(__name__)
        amr_obj.datafile = f"{test_folder / 'isolates.tab'}"
        amr_obj.read1 = f""
        amr_obj.read2 = f""
        amr_obj.one = 16
        amr_obj.five = 24
        amr_obj.fifteen = 32
        amr_obj.total_cores = 64
        amr_obj.jobs = 3
        amr_obj.prefix = ""
        amr_obj.database = "tbdb"

        assert amr_obj._setup() == args


def test_batch_setup_fail():
    """
    assert True when non-empty string is given
    """
    with patch.object(AmrSetup, "__init__", lambda x: None):
        args = DATA("batch", f"{test_folder / 'isolates.tab'}", '', '', '', 3, 'tbdb')
        # print(args)
        amr_obj = AmrSetup()
        amr_obj.logger = logging.getLogger(__name__)
        amr_obj.datafile = f"{test_folder / 'isolates.txt'}"
        amr_obj.read1 = f""
        amr_obj.read2 = f""
        amr_obj.one = 16
        amr_obj.five = 24
        amr_obj.fifteen = 32
        amr_obj.total_cores = 64
        amr_obj.jobs = 3
        amr_obj.prefix = ""
        amr_obj.database = "tbdb"

        with pytest.raises(SystemExit):
            amr_obj._setup()

# def test_single_setup_success():
#     """
#     assert True when non-empty string is given
#     """
#     with patch.object(AmrSetup, "__init__", lambda x: None):
#         args = DATA("single", f"",'some_prefix', f"{test_folder / 'dummy_R1.fq.gz'}", f"{test_folder / 'dummy_R2.fq.gz'}",  3, 'tbdb')
#         # print(args)
#         amr_obj = AmrSetup()
#         amr_obj.logger = logging.getLogger(__name__)
#         amr_obj.datafile = f""
#         amr_obj.read1 = f"{test_folder / 'dummy_R1.fq.gz'}"
#         amr_obj.read2 = f"{test_folder / 'dummy_R2.fq.gz'}"
#         amr_obj.one = 16
#         amr_obj.five = 24
#         amr_obj.fifteen = 32
#         amr_obj.total_cores = 64
#         amr_obj.jobs = 3
#         amr_obj.prefix = "some_prefix"
#         amr_obj.database = "tbdb"

#         assert amr_obj._setup() == args


# def test_single_setup_fail():
#     """
#     assert True when non-empty string is given
#     """
#     with patch.object(AmrSetup, "__init__", lambda x: None):
#         args = DATA("single", f"",'some_prefix', f"{test_folder / 'dummy_R1.fq.gz'}", f"{test_folder / 'dummy_R2.fq.gz'}",  3, 'tbdb')
#         # print(args)
#         amr_obj = AmrSetup()
#         amr_obj.logger = logging.getLogger(__name__)
#         amr_obj.datafile = f""
#         amr_obj.read1 = f"{test_folder / 'dummy_R1.fq.gz'}"
#         amr_obj.read2 = f"{test_folder / 'dummy_R5.fq.gz'}"
#         amr_obj.one = 16
#         amr_obj.five = 24
#         amr_obj.fifteen = 32
#         amr_obj.total_cores = 64
#         amr_obj.jobs = 3
#         amr_obj.prefix = "some_prefix"
#         amr_obj.database = "tbdb"

#         with pytest.raises(SystemExit):
#             amr_obj._setup()

def test_generate_cmd_batch_success():
    """
    assert True when non-empty string is given
    """
    with patch.object(AmrSetup, "__init__", lambda x: None):
        args = DATA("batch", f"{test_folder / 'isolates.tab'}", '', '', '', 3, 'tbdb')
        # print(args)
        amr_obj = RunProfiler(args)
        amr_obj.logger = logging.getLogger(__name__)

        assert amr_obj._batch_cmd(input_data= args) == f"parallel --colsep '\t' -n {args.jobs} 'tb-profiler profile --read1 {{2}} --read2 {{3}} --db {args.db} --prefix {{1}} --dir {{1}} --csv --call_whole_genome --no_trim --threads {args.jobs} > {{1}}/tbprofiler.log 2>&1' :::: {args.datafile}"


# def test_generate_cmd_single_success():
#     """
#     assert True when non-empty string is given
#     """
#     with patch.object(AmrSetup, "__init__", lambda x: None):
#         args = DATA("single", f"",'some_prefix', f"{test_folder / 'dummy_R1.fq.gz'}", f"{test_folder / 'dummy_R2.fq.gz'}",  3, 'tbdb')
#         # print(args)
#         amr_obj = RunProfiler(args)
#         amr_obj.logger = logging.getLogger(__name__)

#         assert amr_obj._single_cmd(input_data= args) == f"tb-profiler profile --read1 {args.read1} --read2 {args.read2} --db {args.db} --prefix {args.prefix} --dir {args.prefix} --csv --call_whole_genome --no_trim --threads {args.jobs} > {args.prefix}/tbprofiler.log 2>&1"

